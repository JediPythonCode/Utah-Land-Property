import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import pandas as pd
import os

# --- LOGIC STACK IMPORTS ---
try:
    from library import SHIELD_LIBRARY
    from automation_engine import generate_utah_addendum
except ImportError:
    SHIELD_LIBRARY = {"System": "Library not found"}
    def generate_utah_addendum(*args): return "Engine Not Found"

# 1. PAGE CONFIG
st.set_page_config(
    page_title="Utah Land & Property | Secure Asset Portal",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. BRANDING CSS (This keeps the look without leaking text)
st.markdown("""
    <style>
        #MainMenu, footer, header {visibility: hidden;}
        .block-container {padding: 0;}
        [data-testid="stAppViewContainer"] { background-color: #fcfcfc; }
        
        /* Cabernet Styling */
        .stMultiSelect [data-baseweb="tag"] { background-color: #631D33 !important; }
        .stButton>button { 
            background-color: #631D33; color: white; border-radius: 0px; 
            border: none; text-transform: uppercase; letter-spacing: 2px; width: 100%;
            height: 3.5rem; font-weight: 600;
        }
        .stButton>button:hover { background-color: #85714D; color: white; }
        
        /* Hero Styling */
        .hero-title { font-family: 'Playfair Display', serif; font-size: 4rem; font-weight: 700; color: white; }
        .disclaimer-box { font-size: 10px; color: #666; text-transform: uppercase; letter-spacing: 1px; padding: 20px; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# 3. SESSION STATE
if 'vault_access' not in st.session_state:
    st.session_state.vault_access = False

# 4. THE FRONT DOOR (Your Original Hero Format)
if not st.session_state.vault_access:
    # We use a cleaner HTML injection to prevent "Leaking"
    html_hero = """
    <div style="height:100vh; display:flex; flex-direction:column; align-items:center; justify-content:center; background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?q=80&w=2070'); background-size:cover; text-align:center; color:white;">
        <div style="font-family:serif; letter-spacing:2px; margin-bottom:10px;">UTAH LAND & PROPERTY</div>
        <h1 style="font-family:serif; font-size: 4rem; margin-bottom: 0;">Precision Acquisition.</h1>
        <p style="letter-spacing:6px; font-size:0.8rem; text-transform:uppercase; margin-bottom:40px;">The Gold Standard in Utah Land Asset Strategy.</p>
        <div style="font-size:10px; text-transform:uppercase; opacity:0.7; max-width:500px;">
            Notice: Utah Land & Property Inc. is a private investment firm and is not a licensed Real Estate Broker or Agent.
        </div>
    </div>
    """
    components.html(html_hero, height=600)
    
    # Sidebar Access (The "Vault Door")
    with st.sidebar:
        st.markdown("### Secure Entry")
        token = st.text_input("Acquisition ID", type="password")
        if st.button("Access Portal"):
            if len(token) > 0:
                st.session_state.vault_access = True
                st.rerun()

# 5. THE DASHBOARD (The "Winner" UI)
else:
    st.markdown("<div style='padding: 40px 60px;'>", unsafe_allow_html=True)
    
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("<h1 style='font-family:serif; color:#631D33;'>PRIVATE CLIENT PORTFOLIO</h1>", unsafe_allow_html=True)
        st.markdown("<p style='letter-spacing:4px; font-size:10px; color:#999;'>STOCHASTIC MODEL: ACTIVE</p>", unsafe_allow_html=True)
    with col2:
        if st.button("Close Vault"):
            st.session_state.vault_access = False
            st.rerun()

    st.divider()

    # Metric Grid
    m1, m2, m3 = st.columns(3)
    m1.metric("Projected Asset Value", "$8,740,200", "Stochastic Premium")
    m2.metric("Land Utilization", "18.42 AC", "Institutional")
    m3.metric("Equity Stability", "94%", "High Confidence")

    # The Engine
    col_viz, col_eng = st.columns([1.5, 1])

    with col_viz:
        st.markdown("<h3 style='font-family:serif;'>Stochastic Trajectory</h3>", unsafe_allow_html=True)
        chart_data = pd.DataFrame(np.random.randn(20, 2) / [15, 25] + [8.74, 8.80], columns=['A', 'B'])
        st.line_chart(chart_data)

    with col_eng:
        st.markdown("<h3 style='font-family:serif;'>Shield Configuration</h3>", unsafe_allow_html=True)
        with st.form("contract_form"):
            seller = st.text_input("Seller Entity Name", value="Owen")
            shields = st.multiselect("Select Active Shields:", list(SHIELD_LIBRARY.keys()), default=["FinCEN_2026", "Legacy_Unit_SNDA"] if "FinCEN_2026" in SHIELD_LIBRARY else [])
            
            if st.form_submit_button("EXECUTE SECURE ADDENDUM"):
                deal = {"seller": seller, "address": "Draper, UT", "addendum_no": "1"}
                result = generate_utah_addendum(deal, shields)
                
                if os.path.exists(result):
                    st.success("Addendum Generated.")
                    with open(result, "rb") as f:
                        st.download_button("Download PDF", f, file_name=f"{seller}_Addendum.pdf")
                else:
                    st.error("Engine Error: Check template.")

    # Footer Disclaimer
    st.markdown("""
        <div class="disclaimer-box">
            Utah Land & Property Inc. is a private investment firm and is not a licensed Real Estate Broker or Agent.
            We do not represent third parties in the sale or purchase of real estate.
        </div>
    """, unsafe_allow_html=True)
