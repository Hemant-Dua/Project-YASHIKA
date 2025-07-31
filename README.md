# 🧠 Project Y.A.S.H.I.K.A.

**Y.A.S.H.I.K.A. (_Yet Another Super Human Intelligent Knowledge Agent_)** is a locally-hosted AI assistant built for true autonomy and personalization. Designed to run entirely offline using Ollama-hosted LLMs, YASHIKA controls your apps, responds with context, and adapts to your behavior — all while keeping your data private.

### Why Local? 🔐  
For privacy, speed, and offline resilience — especially crucial for personal AI on-body devices.

---

## 🚀 Features

- ⚡ **LLM Integration via Ollama API**
- 🧠 **Prompt Injection for Mood Awareness**
- 🗃️ **Local Memory & Context Persistence**
- 🧩 **Modular System Control (app launching, shell ops)**

---

## 🧱 Tech Stack

- **Python**
- **Ollama**
- **FastAPI**
- **HTML-CSS-JS**

---

## ⚙️ Installation Guide

### ✅ Prerequisites

### 💻 Hardware (Recommended)
| Component | Recommendation | Notes |
|----------|----------------|-------|
| 🧠 **CPU** | 4 cores or more (Intel i5 / Ryzen 5+) | Handles general processing and multitasking |
| 💾 **RAM** | 16GB+ | 8GB possible with swap, but performance will suffer |
| 🎮 **GPU** | Dedicated GPU (6GB+ VRAM) | **Highly recommended** — Ollama supports both CPU and GPU; GPU drastically improves LLM performance |


### 🖥️ System & Tools
- **Python 3.10+**
- **Ollama installed inside WSL2**
- **Model pulled (e.g., `gemma:7b`, `llama-2:7b`)**
- **Git**

---

### 📦 Setup Steps

1. **Clone the Repository**
   ```powershell
   git clone https://github.com/Hemant-Dua/Y.A.S.H.I.K.A..git
   cd Y.A.S.H.I.K.A.
   ```

2. **Create a Virtual Environment**
   ```powershell
   python -m venv env
   env\Scripts\activate
   ```

3. **Install Dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Start Ollama in WSL**
   ```bash
   ollama pull gemma:7b
   ollama run gemma:7b
   ```

   > Ollama exposes an API at `http://localhost:11434` (default), which is used by YASHIKA.

5. **Run YASHIKA**
   
   For running in CLI
   ```powershell
   cd LLM
   python main.py
   ```

   For running the Web App
   ```powershell
   cd WebApp
   python server.py
   ```

---

## 🧠 Notes

- Ollama must be active before running YASHIKA.
- If you're accessing from Windows scripts, ensure `localhost` API from WSL is accessible.
- 🛠️ **Troubleshooting Tip:** Visit [`http://localhost:11434`](http://localhost:11434) in your browser.  
  If Ollama is running, you'll see a `"Ollama is running"` message. Otherwise, start it using `ollama run`.


---

## 🧬 Future Scope

- Offline STT and TTS integration
- BLE-based wearable data streams
- Real-time event trigger system
- Native daemon mode for persistent background ops

---

## 🔓 License

This project is licensed under the **MIT License**.  
Feel free to use or modify it — just give proper credit.

---

## 👨‍💻 Made By

**Hemant Dua**  
*"Learning by building one ASCII character at a time."*