# VoltVision: AI-Powered Physical Bench Assistant

## Inspiration
As 2nd-year Electrical and Communication Engineering (ECE) students, we spend hours debugging breadboards, locating incorrect pin connections, and double-checking component values. We wanted to build a hands-free, interactive assistant that visually inspects physical circuits and speaks out real-time diagnostic fixes.

## What it does
VoltVision is an AI-powered physical bench assistant designed for circuit debugging. Using a physical hardware trigger on an ESP32 board, a technician or student captures a high-resolution snapshot of a breadboard via webcam. The image is analyzed by Google Gemini's free-tier Vision-Language Model, which identifies components, checks for wiring issues, and returns voice-guided diagnostic instructions.

## How We Built It
- **Hardware Integration:** An ESP32 Dev Board acts as a physical inspect trigger over USB Serial communication (`INSPECT` signal).
- **Computer Vision & Capture:** A Python backend (`voltvision.py` & `listner_script.py`) captures the workspace camera snapshot when triggered.
- **AI Cloud Processing:** The image is sent to Google Gemini's free-tier API (`gemini-2.5-flash`).
- **Voice Feedback:** Diagnostics are instantly converted into spoken audio using text-to-speech (`pyttsx3`) for hands-free troubleshooting.
- **Web Interface:** A modern browser UI (`VoltVision.html`) provides manual upload and cloud AI evaluation.

## AI Experience & Feedback
- **Model Used:** Google Gemini Vision-Language Model (Free Tier).
- **Setup & Ease of Use:** Gemini's API endpoint provided a fast, simple onboarding experience with a generous free tier, allowing us to connect our local hardware trigger script to multimodal vision inference instantly without credit card hassles.
- **Performance & Latency:** Inference speed was exceptionally fast, enabling natural conversational flow and minimal audio delay during circuit inspection.

## Challenges We Ran Into
Ensuring low latency between the serial hardware trigger from the ESP32, webcam frame capture, and payload delivery to API endpoints, as well as optimizing prompt structures for accurate circuit component recognition.

## Accomplishments That We're Proud Of
Successfully building a functional Physical AI bridge linking low-cost microcontrollers (ESP32) and local computer vision directly with state-of-the-art vision-language models.

## What's Next for VoltVision
Integrating continuous video stream analysis, live bounding-box overlays for incorrect wire placement, and fine-tuning specialized vision models for complex multi-layer PCB analysis.
