import os
from datetime import datetime

def save_story(root):
    os.makedirs("histoires", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    story_filename = f"histoires/histoire_{timestamp}.txt"
    
    with open(story_filename, "w", encoding="utf-8") as f:
        def traverse(node, depth=0):
            f.write("  " * depth + node.text + "\n")
            f.write("  " * depth + f"Personnages : {node.characters}\n")
            for child in node.children:
                traverse(child, depth + 1)
        traverse(root)
    
    print(f"\nL'histoire a été sauvegardée dans {story_filename}.")
