Vispio 🎥🗣️🤖

Deployed at : https://vispio-ver1.streamlit.app/

Image Captioning · Text‑to‑Audio · AI Chatbot — one lightweight Streamlit app.

Vispio lets you:

🖼️ Describe images (upload an image → get an AI caption/analysis)

🔊 Convert text to speech (type text → play/download audio)

💬 Chat with AI (ask questions, brainstorm, or get help)

Built with Streamlit, Google Gemini (google‑genai), gTTS / pydub, and Python 3.9+.

✨ Features

Image → Caption: Upload PNG/JPG; get a concise caption + optional detailed analysis.

Text → Audio: Enter text; generate playable speech (MP3) with download.

AI Chatbot: General chat using Gemini.

History: (optional) show past prompts/captions in-session.

Zero fuss deploy: Works locally and on Streamlit Cloud.

🧱 Tech Stack

Frontend: Streamlit

AI: Google Gemini via google-genai

TTS: gTTS (+ pydub for simple audio ops), or system ffmpeg for conversions

Utils: Pillow, requests, numpy, pandas (optional), altair (charts if needed)

🔑 Environment Variables

You can supply your Gemini key either via Streamlit secrets or env vars.

Option A — Streamlit Secrets (recommended for Cloud)

Create .streamlit/secrets.toml (don’t commit real keys):

GEMINI_API_KEY = "YOUR_REAL_API_KEY"

🚀 Run Locally
streamlit run app.py
