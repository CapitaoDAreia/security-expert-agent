import os

current_file_path = os.path.abspath(__file__)
# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
DATA_PATH = os.path.join(BASE_DIR, "data")
CHROMA_PATH = os.path.join(BASE_DIR, "db")

if not os.path.exists(DATA_PATH):
    os.makedirs(DATA_PATH)

# Ollama
EMBEDDING_MODEL = "mxbai-embed-large"
LLM_MODEL = "llama3"

# RAG
COLLECTION_NAME = "security-knowledge"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
VECTOR_SEARCH_K = 6