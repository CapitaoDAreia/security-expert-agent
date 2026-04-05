import sys
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate

# Configuration
CHROMA_PATH = "db"
COLLECTION_NAME = "security-knowledge"
EMBEDDING_MODEL = "mxbai-embed-large"
LLM_MODEL = "llama3"

def main():
    # 1. Init Models
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    vector_db = Chroma(
        persist_directory=CHROMA_PATH, 
        embedding_function=embeddings, 
        collection_name=COLLECTION_NAME
    )
    llm = ChatOllama(model=LLM_MODEL, temperature=0.1)

    PROMPT_TEMPLATE = """
    Answer the question BASED ONLY on the following context:
    {context}
    ---
    Question: {question}
    """

    print("\n" + "="*60)
    print("🛡️  CISO AI AGENT - TERMINAL INTERFACE")
    print("Type 'exit' or 'quit' to stop the session.")
    print("="*60 + "\n")

    while True:
        # Get user input
        user_query = input("USER > ")

        if user_query.lower() in ['exit', 'quit']:
            print("\nExiting... Stay secure! 🛡️")
            break
        
        if not user_query.strip():
            continue

        try:
            # RAG Flow: Search
            results = vector_db.similarity_search_with_score(user_query, k=6)
            
            print(f"DEBUG: Chunks found {len(results)}")
            if(len(results) <= 0): print(f"DEBUG: Nothing found on resources to answer properly")
            if(len(results) > 0): print(f"DEBUG: Something found on resources to answer properly")
            print(f"----------------------------------------------")

            for i, (doc, score) in enumerate(results):
                print(f"DEBUG Chunk {i} (Score: {score:.4f}): {doc.page_content[:50]}...")

            context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])

            # RAG Flow: Generate
            prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
            final_prompt = prompt.format(context=context_text, question=user_query)
            
            print("\n[*] CISO is thinking...", end="\r")
            response = llm.invoke(final_prompt)
            
            print(f"\nCISO > {response.content}\n")
            print("-" * 30)

        except Exception as e:
            print(f"\n[!] Error: {e}")

if __name__ == "__main__":
    main()