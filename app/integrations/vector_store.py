import chromadb
from app.core import config


def get_chroma_client():
    return chromadb.PersistentClient(path=config.CHROMA_DIR)
