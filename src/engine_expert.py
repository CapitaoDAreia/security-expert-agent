from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate

# 1. Configuration
CHROMA_PATH = "db"
COLLECTION_NAME = "security-knowledge"
EMBEDDING_MODEL = "mxbai-embed-large"
LLM_MODEL = "llama3"

def main():
    # 2. Initialize Embeddings and Vector DB
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    vector_db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME
    )

    # 3. Setup the Brain (Llama3 via Ollama)
    llm = ChatOllama(model=LLM_MODEL, temperature=0.2) # Lower temperature = more precise

    # 4. The "Expert" Prompt Template (The Secret Sauce)
    PROMPT_TEMPLATE = """
    You are a Senior Information Security Officer (CISO). 
    Answer the question below BASED ONLY on the following technical context.
    If the context doesn't contain the answer, say you don't know based on official documents.

    ---
    CONTEXT:
    {context}
    ---
    USER QUESTION: 
    {question}

    INSTRUCTIONS:
    - Be technical and direct.
    - If possible, mention which vulnerability (A01, A02, etc.) you are referring to.
    - Use a professional and advisory tone.
    """

    # 5. Execution Flow
    query = "What are the main changes in the OWASP Top 10 for 2025?"
    
    print(f"[*] Analyzing security context for: '{query}'...")

    # Search for relevant chunks
    results = vector_db.similarity_search_with_score(query, k=3)
    
    # Extract text from chunks to build the context string
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])

    # 6. Generate the Final Answer
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    final_prompt = prompt.format(context=context_text, question=query)
    
    response = llm.invoke(final_prompt)

    print("\n" + "="*50)
    print("🛡️ CISO ADVISORY RESPONSE:")
    print("="*50 + "\n")
    print(response.content)
    print("\n" + "="*50)

if __name__ == "__main__":
    main()