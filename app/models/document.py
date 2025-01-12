from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Document(BaseModel):
    id: str = Field(..., description="Unique identifier for the document")
    content: str = Field(..., description="The main text content of the document")
    metadata: dict = Field(default_factory=dict, description="Additional metadata about the document")
    created_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "doc_001",
                "content": "Sample document content",
                "metadata": {"source": "web", "author": "John Doe"},
                "created_at": "2024-01-11T12:00:00"
            }
        }