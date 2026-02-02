import streamlit as st
import streamlit.components.v1 as components

# Set page configuration for a premium feel
st.set_page_config(
    page_title="Utah Land & Property | Secure Asset Portal",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for high-end branding
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Montserrat:wght@300;400;600&display=swap');
    
    .stApp {
        background-color: #fcfcfc;
    }
    
    .main-title {
        font-family: 'Playfair Display', serif;
        color: #631D33;
        font-size: 3rem;
        margin-bottom: 0;
    }
    
    .sub-title {
        font-family: 'Montserrat', sans-serif;
        letter-spacing: 4px;
        text-transform: uppercase;
        font-size: 0.8rem;
        color: #85714D;
        margin-bottom: 2rem;
    }

    .metric-card {
        background-color: white;
        padding: 2rem;
        border-radius: 4px;
        border-left: 4px solid #631D33;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    .stButton>button {
        background-color: #631D33;
        color: white;
        border-radius: 0;
        width: 100%;
        border: none;
        padding: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #000;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State for Authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# --- LOGIN VIEW ---
if not st.session_state.authenticated:
    # Hero Section
    cols = st.columns([1, 2, 1])
    with cols[1]:
        st.markdown("<div style='text-align: center; margin-top: 100px;'>", unsafe_allow_html=True)
        st.markdown("<h1 class='main-title'>The Gold Standard.</h1>", unsafe_allow_html=True)
        st.markdown("<p class='sub-title'>Utah Land & Property Private Portal</p>", unsafe_allow_html=True)
        
        auth_code = st.text_input("Enter Portfolio Access ID", type="password", help="Enter your secure client ID")
        
        if st.button("Access Portfolio"):
            if auth_code: # You can add specific logic here: if auth_code == "SECRET":
                st.session_state.authenticated = True
                st.session_state.client_id = auth_code.upper()
                st.rerun()
            else:
                st.error("Invalid Access ID")
        st.markdown("</div>", unsafe_allow_html=True)

# --- DASHBOARD VIEW ---
else:
    # Header
    head_l, head_r = st.columns([4, 1])
    with head_l:
        st.markdown(f"<h2 style='font-family: Playfair Display; color: #631D33; margin-bottom:0;'>CLIENT PORTFOLIO</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='letter-spacing: 2px; font-size: 10px; color: #aaa;'>ACCOUNT ID: {st.session_state.client_id}</p>", unsafe_allow_html=True)
    
    with head_r:
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.rerun()

    st.divider()

    # Metrics
    m1, m2, m3 = st.columns(3)
    
    with m1:
        st.markdown("""
            <div class="metric-card">
                <p style="font-size: 10px; letter-spacing: 2px; color: #888; text-transform: uppercase;">Portfolio Valuation</p>
                <h2 style="font-family: Playfair Display; margin: 0;">$12,450,000</h2>
            </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown("""
            <div class="metric-card" style="border-left: 1px solid #eee;">
                <p style="font-size: 10px; letter-spacing: 2px; color: #888; text-transform: uppercase;">Total Acreage</p>
                <h2 style="font-family: Playfair Display; margin: 0;">42.85 AC</h2>
            </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown("""
            <div class="metric-card" style="border-left: 1px solid #eee;">
                <p style="font-size: 10px; letter-spacing: 2px; color: #888; text-transform: uppercase;">Portfolio Status</p>
                <h2 style="font-family: Playfair Display; margin: 0; color: #2ecc71;">ACTIVE</h2>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Content Area
    tab1, tab2 = st.tabs(["Property Overview", "Secure Documents"])
    
    with tab1:
        st.info("Map interface and asset list loading...")
        st.image("https://images.unsplash.com/photo-1506443332154-b1a99b57ad64?auto=format&fit=crop&q=80&w=2070", caption="Zion Vicinity Asset #042")
        
    with tab2:
        st.markdown("""
            <div style="text-align: center; padding: 50px; border: 1px dashed #ccc; background: #fff;">
                <h4 style="font-family: Playfair Display;">Document Vault Locked</h4>
                <p style="color: #666; font-size: 14px;">Detailed legal descriptions and tax assessments are encrypted.<br>Contact your representative for one-time decryption keys.</p>
            </div>
        """, unsafe_allow_html=True)
