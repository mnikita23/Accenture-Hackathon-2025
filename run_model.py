import subprocess

def query_model(prompt: str, model: str = "phi") -> str:
    # This function queries the Ollama model using subprocess
    try:
        result = subprocess.run(["ollama", "run", model], input=prompt.encode(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
        return result.stdout.decode()
    except Exception as e:
        return f"Error querying Ollama model: {e}"
