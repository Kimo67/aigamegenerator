import re
import json
from collections import Counter
from pathlib import Path

# ----------------------------- helper classes ----------------------------- #
class CharacterState:
    """Tracks a character's current on-screen state."""
    def __init__(self, name: str, emotion: str = "", position: str = ""):
        self.name = name.lower()
        self.emotion = emotion.lower()
        self.position = position  # e.g. "at left"

    def __str__(self):
        return f"show {self.name} {self.emotion} {self.position}".strip()

# Positions cycle order
POSITIONS = ["at left", "at center", "at right"]

# ------------------------------------------------------------------------- #

def remove_all(active, outfile):
    """Hide and clear all active characters."""
    for char in active:
        outfile.write(f"    hide {char.name}\n")
    active.clear()

# ------------------------------------------------------------------------- #

def write_character_defs(char_dict, outfile):
    """Write `define` blocks for every character found in JSON."""
    for name, colour in char_dict.items():
        var = name.replace(" ", "_")
        colour = colour or "#ffffff"
        outfile.write(f'define {var} = Character("{name}", color="{colour}")\n')

# ------------------------------------------------------------------------- #

def parse_inline_texte(raw: str):
    """Yield (speaker, text, emotion) triples from the `texte` field."""

    line_pat = re.compile(r"\$(?P<who>[^$]+)\$\s*:?\s*(?P<body>[^%]*?)(?:%(?P<emo>[A-Z]+)%|$)")
    for match in line_pat.finditer(raw):
        yield match["who"].strip(), match["body"].strip(), (match["emo"] or "").lower()

# ------------------------------------------------------------------------- #

def convert_node(node: dict, outfile, dialogue_counter, active_chars, show_state):
    """Recursively render a single JSON node and its children."""
    node_id = node.get("id", "X")
    # print(f"Converting node {node_id}: {node.get("texte")}\n")
    label_name = f"node_{node_id}"

    # --- new label --- #
    outfile.write(f"\nlabel {label_name}:\n")
    remove_all(active_chars, outfile)

    # Optional explicit scene
    if node.get("scène"):
        outfile.write(f"    scene {node['scène']}\n")

    # 1) explicit `répliques` array preferred; else parse raw `texte`
    if node.get("répliques"):
        for rep in node["répliques"]:
            speaker, text, emo = rep["personnage"], rep["texte"], rep.get("emotion", "")
            handle_show(speaker, emo, outfile, dialogue_counter, active_chars, show_state)
            outfile.write(f"    {speaker} \"{text}\"\n")

    elif node.get("texte"):
        # Try inline $CHAR$ parsing first
        any_yielded = False
        for speaker, text, emo in parse_inline_texte(node["texte"]):
            handle_show(speaker, emo, outfile, dialogue_counter, active_chars, show_state)
            outfile.write(f"    {speaker} \"{text}\"\n")
            any_yielded = True
        # If no inline markers were found, treat each paragraph as narrator text
        if not any_yielded:
            for paragraph in filter(None, (p.strip() for p in node["texte"].split("\n"))):
                outfile.write(f"    \"{paragraph}\"\n")

    # 2) choices / children
    children = node.get("children", [])
    choices = node.get("choix_possibles", [])

    if choices:
        # Build menu from explicit choices block
        outfile.write("    menu:\n")
        for ch in choices:
            outfile.write(f"        \"{ch['texte']}\" :\n            jump node_{ch['target_id']}\n")
    elif len(children) == 1:
        outfile.write(f"    jump node_{children[0]['id']}\n")
    elif len(children) > 1:
        outfile.write("    menu:\n")
        for child in children:
            txt = child.get("texte", f"branch {child['id']}")
            outfile.write(f"        \"{txt.splitlines()[0][:40]}...\" :\n            jump node_{child['id']}\n")

    outfile.write("    return\n")  # end of label

    # recurse into children
    for child in children:
        convert_node(child, outfile, dialogue_counter, active_chars, show_state)

# ------------------------------------------------------------------------- #

def handle_show(char_name, emotion, outfile, dialogue_counter, active_chars, show_state):
    """Ensure `char_name` is visible with correct emotion, using replacement rules."""
    char_name = char_name.lower()
    emotion = emotion.lower()
    dialogue_counter[char_name] += 1

    # Already active? update emotion if changed
    found = next((c for c in active_chars if c.name == char_name), None)
    if found:
        if found.emotion != emotion:
            found.emotion = emotion
            outfile.write(f"    {found}\n")
        return

    # Need to add
    if len(active_chars) < 3:
        active_chars.append(CharacterState(char_name, emotion))
    else:
        least = min(active_chars, key=lambda c: dialogue_counter[c.name])
        pos = least.position
        outfile.write(f"    hide {least.name}\n")
        active_chars.remove(least)
        active_chars.append(CharacterState(char_name, emotion, pos))

    # Assign positions if missing
    for i, char in enumerate(active_chars):
        if not char.position:
            char.position = POSITIONS[i] if len(active_chars) > 1 else ""
    # Write shows
    for char in active_chars:
        key = (char.name, char.emotion, char.position)
        if show_state.get(char.name) != key:
            outfile.write(f"    {char}\n")
            show_state[char.name] = key

# ------------------------------------------------------------------------- #

def convert_json_tree_to_rpy(json_path: str | Path, output_path: str | Path):
    """Entry point for v2 parser."""
    data = json.loads(Path(json_path).read_text(encoding="utf-8"))

    # Gather colour map if provided
    char_defs = data.get("characters", {})

    with open(output_path, "w", encoding="utf-8") as out:
        write_character_defs(char_defs, out)
        out.write("\n")
        convert_node(data, out, Counter(), [], {})

    print(f"Converted {json_path} → {output_path}")

# ------------------------------------------------------------------------- #

if __name__ == "__main__":
    convert_json_tree_to_rpy("testConversion/input_ia.json", "testConversion/script_v2.rpy")
