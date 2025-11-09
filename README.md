# 🎙️ Voice Agent – Module 3 Project

**Author:** Di Han  
**Course:** Inference.ai – Module 3: Voice Agent Development  

---

## 🚀 Overview
This project implements a full-stack **voice-enabled AI assistant** capable of real-time multi-turn conversation.  
It integrates **Automatic Speech Recognition (ASR)** → **Large Language Model (LLM)** → **Text-to-Speech (TTS)** in one seamless pipeline.

---

## 🧠 System Architecture
- **Backend:** FastAPI server handling ASR, LLM, and TTS requests  
- **Frontend:** Browser-based interface served via `http.server` on port **8080**  
- **Pipeline:**  
User Speech → ASR (Whisper / HuggingFace) → LLM (HuggingFace TextGenerationPipeline) → TTS (Coqui / HuggingFace) → Audio Reply

📁 **Project Structure**

```
voice-agent/
│
├── app.py                 # Main FastAPI backend
├── modules/               # ASR, LLM, and TTS modules
├── client/                # Frontend HTML/JS client
├── sessions/              # Session cache (auto-created)
├── requirements.txt       # Dependencies
└── start_voice_agent.bat  # One-click launcher (auto dependency check)
```

## ▶️ Quick Start

1. **Clone the repository**
    git clone https://github.com/Di0907/voice-agent-demo
    cd voice-agent-demo
2. **Run the launcher** `start_voice_agent.bat`

   The launcher will:
   - Automatically check and install missing dependencies  
   - Start the FastAPI backend on port **8000**  
   - Start the frontend server on port **8080**  
   - Open your browser automatically


2. **Access in Browser**
http://127.0.0.1:8080/client/index.html

🎥 Demo
A 2-minute demonstration video showing 5+ continuous back-and-forth turns has been submitted to the Inference.ai platform as part of this project’s deliverables.

🧩 Technologies Used
🧩 **Technologies Used**  
FastAPI – Backend web framework  
Uvicorn – ASGI server  
Whisper / HuggingFace – Speech-to-text  
LLaMA / TextGenerationPipeline – Response generation  
Coqui TTS – Text-to-speech synthesis


📜 License
This project was developed for academic purposes as part of the Inference.ai – Voice Agent Development module.
