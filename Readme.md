# Running DeepSeek-R1 Locally with RAG on PDFs

## Overview

This project explores running the DeepSeek-R1 model locally using [Ollama](https://ollama.com) and integrating it with [LangChain](https://python.langchain.com) and [Gradio](https://gradio.app/) to create a web interface for Retrieval-Augmented Generation (RAG) on PDF documents. 

I tested this on my machine:
- **Processor**: Ryzen 7K Series
- **RAM**: 16GB
- **GPU**: RTX 3050

## Installation

### 1. Set Up WSL (Windows Subsystem for Linux)

If you're running Windows, install WSL and set up an Ubuntu environment:
```sh
wsl --install -d Ubuntu
```
After installation, just type wsl on the windows command prompt to get to Linux prompt.
Please note that you will be typing the password in blind mode.

### 2. Install Ollama

Ollama is an easy way to run LLMs locally:
```sh
curl -fsSL https://ollama.com/install.sh | sh
```

Verify installation:
```sh
ollama --version
```

### 3. Download DeepSeek-R1 Models

Choose the appropriate model size:
```sh
ollama pull deepseek-r1:1.5b
ollama pull deepseek-r1:8b
```

### 4. Set Up a Python Virtual Environment

Create and activate a virtual environment:
```sh
python3 -m venv myenv
source myenv/bin/activate  # Linux/macOS
myenv\Scripts\activate  # Windows (CMD/Powershell)
```

### 5. Install Required Python Packages

```sh
pip install -U gradio langchain_community pymupdf langchain-text-splitters "langchain-chroma>=0.1.2" langchain-ollama
```

## Running the Application

### 1. Python Script (RAG Implementation)

[View Web Interface Code](./learn-llm-02_webInterface.py)

### 2. Run the Application

```sh
python ./learn-llm-02_webInterface.py
```

Gradio will launch a web interface at `http://localhost:7860` where you can upload a PDF and ask questions.

## Observations

- The **1.5B model** runs efficiently and quickly but struggles with complex reasoning.
- The **8B model** provides much better responses but is noticeably slower.
- Running RAG with DeepSeek requires **GPU acceleration**, especially for larger models.
- **File processing takes a few minutes**, especially for PDFs with many pages.
- VS Code with the **Remote WSL extension** provides a seamless development experience.

## Conclusion

This setup enables local inference with LLMs and private document analysis without cloud dependencies. Future improvements could include:
- Adding a chatbot UI for an interactive experience
- Testing larger models like 14B if hardware permits
- Improving the RAG pipeline with better chunking and retrieval techniques

## References
- [DeepSeek on Ollama](https://ollama.com/library/deepseek-r1)
- [LangChain Documentation](https://python.langchain.com/)
- [Gradio for Web Apps](https://gradio.app/)
- [WSL Installation Guide](https://learn.microsoft.com/en-us/windows/wsl/install)

---
### 🚀 Happy Experimenting with LLMs! 🎯
