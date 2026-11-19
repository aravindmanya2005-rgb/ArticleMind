
import streamlit as st

# ==================================================
# 1. PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="ArticleMind - AI Research Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================================================
# 2. BACKEND CONNECTION
# ==================================================

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


# ==================================================
# 3. SESSION STATE
# ==================================================

defaults = {
    "articles": [],
    "selected_article": 0,
    "answer": "",
    "sources": [],
    "summary": "",
    "last_question": ""
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ==================================================
# 4. ARTICLE DETAILS
# ==================================================

def get_article_details(document):

    document = str(document)

    title = "Research Article"
    description = document

    if "Title:" in document:

        content = document.split("Title:", 1)[1]

        if "\nArticle:" in content:

            title, description = content.split(
                "\nArticle:", 1
            )

        else:
            title = content

    return title.strip(), description.strip()


# ==================================================
# 5. CUSTOM CSS DESIGN
# ==================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        120deg,
        #090815 0%,
        #170c29 55%,
        #260d3c 100%
    );
    color: #ffffff;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stSidebar"] {
    background-color: #100d20;
    border-right: 1px solid #40304f;
}

[data-testid="stSidebar"] * {
    color: #ffffff;
}

.main-title {
    color: #ffffff;
    font-size: 39px;
    font-weight: 800;
    letter-spacing: -1px;
}

.subtitle {
    color: #c5b9d7;
    font-size: 16px;
    margin-bottom: 15px;
}

.section-heading {
    color: #ffffff;
    font-size: 27px;
    font-weight: 750;
    margin-top: 12px;
    margin-bottom: 15px;
}

div[data-testid="stTextInput"] input {
    background-color: #292532;
    color: white;
    border: 1px solid #51445f;
    border-radius: 13px;
    min-height: 52px;
}

div[data-testid="stTextArea"] textarea {
    background-color: #292532;
    color: white;
    border: 1px solid #51445f;
    border-radius: 13px;
}

div.stButton > button {
    background: rgba(255,255,255,0.07);
    color: white;
    border: 1px solid #55465f;
    border-radius: 16px;
    min-height: 70px;
    width: 100%;
    white-space: normal;
    font-size: 15px;
    text-align: left;
    transition: 0.2s;
}

div.stButton > button:hover {
    background: #49305d;
    border: 1px solid #b78ae0;
    color: white;
}

div[data-testid="stFormSubmitButton"] button {
    background: linear-gradient(
        90deg,
        #7540b8,
        #a44bc8
    );
    color: white;
    border: 1px solid #a77bd0;
    border-radius: 15px;
    min-height: 55px;
    width: 100%;
    font-size: 17px;
}

div[data-testid="stFormSubmitButton"] button:hover {
    background: #914bc5;
    color: white;
}

.answer-card {
    background: #f2f0f7;
    color: #21172e;
    border-radius: 22px;
    padding: 20px;
    line-height: 1.8;
    font-size: 17px;
}

.source-card {
    background: rgba(255,255,255,0.07);
    border: 1px solid #55445f;
    border-radius: 14px;
    padding: 15px;
    margin-bottom: 10px;
}

hr {
    border-color: #51405e;
}

</style>
""", unsafe_allow_html=True)


# ==================================================
# 6. SIDEBAR NAVIGATION
# ==================================================

with st.sidebar:

    st.markdown("# 📚 ArticleMind")

    st.caption("AI-Powered Research Assistant")

    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "🏠 Home",
            "🔬 Research Dashboard",
            "📝 Article Summarizer",
            "ℹ️ About"
        ]
    )

    st.divider()

    st.markdown("### ✨ AI FEATURES")

    st.caption("🔎 Semantic Article Search")
    st.caption("🤖 AI Question Answering")
    st.caption("📝 Article Summarization")
    st.caption("📚 Retrieved Sources")

    st.divider()

    st.caption("Powered by Python, ChromaDB and Groq")


# ==================================================
# 7. HOME PAGE
# ==================================================

if page == "🏠 Home":

    st.markdown(
        '<div class="main-title">📚 Welcome to ArticleMind</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Your intelligent AI-powered research companion. '
        'Search, understand and summarize research articles.'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    col1.metric("Platform", "AI Powered")
    col2.metric("Research", "Smart Search")
    col3.metric("Features", "3 AI Tools")

    st.write("")

    st.markdown("## 🚀 Explore ArticleMind")

    left, right = st.columns(2)

    with left:

        st.markdown("### 🔎 Smart Article Search")

        st.write(
            "Discover relevant research articles "
            "using semantic search."
        )

        st.markdown("### 🤖 AI Research Assistant")

        st.write(
            "Ask questions and get answers "
            "based on retrieved articles."
        )

    with right:

        st.markdown("### 📝 Article Summarizer")

        st.write(
            "Convert lengthy article descriptions "
            "into simple summaries."
        )

        st.markdown("### 📚 Retrieved Sources")

        st.write(
            "View the articles used to generate "
            "your AI answers."
        )

    if not BACKEND_READY:

        st.warning(
            "AI backend is unavailable. "
            "Check your configuration."
        )


# ==================================================
# 8. RESEARCH DASHBOARD
# ==================================================

elif page == "🔬 Research Dashboard":

    st.markdown(
        '<div class="main-title">📚 ArticleMind</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Your AI-powered multi-article research assistant'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()

    left, right = st.columns(
        [0.9, 2.1],
        gap="large"
    )


    # ----------------------------------------------
    # LEFT SIDE: ARTICLE SEARCH
    # ----------------------------------------------

    with left:

        st.markdown(
            '<div class="section-heading">📖 Articles</div>',
            unsafe_allow_html=True
        )

        with st.form("article_search_form"):

            search_query = st.text_input(
                "Search Articles",
                placeholder="Enter your research topic..."
            )

            search_button = st.form_submit_button(
                "🔎 Search Articles"
            )

        if search_button:

            if not search_query.strip():

                st.warning("Please enter a research topic.")

            elif not BACKEND_READY:

                st.error("Backend error: " + BACKEND_ERROR)

            else:

                with st.spinner("Searching articles..."):

                    try:

                        results = search_articles(
                            search_query,
                            top_k=10
                        )

                        st.session_state.articles = results
                        st.session_state.selected_article = 0
                        st.session_state.answer = ""
                        st.session_state.sources = []
                        st.session_state.summary = ""

                        st.rerun()

                    except Exception as error:

                        st.error(
                            f"Article search failed: {error}"
                        )

        articles = st.session_state.articles

        if articles:

            st.caption(
                f"📚 {len(articles)} articles found"
            )

            for i, document in enumerate(articles):

                title, description = get_article_details(
                    document
                )

                prefix = (
                    "✓ "
                    if i == st.session_state.selected_article
                    else ""
                )

                if st.button(
                    f"{prefix}{i + 1}. {title}",
                    key=f"article_{i}"
                ):

                    st.session_state.selected_article = i
                    st.session_state.answer = ""
                    st.session_state.sources = []
                    st.session_state.summary = ""

                    st.rerun()

        else:

            st.info(
                "Search for a topic to display research articles."
            )


    # ----------------------------------------------
    # RIGHT SIDE: AI ASSISTANT
    # ----------------------------------------------

    with right:

        st.markdown(
            '<div class="section-heading">🤖 AI Research Assistant</div>',
            unsafe_allow_html=True
        )

        if articles:

            selected_index = min(
                st.session_state.selected_article,
                len(articles) - 1
            )

            selected_document = articles[selected_index]

            selected_title, selected_description = (
                get_article_details(selected_document)
            )

            st.caption(
                f"Selected article: {selected_title}"
            )

        else:

            selected_document = None

            st.caption(
                "Search for articles to start your research."
            )

        with st.form("question_form"):

            question = st.text_input(
                "Ask your question",
                placeholder="What was the main topic of this article?"
            )

            ask_button = st.form_submit_button(
                "🔎 Ask Question"
            )

        if ask_button:

            if not question.strip():

                st.warning("Please enter a question.")

            elif not BACKEND_READY:

                st.error("Backend error: " + BACKEND_ERROR)

            elif not selected_document:

                st.warning(
                    "Please search for and select an article first."
                )

            else:

                with st.spinner(
                    "ArticleMind is generating your answer..."
                ):

                    try:

                        answer = generate_answer(
                            question,
                            [selected_document]
                        )

                        st.session_state.answer = answer

                        st.session_state.sources = [
                            selected_document
                        ]

                        st.session_state.last_question = question

                    except Exception as error:

                        st.error(
                            f"Answer generation failed: {error}"
                        )

        # ------------------------------------------
        # ANSWER SECTION
        # ------------------------------------------

        st.markdown(
            '<div class="section-heading">💡 Answer</div>',
            unsafe_allow_html=True
        )

        if st.session_state.answer:

            with st.container(border=True):

                st.write(st.session_state.answer)

        else:

            st.info(
                "Your AI-generated answer will appear here."
            )

        # ------------------------------------------
        # RETRIEVED SOURCES
        # ------------------------------------------

        st.markdown(
            '<div class="section-heading">📚 Retrieved Sources</div>',
            unsafe_allow_html=True
        )

        if st.session_state.sources:

            for i, document in enumerate(
                st.session_state.sources
            ):

                title, description = get_article_details(
                    document
                )

                with st.container(border=True):

                    st.markdown(
                        f"**{i + 1}. {title}**"
                    )

                    st.write(
                        description[:500] +
                        ("..." if len(description) > 500 else "")
                    )

        else:

            st.caption(
                "Retrieved article references will appear here."
            )


# ==================================================
# 9. ARTICLE SUMMARIZER
# ==================================================

elif page == "📝 Article Summarizer":

    st.markdown(
        '<div class="main-title">📝 Article Summarizer</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Generate simple summaries of research articles.'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()

    articles = st.session_state.articles

    if not articles:

        st.info(
            "First search for articles in the Research Dashboard."
        )

    else:

        selected_index = st.selectbox(
            "Select an article",
            range(len(articles)),
            format_func=lambda i: get_article_details(
                articles[i]
            )[0]
        )

        title, description = get_article_details(
            articles[selected_index]
        )

        st.markdown(f"### 📄 {title}")

        with st.container(border=True):

            st.write(description)

        if st.button("✨ Generate Summary"):

            if not BACKEND_READY:

                st.error("Backend error: " + BACKEND_ERROR)

            else:

                with st.spinner(
                    "Generating your article summary..."
                ):

                    try:

                        summary = summarize_article(
                            title,
                            description
                        )

                        st.session_state.summary = summary

                    except Exception as error:

                        st.error(
                            f"Summarization failed: {error}"
                        )

        if st.session_state.summary:

            st.markdown("## 💡 AI-Generated Summary")

            with st.container(border=True):

                st.write(st.session_state.summary)


# ==================================================
# 10. ABOUT PAGE
# ==================================================

elif page == "ℹ️ About":

    st.markdown(
        '<div class="main-title">About ArticleMind 📚</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'AI-Powered Multi-Article Research Assistant'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("""
    ## 🎯 Project Overview

    ArticleMind is an AI-powered research assistant
    designed to help users search, understand and
    summarize multiple research articles.

    ## ⚙️ Technologies Used

    - Python
    - Streamlit
    - ChromaDB
    - Sentence Transformers
    - Groq Large Language Model
    - Retrieval-Augmented Generation (RAG)

    ## 🌟 Main Objectives

    - Search relevant research articles.
    - Generate answers using retrieved article content.
    - Summarize lengthy article descriptions.
    - Display retrieved source references.

    """)

    st.divider()

    st.caption(
        "ArticleMind | AI-Powered Research Assistant"
    )
