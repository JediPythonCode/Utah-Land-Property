import streamlit as st
import datetime

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
    /* Hero Background with the requested Architectural Image */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.4), rgba(99, 29, 51, 0.1)), 
                    url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&q=80&w=2070');
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
        color: #ffffff;
    }
    
    /* Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Montserrat:wght@200;300;400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
    }

    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
    }

    /* Glassmorphism Metric Cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.95);
        border-left: 5px solid #631D33; /* BHHS Cabernet */
        padding: 1.5rem;
        border-radius: 2px;
        color: #333;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    }
    
    .gold-label {
        color: #85714D; /* BHHS Gold */
        letter-spacing: 0.2em;
        text-transform: uppercase;
        font-size: 0.7rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }

    /* Input Styling */
    .stTextInput input {
        background-color: white !important;
        border: none !important;
        border-bottom: 2px solid #631D33 !important;
        color: #333 !important;
        text-align: center;
        border-radius: 0px !important;
    }
    
    .stButton button {
        background-color: #631D33 !important;
        color: white !important;
        border-radius: 0px !important;
        border: none !important;
        letter-spacing: 2px !important;
        font-weight: 600 !important;
        padding: 0.75rem 2rem !important;
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
    _, col2, _ = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
        st.markdown("""
            <div style='background: white; padding: 3rem; text-align: center; box-shadow: 0 20px 50px rgba(0,0,0,0.3);'>
                <p style='color: #631D33; font-family: "Playfair Display"; font-size: 2.5rem; margin-bottom: 0;'>Private Client Access</p>
                <p style='letter-spacing: 3px; font-size: 0.7rem; color: #85714D; margin-bottom: 2rem;'>ASSET VERIFICATION REQUIRED</p>
            </div>
        """, unsafe_allow_html=True)
        
        passkey = st.text_input("", type="password", placeholder="ENTER ACCESS TOKEN")
        if st.button("ENTER SECURE PORTAL", use_container_width=True):
            if len(passkey) >= 4:
                st.session_state['authenticated'] = True
                st.rerun()
    st.stop()

# --- Main Dashboard ---
# Header Section
st.markdown("""
    <div style='display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 3rem; padding-top: 2rem;'>
        <div>
            <p style='letter-spacing: 4px; font-size: 0.75rem; color: #85714D; font-weight: 600; margin:0;'>PORTFOLIO MANAGEMENT</p>
            <h1 style='font-size: 3.5rem; margin:0; line-height: 1;'>Experience Elevated.</h1>
        </div>
        <div style='text-align: right;'>
            <p style='margin:0; font-size: 1.1rem; font-weight: 300;'>Active Portfolio: 4402 S Wasatch Blvd</p>
            <p style='margin:0; font-size: 0.7rem; letter-spacing: 2px; opacity: 0.8;'>SECURE SESSION: ACTIVE</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# Stats Row
m1, m2, m3 = st.columns(3)
with m1:
    st.markdown(f"""
        <div class="metric-card">
            <p class="gold-label">Current Asset Value</p>
            <h2 style="font-size: 2.2rem; margin: 0;">$18,450,000</h2>
            <p style="color: #10b981; font-size: 0.8rem; margin:0;">↑ 4.2% YTD Market Growth</p>
        </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown("""
        <div class="metric-card">
            <p class="gold-label">Equity Position</p>
            <h2 style="font-size: 2.2rem; margin: 0;">$12,100,000</h2>
            <p style="color: #666; font-size: 0.8rem; margin:0;">65.5% Loan-to-Value</p>
        </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown("""
        <div class="metric-card">
            <p class="gold-label">Projected Annual ROI</p>
            <h2 style="font-size: 2.2rem; margin: 0;">8.4%</h2>
            <p style="color: #666; font-size: 0.8rem; margin:0;">Inclusive of short-term yields</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# Main Body
c1, c2 = st.columns([2, 1])
with c1:
    st.markdown("<p style='letter-spacing: 3px; font-size: 0.7rem; color: #85714D; font-weight: 600;'>PORTFOLIO APPRECIATION</p>", unsafe_allow_html=True)
    # Using a list to simulate historical data
    chart_data = [15.2, 15.8, 16.1, 16.0, 16.5, 17.2, 17.8, 18.1, 18.4, 18.45]
    st.line_chart(chart_data, color="#631D33")

with c2:
    st.markdown("<p style='letter-spacing: 3px; font-size: 0.7rem; color: #85714D; font-weight: 600;'>RECENT ACTIVITY</p>", unsafe_allow_html=True)
    activities = [
        ("Feb 02", "Tax Assessment Finalized", "Success"),
        ("Jan 15", "Q4 Yield Distribution", "Processed"),
        ("Jan 02", "Land Title Verification", "Verified"),
        ("Dec 20", "Annual Portfolio Review", "Finalized")
    ]
    for date, desc, status in activities:
        st.markdown(f"""
            <div style="padding: 1rem 0; border-bottom: 1px solid rgba(255,255,255,0.2);">
                <span style="font-size: 0.7rem; opacity: 0.7;">{date}</span><br>
                <div style="display: flex; justify-content: space-between;">
                    <span style="font-weight: 400;">{desc}</span>
                    <span style="font-size: 0.7rem; color: #10b981;">{status}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style='text-align: center; opacity: 0.6;'>
        <p style='letter-spacing: 5px; font-size: 0.6rem;'>UTAH LAND & PROPERTY • LUXURY ASSET MANAGEMENT</p>
    </div>
""", unsafe_allow_html=True)
