from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def get_synthesis_chain(llm):
    """Chain to synthesize multiple agent research findings into a brief summary."""
    prompt = ChatPromptTemplate.from_template(
        "Please provide a concise synthesis of the following research inputs for {ticker}:\n\n"
        "Fundamentals: {fundamentals}\n"
        "Sentiment: {sentiment}\n"
        "Comparison: {comparison}\n\n"
        "Summary:"
    )
    return prompt | llm | StrOutputParser()
