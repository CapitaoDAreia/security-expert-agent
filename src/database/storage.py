from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from ..config.config import CHROMA_PATH, COLLECTION_NAME, EMBEDDING_MODEL

class VectorStoreManager:
    def __init__(self):
        self.embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
        self.db = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=self.embeddings,
            collection_name=COLLECTION_NAME
        )

    def search(self, query, k=6):
        """Busca os trechos mais relevantes no banco."""
        return self.db.similarity_search_with_score(query, k=k)