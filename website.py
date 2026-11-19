
import streamlit as st

st.set_page_config(
    page_title="ArticleMind | AI Research Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# BACKEND CONNECTION
# --------------------------------------------------

try:
    from rag_backend import (
        search_articles,
        generate_answer,
        summarize_article
    )
    BACKEND_READY = True
    BACKEND_ERROR = ""
except Exception as error:
    BACKEND_READY = False
    BACKEND_ERROR = str(error)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

defaults = {
    "articles": [],
    "selected_article": 0,
    "answer": "",
    "answer_sources": [],
    "summary": "",
    "question": ""
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def get_article_details(document):
    """Extract title and description from retrieved text."""
    document = str(document)

    title = "Research Article"
    description = document

    if "Title:" in document:
        title_part = document.split("Title:", 1)[1]
        if "\nArticle:" in title_part:
            title, description = title_part.split("\nArticle:", 1)
        else:
            title = title_part

    return title.strip(), description.strip()


def show_backend_error():
    st.error("The AI backend could not be loaded.")
    st.code(BACKEND_ERROR)
    st.info(
        "Check your dependencies and configure GROQ_API_KEY "
        "in Streamlit Cloud Secrets."
    )


# --------------------------------------------------
# CUSTOM DESIGN
# --------------------------------------------------

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #090817 0%, #160d2b 55%, #25103c 100%);
    color: #f5f3ff;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stSidebar"] {
    background: #100d20;
    border-right: 1px solid #39304d;
}

[data-testid="stSidebar"] * {
    color: #f5f3ff;
}

.main-title {
    font-size: 42px;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -1px;
}

.subtitle {
    font-size: 17px;
    color: #bcb4d5;
}

.section-title {
    font-size: 25px;
    font-weight: 700;
    color: #ffffff;
    margin-top: 12px;
}

.article-card {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 17px;
    padding: 17px;
    margin-bottom: 10px;
    color: #f4efff;
}

.answer-card {
    background: rgba(255,255,255,0.96);
    color: #241a38;
    padding: 24px;
    border-radius: 20px;
    line-height: 1.8;
    font-size: 17px;
}

.source-card {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 12px;
    padding: 13px;
    margin: 8px 0;
    color: #eee8ff;
}

div.stButton > button {
    background: linear-gradient(90deg, #7444c8, #a34cdb);
    color: white;
    border: none;
    border-radius: 13px;
    min-height: 45px;
    font-weight: 650;
    width: 100%;
}

div.stButton > button:hover {
    border: 1px solid #d7b5ff;
    color: white;
}

div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {
    background-color: #29233a;
    color: white;
    border: 1px solid #514368;
    border-radius: 12px;
}

div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.07);
    padding: 16px;
    border-radius: 14px;
    border: 1px solid #40344f;
}

div[data-testid="stMetricLabel"] {
    color: #c7bde0;
}

div[data-testid="stMetricValue"] {
    color: white;
}

.stCaption {
    color: #bcb4d5;
}

hr {
    border-color: #40344f;
}
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:
    st.markdown("# 📚 ArticleMind")
    st.caption("AI-Powered Research Assistant")
    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "🏠 Home",
            "🔎 Research Workspace",
            "📝 Article Summarizer",
            "ℹ️ About"
        ],
        label_visibility="visible"
    )

    st.divider()

    st.markdown("### ✨ AI Features")
    st.caption("• Semantic article search")
    st.caption("• AI-powered question answering")
    st.caption("• Article summarization")
    st.caption("• Retrieved source references")

    st.divider()
    st.caption("Powered by Python • ChromaDB • Groq")


# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

if page == "🏠 Home":

    st.markdown(
        '<div class="main-title">📚 Welcome to ArticleMind</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Your intelligent AI-powered research companion. '
        'Search, understand and summarize research articles effortlessly.</div>',
        unsafe_allow_html=True
    )

    st.write("")
    st.divider()

    c1, c2, c3 = st.columns(3)

    c1.metric("Platform", "AI Powered")
    c2.metric("Search", "Semantic")
    c3.metric("Tools", "3 AI Features")

    st.write("")
    st.markdown("## 🚀 Explore ArticleMind")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🔎 Smart Article Search")
        st.write(
            "Find relevant research articles using "
            "meaning-based semantic search."
        )

        st.markdown("### 🤖 AI Research Assistant")
        st.write(
            "Ask questions and receive answers "
            "based on retrieved research articles."
        )

    with col2:
        st.markdown("### 📝 Article Summarizer")
        st.write(
            "Convert lengthy article descriptions "
            "into short and understandable summaries."
        )

        st.markdown("### 📖 Source References")
        st.write(
            "See the article titles used to generate "
            "your AI answers."
        )

    if not BACKEND_READY:
        st.warning(
            "AI services are currently unavailable. "
            "Please configure the backend before using research features."
        )


# --------------------------------------------------
# RESEARCH WORKSPACE
# --------------------------------------------------

elif page == "🔎 Research Workspace":

    st.markdown(
        '<div class="main-title">🔬 Research Workspace</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Discover articles and ask your AI research assistant.</div>',
        unsafe_allow_html=True
    )

    st.divider()

    left, right = st.columns([0.9, 2.1], gap="large")

    # LEFT: ARTICLE SEARCH AND RESULTS
    with left:

        st.markdown("## 📚 Research Articles")

        with st.form("article_search_form"):
            search_query = st.text_input(
                "Search research topics",
                placeholder="e.g. Artificial Intelligence"
            )

            search_button = st.form_submit_button(
                "🔎 Search Articles"
            )

        if search_button:
            if not search_query.strip():
                st.warning("Please enter a research topic.")
            elif not BACKEND_READY:
                show_backend_error()
            else:
                with st.spinner("Searching relevant articles..."):
                    try:
                        results = search_articles(
                            search_query,
                            top_k=10
                        )

                        st.session_state.articles = results
                        st.session_state.selected_article = 0
                        st.session_state.answer = ""
                        st.session_state.answer_sources = []
                        st.session_state.summary = ""

                    except Exception as error:
                        st.error(f"Article search failed: {error}")

        articles = st.session_state.articles

        if articles:
            st.success(f"{len(articles)} articles retrieved")

            article_options = list(range(len(articles)))

            selected = st.radio(
                "Select an article",
                article_options,
                index=min(
                    st.session_state.selected_article,
                    len(article_options) - 1
                ),
                format_func=lambda i: (
                    f"{i + 1}. {get_article_details(articles[i])[0]}"
                ),
                key="article_selector"
            )

            st.session_state.selected_article = selected

            title, description = get_article_details(
                articles[selected]
            )

            with st.container(border=True):
                st.markdown("### 📄 Selected Article")
                st.markdown(f"**{title}**")
                st.write(description[:650] + (
                    "..." if len(description) > 650 else ""
                ))

        else:
            st.info("Search for a topic to discover research articles.")

    # RIGHT: AI QUESTION AND ANSWER
    with right:

        st.markdown("## 🤖 AI Research Assistant")

        with st.form("question_form"):
            question = st.text_input(
                "Ask your research question",
                placeholder="What was the main topic of this article?"
            )

            ask_button = st.form_submit_button(
                "🔎 Ask Question"
            )

        if ask_button:
            if not question.strip():
                st.warning("Please enter a question.")
            elif not BACKEND_READY:
                show_backend_error()
            else:
                context_articles = st.session_state.articles

                if not context_articles:
                    with st.spinner("Finding relevant articles..."):
                        context_articles = search_articles(
                            question,
                            top_k=5
                        )

                if not context_articles:
                    st.warning("No relevant articles were found.")
                else:
                    with st.spinner("ArticleMind is preparing your answer..."):
                        answer = generate_answer(
                            question,
                            context_articles
                        )

                        st.session_state.answer = answer
                        st.session_state.answer_sources = context_articles
                        st.session_state.question = question

        if st.session_state.answer:

            st.markdown(
                '<div class="section-title">💡 Answer</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="answer-card">'
                f'{st.session_state.answer}'
                f'</div>',
                unsafe_allow_html=True
            )

            st.markdown("")
            st.markdown("## 📚 Retrieved Sources")

            for i, document in enumerate(
                st.session_state.answer_sources
            ):
                title, description = get_article_details(document)

                with st.container(border=True):
                    st.markdown(f"**{i + 1}. {title}**")
                    st.caption(description[:250] + (
                        "..." if len(description) > 250 else ""
                    ))

        else:
            st.info(
                "Your AI-generated answer and retrieved sources "
                "will appear here."
            )


# --------------------------------------------------
# ARTICLE SUMMARIZER
# --------------------------------------------------

elif page == "📝 Article Summarizer":

    st.markdown(
        '<div class="main-title">📝 Article Summarizer</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Turn lengthy research articles into simple summaries.</div>',
        unsafe_allow_html=True
    )

    st.divider()

    if st.session_state.articles:

        article_list = st.session_state.articles

        selected_index = st.selectbox(
            "Choose a retrieved article",
            range(len(article_list)),
            format_func=lambda i: get_article_details(
                article_list[i]
            )[0]
        )

        title, description = get_article_details(
            article_list[selected_index]
        )

        st.markdown(f"### 📄 {title}")
        st.write(description)

        if st.button("✨ Generate Summary"):
            if not BACKEND_READY:
                show_backend_error()
            else:
                with st.spinner("Generating article summary..."):
                    st.session_state.summary = summarize_article(
                        title,
                        description
                    )

    else:
        st.info(
            "First visit Research Workspace and search for articles. "
            "Your retrieved articles will appear here."
        )

    if st.session_state.summary:
        st.markdown("## 💡 AI-Generated Summary")

       
        with st.container(border=True):
    st.write(st.session_state.answer)


# --------------------------------------------------
# ABOUT PAGE
# --------------------------------------------------

elif page == "ℹ️ About":

    st.markdown(
        '<div class="main-title">About ArticleMind 📚</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">AI-Powered Multi-Article Research Assistant</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("""
    ### 🎯 Project Overview

    ArticleMind is an AI-powered research assistant designed
    to help users discover, understand and summarize research articles.

    ### ⚙️ Technologies Used

    - Python
    - Streamlit
    - ChromaDB
    - Sentence Transformers
    - Groq Large Language Model
    - Retrieval-Augmented Generation (RAG)

    ### 🌟 Main Objectives

    - Search relevant research articles.
    - Generate answers using retrieved article content.
    - Summarize lengthy article descriptions.
    - Display retrieved source references.
    """)

    st.divider()
    st.caption("ArticleMind | AI-Powered Research Assistant")
