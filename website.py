
import streamlit as st

st.set_page_config(
    page_title="ArticleMind",
    page_icon="📚",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #f5f6ff;
}
[data-testid="stSidebar"] {
    background-color: #171936;
}
[data-testid="stSidebar"] * {
    color: white;
}
.main-title {
    color: #25275e;
    font-size: 42px;
    font-weight: bold;
}
.subtitle {
    color: #666b85;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.title("📚 ArticleMind")
st.sidebar.write("AI Research Assistant")

page = st.sidebar.radio(
    "Navigation",
    ["Home", "Article Search", "AI Assistant",
     "Article Summarizer", "About"]
)

if page == "Home":
    st.markdown(
        '<p class="main-title">Welcome to ArticleMind 🚀</p>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<p class="subtitle">Your AI-powered research assistant</p>',
        unsafe_allow_html=True
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    col1.metric("Platform", "AI Powered")
    col2.metric("Research", "Smart Search")
    col3.metric("Tools", "3 Features")

    st.subheader("What can you do?")
    st.write("🔎 Search research articles")
    st.write("🤖 Ask questions using AI")
    st.write("📝 Summarize lengthy articles")

elif page == "Article Search":
    st.title("🔎 Article Search")
    query = st.text_input("Enter your research topic")
    if st.button("Search Articles"):
        if query:
            st.info("We will connect your article search backend here.")
        else:
            st.warning("Please enter a topic.")

elif page == "AI Assistant":
    st.title("🤖 AI Research Assistant")
    question = st.text_input("Ask a question about your articles")
    if st.button("Get Answer"):
        if question:
            st.info("We will connect your AI backend here.")
        else:
            st.warning("Please enter a question.")

elif page == "Article Summarizer":
    st.title("📝 Article Summarizer")
    article = st.text_area("Paste your article here")
    if st.button("Summarize"):
        if article:
            st.info("We will connect your summarization backend here.")
        else:
            st.warning("Please enter article text.")

elif page == "About":
    st.title("About ArticleMind")
    st.write("""
    ArticleMind is an AI-powered research assistant
    designed to help users search, understand and
    summarize multiple research articles.
    """)
