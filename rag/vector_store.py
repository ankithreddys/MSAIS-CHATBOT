import os
import pickle
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

DB_PATH = "vector_db_faiss"

def get_or_create_vector_store(documents):
    # Load Hugging Face embeddings model (you can choose a different one if needed)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    if os.path.exists(DB_PATH):
        print("Loading existing FAISS vector store...")
        with open(f"{DB_PATH}/index.pkl", "rb") as f:
            vector_store = pickle.load(f)
        vector_store.embedding_function = embeddings
    else:
        print("Creating new FAISS vector store...")
        vector_store = FAISS.from_documents(documents, embedding=embeddings)
        os.makedirs(DB_PATH, exist_ok=True)
        with open(f"{DB_PATH}/index.pkl", "wb") as f:
            pickle.dump(vector_store, f)

    return vector_store
