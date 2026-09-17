from typing import List, Set
import pypdf
from app.integrations.vector_store import get_vector_store
from app.utils.text_splitter import get_text_splitter


def extract_text(file_obj, filename: str) -> str:
    """Extract raw text from a .txt or .pdf file object."""
    lower_name = filename.lower()
    if lower_name.endswith(".pdf"):
        reader = pypdf.PdfReader(file_obj)
        pages_text = [page.extract_text() or "" for page in reader.pages]
        return "\n\n".join(pages_text)
    else:
        raw_bytes = file_obj.read()
        return raw_bytes.decode("utf-8", errors="ignore")


def ingest_document_text(text: str, filename: str, ticker: str) -> int:
    """Split text into chunks and index into ChromaDB with ticker metadata."""
    if not text.strip():
        return 0

    splitter = get_text_splitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(text)
    if not chunks:
        return 0

    clean_ticker = ticker.upper().strip()
    metadatas = [
        {
            "source": filename,
            "chunk_id": i,
            "ticker": clean_ticker,
        }
        for i in range(len(chunks))
    ]

    store = get_vector_store()
    store.add_texts(texts=chunks, metadatas=metadatas)
    return len(chunks)


def get_indexed_tickers() -> List[str]:
    """Return a sorted list of unique tickers found in ChromaDB."""
    try:
        store = get_vector_store()
        data = store.get()
        tickers: Set[str] = set()
        for meta in data.get("metadatas", []):
            if not meta:
                continue
            if "ticker" in meta and meta["ticker"]:
                tickers.add(meta["ticker"].upper().strip())
            elif "apple" in meta.get("source", "").lower() or "aapl" in meta.get("source", "").lower():
                tickers.add("AAPL")
        return sorted(list(tickers))
    except Exception as e:
        print(f"Error fetching indexed tickers: {e}")
        return ["AAPL"]


def is_ticker_indexed(ticker: str) -> bool:
    """Check if a specific ticker exists in the vector store."""
    if not ticker:
        return False
    indexed = get_indexed_tickers()
    return ticker.upper().strip() in indexed

