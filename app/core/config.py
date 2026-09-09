import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
S3_BUCKET = os.getenv("S3_BUCKET_NAME", "ai-investment-research-repo")

CHROMA_DIR = os.getenv("CHROMA_PERSIST_DIR", "./data/chroma_db")
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
