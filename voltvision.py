import os
import time
import base64
import json
import urllib.request
import urllib.error
import serial
import cv2
import pyttsx3

PORT = "COM5"          # your ESP32 port
USE_MOCK = False       # False = use real Google Gemini free tier API
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY")
MODEL_NAME = "gemini-2.5-flash"  # or gemini-1.5-flash

# ---------- Voice ----------
def speak(text):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print("Speech error:", e)

# ---------- Camera ----------
def take_photo(filename="snapshot.jpg"):
    cam = cv2.VideoCapture(0)
    time.sleep(0.5)                 # let the camera adjust to the light
    ok, frame = cam.read()
    cam.release()
    if not ok:
        return None
    cv2.imwrite(filename, frame)
    return filename

# ---------- AI (Google Gemini Free Tier) ----------
def diagnose(image_path):
    if USE_MOCK or not GEMINI_API_KEY or GEMINI_API_KEY == "YOUR_GEMINI_API_KEY":
        return "Mock mode: The circuit looks fine, but please set your Gemini API key for live analysis."
    
    try:
        with open(image_path, "rb") as f:
            img_bytes = f.read()
        img_base64 = base64.b64encode(img_bytes).decode("utf-8")
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent"
        
        prompt = (
            "You are an electronics lab assistant. Inspect this breadboard photo. "
            "Reply ONLY with valid JSON in this exact format: "
            "{\"components\": [\"list\", \"of\", \"components\"], \"issues\": [\"wiring mistake 1 with fix\"], "
            "\"speech\": \"Max 3 short sentences summarizing the diagnosis to read aloud.\"}. "
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
                "x-goog-api-key": GEMINI_API_KEY
            },
            method="POST"
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            candidate = res_data.get("candidates", [])[0]
            text_resp = candidate.get("content", {}).get("parts", [{}])[0].get("text", "")
            
            # Parse json text
            parsed = json.loads(text_resp.replace("```json", "").replace("```", "").strip())
            speech = parsed.get("speech", "Analysis complete.")
            issues = parsed.get("issues", [])
            if issues:
                print("Detected issues:", issues)
            return speech
            
    except Exception as e:
        print("AI diagnostic error:", e)
        return "I encountered an error connecting to the AI service."

# ---------- Main loop ----------
try:
    ser = serial.Serial(PORT, 115200, timeout=1)
    print("VoltVision ready. Press the button.")
    speak("VoltVision is ready.")
except Exception as e:
    print(f"Serial port {PORT} not found or busy. Running in standalone test mode.")
    ser = None

if ser:
    while True:
        line = ser.readline().decode(errors="ignore").strip()
        if line == "INSPECT":
            print("Button pressed. Taking photo...")
            photo = take_photo()
            if photo is None:
                speak("I could not read the camera.")
                continue
            print("Asking Gemini AI...")
            answer = diagnose(photo)
            print("Answer:", answer)
            speak(answer)
else:
    print("No serial connection. Press Enter to simulate button press, or Ctrl+C to exit.")
    while True:
        input("Press Enter to simulate ESP32 button press...")
        photo = take_photo()
        if photo:
            print("Taking photo and analyzing with Gemini...")
            answer = diagnose(photo)
            print("Answer:", answer)
            speak(answer)