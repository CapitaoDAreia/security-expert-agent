from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from ..config.config import LLM_MODEL, OLLAMA_BASE_URL

class CISOExpert:
    def __init__(self, vector_store):
        self.llm = ChatOllama(
            model=LLM_MODEL,
            temperature=0.1,
            base_url=OLLAMA_BASE_URL
        )
        self.vector_store = vector_store
        self.chat_history = []

    def _contextualize_question(self, question):
        """Gera uma pergunta independente baseada no histórico."""
        if not self.chat_history:
            return question

        prompt = ChatPromptTemplate.from_messages([
            ("system", "Given a chat history and the latest user question, formulate a standalone question. Do NOT answer, just reformulate."),
            MessagesPlaceholder("chat_history"),
            ("human", "{question}"),
        ])
        chain = prompt | self.llm
        response = chain.invoke({"chat_history": self.chat_history, "question": question})
        return response.content

    def ask(self, user_query):
        # 1. Re-write question
        standalone_query = self._contextualize_question(user_query)
        
        # 2. Search Database
        results = self.vector_store.search(standalone_query)
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])

        # 3. Generate Answer
        qa_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a Senior CISO. Use the context below to answer:\n\n{context}"),
            MessagesPlaceholder("chat_history"),
            ("human", "{question}"),
        ])
        
        qa_chain = qa_prompt | self.llm
        response = qa_chain.invoke({
            "chat_history": self.chat_history,
            "context": context_text,
            "question": user_query
        })

        # 4. Update History
        self.chat_history.append(HumanMessage(content=user_query))
        self.chat_history.append(AIMessage(content=response.content))
        
        return response.content, results