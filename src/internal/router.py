from fastapi import APIRouter, Depends, Request, HTTPException, Header
from src.internal.retriever import InternalRetriever
import os

router = APIRouter()

# 🔒 Security: simple API key auth
INTERNAL_API_KEY = os.getenv("INTERNAL_API_KEY", "changeme")

def verify_internal_key(x_api_key: str = Header(None)):
    if x_api_key != INTERNAL_API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

# ✅ Routes
@router.get("/ping")
def ping():
    return {"msg": "Internal assistant alive"}

@router.post("/query", dependencies=[Depends(verify_internal_key)])
async def query(req: Request):
    data = await req.json()
    question = data.get("question", "")
    retriever = InternalRetriever()
    results = retriever.search(question)
    return {"context": results}
