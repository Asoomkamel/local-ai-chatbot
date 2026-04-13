# rag.py
print("🚀 Starting rag.py script (Phase 3 Tuning)...")

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
import os

# Define the path for the ChromaDB persistent directory
CHROMA_DB_PATH = "./chroma_db"

def load_and_chunk_document(file_path: str):
    print(f"📄 Loading document: {file_path}")
    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower() == ".pdf":
        loader = PyPDFLoader(file_path)
    elif file_extension.lower() == ".txt":
        loader = TextLoader(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")
    
    pages = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,  
        chunk_overlap=150, 
        separators=["\n\n", "\n", " ", ""],
        length_function=len,
    )
    
    chunks = text_splitter.split_documents(pages)
    # Add metadata to each chunk for source attribution
    for chunk in chunks:
        chunk.metadata["source"] = os.path.basename(file_path)
    print(f"✂️ Split document into {len(chunks)} smarter chunks.")
    return chunks

def get_vector_db():
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    if os.path.exists(CHROMA_DB_PATH):
        # Load existing ChromaDB
        print(f"💾 Loading existing vector database from \'{CHROMA_DB_PATH}\'...")
        vector_db = Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embeddings)
    else:
        # Create a new empty ChromaDB if it doesn't exist
        print(f"✨ Creating new vector database at \'{CHROMA_DB_PATH}\'...")
        vector_db = Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embeddings)
        # No need to call persist() here, it's handled when documents are added

    return vector_db

def add_document_to_vector_db(file_path: str):
    document_chunks = load_and_chunk_document(file_path)
    vector_db = get_vector_db()
    print(f"Adding {len(document_chunks)} chunks from {os.path.basename(file_path)} to vector database.")
    vector_db.add_documents(document_chunks)
    vector_db.persist()
    print(f"💾 Document \'{os.path.basename(file_path)}\' successfully added to vector database!")


if __name__ == "__main__":
    # This part is for initial setup or manual ingestion
    sample_pdf = "/home/ubuntu/local-ai-chatbot/local-ai-chatbot/sample.pdf" 
    if os.path.exists(sample_pdf):
        add_document_to_vector_db(sample_pdf)
    else:
        print(f"🚨 Could not find \'{sample_pdf}\'. Please provide a document to ingest or upload one via the UI.")
    print("🏁 Script finished.")
