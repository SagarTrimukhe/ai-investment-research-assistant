import os
import sys

# allow importing from app directory when run as a standalone script
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.integrations.vector_store import get_vector_store
from app.utils.text_splitter import get_text_splitter


def ingest_file(file_path):
    print(f"Reading {file_path}...")
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    splitter = get_text_splitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(text)
    print(f"Split into {len(chunks)} chunks.")

    # push chunks into chroma
    vector_store = get_vector_store()
    vector_store.add_texts(
        texts=chunks,
        metadatas=[{"source": os.path.basename(file_path), "chunk_id": i} for i in range(len(chunks))]
    )
    print("Successfully saved chunks to ChromaDB!")


if __name__ == "__main__":
    sample_path = "data/sample_apple_10k.txt"
    if os.path.exists(sample_path):
        ingest_file(sample_path)
    else:
        print(f"File not found: {sample_path}")
