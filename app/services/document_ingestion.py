import re
import time
from typing import Callable, List, Optional, Set
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


def ingest_document_text(
    text: str,
    filename: str,
    ticker: str,
    chunk_size: int = 1500,
    chunk_overlap: int = 150,
    batch_size: int = 20,
    progress_callback: Optional[Callable[[int, int, str], None]] = None,
) -> int:
    """Split text into chunks and index into ChromaDB with ticker metadata.
    
    Batches texts into small chunks and uses automatic exponential backoff
    to safely respect Gemini API Free Tier limits (100 requests/minute).
    """
    if not text.strip():
        return 0

    splitter = get_text_splitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
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
    total_ingested = 0
    total_chunks = len(chunks)

    # Process in batches to stay within rate limits
    for start_idx in range(0, total_chunks, batch_size):
        end_idx = min(start_idx + batch_size, total_chunks)
        batch_chunks = chunks[start_idx:end_idx]
        batch_metas = metadatas[start_idx:end_idx]

        if progress_callback:
            progress_callback(
                start_idx,
                total_chunks,
                f"Embedding chunks {start_idx + 1}-{end_idx} of {total_chunks} ({filename})..."
            )

        max_retries = 3
        for attempt in range(max_retries):
            try:
                store.add_texts(texts=batch_chunks, metadatas=batch_metas)
                total_ingested += len(batch_chunks)
                break
            except Exception as e:
                err_msg = str(e)
                is_rate_limit = (
                    "429" in err_msg
                    or "quota" in err_msg.lower()
                    or "resourceexhausted" in err_msg.lower()
                )
                if is_rate_limit and attempt < max_retries - 1:
                    wait_seconds = 60
                    sec_match = re.search(r"retry in ([0-9]+(?:\.[0-9]+)?)s", err_msg)
                    if not sec_match:
                        sec_match = re.search(r"seconds:\s*([0-9]+)", err_msg)
                    if sec_match:
                        wait_seconds = max(10, int(float(sec_match.group(1))) + 2)

                    if progress_callback:
                        progress_callback(
                            start_idx,
                            total_chunks,
                            f"⏳ Gemini Rate Limit (100 RPM). Waiting {wait_seconds}s before retrying batch..."
                        )
                    time.sleep(wait_seconds)
                else:
                    raise e

        # Pacing pause between batches
        if end_idx < total_chunks:
            time.sleep(1.0)

    if progress_callback:
        progress_callback(total_chunks, total_chunks, f"Finished {filename} ({total_ingested} chunks)")

    return total_ingested


def detect_ticker_from_filename(filename: str) -> Optional[str]:
    """Infer the stock ticker symbol from common filename patterns."""
    fn = filename.upper()
    mapping = {
        "NVIDIA": "NVDA", "NVDA": "NVDA",
        "META": "META", "FACEBOOK": "META",
        "INFOSYS": "INFY", "INFY": "INFY",
        "APPLE": "AAPL", "AAPL": "AAPL",
        "MICROSOFT": "MSFT", "MSFT": "MSFT",
        "GOOGLE": "GOOGL", "ALPHABET": "GOOGL", "GOOGL": "GOOGL", "GOOG": "GOOGL",
        "AMAZON": "AMZN", "AMZN": "AMZN",
        "TESLA": "TSLA", "TSLA": "TSLA",
        "TCS": "TCS", "TATA": "TCS",
        "RELIANCE": "RELIANCE",
    }
    for key, ticker in mapping.items():
        if key in fn:
            return ticker
    return None


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
        print("error getting tickers:", e)
        return ["AAPL"]


def get_indexed_summary() -> List[dict]:
    """Return a rich summary list of all indexed tickers, documents, and chunk counts."""
    try:
        store = get_vector_store()
        data = store.get()
        summary = {}
        metas = data.get("metadatas", []) or []
        for meta in metas:
            if not meta:
                continue
            t = meta.get("ticker")
            if not t:
                src_lower = meta.get("source", "").lower()
                t = "AAPL" if "apple" in src_lower or "aapl" in src_lower else "OTHER"
            t = t.upper().strip()

            src = meta.get("source", "Document")
            if t not in summary:
                summary[t] = {
                    "ticker": t,
                    "documents": {},
                    "total_chunks": 0
                }
            summary[t]["documents"][src] = summary[t]["documents"].get(src, 0) + 1
            summary[t]["total_chunks"] += 1

        return sorted(list(summary.values()), key=lambda x: x["ticker"])
    except Exception as e:
        print("error getting summary:", e)
        return []


def is_ticker_indexed(ticker: str) -> bool:
    """Check if a specific ticker exists in the vector store."""
    if not ticker:
        return False
    indexed = get_indexed_tickers()
    return ticker.upper().strip() in indexed


def clear_vector_store() -> bool:
    """Clear all indexed documents from ChromaDB."""
    try:
        from app.core import config
        import chromadb
        client = chromadb.PersistentClient(path=config.CHROMA_DIR)
        try:
            client.delete_collection("financial_filings")
        except Exception:
            pass
        return True
    except Exception as e:
        print("clear failed:", e)
        return False

