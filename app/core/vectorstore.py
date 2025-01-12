from langchain_community.vectorstores import Chroma
from app.core.embeddings import get_embeddings
from app.config import settings

def get_vectorstore():
    return Chroma(
        persist_directory=settings.CHROMA_PERSIST_DIR,
        embedding_function=get_embeddings()
    )