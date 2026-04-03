from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

# Configuration
CHROMA_PATH = "db"
COLLECTION_NAME = "security-knowledge"
MODEL_NAME = "mxbai-embed-large"

def main():
    # 1. Initialize the same embedding model
    embeddings = OllamaEmbeddings(model=MODEL_NAME)

    # 2. Connect to the existing ChromaDB
    vector_db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME
    )

    # 3. Ask a security question
    query = "What are the top security risks for 2025 according to OWASP?"
    
    print(f"\n[*] Searching for: '{query}'")

    # 4. Search for the top 3 most relevant chunks
    # k=3 means "bring the 3 best matches"
    results = vector_db.similarity_search_with_score(query, k=3)

    print(f"\n[+] Found {len(results)} relevant matches:\n")

    for doc, score in results:
        print(f"--- Match (Score: {score:.4f}) ---")
        print(f"Source: {doc.metadata.get('source')}")
        print(f"Content: {doc.page_content[:200]}...") # Print first 200 chars
        print("-" * 30)

if __name__ == "__main__":
    main()