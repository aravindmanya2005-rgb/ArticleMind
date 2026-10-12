import os
import streamlit as st

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaLLM

# -----------------------------
# Streamlit Page Config
# -----------------------------
st.set_page_config(
    page_title="ArticleMind",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 ArticleMind")
st.write("Ask questions based on your article knowledge base.")

# -----------------------------
# Get Project Directory
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

knowledge_path = os.path.join(
    BASE_DIR,
    "data",
    "Knowledge_base.txt"
)

# -----------------------------
# Check File Exists
# -----------------------------
if not os.path.exists(knowledge_path):
    st.error(f"Knowledge base not found:\n\n{knowledge_path}")
    st.stop()

# -----------------------------
# Load Knowledge Base
# -----------------------------
loader = TextLoader(knowledge_path, encoding="utf-8")
documents = loader.load()

if len(documents) == 0:
    st.error("Knowledge base is empty.")
    st.stop()

# -----------------------------
# Split into Chunks
# -----------------------------
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = text_splitter.split_documents(documents)

if len(chunks) == 0:
    st.error("No text chunks created.")
    st.stop()

# -----------------------------
# Embeddings
# -----------------------------
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# -----------------------------
# Chroma Database
# -----------------------------
db_path = os.path.join(BASE_DIR, "chroma_db")

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=db_path
)

# -----------------------------
# Load Ollama
# -----------------------------
llm = OllamaLLM(
    model="llama3.2"
)

# -----------------------------
# User Question
# -----------------------------
question = st.text_input(
    "Ask a question about the article:"
)

if question:

    docs = vectorstore.similarity_search(
        question,
        k=3
    )

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = f"""
You are a helpful AI assistant.

Answer ONLY using the context below.

If the answer is not available, say:

"I don't know based on the provided article."

Context:
{context}

Question:
{question}

Answer:
"""

    answer = llm.invoke(prompt)

    st.subheader("🤖 AI Answer")
    st.write(answer)

    with st.expander("📚 Retrieved Context"):
        st.write(context)