# 🛡️ Roadmap: AI Security Expert (POC)

This guide defines the steps to build an Information Security (Infosec) Specialist Chatbot using local RAG (Retrieval-Augmented Generation).

---

## 1. Environment Setup and Structure
**What it is:** Setting up the base infrastructure and project organization.
- **Actions:** - Install Ollama and models: `llama3` and `mxbai-embed-large`.
    - Create a Python environment (`uv` or `venv`).
    - Structure the repository as follows:
    ```text
    /security-ai-expert
    ├── data/               # Reference PDFs (NIST, OWASP)
    ├── db/                 # Persistent vector database (ChromaDB)
    ├── src/
    │   ├── ingest.py       # ETL Script (Step 2)
    │   ├── engine.py       # RAG Logic and Prompting (Steps 3 and 4)
    │   └── app.py          # Streamlit/FastAPI Interface (Steps 5 and 6)
    └── requirements.txt    # Dependencies
    ```
- **Reason:** Ensure organization and isolation between data ingestion and the chat interface.

## 2. Knowledge Ingestion (Security ETL)
**What it is:** Creating the specialized "brain" of our AI.
- **Actions:** - Collect PDFs (OWASP Top 10, NIST, CIS Benchmarks) in the `/data` folder.
    - Create the `src/ingest.py` script to:
        1. Load documents.
        2. Split text (Chunking) into segments of ~1000 characters.
        3. Generate vectors (Embeddings).
        4. Save to `/db` (ChromaDB).
- **Reason:** Base the AI's responses on real technical standards rather than generic knowledge.

## 3. Building the RAG Engine (Retriever)
**What it is:** The search logic that "fishes" for the right information in the database.
- **Actions:** - Implement the similarity search function in `src/engine.py`.
    - Validate if the search returns the correct excerpts from the manuals before sending them to the LLM.
- **Reason:** Avoid AI hallucinations by ensuring it only uses facts found in the database.

## 4. Personality and Prompt Engineering (The Virtual CISO)
**What it is:** Defining how the AI should behave and speak.
- **Actions:** - Create the `System Prompt` defining the role: "You are a CISO (Chief Information Security Officer)".
    - Define rules for technical accuracy and source citation.
- **Reason:** Ensure a consultative, technical tone focused on risk reduction.

## 5. Chat Interface (MVP Experience)
**What it is:** The front-end of the product for user interaction.
- **Actions:** - Create `src/app.py` using `Streamlit`.
    - Implement conversation history (Memory) for follow-up questions.
- **Reason:** Validate the user experience and showcase the potential of the final product.

## 6. Evolution to API (Production-Ready)
**What it is:** Transforming the local script into a scalable service.
- **Actions:** - Migrate the logic to `FastAPI`.
    - Create `/chat` and `/ingest` endpoints.
- **Reason:** Allow the chatbot to be integrated into the company's official platform.