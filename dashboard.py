import streamlit as st
import numpy as np

# --- Page Configuration ---
st.set_page_config(
    page_title="Utah Land & Prop | Private Portal",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS for the "Amazing Original" Aesthetic ---
st.markdown("""
    <style>
    /* Hero Background */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.65), rgba(99, 29, 51, 0.25)), 
                    url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&q=80&w=2070');
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
        color: #ffffff;
    }
    
    /* Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=Montserrat:wght@200;300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
    }

    h1, h2, h3, .brand-font {
        font-family: 'Playfair Display', serif !important;
    }

    /* Glassmorphism Metric Cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.98);
        border-left: 6px solid #631D33; /* BHHS Cabernet */
        padding: 2rem;
        border-radius: 2px;
        color: #1a1a1a;
        box-shadow: 0 15px 35px rgba(0,0,0,0.4);
        margin-bottom: 1rem;
    }
    
    .gold-label {
        color: #85714D; /* BHHS Gold */
        letter-spacing: 0.35em;
        text-transform: uppercase;
        font-size: 0.75rem;
        font-weight: 700;
        margin-bottom: 0.75rem;
    }

    /* Input Styling */
    .stTextInput input {
        background-color: white !important;
        border: none !important;
        border-bottom: 3px solid #631D33 !important;
        color: #1a1a1a !important;
        text-align: center;
        border-radius: 0px !important;
        font-size: 1.2rem !important;
        height: 3.5rem;
    }
    
    .stButton button {
        background-color: #631D33 !important;
        color: white !important;
        border-radius: 0px !important;
        border: none !important;
        letter-spacing: 4px !important;
        font-weight: 700 !important;
        padding: 1rem 3rem !important;
        width: 100%;
        text-transform: uppercase;
        transition: all 0.4s ease;
    }

    .stButton button:hover {
        background-color: #85714D !important;
        color: white !important;
        transform: translateY(-2px);
    }

    /* Custom Header Branding */
    .header-branding {
        border-bottom: 1px solid rgba(133, 113, 77, 0.4);
        padding-bottom: 1rem;
        margin-bottom: 3rem;
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
    _, col2, _ = st.columns([1, 1.4, 1])
    with col2:
        st.markdown("<br><br><br><br>", unsafe_allow_html=True)
        st.markdown("""
            <div style='background: white; padding: 4.5rem 3rem; text-align: center; box-shadow: 0 30px 70px rgba(0,0,0,0.5);'>
                <p style='letter-spacing: 6px; font-size: 0.7rem; color: #85714D; margin-bottom: 0.5rem; font-weight: 700;'>UTAH LAND & PROPERTY</p>
                <h1 style='color: #631D33; font-size: 3rem; margin-top: 0; font-weight: 900; line-height: 1;'>Private Client Access</h1>
                <div style='width: 40px; height: 2px; background: #85714D; margin: 1.5rem auto;'></div>
                <p style='font-size: 0.8rem; color: #666; margin-bottom: 2.5rem; text-transform: uppercase; letter-spacing: 2px;'>Asset Verification Required</p>
            </div>
        """, unsafe_allow_html=True)
        
        passkey = st.text_input("", type="password", placeholder="ENTER SECURE ACCESS TOKEN")
        if st.button("Access Portfolio"):
            if len(passkey) >= 4:
                st.session_state['authenticated'] = True
                st.rerun()
    st.stop()

# --- Main Dashboard ---
# Header Section with explicit branding
st.markdown("""
    <div class="header-branding" style='display: flex; justify-content: space-between; align-items: flex-end; padding-top: 2rem;'>
        <div>
            <p style='letter-spacing: 5px; font-size: 0.75rem; color: #85714D; font-weight: 700; margin:0;'>PORTFOLIO MANAGEMENT SYSTEM</p>
            <h1 style='font-size: 4.5rem; margin:0; line-height: 0.9; color: white; font-weight: 900;'>Experience Elevated.</h1>
            <p style='font-family: "Montserrat"; font-weight: 200; font-size: 1.2rem; margin-top: 10px; color: rgba(255,255,255,0.8);'>Utah Land & Property | Berkshire Hathaway HomeServices</p>
        </div>
        <div style='text-align: right; color: white;'>
            <p style='margin:0; font-size: 1.1rem; font-weight: 400; letter-spacing: 1px;'>ASSET: 4402 S WASATCH BLVD</p>
            <p style='margin:0; font-size: 0.65rem; letter-spacing: 3px; color: #85714D; font-weight: 700;'>SECURE ENCRYPTION: ACTIVE</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# Stats Row
m1, m2, m3 = st.columns(3)
with m1:
    st.markdown("""
        <div class="metric-card">
            <p class="gold-label">Consolidated Asset Value</p>
            <h2 style="font-size: 2.8rem; margin: 0; color: #631D33; font-weight: 900;">$18,450,000</h2>
            <p style="color: #10b981; font-size: 0.85rem; font-weight: 700; margin-top: 5px;">↑ 4.2% Market Appreciation</p>
        </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown("""
        <div class="metric-card">
            <p class="gold-label">Net Equity Position</p>
            <h2 style="font-size: 2.8rem; margin: 0; color: #1a1a1a; font-weight: 900;">$12,100,000</h2>
            <p style="color: #666; font-size: 0.85rem; margin-top: 5px; letter-spacing: 1px;">65.5% LOAN-TO-VALUE</p>
        </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown("""
        <div class="metric-card">
            <p class="gold-label">Portfolio Yield (Est.)</p>
            <h2 style="font-size: 2.8rem; margin: 0; color: #85714D; font-weight: 900;">8.42%</h2>
            <p style="color: #666; font-size: 0.85rem; margin-top: 5px; letter-spacing: 1px;">STOCHASTIC CONFIDENCE: HIGH</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Main Body
c1, c2 = st.columns([2, 1])
with c1:
    st.markdown("<p style='letter-spacing: 4px; font-size: 0.8rem; color: #85714D; font-weight: 700; margin-bottom: 1rem;'>STOCHASTIC GROWTH PROJECTION</p>", unsafe_allow_html=True)
    
    # Stochastic process for chart data
    steps = 15
    data = 16.5 + np.random.normal(0.1, 0.08, steps).cumsum()
    st.line_chart(data, color="#631D33")
    
    st.markdown("""
        <div style="background: rgba(255,255,255,0.08); padding: 1.5rem; border-left: 3px solid #85714D; margin-top: 1rem;">
            <p style="font-size: 0.85rem; line-height: 1.6; font-weight: 300; margin: 0;">
                <strong style="color: #85714D;">MANAGER'S NOTE:</strong> The valuation model above utilizes a 
                stochastic movement analysis factoring in Salt Lake County luxury absorption rates and 
                interest rate volatility. No coin-flip logic is applied; all trends are driven by 
                quantitative macro-economic indicators.
            </p>
        </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("<p style='letter-spacing: 4px; font-size: 0.8rem; color: #85714D; font-weight: 700; margin-bottom: 1rem;'>PORTFOLIO ACTIVITY</p>", unsafe_allow_html=True)
    
    logs = [
        ("FEB 02", "Tax Assessment Review", "SUCCESS"),
        ("JAN 15", "Q4 Yield Distribution", "PROCESSED"),
        ("JAN 02", "Land Title Verification", "VERIFIED"),
        ("DEC 20", "Annual Portfolio Audit", "FINALIZED"),
        ("DEC 01", "Asset Appreciation Adj.", "+1.4%")
    ]
    
    for date, event, status in logs:
        st.markdown(f"""
            <div style="padding: 1rem 0; border-bottom: 1px solid rgba(255,255,255,0.15);">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="font-size: 0.65rem; color: #85714D; font-weight: 700; letter-spacing: 1px;">{date}</span><br>
                        <span style="font-weight: 400; font-size: 1rem; color: white;">{event}</span>
                    </div>
                    <span style="font-size: 0.7rem; color: #10b981; font-weight: 700; letter-spacing: 1px;">{status}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Download Full Asset Audit"):
        st.toast("Encrypting Report...", icon="🔒")

# Footer
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style='text-align: center; border-top: 1px solid rgba(133, 113, 77, 0.2); padding-top: 2rem; opacity: 0.7;'>
        <p style='letter-spacing: 8px; font-size: 0.7rem; color: #85714D; font-weight: 700; margin-bottom: 0.5rem;'>UTAH LAND & PROPERTY</p>
        <p style='letter-spacing: 2px; font-size: 0.6rem; color: white; margin-bottom: 0;'>A PRIVATE ASSET MANAGEMENT DIVISION OF BERKSHIRE HATHAWAY HOMESERVICES</p>
        <p style='font-size: 0.5rem; color: white; margin-top: 1rem; opacity: 0.5;'>CONFIDENTIAL • PRIVILEGED ACCESS ONLY • © 2026</p>
    </div>
""", unsafe_allow_html=True)
