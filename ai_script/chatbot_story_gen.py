import ollama
import os
from datetime import datetime

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
    
    history = ["Tu es un générateur d'histoires interactives. L'utilisateur te fournit un contexte initial et tu dois générer une histoire immersive en plusieurs étapes en français.", "*" + context + "*"]
    
    session = initialize_model()
    
    for i in range(5):
        prompt = "\n".join(history) + "\nContinue l'histoire avec des réponses concises (maximum 5 phrases)."
        
        if i == 4:
            prompt += "\nTermine l'histoire de manière satisfaisante en restant bref."
        
        print("\nGénération en cours...")
        story_part = generate_text(session, prompt, max_tokens=100)
        print("\n--- Nouvelle partie de l'histoire ---\n")
        print(story_part)
        history.append(story_part)
        
        if i < 4:
            user_input = input("Que se passe-t-il ensuite ? ")
            history.append("*" + user_input + "*")
    
    # Nettoyage du texte pour ne garder que l'histoire sans les interventions de l'utilisateur et l'instruction IA
    cleaned_story = "\n".join([line for line in history if not line.startswith("*") and "générateur d'histoires" not in line])
    
    # Création du dossier histoires s'il n'existe pas
    os.makedirs("histoires", exist_ok=True)
    
    # Génération du nom de fichier avec la date
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    story_filename = f"histoires/histoire_{timestamp}.txt"
    
    # Sauvegarde de l'histoire nettoyée
    with open(story_filename, "w", encoding="utf-8") as f:
        f.write(cleaned_story)
    
    print(f"\nL'histoire a été sauvegardée dans {story_filename}.")

if __name__ == "__main__":
    main()
