from langchain_openai import ChatOpenAI
from app.core import config


def get_llm(model: str = "gpt-4o", temperature: float = 0.2):
    return ChatOpenAI(
        model=model,
        temperature=temperature,
        api_key=config.OPENAI_API_KEY,
    )
