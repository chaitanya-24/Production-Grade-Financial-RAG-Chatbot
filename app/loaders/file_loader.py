from typing import List, Union, BinaryIO
from pathlib import Path
import uuid
from datetime import datetime

from langchain_community.document_loaders import (
    TextLoader,
    PDFMinerLoader,
    Docx2txtLoader,
    CSVLoader
)

from app.loaders.base import BaseLoader
from app.models.document import Document
from app.config import settings

class FileLoader(BaseLoader):
    def __init__(self):
        self.loaders = {
            ".txt": TextLoader,
            ".pdf": PDFMinerLoader,
            ".docx": Docx2txtLoader,
            ".csv": CSVLoader
        }

    def load(self, source: Union[str, Path, BinaryIO]) -> List[Document]:
        path = Path(source) if isinstance(source, str) else source
        
        if path.suffix not in settings.SUPPORTED_FILE_TYPES:
            raise ValueError(f"Unsupported file type: {path.suffix}")
            
        loader_cls = self.loaders[path.suffix]
        loader = loader_cls(str(path))
        docs = loader.load()
        
        return [
            Document(
                id=str(uuid.uuid4()),
                content=doc.page_content,
                metadata={
                    **doc.metadata,
                    "source": str(path),
                    "file_type": path.suffix
                },
                created_at=datetime.now()
            )
            for doc in docs
        ]