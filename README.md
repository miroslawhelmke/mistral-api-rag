# API-based RAG with Mistral and Streamlit

![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)
![Streamlit Version](https://img.shields.io/badge/streamlit-1.45+-orange.svg)
![LlamaIndex Version](https://img.shields.io/badge/LlamaIndex-0.12+-green.svg)

> **Note:** This project is derived from [github.com/safzanpirani/local-rag](https://github.com/safzanpirani/local-rag), modified to use Mistral APIs instead of local models, enabling easier deployment on hosted platforms like Streamlit Community Cloud.

Intelligent conversations with your documents, powered by the Mistral API.

Upload your documents (PDF, TXT, MD) and chat with them using Retrieval Augmented Generation (RAG). This application leverages the Mistral AI API for both language generation and document embeddings, providing high-quality responses without requiring local GPU resources.

## Features

*   **Mistral API Integration:** Uses Mistral Large for generation and Mistral Embed for embeddings via the API.
*   **API Key Management:** Securely handles your Mistral API key using Streamlit Secrets.
*   **Document Upload:** Supports PDF, TXT, and Markdown file uploads.
*   **Vector Storage:** Uses ChromaDB locally to store document embeddings persistently.
*   **Streamlit Interface:** Provides an easy-to-use web interface for uploading documents and chatting.
*   **Streaming Responses:** LLM responses are streamed back to the user for a more interactive experience.
*   **Conversation History:** Remembers the chat history within a session.

## Setup

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/safzanpirani/mistral-api-rag # Replace with your repo URL
    cd mistral-api-rag # Or your project directory name
    ```

2.  **Create a Virtual Environment:** (Recommended)
    ```bash
    python -m venv .venv
    # Activate the environment
    # Windows (PowerShell/Git Bash)
    .venv\Scripts\Activate
    # macOS/Linux
    source .venv/bin/activate
    ```

3.  **Install Dependencies:** This project uses `uv` for faster dependency management, but `pip` works too.
    ```bash
    # Using uv
    uv pip install -r requirements.txt
    # Or using pip
    pip install -r requirements.txt
    ```

4.  **Configure API Key:**
    *   **Local Development:**
        *   Create a directory named `.streamlit` inside your project folder if it doesn't exist.
        *   Inside `.streamlit`, create a file named `secrets.toml`.
        *   Add your Mistral API key to `secrets.toml` like this (ensure quotes are included):
            ```toml
            MISTRAL_API_KEY = "YOUR_MISTRAL_API_KEY_HERE"
            ```
        *   Alternatively, you can set the `MISTRAL_API_KEY` environment variable before running the app.
    *   **Streamlit Community Cloud Deployment:**
        *   Deploy your app from your GitHub repository.
        *   In your app's settings on Streamlit Cloud, go to the "Secrets" section.
        *   Add a secret named `MISTRAL_API_KEY` with your actual Mistral API key as the value.

## Running the Application

1.  Make sure your virtual environment is activated and your API key is configured (via `secrets.toml` or environment variable for local runs).
2.  Run the Streamlit app:
    ```bash
    streamlit run main.py
    ```
3.  The application will open in your web browser.

## Usage

1.  Navigate to the "My Files" tab in the sidebar.
2.  Upload one or more supported documents (PDF, TXT, MD).
3.  Click the "Process Documents" button. The app will load, chunk, embed, and index the documents using the Mistral embedding API and store them in the local ChromaDB (`./chroma_db` directory).
4.  Once processing is complete, the chat input box at the bottom will become active.
5.  Ask questions about your documents!

## Key Technologies

*   **Streamlit:** For the web application interface.
*   **LlamaIndex:** Core framework for the RAG pipeline (data loading, indexing, querying).
*   **Mistral AI API:** For LLM (`mistral-large-latest`) and embedding (`mistral-embed`) capabilities.
*   **ChromaDB:** Local vector store for persistent document embeddings.