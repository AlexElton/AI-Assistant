import os
from langchain_huggingface import HuggingFaceEmbeddings  # new import
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader

def index_folder(data_dir, db_dir):
    if not os.path.exists(data_dir):
        print(f"❌ Skipping {data_dir} (not found)")
        return

    print(f"\n📂 Indexing {data_dir} → {db_dir}")

    loader = DirectoryLoader(data_dir, glob="**/*.md")
    docs = loader.load()

    if not docs:
        print(f"⚠️  No documents found in {data_dir}, skipping.")
        return

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    if not chunks:
        print(f"⚠️  No valid text chunks extracted from {data_dir}, skipping.")
        return

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma.from_documents(chunks, embeddings, persist_directory=db_dir)
    print(f"✅ Indexed {len(chunks)} chunks into {db_dir}")

# --- Paths from environment (or defaults)
base = os.getenv("DATA_PATH", "/mnt/ai-data/data")
index_dir = os.getenv("VECTOR_DB_INTERNAL_PATH", "/mnt/ai-data/vector_dbs/internal")

drift = os.path.join(base, "internal/drift")
index = os.path.join(base, "internal/index")
study = os.path.join(base, "study")

index_folder(drift, f"{index_dir}_drift")
index_folder(index, f"{index_dir}_index")
index_folder(study, os.getenv("VECTOR_DB_STUDY_PATH", "/mnt/ai-data/vector_dbs/study"))
