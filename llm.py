# llm.py
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from rag import get_vector_db # Import the new get_vector_db from rag.py
import os

def get_retriever():
    vector_db = get_vector_db()
    return vector_db.as_retriever(search_kwargs={"k": 3})

def format_docs(docs):
    formatted_string = ""
    for i, doc in enumerate(docs):
        source = doc.metadata.get("source", "Unknown Source")
        formatted_string += f"Content from {source}:\n{doc.page_content}\n\n"
    return formatted_string.strip()

def create_chain(model_name):
    llm = ChatOllama(model=model_name, streaming=True)
    retriever = get_retriever()

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a precise and helpful customer support assistant for 'The Gilded Fig' restaurant. 
        Answer the user's question using ONLY the provided context. If the context contains information from multiple sources, 
        clearly indicate which source each piece of information comes from. If the exact answer is not explicitly stated in the context, 
        say "I apologize, but I do not have that information."
        
        Context:
        {context}"""),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ])

    rag_chain = (
        RunnablePassthrough.assign(
            context=lambda x: format_docs(retriever.invoke(x["input"]))
        )
        | prompt
        | llm
    )
    
    return rag_chain
