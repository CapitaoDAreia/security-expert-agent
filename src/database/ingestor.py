import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from ..config.config import DATA_PATH, CHUNK_SIZE, CHUNK_OVERLAP
from .storage import VectorStoreManager

class DataIngestor:
    def __init__(self):
        self.db_manager = VectorStoreManager()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )

    def process_pdfs(self):
        files = [f for f in os.listdir(DATA_PATH) if f.endswith(".pdf")]
        if not files:
            print(f"[!] No PDFs found in {DATA_PATH}")
            return

        print(f"[*] Found {len(files)} files. Starting ingestion...")
        
        all_chunks = []
        for file in files:
            file_path = os.path.join(DATA_PATH, file)
            print(f"[*] Loading: {file}")
            loader = PyPDFLoader(file_path)
            docs = loader.load()
            chunks = self.text_splitter.split_documents(docs)
            all_chunks.extend(chunks)
            print(f"[+] Generated {len(chunks)} chunks from {file}")

        print(f"[*] Saving {len(all_chunks)} chunks to ChromaDB...")
        self.db_manager.db.add_documents(all_chunks)
        print("[!] Success! Database updated.")

if __name__ == "__main__":
    ingestor = DataIngestor()
    ingestor.process_pdfs()