# Local AI Chatbot with Dynamic RAG (Local-First Improvements)

This project is an enhanced version of the `local-ai-chatbot`, incorporating dynamic document ingestion, persistent knowledge base management using ChromaDB, and improved source attribution, all designed for local execution without cloud dependencies.

## Features

*   **Interactive Chatbot Interface:** Built with Streamlit.
*   **Dynamic Document Uploads:** Users can upload PDF and TXT files directly through the UI to expand the chatbot's knowledge base.
*   **Persistent Knowledge Base:** Uses ChromaDB for efficient storage and retrieval of document embeddings.
*   **Source Attribution:** Chatbot responses indicate the source document for retrieved information.
*   **Configurable LLM Models:** Supports various local LLMs via Ollama.
*   **Conversation History Management:** Maintains context-aware chat history.
*   **Streaming Responses:** Provides a smooth, real-time conversational experience.

## Prerequisites

Before running the application, you need to have the following installed:

*   **Python 3.9+**
*   **Ollama:** A local LLM server. Download and install it from [ollama.com](https://ollama.com/download).

## Setup and Installation

1.  **Clone the repository (or extract the provided files):**
    ```bash
    # If you have it as a git repo
    git clone <your-repo-url>
    cd local-ai-chatbot
    # If you extracted the rar file, navigate to the directory
    cd /home/ubuntu/local-ai-chatbot/local-ai-chatbot
    ```

2.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: A `requirements.txt` file will be created in the next step if it doesn't exist.)*

3.  **Download Ollama Models:**
    You need to download the `llama3.2` and `nomic-embed-text` models using Ollama. Open your terminal and run:
    ```bash
    ollama pull llama3.2
    ollama pull nomic-embed-text
    ```
    Ensure the Ollama server is running in the background.

4.  **Initial Knowledge Base Ingestion:**
    The project includes a `sample.pdf`. You need to ingest this into the ChromaDB vector store. Run the `rag.py` script:
    ```bash
    python3 rag.py
    ```
    This will create a `./chroma_db` directory with your persistent knowledge base.

## Running the Application

1.  **Start the FastAPI Backend:**
    Open a new terminal window, navigate to the `local-ai-chatbot` directory, and run:
    ```bash
    python3 api.py
    ```
    You should see output indicating the FastAPI server is starting on `http://127.0.0.1:8000`.

2.  **Start the Streamlit Frontend:**
    Open another new terminal window, navigate to the `local-ai-chatbot` directory, and run:
    ```bash
    streamlit run app.py
    ```
    This will open the Streamlit application in your web browser, typically at `http://localhost:8501`.

## Usage

*   Interact with the chatbot in the main chat window.
*   Use the sidebar to select an LLM model or clear the chat history.
*   **Upload Documents:** In the sidebar, use the "Upload a document (PDF/TXT)" section to add new files to the chatbot's knowledge base. After uploading, click "Add to Knowledge Base" to process and ingest the document.

## Project Structure

```
local-ai-chatbot/
├── api.py          # FastAPI backend for LLM inference and document ingestion
├── app.py          # Streamlit frontend for user interaction
├── config.py       # Configuration for models and history
├── llm.py          # LLM chain definition and RAG integration
├── memory.py       # Chat history management
├── rag.py          # Document loading, chunking, embedding, and ChromaDB management
├── sample.pdf      # Example document for initial knowledge base
├── chroma_db/      # Persistent ChromaDB vector store (created after running rag.py)
└── uploaded_docs/  # Directory for dynamically uploaded documents
```

## Future Enhancements (Cloud-Ready Considerations)

While this version focuses on local execution, here are considerations for future cloud deployment:

*   **Containerization:** Use Docker and Docker Compose for easier deployment to cloud platforms.
*   **Scalable Vector Database:** Migrate ChromaDB to a managed service like Pinecone, Weaviate, or Qdrant for production-grade scalability and reliability.
*   **Managed LLM Services:** Integrate with cloud-based LLM APIs (e.g., OpenAI, Google Gemini) or deploy self-hosted models on scalable inference infrastructure (e.g., Kubernetes with vLLM).
*   **Authentication & Authorization:** Implement robust user management and API security for multi-user environments.
*   **Asynchronous Task Queues:** Utilize cloud-native message queues (e.g., AWS SQS, Google Cloud Pub/Sub) for background document processing.
