from typing import List
from langchain_core.documents import Document
from app.integrations.vector_store import get_vector_store


class RetrievalService:
    """Service to query indexed filing chunks from ChromaDB."""

    def __init__(self, collection_name: str = "financial_filings"):
        self.vector_store = get_vector_store(collection_name=collection_name)

    def search(self, query: str, ticker: str, top_k: int = 5) -> List[Document]:
        """Retrieve relevant filing document chunks filtered by ticker symbol."""
        try:
            filter_dict = {"ticker": ticker.upper()} if ticker else None
            results = self.vector_store.similarity_search(
                query,
                k=top_k,
                filter=filter_dict
            )
            return results
        except Exception:
            return []
