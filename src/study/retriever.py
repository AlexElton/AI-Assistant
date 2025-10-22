import os
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

class StudyRetriever:
    def __init__(self):
        db_path = os.getenv("VECTOR_DB_STUDY_PATH", "vector_db_study")
        print(f"[StudyRetriever] Loading from: {db_path}")  # Debug log
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.db = Chroma(persist_directory=db_path, embedding_function=self.embeddings)

    def search(self, query, k=3):
        results = self.db.similarity_search(query, k=k)
        return [r.page_content for r in results]
