from langchain_google_genai import ChatGoogleGenerativeAI
from app.core import config


# using gemini 3.6 flash (free tier) for all LLM calls
def get_llm(temperature=0.2):
    return ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        google_api_key=config.GEMINI_API_KEY,
        temperature=temperature
    )
