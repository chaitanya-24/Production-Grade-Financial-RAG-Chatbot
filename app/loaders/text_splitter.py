from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.models.document import Document
from app.config import settings

class DocumentSplitter:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP
        )
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        split_docs = []
        
        for doc in documents:
            splits = self.text_splitter.split_text(doc.content)
            
            for i, split in enumerate(splits):
                split_docs.append(
                    Document(
                        id=f"{doc.id}_chunk_{i}",
                        content=split,
                        metadata={
                            **doc.metadata,
                            "chunk_index": i,
                            "parent_id": doc.id
                        },
                        created_at=doc.created_at
                    )
                )
        
        return split_docs