import re
import time
from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.core import config
from app.utils.logger import get_logger

logger = get_logger("vector_store")


class ResilientGoogleEmbeddings(Embeddings):
    """Wrapper around GoogleGenerativeAIEmbeddings with automatic 429 rate limit backoff and caching."""

    def __init__(self, **kwargs):
        self._base = GoogleGenerativeAIEmbeddings(**kwargs)
        self._query_cache = {}

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        for attempt in range(4):
            try:
                return self._base.embed_documents(texts)
            except Exception as exc:
                err_str = str(exc)
                if "429" in err_str or "quota" in err_str.lower() or "resourceexhausted" in err_str.lower():
                    m = re.search(r"seconds:\s*([0-9]+)", err_str)
                    delay = min(40, int(m.group(1)) + 2) if m else min(30, 2 ** attempt * 5)
                    logger.warning(f"Embedding 429 limit hit. Backing off for {delay}s (attempt {attempt+1}/4)...")
                    time.sleep(delay)
                else:
                    raise exc
        return self._base.embed_documents(texts)

    def embed_query(self, text: str) -> list[float]:
        if text in self._query_cache:
            return self._query_cache[text]

        for attempt in range(4):
            try:
                res = self._base.embed_query(text)
                self._query_cache[text] = res
                return res
            except Exception as exc:
                err_str = str(exc)
                if "429" in err_str or "quota" in err_str.lower() or "resourceexhausted" in err_str.lower():
                    m = re.search(r"seconds:\s*([0-9]+)", err_str)
                    delay = min(40, int(m.group(1)) + 2) if m else min(25, 2 ** attempt * 4)
                    logger.warning(f"Query embedding 429 limit hit. Backing off for {delay}s (attempt {attempt+1}/4)...")
                    time.sleep(delay)
                else:
                    raise exc
        return self._base.embed_query(text)


def get_embedding_model():
    return ResilientGoogleEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=config.GEMINI_API_KEY
    )


def get_vector_store(collection_name="financial_filings"):
    # connects to local chroma db stored in data/chroma_db
    return Chroma(
        collection_name=collection_name,
        embedding_function=get_embedding_model(),
        persist_directory=config.CHROMA_DIR
    )


