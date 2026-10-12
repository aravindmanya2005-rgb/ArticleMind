import streamlit as st
import pandas as pd
import os

from rag_backend import (
    search_articles,
    generate_answer,
    summarize_article
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="ArticleMind",
    page_icon="🧠",
    layout="wide"
)


# ============================================================
# FILE PATH
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

CSV_PATH = os.path.join(
    BASE_DIR,
    "data",
    "train.csv"
)


# ============================================================
# CHECK DATASET
# ============================================================

if not os.path.exists(CSV_PATH):

    st.error("❌ train.csv was not found.")

    st.code(CSV_PATH)

    st.stop()


# ============================================================
# LOAD DATASET
# ============================================================

df = pd.read_csv(CSV_PATH)

df.columns = (
    df.columns
    .astype(str)
    .str.strip()
    .str.lower()
)

# Use only first 1000 articles
df = df.head(1000).reset_index(drop=True)


# ============================================================
# CHECK REQUIRED COLUMNS
# ============================================================

if "title" not in df.columns:

    st.error("❌ Title column not found.")

    st.write(
        "Available columns:",
        list(df.columns)
    )

    st.stop()


if "description" not in df.columns:

    st.error("❌ Description column not found.")

    st.write(
        "Available columns:",
        list(df.columns)
    )

    st.stop()


# ============================================================
# SESSION STATE
# ============================================================

if "selected_article" not in st.session_state:

    st.session_state.selected_article = 0


# ============================================================
# HEADER
# ============================================================

st.title("🤖 ArticleMind Research Assistant")

st.write(
    "Ask questions from the article knowledge base "
    "using semantic retrieval and Llama 3.2."
)


# ============================================================
# MAIN COLUMNS
# ============================================================

left_column, right_column = st.columns(
    [1, 2],
    gap="large"
)


# ============================================================
# LEFT COLUMN - ARTICLE KNOWLEDGE BASE
# ============================================================

with left_column:

    st.header("📚 Article Knowledge Base")

    search_text = st.text_input(
        "🔍 Search article",
        placeholder="Search by article title..."
    )

    # Search titles
    if search_text.strip():

        filtered_articles = df[
            df["title"]
            .astype(str)
            .str.contains(
                search_text,
                case=False,
                na=False
            )
        ].copy()

    else:

        filtered_articles = df.copy()


    st.caption(
        f"{len(filtered_articles)} articles"
    )

    st.divider()


    # Display article buttons
    for index, row in filtered_articles.iterrows():

        article_title = str(
            row["title"]
        )

        if st.button(
            f"{index + 1}. {article_title}",
            key=f"article_button_{index}",
            use_container_width=True
        ):

            st.session_state.selected_article = index

            st.rerun()


# ============================================================
# SELECT CURRENT ARTICLE
# ============================================================

selected_index = (
    st.session_state.selected_article
)


# Safety check
if selected_index >= len(df):

    selected_index = 0

    st.session_state.selected_article = 0


selected_article = df.iloc[
    selected_index
]


article_title = str(
    selected_article["title"]
)

article_description = str(
    selected_article["description"]
)


# ============================================================
# RIGHT COLUMN
# ============================================================

with right_column:

    st.header(
        "🤖 ArticleMind Research Assistant"
    )

    st.caption(
        "Semantic Search + RAG + Llama 3.2"
    )


    # ========================================================
    # SELECTED ARTICLE
    # ========================================================

    st.subheader("📄 Selected Article")

    st.markdown(
        f"## {article_title}"
    )


    with st.expander(
        "View article description",
        expanded=True
    ):

        st.write(
            article_description
        )


    st.divider()


    # ========================================================
    # ASK QUESTION
    # ========================================================

    st.subheader("💬 Ask a Question")

    st.write(
        "Ask a question about the article knowledge base."
    )


    question = st.text_input(
        "Your question",
        placeholder=(
            "Example: What is the main topic "
            "of this article?"
        ),
        key="article_question"
    )


    ask_button = st.button(
        "🔎 Ask Question",
        key="ask_question_button",
        use_container_width=True
    )


    if ask_button:

        if not question.strip():

            st.warning(
                "⚠️ Please enter a question first."
            )

        else:

            # ----------------------------------------------
            # STEP 1: Semantic Search
            # ----------------------------------------------

            with st.spinner(
                "🔎 Searching the knowledge base..."
            ):

                results = search_articles(
                    question,
                    top_k=5
                )


            documents = results.get(
                "documents",
                [[]]
            )


            if documents:

                documents = documents[0]


            else:

                documents = []


            # ----------------------------------------------
            # STEP 2: Generate Answer
            # ----------------------------------------------

            if documents:

                with st.spinner(
                    "🤖 Llama 3.2 is generating the answer..."
                ):

                    answer = generate_answer(
                        question,
                        documents
                    )


                # ------------------------------------------
                # ANSWER
                # ------------------------------------------

                st.subheader(
                    "💡 Answer"
                )

                st.success(
                    answer
                )


                # ------------------------------------------
                # SOURCES
                # ------------------------------------------

                st.subheader(
                    "📚 Retrieved Sources"
                )


                for number, document in enumerate(
                    documents,
                    start=1
                ):

                    with st.expander(
                        f"Source {number}"
                    ):

                        st.write(
                            document
                        )


            else:

                st.warning(
                    "No relevant information was found "
                    "in the knowledge base."
                )


    # ========================================================
    # SUMMARY SECTION
    # ========================================================

    st.divider()

    st.subheader(
        "📝 Article Summarization"
    )

    st.write(
        "Generate a concise summary of the selected "
        "article using Llama 3.2."
    )


    summarize_button = st.button(
        "✨ Generate Summary",
        key="summary_button",
        use_container_width=True
    )


    if summarize_button:

        # ----------------------------------------------
        # Check description
        # ----------------------------------------------

        if (
            not article_description.strip()
            or
            article_description.lower() == "nan"
        ):

            st.warning(
                "⚠️ This article does not have "
                "a description to summarize."
            )

        else:

            # ------------------------------------------
            # Generate summary
            # ------------------------------------------

            with st.spinner(
                "🤖 Llama 3.2 is creating the summary..."
            ):

                summary = summarize_article(
                    article_title,
                    article_description
                )


            # ------------------------------------------
            # Display summary
            # ------------------------------------------

            st.subheader(
                "📝 Short Summary"
            )

            st.success(
                summary
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "ArticleMind | Semantic Search + RAG + Llama 3.2"
)