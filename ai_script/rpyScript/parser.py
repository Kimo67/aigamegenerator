import re
from collections import Counter

def removeChar(active_characters, outfile):
    for char in active_characters:
        outfile.write(f'    hide {char.name}\n')
    active_characters.clear()

def convert_to_rpy(input_file, output_file):
    class CharacterState:
        def __init__(self, name, emotion="", position=""):
            self.name = name
            self.emotion = emotion
            self.position = position

        def __str__(self):
            return f'show {self.name} {self.emotion} {self.position}'.strip()

    with open(input_file, 'r') as infile:
        lines = infile.readlines()

    with open(output_file, 'w') as outfile:
        characters = {}
        active_label = None
        active_characters = []  # List of CharacterState objects
        dialogue_count = Counter()  # Tracks how many times each character has spoken
        show_commands = {}  # Tracks which characters have been shown and their emotions

        for line in lines:
            line = line.strip()
            keyword = line.split(' ', 1)[0].strip('[]') if line.startswith('[') else None
            
            match keyword:
                case 'CHARACTERS':
                    continue
                case 'LABEL':
                    if active_label:
                        removeChar(active_characters, outfile)
                        outfile.write('    return\n')  # Close previous label
                    
                    label = line.replace('[LABEL]', '').strip()
                    active_label = label
                    outfile.write(f'label {label}:\n')
                case 'JUMP':
                    removeChar(active_characters, outfile)
                    jump_command = line.replace('[JUMP]', '').strip()
                    outfile.write(f'    jump {jump_command}\n')
                case 'SCENE':
                    scene_command = line.replace('[SCENE]', '').strip()
                    if active_label:
                        outfile.write(f'    scene {scene_command}\n')
                    else:
                        outfile.write(f'scene {scene_command}\n')
                    show_commands.clear()
                    active_characters.clear()
                case 'SHOW':
                    show_command = line.replace('[SHOW]', '').strip().split()
                    char_name = show_command[0].lower()
                    emotion = " ".join(show_command[1:]) if len(show_command) > 1 else ""
                    
                    if char_name not in show_commands or show_commands[char_name] != emotion:
                        show_commands[char_name] = emotion  # Store the character and their emotion
                    
                    if not any(c.name == char_name for c in active_characters):
                        if len(active_characters) < 3:
                            active_characters.append(CharacterState(char_name, emotion))
                        else:
                            # Replace the character that has spoken the least
                            least_speaking_char = min(active_characters, key=lambda c: dialogue_count[c.name])
                            position_to_use = least_speaking_char.position  # Keep the position of removed character
                            active_characters.remove(least_speaking_char)
                            active_characters.append(CharacterState(char_name, emotion, position_to_use))
                            outfile.write(f'    hide {least_speaking_char.name}\n')
                    
                    # Assign positions based on active characters count
                    positions = ["at left", "at center", "at right"]
                    for i, char in enumerate(active_characters):
                        if not char.position:  # Only update position if it's not set
                            char.position = positions[i] if len(active_characters) > 1 else ""
                    
                    for char in active_characters:
                        outfile.write(f'    {char}\n')
                case 'HIDE':
                    hide_command = line.replace('[HIDE]', '').strip()
                    outfile.write(f'    hide {hide_command}\n')
                case 'DIALOGUE':
                    match = re.match(r'\[DIALOGUE\] (.*?): (.*)', line)
                    if match:
                        character, dialogue = match.groups()
                        char_var = character.lower()
                        
                        # Track dialogue count
                        dialogue_count[char_var] += 1
                        
                        if not any(c.name == char_var for c in active_characters):
                            if len(active_characters) >= 3:
                                # Replace the character that has spoken the least
                                least_speaking_char = min(active_characters, key=lambda c: dialogue_count[c.name])
                                position_to_use = least_speaking_char.position  # Keep the position of removed character
                                active_characters.remove(least_speaking_char)
                                outfile.write(f'    hide {least_speaking_char.name}\n')
                                active_characters.append(CharacterState(char_var, position=position_to_use))
                                outfile.write(f'    {active_characters[-1]}\n')
                        
                        outfile.write(f'    {character} "{dialogue}"\n')
                case 'COMMAND':
                    command = line.replace('[COMMAND]', '').strip()
                    outfile.write(f'    {command}\n')
                case 'MENU':
                    removeChar(active_characters, outfile)
                    menu_text = line.replace('[MENU]', '').strip()
                    outfile.write(f'    menu:\n        "{menu_text}"\n')
                case _ if re.match(r'- .*? -> .*', line):
                    option, path = re.match(r'- (.*?) -> (.*)', line).groups()
                    outfile.write(f'        "{option}" :\n            jump {path}\n')
                case _ if ',' in line and not line.startswith('['):
                    char_name, char_color = [part.strip() for part in line.split(',', 1)]
                    char_var = char_name.replace(' ', '_')
                    characters[char_name] = char_color
                    outfile.write(f'define {char_var} = Character("{char_name}", color="{char_color}")\n')
                case None:
                    if line:
                        outfile.write(f'    "{line}"\n')  # Narrator text

        if active_label:
            outfile.write('    return\n')  # Close final label if needed

    print(f'Converted {input_file} to {output_file}')

# Example usage:
convert_to_rpy('testConversion/input1.txt', 'testConversion/script.rpy')