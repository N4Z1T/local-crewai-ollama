# Local AI Team with Streamlit UI 🤖🇲🇾

A fully offline, local Multi-Agent System with a modern **Streamlit Web Interface**.

Powered by **CrewAI** and **Ollama**, this project features a team of AI agents (Coder, QA, and Technical Writer) who collaborate to solve programming tasks and generate documentation—**communicating entirely in Bahasa Melayu**.


## ✨ Key Features

* **🖥️ Streamlit UI:** No more black terminal screens. Use a clean, interactive web dashboard.
* **🧠 Real-Time Logic:** Watch the agents "think" and debate via the real-time log viewer.
* **🗣️ Bahasa Melayu Native:** Agents are prompted to code, critique, and document in Malay.
* **🔒 100% Offline:** Runs locally on your hardware (NVIDIA RTX or Mac M-Series). No API keys required.
* **💾 Memory Enabled:** Agents retain context within the session.

## 🛠️ Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io)
* **Orchestration:** [CrewAI](https://crewai.com)
* **LLM Backend:** [Ollama](https://ollama.com)
* **Supported Models:** Qwen 3 (8B), Llama 3.1 (8B), Llama 3.2 (3B)

## 📋 Prerequisites

### 1. Hardware
* **Windows:** NVIDIA GPU with 6GB+ VRAM (Recommended: RTX 3060/3080/4090).
* **Mac:** M1/M2/M3 Chip with 8GB+ Unified Memory (16GB recommended for 8B models).

### 2. Software
* **Python:** Version 3.10, 3.11, or 3.12.
* **Ollama:** Must be installed and running in the background.

## 📥 Installation Guide

### Step 1: Clone Repository
```bash
git clone https://github.com/N4Z1T/local-crewai-ollama.git
cd local-crewai-ollama

## 📋 Prerequisites

Before running the project, ensure you have:

1.  **Python 3.10 - 3.12** installed.
2.  **Ollama** installed and running.
3.  **Hardware:**
    * Minimum: 8GB RAM (runs Llama 3.2 3B).
    * Recommended: 16GB+ RAM or NVIDIA RTX GPU (runs Llama 3.1 8B).

## 📥 Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/N4Z1T/local-crewai-ollama.git
    cd local-crewai-ollama
    ```

2.  **Create a Virtual Environment:**
    ```bash
    python -m venv venv
    # Windows:
    venv\Scripts\activate
    # Mac/Linux:
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install streamlit crewai langchain_ollama
    ```

4.  **Pull the LLM Model:**
    Open your terminal/command prompt and run:
    ```bash
    ollama pull llama3.2
    # Or for better performance/language skills:
    # ollama pull llama3.1
    ```
   **For Memory Features:**
   ```bash
   ollama pull nomic-embed-text
   ```

## 🚀 Usage

1.  Make sure the **Ollama app** is running in the background.
2.  Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```
3.  Your browser will open automatically at http://localhost:8501.
4.  Enter your task in the text box and click "🚀 MULA MISI".

## ⚙️ Configuration

You can change the default model directly in the Web UI Sidebar, or permanently in app.py:

```python
# In app.py line 40
model_name = st.text_input("Nama Model", value="ollama/qwen3:8b")
