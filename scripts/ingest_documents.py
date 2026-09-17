import os
import sys

# allow importing from app directory when run as a standalone script
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pydantic import BaseModel
from app.integrations.vector_store import get_vector_store
from app.utils.text_splitter import get_text_splitter


class DocumentChunkMetadata(BaseModel):
    source: str
    chunk_id: int


def ingest_file(file_path):
    print(f"Reading {file_path}...")
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    splitter = get_text_splitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(text)
    print(f"Split into {len(chunks)} chunks.")

    # validate metadata schema using pydantic
    metadatas = [
        DocumentChunkMetadata(
            source=os.path.basename(file_path),
            chunk_id=i
        ).model_dump()
        for i in range(len(chunks))
    ]

    # push chunks into chroma
    vector_store = get_vector_store()
    vector_store.add_texts(texts=chunks, metadatas=metadatas)
    print("Successfully saved chunks to ChromaDB!")


if __name__ == "__main__":
    sample_path = "data/sample_apple_10k.txt"
    if os.path.exists(sample_path):
        ingest_file(sample_path)
    else:
        print(f"File not found: {sample_path}")
