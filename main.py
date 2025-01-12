from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import uvicorn
from typing import List
import asyncio
from dotenv import load_dotenv
import os

# Load environment variables at startup
load_dotenv()

# Verify OpenAI API key is present
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY environment variable is not set")

from app.chains.rag_chain import RAGChain
from app.models.prompt import PromptStrategy

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG chain
rag_chain = None

@app.on_event("startup")
async def startup_event():
    global rag_chain
    try:
        rag_chain = RAGChain(prompt_strategy=PromptStrategy.CHAIN_OF_THOUGHT)
        
        # Load documents from each supported type
        document_paths = [
            # "documents/pdf/quantum_computing.pdf",
            # "documents/pdf/machine_learning.pdf",
            # "documents/txt/python_basics.txt",
            # "documents/txt/data_structures.txt",
            # "documents/docx/web_development.docx",
            # "documents/docx/cloud_computing.docx",
            # "documents/csv/stock_data.csv",
            # "documents/csv/sales_data.csv"
            "documents/pdf/finance.pdf"
        ]
        
        await rag_chain.ingest_documents(document_paths)
        print("Documents loaded successfully!")
    except Exception as e:
        print(f"Error during startup: {str(e)}")
        raise e

@app.get("/", response_class=HTMLResponse)
async def get_chat_interface():
    try:
        with open("templates/index.html") as f:
            return f.read()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Chat interface template not found")

@app.post("/api/chat")
async def chat(message: dict):
    if not rag_chain:
        raise HTTPException(status_code=500, detail="RAG chain not initialized")
    
    try:
        user_message = message.get("message")
        if not user_message:
            raise HTTPException(status_code=400, detail="Message is required")
        
        response = await rag_chain.chat(user_message)
        return {
            "answer": response.answer,
            "source_documents": response.source_documents,
            "confidence_score": response.confidence_score
        }
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)