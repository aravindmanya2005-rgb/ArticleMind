import streamlit as st
import pandas as pd
import os

from rag_backend import (
    search_articles,
    generate_answer,
    summarize_article
)
from auth_manager import authenticate_user
from theme import apply_custom_theme


# ============================================================
# 1. PAGE CONFIGURATION & THEME
# ============================================================

st.set_page_config(
    page_title="ArticleMind - AI Research Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply dark navy & purple glassmorphism theme
apply_custom_theme()


# ============================================================
# 2. SESSION STATE INITIALIZATION
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_profile" not in st.session_state:
    st.session_state.user_profile = None

if "selected_article" not in st.session_state:
    st.session_state.selected_article = 0


# ============================================================
# 3. LOGOUT FUNCTION
# ============================================================

def logout():
    """Reset session state and log the user out."""
    st.session_state.logged_in = False
    st.session_state.user_profile = None
    st.rerun()


# ============================================================
# 4. GLASSMORPHISM LOGIN PAGE
# ============================================================

def render_login_page():
    """Render the glassmorphism login interface."""

    # Top floating brand container
    st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem; margin-top: 1rem;">
            <div style="display: inline-flex; align-items: center; gap: 14px; background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.12); padding: 10px 24px; border-radius: 50px; backdrop-filter: blur(16px); box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
                <svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="url(#brain-grad)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <defs>
                        <linearGradient id="brain-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stop-color="#a855f7" />
                            <stop offset="50%" stop-color="#6366f1" />
                            <stop offset="100%" stop-color="#38bdf8" />
                        </linearGradient>
                    </defs>
                    <path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z"/>
                    <path d="M12 5a3 3 0 1 1 5.997.125 4 4 0 0 1 2.526 5.77 4 4 0 0 1-.556 6.588A4 4 0 1 1 12 18Z"/>
                    <path d="M15 13a3 3 0 1 0-6 0"/>
                    <path d="M12 5v13"/>
                </svg>
                <span class="gradient-text" style="font-size: 1.8rem; letter-spacing: -0.5px;">ArticleMind</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Main Card Container
    _, center_col, _ = st.columns([0.05, 0.9, 0.05])

    with center_col:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        left_col, right_col = st.columns([1.1, 0.9], gap="large")

        # LEFT SECTION - BRAND & FEATURES
        with left_col:
            st.markdown('<span class="feature-badge">⚡ AI-POWERED INTELLIGENCE</span>', unsafe_allow_html=True)
            
            st.markdown("""
                <h1 class="gradient-text" style="font-size: 2.2rem; line-height: 1.2; margin-top: 0.5rem; margin-bottom: 1rem;">
                    Your AI-Powered Research Assistant
                </h1>
                <p style="color: #94a3b8; font-size: 1rem; line-height: 1.6; margin-bottom: 1.5rem;">
                    Accelerate your scientific literature discovery with ArticleMind. Access instant semantic vector retrieval across 1,000+ research papers, powered by Llama 3.2.
                </p>
            """, unsafe_allow_html=True)

            st.markdown("""
                <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 1.5rem;">
                    <span class="feature-badge">🤖 Llama 3.2 LLM</span>
                    <span class="feature-badge">⚡ 1,000 Indexed Articles</span>
                    <span class="feature-badge">🔍 Semantic Vector Search</span>
                    <span class="feature-badge">📝 Article Summarization</span>
                    <span class="feature-badge">🔗 Direct Source Links</span>
                </div>
            """, unsafe_allow_html=True)

            with st.expander("🔑 View Demo Access Credentials", expanded=False):
                st.markdown("""
                    **Default Demo Accounts:**
                    - **Admin:** `admin` / `admin123`
                    - **Researcher:** `researcher` / `research123`
                """)

        # RIGHT SECTION - LOGIN FORM
        with right_col:
            st.markdown("""
                <div style="margin-bottom: 1.2rem;">
                    <h2 style="font-size: 1.4rem; font-weight: 700; color: #f8fafc; margin-bottom: 0.3rem;">Sign In</h2>
                    <p style="color: #64748b; font-size: 0.88rem;">Enter your credentials to access the research portal</p>
                </div>
            """, unsafe_allow_html=True)

            username_input = st.text_input(
                "Username",
                placeholder="Enter username (e.g. admin)",
                key="login_username"
            )

            # Show / Hide password toggle
            show_password = st.checkbox("Show password", key="toggle_show_password")
            
            password_type = "default" if show_password else "password"
            password_input = st.text_input(
                "Password",
                type=password_type,
                placeholder="Enter password",
                key="login_password"
            )

            st.markdown('<div class="login-btn-wrapper">', unsafe_allow_html=True)
            login_clicked = st.button("🔐 Sign In to ArticleMind", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

            if login_clicked:
                success, message, profile = authenticate_user(username_input, password_input)
                
                if success:
                    st.session_state.logged_in = True
                    st.session_state.user_profile = profile
                    st.success("✅ Login successful! Redirecting...")
                    st.rerun()
                else:
                    st.error(f"❌ {message}")

        st.markdown('</div>', unsafe_allow_html=True)

    # Footer signature
    st.markdown("""
        <div style="text-align: center; color: #64748b; font-size: 0.8rem; margin-top: 2rem;">
            ArticleMind Portal &bull; Multi-Article RAG Engine &bull; Llama 3.2
        </div>
    """, unsafe_allow_html=True)


# ============================================================
# 5. AUTH CHECK & RENDERING
# ============================================================

if not st.session_state.logged_in:
    render_login_page()
    st.stop()


# ============================================================
# 6. DASHBOARD - LOAD DATASET & RAG BACKEND
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "data", "train.csv")
URL_CSV_PATH = os.path.join(BASE_DIR, "data", "articles_with_urls.csv")

if not os.path.exists(CSV_PATH):
    st.error("❌ train.csv was not found.")
    st.code(CSV_PATH)
    st.stop()

# Load Dataset
df = pd.read_csv(CSV_PATH)
df.columns = df.columns.astype(str).str.strip().str.lower()
df = df.head(1000).reset_index(drop=True)

if "title" not in df.columns or "description" not in df.columns:
    st.error("❌ Required columns ('title', 'description') missing in dataset.")
    st.stop()

# Load URLs if present
if os.path.exists(URL_CSV_PATH):
    url_df = pd.read_csv(URL_CSV_PATH)
    url_df.columns = url_df.columns.astype(str).str.strip().str.lower()
    url_df = url_df.head(1000).reset_index(drop=True)
    if "article_url" in url_df.columns:
        df["article_url"] = url_df["article_url"].reindex(df.index)
    else:
        df["article_url"] = ""
else:
    df["article_url"] = ""


# ============================================================
# 7. DASHBOARD - SIDEBAR
# ============================================================

profile = st.session_state.get("user_profile", {})
user_display = profile.get("display_name", "Administrator") if profile else "Administrator"
user_role = profile.get("role", "Lead Researcher") if profile else "Lead Researcher"

with st.sidebar:
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 1rem;">
            <div style="width: 40px; height: 40px; border-radius: 50%; background: linear-gradient(135deg, #a855f7, #6366f1); display: flex; align-items: center; justify-content: center; font-weight: 700; color: white; font-size: 1.2rem;">
                🧠
            </div>
            <div>
                <h3 style="margin: 0; font-size: 1.1rem; color: #f8fafc;">ArticleMind</h3>
                <span style="font-size: 0.75rem; color: #a855f7; font-weight: 600;">AI RESEARCH SUITE</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()

    st.markdown(f"""
        <div style="background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.08); padding: 14px; border-radius: 14px; margin-bottom: 1rem;">
            <p style="margin: 0; font-size: 0.75rem; color: #64748b; text-transform: uppercase; font-weight: 700;">CURRENT USER</p>
            <p style="margin: 2px 0 0 0; font-size: 1rem; font-weight: 700; color: #f8fafc;">{user_display}</p>
            <p style="margin: 0; font-size: 0.8rem; color: #c084fc;">{user_role}</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("**Dataset:** 1,000 Scientific Papers")
    st.markdown("**Engine:** Llama 3.2 via Ollama")
    st.markdown("**Embeddings:** all-MiniLM-L6-v2")

    st.divider()

    if st.button("🚪 Sign Out", use_container_width=True):
        logout()


# ============================================================
# 8. DASHBOARD - MAIN HEADER
# ============================================================

top_col1, top_col2 = st.columns([2, 1])

with top_col1:
    st.markdown("""
        <h1 class="gradient-text" style="font-size: 2.2rem; margin-bottom: 0.2rem;">
            🤖 ArticleMind Research Assistant
        </h1>
        <p style="color: #94a3b8; font-size: 0.95rem; margin-bottom: 1rem;">
            Ask questions from the article knowledge base using semantic retrieval and Llama 3.2.
        </p>
    """, unsafe_allow_html=True)

with top_col2:
    st.markdown(f"""
        <div style="text-align: right; padding-top: 10px;">
            <span class="feature-badge">🟢 Knowledge Base Active</span>
        </div>
    """, unsafe_allow_html=True)

st.divider()


# ============================================================
# 9. DASHBOARD - TWO COLUMN LAYOUT
# ============================================================

left_column, right_column = st.columns([1, 2], gap="large")


# ============================================================
# LEFT COLUMN: ARTICLE SELECTION & SEARCH
# ============================================================

with left_column:
    st.subheader("📚 Article Knowledge Base")

    search_text = st.text_input(
        "🔍 Search article",
        placeholder="Search by article title...",
        key="dashboard_search"
    )

    if search_text.strip():
        filtered_articles = df[
            df["title"]
            .astype(str)
            .str.contains(search_text, case=False, na=False)
        ].copy()
    else:
        filtered_articles = df.copy()

    st.caption(f"Showing {len(filtered_articles)} of {len(df)} articles")
    st.divider()

    # Render article buttons inside a scrollable-like vertical block
    for index, row in filtered_articles.head(50).iterrows():
        title = str(row["title"])
        is_selected = (st.session_state.selected_article == index)
        prefix = "📌 " if is_selected else ""
        
        if st.button(
            f"{prefix}{index + 1}. {title}",
            key=f"article_{index}",
            use_container_width=True
        ):
            st.session_state.selected_article = index
            st.rerun()

    if len(filtered_articles) > 50:
        st.info("ℹ️ Displaying first 50 search matches for quick navigation.")


# ============================================================
# GET SELECTED ARTICLE
# ============================================================

selected_index = st.session_state.selected_article
if selected_index >= len(df):
    selected_index = 0
    st.session_state.selected_article = 0

selected_article = df.iloc[selected_index]
article_title = str(selected_article["title"])
article_description = str(selected_article["description"])
article_url = str(selected_article["article_url"])


# ============================================================
# RIGHT COLUMN: ARTICLE DETAILS, RAG QA, SUMMARIZATION
# ============================================================

with right_column:

    # --------------------------------------------------------
    # SELECTED ARTICLE DISPLAY
    # --------------------------------------------------------
    st.subheader("📄 Selected Article")
    st.markdown(f"### {article_title}")

    if article_url.strip() and article_url.lower() != "nan":
        st.markdown(f"🔗 **[Search / View Article Source]({article_url})**")
    else:
        st.info("ℹ️ No source link available for this article.")

    with st.expander("View full article description", expanded=True):
        st.write(article_description)

    st.divider()

    # --------------------------------------------------------
    # ASK QUESTION (RAG)
    # --------------------------------------------------------
    st.subheader("💬 Ask a Question")
    st.write("Ask a question about the article knowledge base using semantic search and Llama 3.2.")

    question = st.text_input(
        "Your question",
        placeholder="Example: What is the main topic of this article?",
        key="article_question"
    )

    ask_button = st.button(
        "🔎 Ask Question",
        key="ask_question_button",
        use_container_width=True
    )

    if ask_button:
        if not question.strip():
            st.warning("⚠️ Please enter a question first.")
        else:
            with st.spinner("🔎 Searching the vector knowledge base..."):
                results = search_articles(question, top_k=5)

            documents = results.get("documents", [[]])
            documents = documents[0] if documents else []

            if documents:
                with st.spinner("🤖 Llama 3.2 is generating the answer..."):
                    answer = generate_answer(question, documents)

                st.subheader("💡 Answer")
                st.success(answer)

                st.subheader("📚 Retrieved Sources")
                for number, document in enumerate(documents, start=1):
                    with st.expander(f"Source {number}"):
                        st.write(document)
            else:
                st.warning("No relevant information was found in the knowledge base.")

    st.divider()

    # --------------------------------------------------------
    # ARTICLE SUMMARIZATION
    # --------------------------------------------------------
    st.subheader("📝 Article Summarization")
    st.write("Generate a concise 1-2 sentence summary of the selected article using Llama 3.2.")

    summarize_button = st.button(
        "✨ Generate Summary",
        key="summary_button",
        use_container_width=True
    )

    if summarize_button:
        if not article_description.strip() or article_description.lower() == "nan":
            st.warning("⚠️ This article does not have a description to summarize.")
        else:
            with st.spinner("🤖 Llama 3.2 is creating the summary..."):
                summary = summarize_article(article_title, article_description)

            st.subheader("📝 Short Summary")
            st.success(summary)


# ============================================================
# FOOTER
# ============================================================

st.divider()
st.caption("ArticleMind | Semantic Search + RAG + Llama 3.2")