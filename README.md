# Local Multi-Agent System (Offline) 🇲🇾

A fully offline Multi-Agent System built with **CrewAI** and **Ollama**, designed to run on local hardware (NVIDIA RTX / Mac M-Series).

This project features a team of AI agents (Coder, QA, and Technical Writer) who collaborate to solve programming tasks, debug code, and generate documentation—**all communicating in Bahasa Melayu**.

## 🚀 Key Features
* **100% Offline:** No OpenAI API keys required. Runs locally for free.
* **Privacy First:** Your data never leaves your machine.
* **Bahasa Melayu Support:** Agents are prompted to think, critique, and document in Malay.
* **Role-Based Collaboration:**
    * 🧑‍💻 **Coder:** Writes efficient Python code.
    * 🕵️ **QA:** Reviews logic and enforces coding standards.
    * 📝 **Writer:** Compiles the final output into a Markdown report.

## 🛠️ Tech Stack
* [CrewAI](https://crewai.com) - Agent Orchestration
* [Ollama](https://ollama.com) - Local LLM Runner
* [LangChain](https://langchain.com) - LLM Framework
* **Model:** Llama 3.2 (3B) or Llama 3.1 (8B)

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
    pip install crewai langchain_ollama
    ```

4.  **Pull the LLM Model:**
    Open your terminal/command prompt and run:
    ```bash
    ollama pull llama3.2
    # Or for better performance/language skills:
    # ollama pull llama3.1
    ```

## 🚀 Usage

1.  Make sure the **Ollama app** is running in the background.
2.  Run the main script:
    ```bash
    python main.py
    ```
3.  The agents will start collaborating in the terminal.
4.  Once finished, check the generated file: `Laporan_Projek.md`.

## ⚙️ Configuration

You can customize the topic or the model in `main.py`:

```python
# Change Model (line 12)
my_llm = LLM(model="ollama/llama3.1", base_url="http://localhost:11434")

# Change Topic (line 108)
input_topik = "Satu program untuk analisa saham menggunakan Python"
