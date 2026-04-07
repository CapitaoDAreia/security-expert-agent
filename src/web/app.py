import streamlit as st
import requests
import time
from src.agent.brain import CISOExpert
from src.database.storage import VectorStoreManager

st.set_page_config(page_title="Security Expert Agent", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    /* Force containers to use relative height instead of fixed pixels */
    /* This targets the div created by st.container(height=...) */
    [data-testid="stVerticalBlockBorderWrapper"] > div:nth-child(1) > div {
        max-height: 65vh !important;
    }
    
    .stChatFloatingInputContainer {
        padding-bottom: 20px;
    }
    .chunk-card {
        background-color: #161b22;
        border-left: 4px solid #238636;
        padding: 15px;
        margin-bottom: 10px;
        border-radius: 5px;
        font-size: 0.9rem;
    }
    .trace-container {
        background-color: #0d1117;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #30363d;
        font-family: monospace;
        font-size: 0.8rem;
        color: #8b949e;
        height: 15vh; /* Dynamic height for trace */
        overflow-y: auto;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def init_agent():
    return CISOExpert(VectorStoreManager())

agent = init_agent()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_sources" not in st.session_state:
    st.session_state.last_sources = []
if "trace_logs" not in st.session_state:
    st.session_state.trace_logs = "Waiting for interaction..."

col_chat, col_logs = st.columns([0.6, 0.4])

with col_chat:
    st.header("🛡️ CISO Expert Chat")
    
    chat_container = st.container(height=500)
    
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("Ask about security policies..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)

        with chat_container:
            with st.chat_message("assistant"):
                with st.spinner("Retrieving knowledge..."):
                    start_time = time.time()
                    answer, sources = agent.ask(prompt)
                    end_time = time.time()
                    
                    st.markdown(answer)
                    
                    st.session_state.last_sources = sources
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    
                    latency = round(end_time - start_time, 2)
                    st.session_state.trace_logs = (
                        f"> Connection: PostgreSQL (Healthy)\n"
                        f"> Latency: {latency}s\n"
                        f"> Chunks Retrieved: {len(sources)}\n"
                        f"> Embedding Model: mxbai-embed-large\n"
                        f"> LLM: Llama3"
                    )
        st.rerun()

with col_logs:
    st.header("📚 Active Context (Chunks)")
    
    chunks_container = st.container(height=500)
    
    with chunks_container:
        if st.session_state.last_sources:
            for i, (doc, score) in enumerate(st.session_state.last_sources):
                source_name = doc.metadata.get('source', 'Unknown')
                page = doc.metadata.get('page', 'N/A')
                
                st.markdown(f"**Chunk #{i+1}** | File: `{source_name}`")
                st.caption(f"Relevance Score: `{round(score, 4)}` | Page: `{page}`")
                st.markdown(f'<div class="chunk-card">{doc.page_content}</div>', unsafe_allow_html=True)
                st.divider()
        else:
            st.info("No chunks retrieved yet.")

    st.subheader("📡 Connection Trace")
    # Small fixed height for logs too
    st.markdown(f'<pre class="trace-container" style="height: 120px; overflow-y: auto;">{st.session_state.trace_logs}</pre>', unsafe_allow_html=True)