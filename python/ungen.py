from flask import Flask, request, jsonify
from llama_cpp import Llama
import requests
import os

app = Flask(__name__)

MODEL_PATH = "/home/yourusername/model.gguf"

def download_model_from_gdrive():
    if not os.path.exists(MODEL_PATH):
        print("Downloading model from Google Drive...")
        url = "https://drive.google.com/uc?export=download&id=1M1Mu2QmKXVHzyInvyBgpaib_mq1Fk96E"
        response = requests.get(url, stream=True)
        with open(MODEL_PATH, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print("Model downloaded successfully.")

# Download the model if it doesn't exist
download_model_from_gdrive()

# Load the model once the file is downloaded
llama = Llama(model_path=MODEL_PATH)

@app.route('/generate_username', methods=['POST'])
def generate_username():
    data = request.json
    theme = data.get("theme", "Fantasy")

    prompt = f"Generate a {theme} username."
    response = llama(prompt, max_tokens=20, stop=["<|end|>"])
    generated_username = response['choices'][0]['text'].strip()

    return jsonify({"username": generated_username})

if __name__ == '__main__':
    app.run()
