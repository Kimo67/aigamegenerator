import ollama
import os
from datetime import datetime

class StoryNode:
    def __init__(self, text, parent=None, session=None):
        self.session = session
        self.text = text
        self.parent = parent
        self.children = []
        self.characters = self.extract_characters(text, session)
    
    def extract_characters(self, text, session):
        prompt = f"Donne moi le nom des personnages qui parlent explicitement présents dans ce bout d'histoire :\n{text}\n\nLa liste des personnages doit être ainsi : [NOM] - [NOM] - [NOM], n'envoie que la liste de noms."
        response = generate_text(session, prompt, max_tokens=50) if session else ""
        return response.strip()
    
    def add_child(self, text):
        child_node = StoryNode(text, parent=self, session=self.session)
        self.children.append(child_node)
        return child_node

def initialize_model(model="huihui_ai/qwen2.5-abliterate:14b"):
    print("Chargement du modèle, veuillez patienter...")
    ollama.pull(model)  # Assure que le modèle est bien téléchargé et prêt
    return model

def generate_text(session, prompt, max_tokens=100):
    response = ollama.chat(model=session, messages=[{"role": "user", "content": prompt}], options={"max_tokens": max_tokens})
    return response["message"].get("content", "")

def main():
    print("Bienvenue dans le générateur d'histoires interactives !")
    context = input("Entrez une phrase de départ décrivant le contexte de votre histoire : ")
    
    session = initialize_model()
    context_with_instruction = "Tu es un générateur d'histoires interactives de type Visual Novel. L'utilisateur te fournit un contexte initial et tu dois générer une histoire immersive en plusieurs étapes en français en gardant un style proche des visual novel avec des dialogues entre les passages narratifs." + context
    root = StoryNode(context_with_instruction, session=session)
    current_node = root
    
    while True:
        prompt = "\n".join([node.text for node in get_story_path(current_node)]) + "\nContinue l'histoire avec des réponses concises (maximum 5 phrases) sans jamais proposer de choix."
        
        print("\nGénération en cours...")
        story_part = generate_text(session, prompt, max_tokens=100)
        print("\n--- Nouvelle partie de l'histoire ---\n")
        print(story_part)
        current_node = current_node.add_child(story_part)
        
        user_input = input("Que se passe-t-il ensuite ? (Tapez '/fin' pour terminer) ")
        if user_input.strip().lower() == "/fin":
            print("\nFinalisation de l'histoire en cours...")
            final_prompt = "\n".join([node.text for node in get_story_path(current_node)]) + "\nTermine l'histoire de manière satisfaisante et cohérente."
            final_part = generate_text(session, final_prompt, max_tokens=75)
            print("\n--- Fin de l'histoire ---\n")
            print(final_part)
            current_node.add_child(final_part)
            break
        current_node = current_node.add_child(user_input)
    
    # Sauvegarde de l'histoire
    save_story(root)

def get_story_path(node):
    path = []
    while node:
        path.insert(0, node)
        node = node.parent
    return path

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

if __name__ == "__main__":
    main()
