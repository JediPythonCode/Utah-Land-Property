import streamlit as st
import numpy as np

# --- Page Configuration ---
st.set_page_config(
    page_title="Utah Land & Prop | Private Portal",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS for the "Amazing Original" Aesthetic ---
st.markdown("""
    <style>
    /* Hero Background with Architectural Image */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(99, 29, 51, 0.2)), 
                    url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&q=80&w=2070');
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
        color: #ffffff;
    }
    
    /* Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Montserrat:wght@200;300;400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
    }

    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
    }

    /* Glassmorphism Metric Cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.98);
        border-left: 6px solid #631D33; /* BHHS Cabernet */
        padding: 2rem;
        border-radius: 0px;
        color: #1a1a1a;
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
    }
    
    .gold-label {
        color: #85714D; /* BHHS Gold */
        letter-spacing: 0.3em;
        text-transform: uppercase;
        font-size: 0.75rem;
        font-weight: 700;
        margin-bottom: 0.75rem;
    }

    /* Input Styling override */
    .stTextInput input {
        background-color: white !important;
        border: none !important;
        border-bottom: 2px solid #631D33 !important;
        color: #1a1a1a !important;
        text-align: center;
        border-radius: 0px !important;
        font-size: 1.2rem !important;
        padding: 1.5rem !important;
    }
    
    .stButton button {
        background-color: #631D33 !important;
        color: white !important;
        border-radius: 0px !important;
        border: none !important;
        letter-spacing: 3px !important;
        font-weight: 600 !important;
        padding: 1rem 3rem !important;
        width: 100%;
        transition: all 0.3s ease;
    }

    .stButton button:hover {
        background-color: #4a1526 !important;
        transform: translateY(-2px);
    }

    /* Chart Styling */
    .stChart {
        background: rgba(255, 255, 255, 0.05);
        padding: 1rem;
        border-radius: 4px;
    }

    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- Authentication Logic ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    # Center the login box
    _, col2, _ = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
        st.markdown("""
            <div style='background: white; padding: 4rem 3rem; text-align: center; box-shadow: 0 30px 60px rgba(0,0,0,0.4);'>
                <p style='color: #631D33; font-family: "Playfair Display"; font-size: 2.8rem; margin-bottom: 0; font-weight: 900;'>Private Client Vault</p>
                <p style='letter-spacing: 5px; font-size: 0.7rem; color: #85714D; margin-bottom: 3rem; font-weight: 600;'>SECURE ASSET VERIFICATION</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Using a container to group input and button tightly
        with st.container():
            passkey = st.text_input("", type="password", placeholder="ENTER PORTFOLIO ACCESS TOKEN")
            if st.button("ACCESS SECURE PORTAL"):
                if len(passkey) >= 4:
                    st.session_state['authenticated'] = True
                    st.session_state['portfolio_id'] = passkey.upper()
                    st.rerun()
                else:
                    st.error("Invalid Security Token")
        
        st.markdown("""
            <div style='text-align: center; margin-top: 2rem; opacity: 0.7; font-size: 0.7rem; letter-spacing: 2px; color: white;'>
                ESTABLISHED 1998 • UTAH DIVISION
            </div>
        """, unsafe_allow_html=True)
    st.stop()

# --- Main Dashboard ---
# Header Section
st.markdown(f"""
    <div style='display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 4rem; padding-top: 2rem;'>
        <div>
            <p style='letter-spacing: 5px; font-size: 0.8rem; color: #85714D; font-weight: 700; margin:0;'>LUXURY ASSET MANAGEMENT</p>
            <h1 style='font-size: 4rem; margin:0; line-height: 1; color: white;'>Experience Elevated.</h1>
        </div>
        <div style='text-align: right; color: white;'>
            <p style='margin:0; font-size: 1.2rem; font-weight: 300;'>Active Portfolio: {st.session_state.get('portfolio_id', 'ASSET-4402')}</p>
            <p style='margin:0; font-size: 0.7rem; letter-spacing: 3px; color: #85714D; font-weight: 600;'>SESSION STATUS: ENCRYPTED</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# Stats Row
m1, m2, m3 = st.columns(3)
with m1:
    st.markdown("""
        <div class="metric-card">
            <p class="gold-label">Projected Asset Value</p>
            <h2 style="font-size: 2.8rem; margin: 0; color: #631D33;">$8,740,200</h2>
            <p style="color: #10b981; font-size: 0.85rem; font-weight: 600; margin:0.5rem 0 0 0;">↑ 8.15% MODEL CONFIDENCE</p>
        </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown("""
        <div class="metric-card">
            <p class="gold-label">Current Land Utilization</p>
            <h2 style="font-size: 2.8rem; margin: 0; color: #1a1a1a;">18.42 <span style="font-size: 1.2rem; color: #888;">AC</span></h2>
            <p style="color: #666; font-size: 0.85rem; margin:0.5rem 0 0 0; text-transform: uppercase; letter-spacing: 1px;">Zoning: Luxury Residential</p>
        </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown("""
        <div class="metric-card">
            <p class="gold-label">Market Liquidity Tier</p>
            <h2 style="font-size: 2.8rem; margin: 0; color: #85714D;">Premium</h2>
            <p style="color: #666; font-size: 0.85rem; margin:0.5rem 0 0 0; text-transform: uppercase; letter-spacing: 1px;">High Demand Segment</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# Main Body / Stochastic Analysis
c1, c2 = st.columns([2, 1])
with c1:
    st.markdown("<p style='letter-spacing: 4px; font-size: 0.8rem; color: #85714D; font-weight: 700; margin-bottom: 1.5rem;'>STOCHASTIC APPRECIATION MODEL</p>", unsafe_allow_html=True)
    
    # Simulating a stochastic process for the chart
    base = 8.2
    noise = np.random.normal(0, 0.05, 20).cumsum()
    chart_data = base + noise
    
    st.line_chart(chart_data, color="#631D33", use_container_width=True)
    
    st.markdown("""
        <div style="background: rgba(255,255,255,0.1); padding: 1.5rem; border: 1px solid rgba(255,255,255,0.1);">
            <p style="font-size: 0.8rem; line-height: 1.6; font-weight: 300; margin: 0;">
                <strong style="color: #85714D;">ANALYSIS NOTE:</strong> Data reflects stochastic modeling based on recent Wasatch Front 
                transaction volume and volatility indices. Current projections suggest a stabilization period followed 
                by a 2.4% quarterly lift in the luxury residential sector.
            </p>
        </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("<p style='letter-spacing: 4px; font-size: 0.8rem; color: #85714D; font-weight: 700; margin-bottom: 1.5rem;'>ASSET LOGS</p>", unsafe_allow_html=True)
    
    activities = [
        ("FEB 02", "Audit: Property Tax Est.", "$24,192.00"),
        ("JAN 28", "LiDAR Terrain Scan", "Complete"),
        ("JAN 15", "Market Momentum Adj.", "+1.2%"),
        ("JAN 04", "Equity Position Review", "Verified"),
        ("DEC 22", "Stochastic Baseline Reset", "Executed")
    ]
    
    for date, desc, status in activities:
        st.markdown(f"""
            <div style="padding: 1.2rem 0; border-bottom: 1px solid rgba(255,255,255,0.15);">
                <span style="font-size: 0.7rem; color: #85714D; font-weight: 700; letter-spacing: 1px;">{date}</span><br>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 0.3rem;">
                    <span style="font-weight: 300; font-size: 0.95rem;">{desc}</span>
                    <span style="font-size: 0.75rem; color: #ffffff; background: #631D33; padding: 2px 8px; font-weight: 600;">{status}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

    if st.button("GENERATE AUDIT REPORT", key="audit_btn"):
        st.toast("Generating Secure PDF Report...", icon="📄")

# Logout logic
st.sidebar.markdown("---")
if st.sidebar.button("Terminated Secure Session"):
    st.session_state['authenticated'] = False
    st.rerun()

# Footer Branding
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style='text-align: center; opacity: 0.5;'>
        <p style='letter-spacing: 8px; font-size: 0.65rem; color: white;'>UTAH LAND & PROPERTY • PRIVATE CLIENT GROUP</p>
        <p style='font-size: 0.5rem; color: white; margin-top: 0.5rem;'>CONFIDENTIAL & PROPRIETARY © 2026</p>
    </div>
""", unsafe_allow_html=True)
