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
