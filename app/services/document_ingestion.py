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
    """Split text into chunks and index into ChromaDB with ticker metadata."""
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
                    # BUG: re and time not imported - this will crash
                    sec_match = re.search(r"retry in ([0-9]+(?:\.[0-9]+)?)s", err_msg)
                    if sec_match:
                        wait_seconds = max(10, int(float(sec_match.group(1))) + 2)

                    if progress_callback:
                        progress_callback(
                            start_idx,
                            total_chunks,
                            f"Rate limited. Waiting {wait_seconds}s..."
                        )
                    time.sleep(wait_seconds)
                else:
                    raise e

        if end_idx < total_chunks:
            time.sleep(1.0)

    return total_ingested
