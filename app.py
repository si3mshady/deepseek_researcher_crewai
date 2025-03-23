from flask import Flask, request, jsonify
import subprocess
import time
import ollama

app = Flask(__name__)

# ✅ Use LLaMA 3.2 model with Ollama
MODEL_NAME = "llama3.2"

def is_ollama_running():
    try:
        result = subprocess.run(["pgrep", "-f", "ollama serve"], capture_output=True, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"[ERROR] Checking Ollama: {e}")
        return False

def start_ollama_server():
    if not is_ollama_running():
        print("🔄 Starting Ollama server...")
        subprocess.Popen(["ollama", "serve"])
        time.sleep(5)
    else:
        print("✅ Ollama server is already running.")

def pull_model():
    print(f"📦 Pulling model: {MODEL_NAME}")
    try:
        ollama.pull(MODEL_NAME)
        print(f"✅ Model '{MODEL_NAME}' is ready.")
    except Exception as e:
        print(f"[ERROR] Pulling model '{MODEL_NAME}': {e}")

@app.route('/webparser', methods=['POST'])
def webparser():
    data = request.get_json()
    topic = data.get('topic', '')
    url_content = data.get('content', '')

    if not topic or not url_content:
        return jsonify({"error": "Missing topic or content."}), 400

    prompt = f"""
    You are an expert relevance evaluator. Analyze the following webpage content for relevance to the topic: '{topic}'.
    Return only the relevant parts and summarize them clearly, focusing on insights, facts, or methods that could support research or teaching.

    Content:
    {url_content}
    """

    try:
        start_ollama_server()
        pull_model()
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[{'role': 'user', 'content': prompt}]
        )
        return jsonify({"response": response['message']['content']})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/markdown', methods=['POST'])
def markdown():
    data = request.get_json()
    topic = data.get('topic', '')
    artifact = data.get('artifact', '')

    if not topic or not artifact:
        return jsonify({"error": "Missing topic or artifact."}), 400

    prompt = f"""
    You are a senior course architect. Based on the following validated research content on '{topic}', structure a markdown report.
    Include:
    - A brief introduction to the topic
    - Key learning objectives
    - Teaching structure with demo outlines
    - Hands-on activities and discussion questions
    - A final summary or next steps

    Artifact:
    {artifact}
    """

    try:
        start_ollama_server()
        pull_model()
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[{'role': 'user', 'content': prompt}]
        )
        return jsonify({"response": response['message']['content']})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    start_ollama_server()
    pull_model()
    app.run(host="0.0.0.0", port=5000, debug=True)

