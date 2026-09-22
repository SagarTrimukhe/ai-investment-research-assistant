from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Investment Research API")


class ResearchRequest(BaseModel):
    ticker: str
    benchmark: str = "MSFT"


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "investment-research-assistant"}


@app.get("/info")
def get_info():
    return {
        "title": "AI Investment Research Assistant",
        "description": "Multi-agent equity research platform",
        "version": "1.0.0",
    }
