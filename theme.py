import streamlit as st

def apply_custom_theme():
    """
    Inject custom CSS into Streamlit for modern glassmorphism styling,
    dark navy & purple gradient background, glowing AI elements,
    custom inputs, and smooth animations.
    """
    custom_css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    /* ============================================================
       GLOBAL COLOR PALETTE & RESET
       ============================================================ */
    :root {
        --bg-gradient: linear-gradient(135deg, #070814 0%, #120b24 45%, #25093e 100%);
        --glass-bg: rgba(255, 255, 255, 0.035);
        --glass-bg-hover: rgba(255, 255, 255, 0.06);
        --glass-border: rgba(255, 255, 255, 0.12);
        --glass-border-focus: rgba(168, 85, 247, 0.6);
        --purple-accent: #a855f7;
        --purple-glow: rgba(168, 85, 247, 0.4);
        --indigo-accent: #6366f1;
        --cyan-accent: #06b6d4;
        --text-primary: #f8fafc;
        --text-secondary: #94a3b8;
        --text-muted: #64748b;
    }

    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background: var(--bg-gradient) !important;
        background-attachment: fixed !important;
        color: var(--text-primary) !important;
    }

    /* Hide default streamlit clutter */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    /* Ambient background glowing orbs */
    [data-testid="stAppViewContainer"]::before {
        content: "";
        position: fixed;
        top: 10%;
        left: 15%;
        width: 350px;
        height: 350px;
        background: radial-gradient(circle, rgba(168, 85, 247, 0.18) 0%, rgba(0,0,0,0) 70%);
        pointer-events: none;
        z-index: 0;
    }

    [data-testid="stAppViewContainer"]::after {
        content: "";
        position: fixed;
        bottom: 15%;
        right: 15%;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(99, 102, 241, 0.15) 0%, rgba(0,0,0,0) 70%);
        pointer-events: none;
        z-index: 0;
    }

    /* ============================================================
       GLASSMORPHISM CONTAINERS & CARDS
       ============================================================ */
    .glass-card {
        background: var(--glass-bg);
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border: 1px solid var(--glass-border);
        border-radius: 24px;
        padding: 2.5rem;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.55), inset 0 1px 0 rgba(255, 255, 255, 0.15);
        transition: all 0.3s ease;
    }

    .glass-card:hover {
        border-color: rgba(168, 85, 247, 0.3);
        box-shadow: 0 25px 60px rgba(0, 0, 0, 0.65), 0 0 30px rgba(168, 85, 247, 0.15);
    }

    .feature-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(168, 85, 247, 0.1);
        border: 1px solid rgba(168, 85, 247, 0.25);
        border-radius: 30px;
        padding: 6px 14px;
        font-size: 0.85rem;
        font-weight: 600;
        color: #d8b4fe;
        margin-right: 8px;
        margin-bottom: 10px;
    }

    .gradient-text {
        background: linear-gradient(135deg, #ffffff 0%, #d8b4fe 50%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }

    .gradient-text-cyan {
        background: linear-gradient(135deg, #a5f3fc 0%, #38bdf8 50%, #818cf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }

    /* ============================================================
       FORM INPUTS & CONTROLS
       ============================================================ */
    div[data-baseweb="input"] {
        background: rgba(15, 17, 35, 0.75) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 14px !important;
        color: var(--text-primary) !important;
        transition: all 0.3s ease !important;
    }

    div[data-baseweb="input"]:focus-within {
        border-color: var(--purple-accent) !important;
        box-shadow: 0 0 20px var(--purple-glow) !important;
        background: rgba(20, 22, 45, 0.9) !important;
    }

    input[type="text"], input[type="password"] {
        color: #f8fafc !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 0.95rem !important;
    }

    input::placeholder {
        color: #64748b !important;
    }

    .stWidgetLabel p {
        color: #cbd5e1 !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        letter-spacing: 0.3px !important;
    }

    /* Checkbox Styling */
    div[data-testid="stCheckbox"] label p {
        color: #94a3b8 !important;
        font-size: 0.88rem !important;
    }

    /* ============================================================
       BUTTONS & HOVER ANIMATIONS
       ============================================================ */
    .stButton button {
        background: linear-gradient(135deg, #7c3aed 0%, #a855f7 50%, #c084fc 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 0.75rem 1.5rem !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        letter-spacing: 0.4px !important;
        box-shadow: 0 8px 25px rgba(124, 58, 237, 0.45) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    .stButton button:hover {
        transform: translateY(-2px) scale(1.01) !important;
        box-shadow: 0 12px 35px rgba(168, 85, 247, 0.65), 0 0 20px rgba(192, 132, 252, 0.4) !important;
        color: #ffffff !important;
    }

    .stButton button:active {
        transform: translateY(0) scale(0.99) !important;
    }

    /* Secondary / Article Action Buttons */
    div[data-testid="stVerticalBlock"] div.stButton > button {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        box-shadow: none !important;
        text-align: left !important;
        justify-content: flex-start !important;
        color: #e2e8f0 !important;
        font-weight: 500 !important;
    }

    div[data-testid="stVerticalBlock"] div.stButton > button:hover {
        background: rgba(168, 85, 247, 0.2) !important;
        border-color: rgba(168, 85, 247, 0.5) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 15px rgba(168, 85, 247, 0.2) !important;
    }

    /* Primary Login Button override */
    .login-btn-wrapper button {
        width: 100% !important;
        padding: 0.85rem 1.5rem !important;
        font-size: 1.05rem !important;
        margin-top: 10px !important;
    }

    /* ============================================================
       SIDEBAR & DASHBOARD STYLING
       ============================================================ */
    [data-testid="stSidebar"] {
        background: rgba(10, 11, 26, 0.85) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
    }

    [data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.025) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 14px !important;
    }

    .stAlert {
        border-radius: 14px !important;
        backdrop-filter: blur(12px) !important;
    }

    /* ============================================================
       RESPONSIVE DESIGN BREAKPOINTS
       ============================================================ */
    @media (max-width: 768px) {
        .glass-card {
            padding: 1.5rem !important;
            border-radius: 18px !important;
        }
        .gradient-text {
            font-size: 1.8rem !important;
        }
        .feature-badge {
            font-size: 0.78rem !important;
            padding: 4px 10px !important;
        }
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
