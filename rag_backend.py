
import os
from pathlib import Path

import chromadb
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from langchain_groq import ChatGroq


# ==================================================
# 1. CONFIGURATION
# ==================================================

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

CSV_PATH = BASE_DIR / "data" / "train.csv"
CHROMA_PATH = BASE_DIR / "chroma_db"


# ==================================================
# 2. GROQ API KEY AND LANGUAGE MODEL
# ==================================================

def get_groq_api_key():
    try:
        key = st.secrets.get("GROQ_API_KEY", "")
        if key:
            return key
    except Exception:
        pass

    return os.getenv("GROQ_API_KEY", "")


api_key = get_groq_api_key()

if not api_key:
    raise RuntimeError(
        "Groq API key missing. Add GROQ_API_KEY to your "
        "project's .env file or Streamlit Cloud Secrets."
    )

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    groq_api_key=api_key,
    temperature=0.2,
    max_tokens=1024,
    timeout=60,
    max_retries=2,
)


# ==================================================
# 3. LOAD ARTICLE DATASET
# ==================================================

if not CSV_PATH.exists():
    raise FileNotFoundError(f"Dataset not found: {CSV_PATH}")

df = pd.read_csv(CSV_PATH)
df.columns = df.columns.astype(str).str.strip().str.lower()

required_columns = {"title", "description"}

if not required_columns.issubset(df.columns):
    raise ValueError(
        "train.csv must contain 'title' and 'description' columns."
    )

df = df[["title", "description"]].fillna("")
df = df.head(1000).reset_index(drop=True)

documents = []

for _, row in df.iterrows():
    title = str(row["title"]).strip()
    description = str(row["description"]).strip()

    if title or description:
        documents.append(f"Title: {title}\nArticle: {description}")

if not documents:
    raise ValueError("No articles found in train.csv.")


# ==================================================
# 4. LOAD EMBEDDING MODEL
# ==================================================

@st.cache_resource
def load_embedding_model():
    return SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2"
    )


embedding_model = load_embedding_model()


# ==================================================
# 5. INITIALIZE CHROMADB
# ==================================================

CHROMA_PATH.mkdir(parents=True, exist_ok=True)

client = chromadb.PersistentClient(path=str(CHROMA_PATH))

collection = client.get_or_create_collection(name="articles")


# ==================================================
# 6. INDEX ARTICLES
# ==================================================

# Rebuild the collection if the number of indexed articles differs.
# For this simple project, the first 1000 dataset rows are indexed.

if collection.count() != len(documents):
    existing_ids = collection.get().get("ids", [])

    for start in range(0, len(existing_ids), 500):
        collection.delete(ids=existing_ids[start:start + 500])

    batch_size = 100

    for start in range(0, len(documents), batch_size):
        batch = documents[start:start + batch_size]
        embeddings = embedding_model.encode(batch)

        collection.upsert(
            ids=[
                str(i)
                for i in range(start, start + len(batch))
            ],
            documents=batch,
            embeddings=embeddings.tolist(),
        )


# ==================================================
# 7. SEARCH ARTICLES
# ==================================================

def search_articles(query, top_k=5):
    """Return a list of relevant article text documents."""

    query = str(query or "").strip()

    if not query or collection.count() == 0:
        return []

    query_embedding = embedding_model.encode([query])[0]

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=min(top_k, collection.count()),
        include=["documents", "distances"],
    )

    return results.get("documents", [[]])[0]


# ==================================================
# 8. GENERATE ANSWERS USING RAG
# ==================================================

def generate_answer(question, documents):
    """Answer a question using retrieved article context."""

    question = str(question or "").strip()

    if not question:
        return "Please enter a question."

    if not documents:
        return "No relevant information was found in the knowledge base."

    context_parts = []

    for document in documents:
        if isinstance(document, str):
            context_parts.append(document)
        elif hasattr(document, "page_content"):
            context_parts.append(document.page_content)
        else:
            context_parts.append(str(document))

    context = "\n\n".join(context_parts)

    prompt = f"""
You are ArticleMind, an AI research assistant.

Answer the user's question using the article context below.
Do not invent facts. If the answer is not in the context,
explain that the available articles do not provide enough information.

ARTICLE CONTEXT:
{context}

USER QUESTION:
{question}

Give a clear, helpful answer.
"""

    try:
        response = llm.invoke(prompt)
        return str(response.content).strip()

    except Exception as error:
        print(
            f"Answer generation error: "
            f"{type(error).__name__}: {error}"
        )
        return (
            "Unable to generate an answer. Check the Groq API key, "
            "model availability, and internet connection."
        )


# ==================================================
# 9. SUMMARIZE ARTICLES
# ==================================================

def summarize_article(title, description):
    """Generate a concise summary of a selected article."""

    title = str(title or "").strip()
    description = str(description or "").strip()

    if not title and not description:
        return "No article content was provided."

    prompt = f"""
You are ArticleMind, an AI research assistant.

Summarize this article in 1–2 concise sentences.
Use simple language and only the information provided.
Do not invent facts or findings.

ARTICLE TITLE:
{title}

ARTICLE DESCRIPTION:
{description}

SHORT SUMMARY:
"""

    try:
        response = llm.invoke(prompt)
        summary = str(response.content).strip()

        if not summary:
            return "The AI returned an empty summary. Please try again."

        return summary

    except Exception as error:
        print(
            f"Summarization error: "
            f"{type(error).__name__}: {error}"
        )
        return (
            "Unable to summarize the article. "
            f"Error: {type(error).__name__}: {error}"
        )