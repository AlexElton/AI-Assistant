from fastapi import APIRouter, Request
from src.study.retriever import StudyRetriever

router = APIRouter()

@router.get("/ping")
def ping():
    return {"msg": "Study assistant alive"}

@router.post("/query")
async def query(req: Request):
    data = await req.json()
    question = data.get("question", "")
    retriever = StudyRetriever()
    results = retriever.search(question)
    return {"context": results}
