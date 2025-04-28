from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from model import initialize_model  # Assure-toi que le modèle est importé
from story_node import StoryNode
import requests

app = FastAPI()
session = None
root_story = None

@app.on_event("startup")
async def startup_event():
    global session, root_story
    print("L'application FastAPI est démarrée !")
    # Initialiser le modèle
    session = initialize_model()  # Imaginons que c'est l'initialisation de ton modèle
    print("Modèle initialisé avec succès !")
    
    # Créer le premier nœud de l'histoire (exemple basique)
    initial_text = "Ceci est le début de notre histoire."
    root_story = StoryNode(initial_text, session=session)
    print(f"Premier nœud de l'histoire créé : {root_story.text}")


@app.get("/story/tree")
async def get_story_tree():
    global root_story
    StoryNode.print_tree(root_story)
    if root_story is None:
        return JSONResponse(status_code=404, content={"message": "Story not found"})
    
    # Convert the tree to a dictionary and return it as JSON
    tree_data = root_story.tree_to_dict()
    return JSONResponse(content=tree_data)


DJANGO_API_URL = "http://django-app:8001/api/case/"

def add_case_to_story(cases, story_node):
    """
    Build the story tree properly by linking cases to their parent nodes.
    """
    id_to_node = {}  # Map of case ID -> StoryNode

    # First pass: create all nodes
    for case in cases:
        case_text = case.get("text") or case.get("title") or "No Text"
        node = StoryNode(text=case_text)

        # Attach additional info
        node.scene = case.get("background", "")
        node.repliques = [case.get("description", "")] if case.get("description") else []
        node.id = case.get("id")
        # Store the case ID in the node's session or scene if needed
        node.session = {"id": case["id"]}

        id_to_node[case["id"]] = node

    # Second pass: assign children to parents
    for case in cases:
        node = id_to_node[case["id"]]
        parent_id = case.get("parent")

        if parent_id:
            parent_node = id_to_node.get(parent_id)
            if parent_node:
                parent_node.children.append(node)
            else:
                # Orphan node, no known parent -> attach to root
                story_node.children.append(node)
        else:
            # No parent -> attach to root
            story_node.children.append(node)

    return story_node

@app.get("/sync-story-with-cases")
async def sync_story_with_cases():
    """
    Syncs the story with cases from the Django API by adding each case as a child to the root node.
    """
    global root_story
    try:
        # Fetch all cases for the given story ID from the Django API
        response = requests.get(DJANGO_API_URL)
        
        if response.status_code == 200:
            cases = response.json()  # Extract cases from the API response
            
            # Create the root story node (assuming you can create it here)
            root_story = StoryNode("Root Story Text")  # Placeholder for the root story node text
            
            # Add cases to the root story node
            updated_story = add_case_to_story(cases, root_story)
            
            # Optionally print the tree for debugging purposes
            updated_story.print_tree()  # Or, convert to a dictionary or JSON if you need to return it
            
            return JSONResponse(content={"message": "Story synced with cases", "tree": "Tree updated successfully!"})
        else:
            print("Code status : " + str(response.status_code))
            print(response.text)
            raise HTTPException(status_code=response.status_code, detail="Error fetching cases from Django API")
    
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while requesting the Django API: {e}")
