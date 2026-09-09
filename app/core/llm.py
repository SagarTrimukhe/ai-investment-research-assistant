from langchain_openai import ChatOpenAI
from app.core import config


def get_llm(temperature=0.2):
    return ChatOpenAI(
        model="gpt-4o-mini",
        api_key=config.OPENAI_API_KEY,
        temperature=temperature,
        max_retries=2,
    )
