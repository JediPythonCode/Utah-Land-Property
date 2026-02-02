import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# --- SETTINGS & THEME ---
st.set_page_config(
    page_title="Utah Land & Property | Private Client Group",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- LUXURY STYLING (CSS INJECTION) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;500;600&family=Inter:wght@100;300;400;600&display=swap');

    /* Global Overrides */
    .stApp {
        background-color: #0a0a0a;
        color: #e0e0e0;
    }
    
    header, [data-testid="stHeader"] {
        background: rgba(0,0,0,0) !important;
    }

    /* Typography */
    h1, h2, h3, .serif {
        font-family: 'Cormorant Garamond', serif !important;
        font-weight: 500 !important;
        letter-spacing: 0.02em !important;
    }
    
    p, div, span {
        font-family: 'Inter', sans-serif !important;
        font-weight: 300;
    }

    /* Custom Header Component */
    .luxury-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 3rem;
    }
    
    .logo-text {
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.8rem;
        color: #d4af37;
        text-transform: uppercase;
        letter-spacing: 4px;
    }

    /* Luxury Cards */
    .stat-card {
        background: linear-gradient(145deg, #111111, #080808);
        padding: 2.5rem;
        border: 1px solid rgba(212, 175, 55, 0.2);
        border-radius: 2px;
        text-align: center;
        transition: all 0.5s ease;
    }
    
    .stat-card:hover {
        border-color: rgba(212, 175, 55, 0.8);
        transform: translateY(-5px);
    }

    .stat-label {
        color: #888;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-size: 0.7rem;
        margin-bottom: 0.5rem;
    }

    .stat-value {
        color: #d4af37;
        font-size: 2.2rem;
        font-family: 'Cormorant Garamond', serif;
    }

    /* Buttons */
    .stButton > button {
        background: transparent !important;
        color: #d4af37 !important;
        border: 1px solid #d4af37 !important;
        border-radius: 0px !important;
        padding: 0.6rem 2rem !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        font-size: 0.8rem !important;
        transition: 0.4s all !important;
        width: 100%;
    }
    
    .stButton > button:hover {
        background: #d4af37 !important;
        color: #000 !important;
    }

    /* Inputs */
    .stTextInput input {
        background-color: transparent !important;
        border: none !important;
        border-bottom: 1px solid #333 !important;
        color: white !important;
        border-radius: 0 !important;
        text-align: center;
    }

    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .hero-overlay {
        height: 60vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        background-image: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.8)), url('https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&q=80&w=2070');
        background-size: cover;
        background-position: center;
        margin-bottom: 4rem;
        border: 1px solid rgba(212, 175, 55, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- UI LOGIC ---
def show_login():
    st.markdown("""
        <div class="hero-overlay">
            <h3 style="letter-spacing: 10px; font-weight: 100; color: #d4af37;">EST. 1998</h3>
            <h1 style="font-size: 4.5rem; margin: 10px 0;">Utah Land & Property</h1>
            <p style="letter-spacing: 3px; color: #aaa;">PRIVATE ASSET MANAGEMENT PORTAL</p>
        </div>
    """, unsafe_allow_html=True)
    
    _, col, _ = st.columns([1, 1, 1])
    with col:
        st.markdown("<br>", unsafe_allow_html=True)
        access_id = st.text_input("CLIENT ACCESS KEY", type="password", placeholder="••••••••")
        if st.button("Authenticate"):
            if access_id:
                st.session_state.logged_in = True
                st.rerun()

def show_dashboard():
    # Top Navigation Bar
    st.markdown("""
        <div class="luxury-nav">
            <div class="logo-text">U L & P</div>
            <div style="letter-spacing: 2px; font-size: 0.7rem; color: #666;">
                SECURE SESSION ACTIVE &nbsp; | &nbsp; """ + datetime.now().strftime("%H:%M") + """
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Main Grid
    st.markdown("<h1 style='font-size: 3rem;'>Portfolio Intelligence</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #888; margin-bottom: 3rem;'>Strategic land acquisitions and asset performance for the current fiscal year.</p>", unsafe_allow_html=True)

    # Key Metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown('<div class="stat-card"><div class="stat-label">Total Asset Value</div><div class="stat-value">$18.4M</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown('<div class="stat-card"><div class="stat-label">Acreage Under Mgmt</div><div class="stat-value">1,240</div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown('<div class="stat-card"><div class="stat-label">Active Listings</div><div class="stat-value">12</div></div>', unsafe_allow_html=True)
    with m4:
        st.markdown('<div class="stat-card"><div class="stat-label">Projected Yield</div><div class="stat-value">8.2%</div></div>', unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Asset Visualization Section
    col_a, col_b = st.columns([2, 1])
    
    with col_a:
        st.markdown("<h3 style='border-left: 2px solid #d4af37; padding-left: 15px;'>Portfolio Allocation</h3>", unsafe_allow_html=True)
        # Professional-looking chart
        chart_data = pd.DataFrame(
            np.random.randn(20, 3),
            columns=['Summit County', 'Wasatch Front', 'Southern Utah']
        ).cumsum()
        st.line_chart(chart_data, height=350)
        
    with col_b:
        st.markdown("<h3 style='border-left: 2px solid #d4af37; padding-left: 15px;'>Asset Status</h3>", unsafe_allow_html=True)
        st.markdown("""
            <div style="background: #111; padding: 1.5rem; border-radius: 4px; border: 1px solid #222;">
                <p style="font-size: 0.8rem; color: #d4af37; margin-bottom: 5px;">RECENT ACTIVITY</p>
                <div style="border-bottom: 1px solid #222; padding: 10px 0;">
                    <span style="color: #eee; font-size: 0.9rem;">Park City Expansion</span><br>
                    <span style="color: #555; font-size: 0.7rem;">Permit Approved • 2h ago</span>
                </div>
                <div style="border-bottom: 1px solid #222; padding: 10px 0;">
                    <span style="color: #eee; font-size: 0.9rem;">Heber Valley Parcel</span><br>
                    <span style="color: #555; font-size: 0.7rem;">Appraisal Updated • 1d ago</span>
                </div>
                <div style="padding: 10px 0; margin-bottom: 20px;">
                    <span style="color: #eee; font-size: 0.9rem;">Moab Commercial</span><br>
                    <span style="color: #555; font-size: 0.7rem;">Under Contract • 3d ago</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Logout System"):
            st.session_state.logged_in = False
            st.rerun()

# --- MAIN RENDER ---
if not st.session_state.logged_in:
    show_login()
else:
    show_dashboard()
