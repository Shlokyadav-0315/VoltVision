# ⚡ VoltVision: AI-Powered Breadboard & Wiring Assistant

> **Detect clustered, tangled, and incorrect wiring on breadboards instantly using computer vision and AI.**

VoltVision is an intelligent bench assistant designed for Electrical & Communication Engineering (ECE) students and hobbyists. By uploading a camera photo or using a physical hardware trigger (ESP32 microcontroller), VoltVision analyzes breadboard circuits in seconds, flags short circuits and wiring mistakes, and speaks out corrective instructions hands-free.

---

## 🌟 Key Features

- **Clustered & Tangled Wiring Detection**: Automatically analyzes wire density and identifies crossing lines or messy connections.
- **Wrong Wiring & Polarity Checks**: Spots misaligned component pins, reversed power/ground rails, and short circuits.
- **Voice-Guided Diagnostics**: Converts AI feedback into natural text-to-speech audio so your hands never have to leave your circuit.
- **Dual Mode (Web App & Hardware)**: 
  - **Web App**: Upload photos directly in your browser.
  - **Hardware Bridge**: Connect an ESP32 board via USB Serial to trigger snapshots with a physical button press.
- **Free-Tier AI**: Powered by Google Gemini's multimodal vision models.

---

## 🛠️ Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript (Responsive dark/light UI with Schibsted Grotesk font)
- **Backend**: Python, Flask, OpenCV (`cv2`), `pyttsx3` (Text-to-Speech)
- **AI Vision Engine**: Google Gemini API (`gemini-2.5-flash`)
- **Hardware Integration**: ESP32 microcontroller over USB Serial (`pyserial`)

---

## 🚀 Quick Start Guide

### 1. Clone or Open the Project
```powershell
cd c:\Users\shlok\OneDrive\Desktop\Volt_Vision
```

### 2. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 3. Run the Web App
Set your Gemini API key (or paste it directly into the web UI settings):
```powershell
$env:GEMINI_API_KEY="your_gemini_api_key_here"
python app.py
```
Open your browser and navigate to **`http://localhost:5000`**.

### 4. Run the Hardware Script (Optional)
If you are using the physical ESP32 button trigger:
```powershell
python voltvision.py
```

---

## 📁 Project Structure
- `app.py` — Flask backend server for API image processing.
- `VoltVision.html` — Student-facing web application UI.
- `voltvision.py` — Python script for ESP32 serial communication and webcam capture.
- `HACKATHON_SUBMISSION.md` — Project description and pitch deck guide.
- `volt_vision_api.proto` — Protocol Buffer API definition.
- `requirements.txt` — Python dependencies.
- `.gitignore` — Keeps sensitive keys and local cache out of version control.
