import streamlit as st
import datetime

# --- Page Configuration ---
st.set_page_config(
    page_title="Utah Land & Prop | Private Portal",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS for Private Equity Aesthetic ---
st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background-color: #050505;
        color: #e0e0e0;
    }
    
    /* Custom Font styling */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Gold Accents & Borders */
    .metric-card {
        background-color: #0f0f0f;
        border: 1px solid rgba(212, 175, 55, 0.1);
        padding: 2rem;
        border-radius: 4px;
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        border-color: rgba(212, 175, 55, 0.4);
    }
    .gold-text {
        color: #d4af37;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        font-size: 0.7rem;
    }
    .header-text {
        font-size: 3rem;
        font-weight: 300;
        letter-spacing: -0.02em;
        margin-bottom: 2rem;
    }
    
    /* Sidebar/Nav cleanup */
    section[data-testid="stSidebar"] {
        background-color: #0a0a0a;
    }
    </style>
""", unsafe_allow_html=True)

# --- Authentication Logic (Simple) ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("<p class='gold-text' style='text-align: center;'>Security Protocol Active</p>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; font-weight: 200;'>UTAH LAND & PROP</h1>", unsafe_allow_html=True)
        
        passkey = st.text_input("ENTER ACCESS KEY", type="password")
        if st.button("AUTHORIZE", use_container_width=True):
            if len(passkey) >= 4:
                st.session_state['authenticated'] = True
                st.rerun()
        
        st.markdown("<p style='text-align: center; opacity: 0.3; font-size: 0.6rem; letter-spacing: 0.3em; margin-top: 5rem;'>TIER IV ENCRYPTED ENVIRONMENT</p>", unsafe_allow_html=True)
    st.stop()

# --- Main Dashboard ---
# Top Bar
t1, t2 = st.columns([3, 1])
with t1:
    st.markdown("<p class='gold-text'>Executive Summary</p>", unsafe_allow_html=True)
    st.markdown("<h1 class='header-text'>Portfolio Performance</h1>", unsafe_allow_html=True)
with t2:
    st.markdown(f"<p style='text-align: right; opacity: 0.5; font-size: 0.8rem; margin-top: 2rem;'>{datetime.datetime.now().strftime('%H:%M:%S')} MST</p>", unsafe_allow_html=True)

# Metrics Row
m1, m2, m3 = st.columns(3)
with m1:
    st.markdown("""
        <div class="metric-card">
            <p class="gold-text">Assets Under Management</p>
            <h2 style="font-size: 2.5rem; font-weight: 400;">$24.8M</h2>
            <p style="color: #10b981; font-size: 0.8rem;">+12.4% YTD</p>
        </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown("""
        <div class="metric-card">
            <p class="gold-text">Liquidity Position</p>
            <h2 style="font-size: 2.5rem; font-weight: 400;">$4.2M</h2>
            <p style="color: rgba(255,255,255,0.3); font-size: 0.8rem;">Cash & Equivalents</p>
        </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown("""
        <div class="metric-card">
            <p class="gold-text">Active Holdings</p>
            <h2 style="font-size: 2.5rem; font-weight: 400;">14 Assets</h2>
            <p style="color: rgba(255,255,255,0.3); font-size: 0.8rem;">Summit & Wasatch Co.</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Chart & Activity
c1, c2 = st.columns([2, 1])
with c1:
    st.markdown("<p class='gold-text' style='margin-bottom: 1rem;'>Growth Trajectory</p>", unsafe_allow_html=True)
    # Mock data for chart
    chart_data = [10, 15, 12, 18, 24, 22, 30, 28, 35, 40]
    st.area_chart(chart_data, color="#d4af37")

with c2:
    st.markdown("<p class='gold-text' style='margin-bottom: 1rem;'>Access Logs</p>", unsafe_allow_html=True)
    logs = [
        {"Loc": "Salt Lake City, UT", "Time": "Just Now"},
        {"Loc": "Park City, UT", "Time": "4h ago"},
        {"Loc": "Secure Gateway", "Time": "1d ago"}
    ]
    for log in logs:
        st.markdown(f"""
            <div style="border-bottom: 1px solid rgba(255,255,255,0.05); padding: 0.5rem 0;">
                <p style="margin: 0; font-size: 0.9rem;">{log['Loc']}</p>
                <p style="margin: 0; font-size: 0.7rem; color: #d4af37; opacity: 0.6;">{log['Time']}</p>
            </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("<br><br><br><br>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 2rem;'>", unsafe_allow_html=True)
st.markdown("<p class='gold-text' style='opacity: 0.5;'>Utah Land & Property Private Wealth Management</p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
