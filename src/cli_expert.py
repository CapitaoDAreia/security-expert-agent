import sys
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

# Configuration
CHROMA_PATH = "db"
COLLECTION_NAME = "security-knowledge"
EMBEDDING_MODEL = "mxbai-embed-large"
LLM_MODEL = "llama3"

class CISOAgent:
    def __init__(self):
        # 1. Init Core Components
        self.embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
        self.vector_db = Chroma(
            persist_directory=CHROMA_PATH, 
            embedding_function=self.embeddings, 
            collection_name=COLLECTION_NAME
        )
        self.llm = ChatOllama(model=LLM_MODEL, temperature=0.1)
        self.chat_history = [] # Short term memory

    def contextualize_query(self, user_query):
        if not self.chat_history:
            return user_query

        contextualize_prompt = ChatPromptTemplate.from_messages([
            (
                "system", 
                "Given a chat history and the latest user question, formulate a standalone question which can be understood without the chat history. Do NOT answer the question, just reformulate it if needed and otherwise return it as is."
            ),
            MessagesPlaceholder("chat_history"),
            ("human", "{question}"),
        ])
        
        chain = contextualize_prompt | self.llm
        response = chain.invoke({"chat_history": self.chat_history, "question": user_query})
        return response.content

    def answer_question(self, user_query):
        # STEP A: Giving context to query
        standalone_query = self.contextualize_query(user_query)
        if standalone_query != user_query:
            print(f"DEBUG RE-WRITE: '{user_query}' -> '{standalone_query}'")

        # STEP B: RETRIVAL
        results = self.vector_db.similarity_search_with_score(standalone_query, k=6)
        
        # DEBUG
        print(f"DEBUG: Found {len(results)} chunks for search.")
        context_text = ""
        if results:
            context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
            for i, (doc, score) in enumerate(results):
                print(f"DEBUG Chunk {i} (Score: {score:.4f}): {doc.page_content[:40]}...")

        # STEP C: RAG
        qa_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a Senior CISO. Answer the user question based ONLY on the context below:\n\n{context}"),
            MessagesPlaceholder("chat_history"),
            ("human", "{question}"),
        ])

        qa_chain = qa_prompt | self.llm
        response = qa_chain.invoke({
            "chat_history": self.chat_history,
            "context": context_text,
            "question": user_query
        })

        # STEP D: REFRESH HISTORY
        self.chat_history.append(HumanMessage(content=user_query))
        self.chat_history.append(AIMessage(content=response.content))
        
        # Keep only 6 last messages to avoid mess the history context
        if len(self.chat_history) > 6:
            self.chat_history = self.chat_history[-6:]

        return response.content

def main():
    agent = CISOAgent()

    print("\n" + "="*60)
    print("🛡️  CISO AI AGENT PRO - WITH MEMORY & QUERY REWRITING")
    print("Type 'exit' to stop.")
    print("="*60 + "\n")

    while True:
        user_input = input("USER > ")
        if user_input.lower() in ['exit', 'quit']: break
        if not user_input.strip(): continue

        try:
            print("[*] CISO is processing...", end="\r")
            answer = agent.answer_question(user_input)
            print(f"\nCISO > {answer}\n")
            print("-" * 30)
        except Exception as e:
            print(f"\n[!] Error: {e}")

if __name__ == "__main__":
    main()