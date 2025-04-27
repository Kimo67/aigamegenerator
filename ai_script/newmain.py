from model import initialize_model, generate_text
from story_node import StoryNode
from prompt_manager import initial_prompt, continuation_prompt, final_prompt
from utils import save_story

def main():
    print("Bienvenue dans le générateur d'histoires interactives !")
    context = input("Entrez une phrase de départ décrivant le contexte de votre histoire : ")

    session = initialize_model()
    prompt_intro = initial_prompt(context)

    intro_part = generate_text(session, prompt_intro, max_tokens=50)
    print("\n--- Introduction de l'histoire ---\n")
    print(intro_part)

    root_story = StoryNode(intro_part, session=session)
    current_node = root_story

    while True:
        user_input = input("Que se passe-t-il ensuite ? (Tapez '/fin' pour terminer) ").strip()
        if user_input.strip().lower() == "/fin":
            prompt_fin = final_prompt(current_node)
            final_part = generate_text(session, prompt_fin, max_tokens=75)
            print("\n--- Fin de l'histoire ---\n")
            print(final_part)
            current_node.add_child(final_part)
            root_story.print_tree()
            break

        prompt_suite = continuation_prompt(current_node, user_input)
        story_part = generate_text(session, prompt_suite, max_tokens=50)
        print("\n--- Nouvelle partie de l'histoire ---\n")
        print(story_part)
        current_node = current_node.add_child(story_part)

    save_story(root_story)

if __name__ == "__main__":
    main()
