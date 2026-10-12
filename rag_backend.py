import os
import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer
from langchain_ollama import OllamaLLM


# ==========================================================
# PROJECT PATHS
# ==========================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

CSV_PATH = os.path.join(
    BASE_DIR,
    "data",
    "train.csv"
)

CHROMA_PATH = os.path.join(
    BASE_DIR,
    "chroma_db"
)


# ==========================================================
# LOAD DATASET
# ==========================================================

print("Loading dataset...")

df = pd.read_csv(CSV_PATH)

df.columns = (
    df.columns
    .astype(str)
    .str.strip()
    .str.lower()
)

df = df.head(1000).reset_index(drop=True)

print(f"Loaded {len(df)} articles.")


# ==========================================================
# CREATE DOCUMENTS
# ==========================================================

documents = []

for _, row in df.iterrows():

    title = str(row["title"])
    description = str(row["description"])

    document = title + ". " + description

    documents.append(document)


# ==========================================================
# LOAD EMBEDDING MODEL
# ==========================================================

print("Loading embedding model...")

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("Embedding model loaded.")


# ==========================================================
# CONNECT TO CHROMADB
# ==========================================================

client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

collection = client.get_or_create_collection(
    name="articles"
)


# ==========================================================
# STORE EMBEDDINGS
# ==========================================================

if collection.count() < len(documents):

    print(
        "Creating embeddings for 1000 articles..."
    )

    embeddings = embedding_model.encode(
        documents,
        show_progress_bar=True
    )

    collection.upsert(
        ids=[
            str(i)
            for i in range(len(documents))
        ],
        documents=documents,
        embeddings=embeddings.tolist()
    )

    print(
        "Articles stored successfully!"
    )

else:

    print(
        "Existing ChromaDB found."
    )

    print(
        f"{collection.count()} articles already stored."
    )


# ==========================================================
# LOAD LLAMA 3.2
# ==========================================================

print("Loading Llama 3.2...")

llm = OllamaLLM(
    model="llama3.2"
)

print("Llama 3.2 ready.")


# ==========================================================
# SEMANTIC SEARCH
# ==========================================================

def search_articles(
    query,
    top_k=5
):

    query_embedding = embedding_model.encode(
        [query]
    )[0]

    results = collection.query(
        query_embeddings=[
            query_embedding.tolist()
        ],
        n_results=top_k
    )

    return results


# ==========================================================
# QUESTION ANSWERING
# ==========================================================

def generate_answer(
    question,
    documents
):

    context = "\n\n".join(
        documents
    )

    prompt = f"""
You are ArticleMind, an AI-powered
multi-article research assistant.

Answer the user's question using ONLY
the information provided in the article context.

Do not invent information.

If the answer cannot be found in the context,
say:

"I could not find enough information in the
article knowledge base."

ARTICLE CONTEXT:

{context}

USER QUESTION:

{question}

Give a clear and concise answer.
"""

    response = llm.invoke(
        prompt
    )

    return response


# ==========================================================
# SHORT ARTICLE SUMMARIZATION
# ==========================================================

def summarize_article(
    title,
    description
):

    article = f"""
Title: {title}

Article:
{description}
"""

    prompt = f"""
You are an article summarization assistant.

Summarize the article below in ONLY 1 or 2
short sentences.

Keep the summary simple, clear and concise.

Use ONLY information from the article.

Do not say that information is missing.

Do not say "I could not find enough information".

Do not create bullet points.

ARTICLE:

{article}

SHORT SUMMARY:
"""

    response = llm.invoke(
        prompt
    )

    return response.strip()