import os
from dotenv import load_dotenv
from fastapi import FastAPI
from src.internal.router import router as internal_router
from src.study.router import router as study_router
import nltk

# Configure NLTK and Hugging Face cache paths
nltk.data.path.append("/home/ubuntu/ai-assistant/nltk_data")

# Load environment variables from .env
load_dotenv()
os.environ["HF_HOME"] = os.getenv("HF_HOME", "/mnt/ai-data/cache/huggingface")

# Initialize the FastAPI app
app = FastAPI(title="AI Assistant Framework")

# Register routers
app.include_router(internal_router, prefix="/internal", tags=["Internal Assistant"])
app.include_router(study_router, prefix="/study", tags=["Study Assistant"])

@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "AI Assistant running with /internal and /study endpoints."
    }
