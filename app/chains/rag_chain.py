from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def get_rag_chain(retriever, llm):
    """RAG chain combining vector retrieval with an LLM prompt."""
    prompt = ChatPromptTemplate.from_template(
        "Answer the financial question using the context below:\n\n"
        "Context:\n{context}\n\n"
        "Question: {question}"
    )

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {"context": retriever | format_docs, "question": lambda x: x}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain
