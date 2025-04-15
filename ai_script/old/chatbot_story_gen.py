import ollama
import os
from datetime import datetime
import tkinter as tk
import re

# Paramètres de mise en page et style
horizontal_spacing = 200   # espace horizontal entre les feuilles
vertical_spacing = 120     # espace vertical entre les niveaux
node_width = 400           # on élargit le nœud
node_height = 100          # on augmente la hauteur du nœud

def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=10, **kwargs):
    """
    Dessine un rectangle aux coins arrondis sur le canvas.
    """
    points = [
        x1+radius, y1,
        x2-radius, y1,
        x2, y1,
        x2, y1+radius,
        x2, y2-radius,
        x2, y2,
        x2-radius, y2,
        x1+radius, y2,
        x1, y2,
        x1, y2-radius,
        x1, y1+radius,
        x1, y1
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)

class StoryNode:
    def __init__(self, text, parent=None, session=None):
        self.session = session
        self.text = text
        self.parent = parent
        self.children = []
        self.characters = self.extract_characters()
        self.emotions = self.extract_emotions()
        self.repliques = self.extract_repliques()
        self.scene = ""  # Chemin vers un fichier JPEG représentant la scène

    def extract_characters(self):
        return list(set(re.findall(r'\$(.*?)\$', self.text)))

    def extract_emotions(self):
        return list(set(re.findall(r'%(.*?)%', self.text)))

    def extract_repliques(self):
        pattern = r'\$(.*?)\$\s*:\s*(.*?)\s*%(.*?)%'
        repliques = []
        # On cherche toutes les occurrences correspondant au pattern dans le texte
        # Le pattern extrait :
        # - Le nom du personnage entre les signes $ : (.*?)
        # - Le texte de la réplique après ":" et avant "%" : (.*?)
        # - L'émotion spécifiée entre les signes % : (.*?)
        for match in re.findall(pattern, self.text):
            personnage, texte, emotion = match
            # On exclut les répliques du narrateur, on ne garde que les répliques des personnages
            if personnage.strip().upper() != "NARRATEUR":
                repliques.append({
                    "personnage": personnage.strip(),
                    "texte": texte.strip(),
                    "emotion": emotion.strip()
                })
        return repliques

    def add_child(self, text):
        child_node = StoryNode(text, parent=self, session=self.session)
        self.children.append(child_node)
        return child_node

    def print_tree(self, depth=0):
        indent = "  " * depth
        print(f"{indent}Texte: {self.text}")
        print(f"{indent}Personnages: {self.characters}")
        print(f"{indent}Émotions: {self.emotions}")
        print(f"{indent}Répliques:")
        for rep in self.repliques:
            print(f"{indent}  {rep}")
        print(f"{indent}Scène: {self.scene}")
        for child in self.children:
            child.print_tree(depth + 1)

def initialize_model(model="huihui_ai/qwen2.5-abliterate:14b"):
    print("Chargement du modèle, veuillez patienter...")
    ollama.pull(model)  # S'assure que le modèle est bien téléchargé et prêt
    return model

def generate_text(session, prompt, max_tokens=100):
    response = ollama.chat(
        model=session,
        messages=[{"role": "user", "content": prompt}],
        options={"max_tokens": max_tokens}
    )
    return response["message"].get("content", "")

def compute_tree_positions(node, depth=0):
    """
    Algorithme récursif simple pour positionner les nœuds.
    Chaque feuille se voit attribuer une position horizontale selon un compteur,
    et les parents sont centrés au-dessus de leurs enfants.
    """
    if not hasattr(compute_tree_positions, "counter"):
        compute_tree_positions.counter = 0
    node.y = depth * vertical_spacing + 60
    if not node.children:
        node.x = compute_tree_positions.counter * horizontal_spacing + node_width//2 + 50
        compute_tree_positions.counter += 1
    else:
        for child in node.children:
            compute_tree_positions(child, depth+1)
        node.x = (node.children[0].x + node.children[-1].x) / 2

def update_tree_visualization(tree_root, canvas):
    """
    Calcule les positions des nœuds, efface le canvas,
    et redessine l'arbre avec des cases arrondies et des liaisons.
    """
    compute_tree_positions.counter = 0
    compute_tree_positions(tree_root, depth=0)
    canvas.delete("all")
    
    def draw_node(node):
        x, y = node.x, node.y
        # Coordonnées du rectangle (centré sur (x, y))
        x0 = x - node_width/2
        y0 = y - node_height/2
        x1 = x + node_width/2
        y1 = y + node_height/2
        
        # Dessin du rectangle arrondi (fond jaune clair, texte noir)
        create_rounded_rectangle(
            canvas, x0, y0, x1, y1, radius=10,
            fill="lightyellow", outline="black", width=2
        )
        
        # Affichage d'un extrait du texte (jusqu’à 150 caractères) en noir
        display_text = node.text.strip().replace("\n", " ")
        max_chars = 150
        if len(display_text) > max_chars:
            display_text = display_text[:max_chars] + "..."
        
        canvas.create_text(
            x, y,
            text=display_text,
            fill="black",               
            font=("Helvetica", 10),
            width=node_width - 20,      
            anchor="center"
        )
        
        # Liaisons avec les enfants
        for child in node.children:
            parent_bottom = (x, y + node_height/2)
            child_top = (child.x, child.y - node_height/2)
            canvas.create_line(parent_bottom, child_top, smooth=True, width=2, fill="gray")
            draw_node(child)
    
    draw_node(tree_root)
    canvas.update()

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

def main():
    # Création de la fenêtre graphique
    viz_window = tk.Tk()
    viz_window.title("Arbre de l'histoire")
    canvas = tk.Canvas(viz_window, width=1400, height=900, bg="white")
    canvas.pack(side="left", fill="both", expand=True)
    
    print("Bienvenue dans le générateur d'histoires interactives !")
    context = input("Entrez une phrase de départ décrivant le contexte de votre histoire : ")
    
    session = initialize_model()
    
    # Prépare l'instruction pour la première génération
    # (On ne met pas le 'context' dans l'arbre, on l'utilise juste pour la 1re génération)
    context_with_instruction = (
        "Tu es un générateur d'histoires interactives de type Visual Novel. "
        "L'utilisateur te fournit un contexte initial et tu dois générer une histoire immersive en plusieurs étapes en français "
        "en gardant un style proche des visual novel avec des dialogues entre les passages narratifs. "
        "N'envoie que l'histoire en français et rien d'autre"
        "Débute chaque ligne par la personne qui parle écrite entre deux signes $, si personne ne parle écrit $NARRATEUR$, par exemple pour une histoire basique ça serait : $NARRATEUR$ L'histoire se déroule dans le royaume champignon."
        "$MARIO$ : Bonjour comment vas-tu ?"
        "Ajoute à la fin de chaque ligne qui n'est pas dite par le narrateur l'émotion entre ANGRY, HAPPY et NEUTRAL, écrit ça à la fin de la ligne entre deux signe %, c'est à dire %HAPPY% par exemple"
        + context
    )
    
    # Génére immédiatement une introduction depuis ce contexte
    print("\nGénération de l'introduction de l'histoire...")
    intro_part = generate_text(session, context_with_instruction, max_tokens=50)
    print("\n--- Introduction de l'histoire ---\n")
    print(intro_part)
    
    # On crée le noeud racine uniquement avec le texte généré (pas le contexte utilisateur)
    root_story = StoryNode(intro_part, session=session)
    current_node = root_story
    
    # Mise à jour de l'affichage
    update_tree_visualization(root_story, canvas)
    viz_window.update()
    
    # Boucle d'interaction
    while True:
        user_input = input("Que se passe-t-il ensuite ? (Tapez '/fin' pour terminer) ")
        if user_input.strip().lower() == "/fin":
            # On génère la fin en se basant uniquement sur les textes déjà générés
            print("\nFinalisation de l'histoire en cours...")
            final_prompt = (
            "\n".join([node.text for node in get_story_path(current_node)]) 
            + "\nTermine l'histoire de manière satisfaisante et cohérente."
            " Débute chaque ligne par la personne qui parle écrite entre deux signes $, "
            "si personne ne parle écrit $NARRATEUR$, par exemple pour une histoire basique ça serait : "
            "$NARRATEUR$ L'histoire se déroule dans le royaume champignon. "
            "$MARIO$ : Bonjour comment vas-tu ? "
            "Ajoute à la fin de chaque ligne qui n'est pas dite par le narrateur l'émotion entre ANGRY, HAPPY et NEUTRAL, "
            "écrit ça à la fin de la ligne entre deux signe %, c'est à dire %HAPPY% par exemple."
)

            final_part = generate_text(session, final_prompt, max_tokens=75)
            print("\n--- Fin de l'histoire ---\n")
            print(final_part)
            current_node.add_child(final_part)
            update_tree_visualization(root_story, canvas)
            viz_window.update()
            root_story.print_tree()
            break
        
        # On construit un prompt : concaténation des textes générés + l'entrée utilisateur
        # (Mais on n'ajoute PAS l'entrée utilisateur dans l'arbre)
        prompt = ("\n".join([node.text for node in get_story_path(current_node)]) \
                 + "\n" + user_input \
                 + "\nContinue l'histoire avec des réponses concises (maximum 5 phrases) sans jamais proposer de choix."
                  " Débute chaque ligne par la personne qui parle écrite entre deux signes $, "
                    "si personne ne parle écrit $NARRATEUR$, par exemple pour une histoire basique ça serait : "
                    "$NARRATEUR$ L'histoire se déroule dans le royaume champignon. "
                    "$MARIO$ : Bonjour comment vas-tu ? "
                    "Ajoute à la fin de chaque ligne qui n'est pas dite par le narrateur l'émotion entre ANGRY, HAPPY et NEUTRAL, "
                    "écrit ça à la fin de la ligne entre deux signe %, c'est à dire %HAPPY% par exemple."

        )
        print("\nGénération en cours...")
        story_part = generate_text(session, prompt, max_tokens=50)
        print("\n--- Nouvelle partie de l'histoire ---\n")
        print(story_part)
        
        # On ajoute la nouvelle partie générée comme enfant
        current_node = current_node.add_child(story_part)
        
        update_tree_visualization(root_story, canvas)
        viz_window.update()
    
    # Sauvegarde de l'histoire complète
    save_story(root_story)
    print("Appuyez sur Entrée pour fermer la fenêtre graphique...")
    input()
    viz_window.destroy()

if __name__ == "__main__":
    main()
