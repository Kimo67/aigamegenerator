from story_node import StoryNode

def initial_prompt(context):
    return (
        "Tu es un générateur d'histoires interactives de type Visual Novel. "
        "L'utilisateur te fournit un contexte initial et tu dois générer une histoire immersive en plusieurs étapes en français "
        "en gardant un style proche des visual novel avec des dialogues entre les passages narratifs. "
        "N'envoie que l'histoire en français et rien d'autre"
        "Débute chaque ligne par la personne qui parle écrite entre deux signes $, si personne ne parle écrit $NARRATEUR$, par exemple pour une histoire basique ça serait : $NARRATEUR$ L'histoire se déroule dans le royaume champignon."
        "$MARIO$ : Bonjour comment vas-tu ?"
        "Ajoute à la fin de chaque ligne qui n'est pas dite par le narrateur l'émotion entre ANGRY, HAPPY et NEUTRAL, écrit ça à la fin de la ligne entre deux signe %, c'est à dire %HAPPY% par exemple"
        + context
    )

def continuation_prompt(current_node, user_input):
    return ("\n".join([node.text for node in get_story_path(current_node)]) \
                 + "\n" + user_input \
                 + "\nContinue l'histoire avec des réponses concises (maximum 5 phrases) sans jamais proposer de choix."
                  " Débute chaque ligne par la personne qui parle écrite entre deux signes $, "
                    "si personne ne parle écrit $NARRATEUR$, par exemple pour une histoire basique ça serait : "
                    "$NARRATEUR$ L'histoire se déroule dans le royaume champignon. "
                    "$MARIO$ : Bonjour comment vas-tu ? "
                    "Ajoute à la fin de chaque ligne qui n'est pas dite par le narrateur l'émotion entre ANGRY, HAPPY et NEUTRAL, "
                    "écrit ça à la fin de la ligne entre deux signe %, c'est à dire %HAPPY% par exemple."
            )
def final_prompt(current_node):
    return (
        "\n".join([node.text for node in get_story_path(current_node)]) 
        + "\nTermine l'histoire de manière satisfaisante et cohérente."
        " Débute chaque ligne par la personne qui parle écrite entre deux signes $, "
        "si personne ne parle écrit $NARRATEUR$, par exemple pour une histoire basique ça serait : "
        "$NARRATEUR$ L'histoire se déroule dans le royaume champignon. "
        "$MARIO$ : Bonjour comment vas-tu ? "
        "Ajoute à la fin de chaque ligne qui n'est pas dite par le narrateur l'émotion entre ANGRY, HAPPY et NEUTRAL, "
        "écrit ça à la fin de la ligne entre deux signe %, c'est à dire %HAPPY% par exemple."
    )

def prompt_with_choice(current_node, user_choice):
    """
    Génère le prompt prenant en compte le choix utilisateur explicite.
    """
    return (
        "\n".join([node.text for node in get_story_path(current_node)])
        + "\nLe joueur a choisi l'option suivante : "
        + user_choice
        + "\nContinue l'histoire à partir de ce choix avec des réponses concises (maximum 5 phrases)."
    )

def get_story_path(node):
    path = []
    while node:
        path.insert(0, node)
        node = node.parent
    return path