from abc import ABC, abstractmethod
from typing import List, Union, BinaryIO
from pathlib import Path
from app.models.document import Document

class BaseLoader(ABC):
    @abstractmethod
    def load(self, source: Union[str, Path, BinaryIO]) -> List[Document]:
        pass