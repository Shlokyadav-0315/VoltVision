import os
import base64
import json
import urllib.request
import urllib.error
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder=".", template_folder=".")

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
MODEL_NAME = "gemini-2.5-flash"

@app.route("/")
def index():
    return send_from_directory(".", "VoltVision.html")

@app.route("/api/inspect", methods=["POST"])
def inspect_circuit():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    
    file = request.files["image"]
    img_bytes = file.read()
    img_base64 = base64.b64encode(img_bytes).decode("utf-8")
    
    api_key = request.form.get("key") or GEMINI_API_KEY
    if not api_key:
        return jsonify({"error": "Gemini API key is required. Please provide it in the web UI or set GEMINI_API_KEY environment variable."}), 400
    
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent"
        prompt = (
            "You are an expert ECE lab TA helping engineering students. Inspect this breadboard photo specifically for "
            "clustered, tangled, or wrong wiring (such as reversed polarity, misplaced component pins, short circuits, "
            "or crossed power/ground rails). Reply ONLY with valid JSON in this exact format: "
            "{\"components\": [\"list\", \"of\", \"components\"], \"wiring_density\": \"clean or clustered/tangled\", "
            "\"issues\": [\"specific wiring mistake or clustering hazard with exact fix\"], "
            "\"speech\": \"Max 3 short encouraging sentences summarizing the diagnosis to read aloud.\"}. "
            "If the circuit looks correct, issues should be an empty list []."
        )
        
        payload = {
            "contents": [{
                "parts": [
                    {"text": prompt},
                    {"inline_data": {"mime_type": "image/jpeg", "data": img_base64}}
                ]
            }],
            "generationConfig": {
                "responseMimeType": "application/json"
            }
        }
        
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "x-goog-api-key": api_key
            },
            method="POST"
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            candidate = res_data.get("candidates", [])[0]
            text_resp = candidate.get("content", {}).get("parts", [{}])[0].get("text", "")
            parsed = json.loads(text_resp.replace("```json", "").replace("```", "").strip())
            return jsonify(parsed)
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("Starting VoltVision Web Server on http://localhost:5000")
    app.run(host="127.0.0.1", port=5000, debug=True)
