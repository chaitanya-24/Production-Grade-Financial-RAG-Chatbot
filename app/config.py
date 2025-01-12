from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv  # Import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    OPENAI_API_KEY: str 
    CHROMA_PERSIST_DIR: str = "./chroma_db"
    MODEL_NAME: str = "gpt-4o"
    EMBEDDING_MODEL: str = "text-embedding-ada-002"
    TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 500
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    SUPPORTED_FILE_TYPES: list = [".txt", ".pdf", ".docx", ".csv"]
    
    class Config:
        env_file = ".env"

settings = Settings()