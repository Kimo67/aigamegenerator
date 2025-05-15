from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from model import initialize_model  # Assure-toi que le modèle est importé
from story_node import StoryNode
import requests
from pydantic import BaseModel
from prompt_manager import initial_prompt, continuation_prompt, final_prompt
from model import initialize_model, generate_text
from pydantic import BaseModel
from pathlib import Path
import json
import time
from collections import Counter
from typing import Dict, Any, Union
from rpyScript.jsonParser_v2 import convert_json_tree_to_rpy

app = FastAPI()
session = None
root_story = None

DJANGO_API_CASE_URL = "http://django-app:8001/api/case/"

############### API CALL STARTUP
############### HAPPENS WHEN API STARTS 
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
############### API CALL STARTUP
############### HAPPENS WHEN API STARTS

################################################################################

############### API CALL - STORY TREE
############### DISPLAYS THE STORY TREE, USED FOR DEBUG PURPOUSES
'''
Api call that returns the complete story in the form of a tree dictionnary
'''
@app.get("/story/tree")
async def get_story_tree():
    global root_story
    StoryNode.print_tree(root_story)
    if root_story is None:
        return JSONResponse(status_code=404, content={"message": "Story not found"})
    
    # Convert the tree to a dictionary and return it as JSON
    tree_data = root_story.tree_to_dict()
    return JSONResponse(content=tree_data)
############### API CALL - STORY TREE
############### DISPLAYS THE STORY TREE, USED FOR DEBUG PURPOUSES

################################################################################

############### API CALL SYNCH STORY 
############### CALLS THE DJANGO API TO GET THE STORY FROM IT AND INITIALIZES IT IN THE AI.
@app.get("/sync-story-with-cases")
async def sync_story_with_cases():
    """
    Syncs the story with cases from the Django API by adding each case as a child to the root node.
    """
    global root_story
    try:
        # Fetch all cases for the given story ID from the Django API
        response = requests.get(DJANGO_API_CASE_URL)
        
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


'''
Helper function that adds a case to a story
'''
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
        node.repliques = [case.get("repliques", "")] if case.get("repliques") else []
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
############### API CALL SYNCH STORY 
############### CALLS THE DJANGO API TO GET THE STORY FROM IT AND INITIALIZES IT IN THE AI.

################################################################################

############### API CALL - ADD NODE
############### ADDS A NODE BASED ON A PROMPT SENT BY FRONTEND WITH POST METHOD
class AddNodeRequest(BaseModel):
    prompt: str
    parent_id: int
    id: int

def find_node_by_id(node, target_id):
    if getattr(node, "id", None) == target_id:
        return node

    for child in node.children:
        result = find_node_by_id(child, target_id)
        if result:
            return result
    return None

@app.post("/story/add-node")
async def add_node(request: AddNodeRequest):
    global root_story

    parent_node = find_node_by_id(root_story, request.parent_id)
    if parent_node is None:
        raise HTTPException(status_code=404, detail="Parent node not found.")

    prompt_suite = continuation_prompt(parent_node, request.prompt)
    story_part = generate_text(session, prompt_suite, max_tokens=50)
    print("\n--- Nouvelle partie de l'histoire ---\n")
    print(story_part)

    # Create new node and attach it
    new_node = StoryNode(story_part, parent=parent_node, session=session)
    new_node.id = request.id
    parent_node.children.append(new_node)

    return JSONResponse(new_node.tree_to_dict())
############### API CALL - ADD NODE
############### ADDS A NODE BASED ON A PROMPT SENT BY FRONTEND WITH POST METHOD

################################################################################


############### API CALL - ADD NODE START - INIT PROMPT
############### ADDS A NODE BASED ON A PROMPT SENT BY FRONTEND WITH POST METHOD - INIT PROMPT

@app.post("/story/add-node-start")
async def add_node(request: AddNodeRequest):
    global root_story

    parent_node = find_node_by_id(root_story, 0)
    if parent_node is None:
        raise HTTPException(status_code=404, detail="Parent node not found.")

    prompt_suite = initial_prompt(request.prompt)
    story_part = generate_text(session, prompt_suite, max_tokens=50)
    print("\n--- Nouvelle partie de l'histoire ---\n")
    print(story_part)

    # Create new node and attach it
    new_node = StoryNode(story_part, parent=parent_node, session=session)
    new_node.id = request.id
    parent_node.children.append(new_node)

    return JSONResponse(content=new_node.tree_to_dict())
############### API CALL - ADD NODE START - INIT PROMPT
############### ADDS A NODE BASED ON A PROMPT SENT BY FRONTEND WITH POST METHOD - INIT PROMPT

################################################################################

# Request model
class RenpyRequest(BaseModel):
    data: Dict[str, Any]

@app.get("/renpy")
async def generate_rpy():
    # Generate unique filename based on timestamp
    global root_story
    timestamp = int(time.time() * 1000)
    json_filename = f"input_{timestamp}.json"
    rpy_filename = f"output_{timestamp}.rpy"
    print("before")
    backend_path = Path("/backend/backend")
    print("after")
    # Paths for saved files
    json_path = backend_path / json_filename
    rpy_path = backend_path / rpy_filename

    # Save raw JSON to file
    json_path.write_text(json.dumps(StoryNode.tree_to_dict(root_story), indent=2), encoding="utf-8")

    # Convert JSON file to rpy
    convert_json_tree_to_rpy(json_path, rpy_path)

    return {
        "message": "Conversion successful",
        "json_path": str(json_path.resolve()),
        "rpy_path": str(rpy_path.resolve()),
    }