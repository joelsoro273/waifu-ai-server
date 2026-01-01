from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

#  clé IA récupérée depuis l’environnement
HF_API_KEY = os.environ.get("HF_API_KEY")

MODEL_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

@app.route("/", methods=["GET"])
def home():
    return "Waifu AI Server is running 🚀"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message", "")
    language = data.get("language", "fr")

    prompt = f"Réponds clairement en {language}. Question : {message}"

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 200,
            "temperature": 0.7
        }
    }

    response = requests.post(MODEL_URL, headers=headers, json=payload)
    result = response.json()

    if isinstance(result, list):
        reply = result[0].get("generated_text", "")
    else:
        reply = "Erreur lors de la réponse de l'IA"

    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
