import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

# Configuration
DATA_PATH = "data"
CHROMA_PATH = "db"
COLLECTION_NAME = "security-knowledge"
MODEL_NAME = "mxbai-embed-large"

def main():
    # 1. Check if the PDF exists
    files = [f for f in os.listdir(DATA_PATH) if f.endswith(".pdf")]
    if not files:
        print(f"[-] No PDF files found in {DATA_PATH}")
        return

    print(f"[*] Found {len(files)} files. Starting ingestion...")

    all_chunks = []

    for file_name in files:
        file_path = os.path.join(DATA_PATH, file_name)
        print(f"[*] Loading: {file_name}")

        # 2. Load PDF
        loader = PyPDFLoader(file_path)
        docs = loader.load()

        # 3. Split Text (Chunking)
        # Using 1000 chars with 200 overlap to maintain security context
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            add_start_index=True # Metadata: tracks where the chunk starts in the doc
        )
        
        chunks = text_splitter.split_documents(docs)
        print(f"[+] Generated {len(chunks)} chunks from {file_name}")
        all_chunks.extend(chunks)

    # 4. Initialize Embeddings (mxbai-embed-large via Ollama)
    embeddings = OllamaEmbeddings(model=MODEL_NAME)

    # 5. Create and Persist Vector Database (ChromaDB)
    print(f"[*] Embedding and saving to {CHROMA_PATH}...")
    
    # This will create the /db folder and store the vectors locally
    vector_db = Chroma.from_documents(
        documents=all_chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH,
        collection_name=COLLECTION_NAME
    )

    print(f"[!] Success! Ingestion completed. Database created at /{CHROMA_PATH}")

if __name__ == "__main__":
    main()