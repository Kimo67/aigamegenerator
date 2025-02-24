import ollama
import os
from datetime import datetime
import tkinter as tk

# Paramètres de mise en page et style
horizontal_spacing = 200   # espace horizontal entre les feuilles
vertical_spacing = 100     # espace vertical entre les niveaux
node_width = 140
node_height = 50

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
        self.characters = self.extract_characters(text, session)
    
    def extract_characters(self, text, session):
        prompt = (
            f"Donne moi le nom des personnages qui parlent explicitement présents dans ce bout d'histoire :\n"
            f"{text}\n\n"
            "La liste des personnages doit être ainsi : [NOM] - [NOM] - [NOM], n'envoie que la liste de noms."
        )
        response = generate_text(session, prompt, max_tokens=50) if session else ""
        return response.strip()
    
    def add_child(self, text):
        child_node = StoryNode(text, parent=self, session=self.session)
        self.children.append(child_node)
        return child_node

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
    node.y = depth * vertical_spacing + 50
    if not node.children:
        node.x = compute_tree_positions.counter * horizontal_spacing + node_width//2 + 20
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
        
        # Dessin du rectangle arrondi
        create_rounded_rectangle(canvas, x0, y0, x1, y1, radius=10,
                                 fill="lightyellow", outline="black", width=2)
        
        # Affichage d'un extrait du texte (limité à 30 caractères)
        display_text = node.text.strip().replace("\n", " ")
        if len(display_text) > 30:
            display_text = display_text[:30] + "..."
        canvas.create_text(x, y, text=display_text, font=("Helvetica", 10), width=node_width-10)
        
        # Liaisons avec les enfants (ligne lisse entre le bas du parent et le haut de l'enfant)
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
    canvas = tk.Canvas(viz_window, width=1200, height=800, bg="white")
    canvas.pack(side="left", fill="both", expand=True)
    
    print("Bienvenue dans le générateur d'histoires interactives !")
    context = input("Entrez une phrase de départ décrivant le contexte de votre histoire : ")
    
    session = initialize_model()
    context_with_instruction = (
        "Tu es un générateur d'histoires interactives de type Visual Novel. "
        "L'utilisateur te fournit un contexte initial et tu dois générer une histoire immersive en plusieurs étapes en français "
        "en gardant un style proche des visual novel avec des dialogues entre les passages narratifs. " + context
    )
    root_story = StoryNode(context_with_instruction, session=session)
    current_node = root_story
    
    update_tree_visualization(root_story, canvas)
    viz_window.update()
    
    while True:
        prompt = "\n".join([node.text for node in get_story_path(current_node)]) + \
                 "\nContinue l'histoire avec des réponses concises (maximum 5 phrases) sans jamais proposer de choix."
        
        print("\nGénération en cours...")
        story_part = generate_text(session, prompt, max_tokens=100)
        print("\n--- Nouvelle partie de l'histoire ---\n")
        print(story_part)
        current_node = current_node.add_child(story_part)
        
        update_tree_visualization(root_story, canvas)
        viz_window.update()
        
        user_input = input("Que se passe-t-il ensuite ? (Tapez '/fin' pour terminer) ")
        if user_input.strip().lower() == "/fin":
            print("\nFinalisation de l'histoire en cours...")
            final_prompt = "\n".join([node.text for node in get_story_path(current_node)]) + \
                           "\nTermine l'histoire de manière satisfaisante et cohérente."
            final_part = generate_text(session, final_prompt, max_tokens=75)
            print("\n--- Fin de l'histoire ---\n")
            print(final_part)
            current_node.add_child(final_part)
            update_tree_visualization(root_story, canvas)
            viz_window.update()
            break
        
        current_node = current_node.add_child(user_input)
        update_tree_visualization(root_story, canvas)
        viz_window.update()
    
    save_story(root_story)
    print("Appuyez sur Entrée pour fermer la fenêtre graphique...")
    input()
    viz_window.destroy()

if __name__ == "__main__":
    main()
