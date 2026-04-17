# api.py
print("🚀 Starting FastAPI Server...")

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Dict
from langchain_core.messages import HumanMessage, AIMessage
import os

# Import your existing AI logic!
from llm import create_chain
from rag import add_document_to_vector_db

app = FastAPI(title="Local AI Chatbot API")

# 1. Define the Data Structure we expect from the frontend
class ChatRequest(BaseModel):
    input: str
    model: str
    chat_history: List[Dict[str, str]] = []

def parse_history(history_list):
    """Converts JSON dictionaries back into LangChain message objects."""
    parsed_messages = []
    for msg in history_list:
        if msg["role"] == "user":
            parsed_messages.append(HumanMessage(content=msg["content"]))
        else:
            parsed_messages.append(AIMessage(content=msg["content"]))
    return parsed_messages

# 2. Create the Chat Endpoint
@app.post("/chat")
async def chat_stream(request: ChatRequest):
    try:
        # Rebuild the LangChain history format
        formatted_history = parse_history(request.chat_history)
        
        # Initialize the RAG chain
        chain = create_chain(request.model)

        # 3. Generator function to stream chunks out to the web
        def generate():
            for chunk in chain.stream({
                "input": request.input,
                "chat_history": formatted_history
            }):
                # Yield the text chunks as they are generated
                if chunk.content:
                    yield chunk.content

        # Return the streaming response
        return StreamingResponse(generate(), media_type="text/plain")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 4. Create a Document Upload Endpoint
@app.post("/upload-document")
async def upload_document(file: UploadFile = File(...)):
    try:
        file_location = f"./uploaded_docs/{file.filename}"
        os.makedirs(os.path.dirname(file_location), exist_ok=True)
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())
        
        # Add document to vector database
        add_document_to_vector_db(file_location)
        
        return {"message": f"Successfully uploaded {file.filename} and added to knowledge base."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload or process document: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    # This runs the server on your local machine, port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
