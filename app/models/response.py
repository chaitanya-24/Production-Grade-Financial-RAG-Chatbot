from pydantic import BaseModel, Field
from typing import List, Optional

class ChatResponse(BaseModel):
    answer: str = Field(..., description="Generated answer from the RAG pipeline")
    source_documents: List[str] = Field(
        default_factory=list,
        description="List of source documents used for generation"
    )
    confidence_score: float = Field(
        ..., 
        description="Confidence score of the generated answer",
        ge=0.0,
        le=1.0
    )