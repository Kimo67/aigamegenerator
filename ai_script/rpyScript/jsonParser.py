import json 
from collections import Counter  # for counting character dialogue frequency

# Helper function to hide all currently active characters and clear the list
def removeChar(active_characters, outfile):
    for char in active_characters:
        outfile.write(f'    hide {char.name}\n')
    active_characters.clear()

# Main function to convert structured JSON into a Ren'Py script
def convert_json_to_rpy(json_input, output_file):

    # Inner class to track a character's display state (emotion, position)
    class CharacterState:
        def __init__(self, name, emotion="", position=""):
            self.name = name
            self.emotion = emotion
            self.position = position

        def __str__(self):
            # Return a Ren'Py show command
            return f'show {self.name} {self.emotion} {self.position}'.strip()

    with open(json_input, 'r') as infile:
        data = json.load(infile)

    characters = data.get("characters", {})
    script = data.get("script", [])

    # Open the output .rpy file for writing
    with open(output_file, 'w') as outfile:
        active_label = None  # Current active label
        active_characters = []  # Characters currently on screen
        dialogue_count = Counter()  # Tracks how much each character speaks
        show_commands = {}  # Tracks current show state per character

        # Write character definitions (Ren'Py style)
        for char_name, char_color in characters.items():
            char_var = char_name.replace(" ", "_")  # Safe variable name
            outfile.write(f'define {char_var} = Character("{char_name}", color="{char_color}")\n')

        outfile.write('\n')  # Add spacing before the script

        # Iterate through script events
        for entry in script:
            match entry:
                # Scene changes
                case {"scene": scene}:
                    if active_label:
                        outfile.write(f'    scene {scene}\n')  # Indent if within label
                    else:
                        outfile.write(f'scene {scene}\n')  # No indent for first scene

                    # Reset visible character and show states
                    show_commands.clear()
                    active_characters.clear()

                # New label (scene entry point)
                case {"label": label}:
                    if active_label:
                        removeChar(active_characters, outfile)
                        outfile.write('    return\n')  # Close the previous label
                    active_label = label
                    outfile.write(f'\nlabel {label}:\n')  # Begin new label block

                # Jump to another label
                case {"jump": target}:
                    removeChar(active_characters, outfile)
                    outfile.write(f'    jump {target}\n')

                # Show a character on screen
                case {"show": char_name}:
                    char_name = char_name.lower()
                    emotion = ""  # Can be extended to support emotions

                    # Only update if the emotion or character has changed
                    if char_name not in show_commands or show_commands[char_name] != emotion:
                        show_commands[char_name] = emotion

                    # If character not already visible
                    if not any(c.name == char_name for c in active_characters):
                        if len(active_characters) < 3:
                            # Add directly if there's room
                            active_characters.append(CharacterState(char_name, emotion))
                        else:
                            # Remove least active speaker to make room
                            least_speaking = min(active_characters, key=lambda c: dialogue_count[c.name])
                            position = least_speaking.position
                            outfile.write(f'    hide {least_speaking.name}\n')
                            active_characters.remove(least_speaking)
                            active_characters.append(CharacterState(char_name, emotion, position))

                    # Assign default positions to characters (left, center, right)
                    positions = ["at left", "at center", "at right"]
                    for i, char in enumerate(active_characters):
                        if not char.position:
                            char.position = positions[i] if len(active_characters) > 1 else ""

                    # Write show command for all currently visible characters
                    for char in active_characters:
                        outfile.write(f'    {char}\n')

                # Dialogue line from a character
                case {"dialogue": {"character": char, "text": text}}:
                    char_var = char.lower()
                    dialogue_count[char_var] += 1  # Track speaker frequency

                    # If character not currently on screen
                    if not any(c.name == char_var for c in active_characters):
                        if len(active_characters) >= 3:
                            # Remove the least speaking character
                            least_speaking = min(active_characters, key=lambda c: dialogue_count[c.name])
                            position = least_speaking.position
                            outfile.write(f'    hide {least_speaking.name}\n')
                            active_characters.remove(least_speaking)
                            active_characters.append(CharacterState(char_var, position=position))
                            outfile.write(f'    {active_characters[-1]}\n')

                    # Write the Ren'Py dialogue line
                    outfile.write(f'    {char} "{text}"\n')

                # Menu with options
                case {"menu": question, "options": options}:
                    removeChar(active_characters, outfile)  # Clear characters before menu
                    outfile.write(f'    menu:\n        "{question}"\n')  # Question prompt
                    for opt in options:
                        outfile.write(f'        "{opt["text"]}" :\n            jump {opt["jump"]}\n')  # Option + jump

                # Unknown/unexpected entry
                case _:
                    print(f"Unknown entry type: {entry}")

        # Final return statement if inside a label
        if active_label:
            outfile.write('    return\n')

    print(f"Converted {json_input} -> {output_file}")

# Example usage: converts input2.json to script.rpy
convert_json_to_rpy('testConversion/input2.json', 'testConversion/script.rpy')
