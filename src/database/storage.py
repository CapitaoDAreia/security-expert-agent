from langchain_ollama import OllamaEmbeddings
from langchain_postgres.vectorstores import PGVector
from ..config.config import CONNECTION_STRING, COLLECTION_NAME, EMBEDDING_MODEL, OLLAMA_BASE_URL

class VectorStoreManager:
    def __init__(self):
        self.embeddings = OllamaEmbeddings(
            model=EMBEDDING_MODEL,
            base_url=OLLAMA_BASE_URL
        )
        
        self.db = PGVector(
            embeddings=self.embeddings,
            collection_name=COLLECTION_NAME,
            connection=CONNECTION_STRING,
            use_jsonb=True, # Best performance for metadata
        )

    def search(self, query, k=6):
        return self.db.similarity_search_with_score(query, k=k)