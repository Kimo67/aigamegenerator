import ollama

def initialize_model(model="huihui_ai/qwen2.5-abliterate:14b"):
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
