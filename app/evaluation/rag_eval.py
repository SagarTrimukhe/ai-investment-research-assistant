from typing import List, Dict


def evaluate_rag_retrieval(query: str, retrieved_docs: list, answer: str = "") -> Dict[str, float]:
    """Basic evaluation of retreival relevance using keyword overlap."""
    if not query or not retrieved_docs:
        return {"relevance_score": 0.0, "doc_count": 0}

    query_words = set(query.lower().split())
    if not query_words:
        return {"relevance_score": 0.0, "doc_count": len(retrieved_docs)}

    scores = []
    for doc in retrieved_docs:
        content = getattr(doc, "page_content", str(doc)).lower()
        matched = sum(1 for w in query_words if w in content)
        scores.append(matched / len(query_words))

    avg_score = sum(scores) / len(scores) if scores else 0.0
    return {
        "relevance_score": round(avg_score, 2),
        "doc_count": len(retrieved_docs),
    }
