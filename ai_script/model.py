import ollama
import subprocess
import time

def initialize_model(model="qwen2.5:3b"):
# Running a simple shell command (e.g., 'ls')
    subprocess.Popen(['ollama', 'serve'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)
    print("Chargement du modèle, veuillez patienter...")
    ollama.pull(model)
    return model

def generate_text(session, prompt, max_tokens=100):
    response = ollama.chat(
        model=session,
        messages=[{"role": "user", "content": prompt}],
        options={"max_tokens": max_tokens}
    )
    return response["message"].get("content", "")

def summarize_for_image_prompt(session, text, max_tokens=5):
    prompt = (
        "Tu es un assistant de génération d'images pour visual novels. "
        "Analyse le texte suivant et résume-le en une scène visuelle adaptée comme fond d'écran : "
        "décris uniquement le décor (pas les personnages), de façon évocatrice et compatible avec une image générée par une IA. "
        "Sois synthétique, mais assez détaillé pour donner une idée claire du lieu ou de l'ambiance visuelle. "
        "Ne renvoie qu'une liste de mots clés décrivant une image"
        "Voici le texte à analyser :\n\n"
        f"{text}"
    )
    response = ollama.chat(
        model=session,
        messages=[{"role": "user", "content": prompt}],
        options={"max_tokens": max_tokens}
    )
    return response["message"].get("content", "")