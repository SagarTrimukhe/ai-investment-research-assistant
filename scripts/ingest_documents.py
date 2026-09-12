"""Batch ingest PDFs from data/raw_pdfs into ChromaDB."""

from app.core import config


def main():
    print(f"Ingesting documents into {config.CHROMA_DIR}...")


if __name__ == "__main__":
    main()
