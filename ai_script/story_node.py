import re

class StoryNode:
    def __init__(self, text, parent=None, session=None):
        self.session = session
        self.text = text
        self.parent = parent
        self.children = []
        self.choix = []  # Liste des choix textuels proposés par l'utilisateur
        self.characters = self.extract_characters()
        self.emotions = self.extract_emotions()
        self.repliques = self.extract_repliques()
        self.scene = ""

    def extract_characters(self):
        return list(set(re.findall(r'\$(.*?)\$', self.text)))

    def extract_emotions(self):
        return list(set(re.findall(r'%(.*?)%', self.text)))

    def extract_repliques(self):
        pattern = r'\$(.*?)\$\s*:\s*(.*?)\s*%(.*?)%'
        repliques = []
        for match in re.findall(pattern, self.text):
            personnage, texte, emotion = match
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

    def add_sibling_choice(self, text, choix_utilisateur=""):
        """
        Ajoute un frère (autre choix au même niveau).
        """
        if not self.parent:
            raise ValueError("La racine ne peut pas avoir de frère.")
        sibling_node = StoryNode(text, parent=self.parent, session=self.session)
        self.parent.children.append(sibling_node)
        if choix_utilisateur:
            self.parent.choix.append(choix_utilisateur)
        return sibling_node

    def definir_choix(self, liste_choix):
        """
        Définit les choix textuels possibles à partir de ce nœud.
        """
        self.choix = liste_choix

    def print_tree(self, depth=0):
        indent = "  " * depth
        print(f"{indent}Texte: {self.text}")
        if self.choix:
            print(f"{indent}Choix possibles: {self.choix}")
        print(f"{indent}Personnages: {self.characters}")
        print(f"{indent}Émotions: {self.emotions}")
        print(f"{indent}Répliques:")
        for rep in self.repliques:
            print(f"{indent}  {rep}")
        print(f"{indent}Scène: {self.scene}")
        for child in self.children:
            child.print_tree(depth + 1)
