import streamlit as st
from streamlit_autorefresh import st_autorefresh

# --- 1. CONFIG ---
st.set_page_config(
    page_title="Utah Land & Property", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)
st_autorefresh(interval=60000, key="ulp_sync_ping")

# --- 2. BHHS LUXURY CSS ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,900&family=Montserrat:wght@300;400;600&display=swap');
        
        /* BHHS Color Palette */
        :root {
            --bhhs-cabernet: #631D33;
            --bhhs-gold: #85714D;
            --bhhs-grey: #F4F4F4;
            --text-dark: #2D2D2D;
        }

        .stApp {
            background-color: white !important;
            color: var(--text-dark);
        }

        /* Typography */
        h1, h2, h3, .serif {
            font-family: 'Playfair Display', serif !important;
        }
        
        p, div, span, label {
            font-family: 'Montserrat', sans-serif !important;
        }

        /* Top Luxury Bar */
        .luxury-nav {
            background-color: var(--bhhs-cabernet);
            height: 5px;
            width: 100%;
            position: fixed;
            top: 0;
            left: 0;
            z-index: 999;
        }

        /* Hero Section */
        .main-header {
            font-family: 'Playfair Display', serif;
            font-size: 52px;
            font-weight: 700;
            color: var(--bhhs-cabernet);
            text-align: center;
            letter-spacing: -1px;
            margin-top: 50px;
        }

        .sub-header {
            font-family: 'Montserrat', sans-serif;
            font-size: 14px;
            font-weight: 400;
            text-transform: uppercase;
            letter-spacing: 4px;
            color: var(--bhhs-gold);
            text-align: center;
            margin-bottom: 60px;
        }

        /* Property Card */
        .prop-card {
            border: 1px solid #E0E0E0;
            padding: 40px;
            border-radius: 0px; /* BHHS uses sharp corners for luxury */
            background: white;
            box-shadow: 0 4px 20px rgba(0,0,0,0.05);
            margin-bottom: 25px;
        }

        .label-gold {
            color: var(--bhhs-gold);
            font-weight: 600;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 8px;
        }

        .price-display {
            font-family: 'Playfair Display', serif;
            font-size: 48px;
            color: var(--bhhs-cabernet);
            font-weight: 700;
        }

        /* Buttons */
        div.stButton > button {
            background-color: var(--bhhs-cabernet) !important;
            color: white !important;
            border-radius: 0px !important;
            border: none !important;
            font-family: 'Montserrat', sans-serif !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 2px !important;
            padding: 20px !important;
            height: auto !important;
            transition: 0.3s all;
        }

        div.stButton > button:hover {
            background-color: #4a1526 !important;
            box-shadow: 0 4px 12px rgba(99, 29, 51, 0.3);
        }

        /* Form Inputs */
        .stTextInput input {
            border-radius: 0px !important;
            border: 1px solid #CCC !important;
            padding: 12px !important;
        }

        /* Sidebar Customization */
        [data-testid="stSidebar"] {
            background-color: var(--bhhs-grey);
            border-right: 1px solid #E0E0E0;
        }

        hr {
            border-top: 1px solid #E0E0E0;
        }
    </style>
    <div class="luxury-nav"></div>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

D = {
    "address": "4402 SOUTH WASATCH BLVD, SALT LAKE CITY",
    "price": 330000.0,
    "equity": 20000.0,
    "fee": 15000.0,
}

# --- 4. LOGIN INTERFACE ---
if not st.session_state.authenticated:
    st.markdown('<div style="height: 10vh;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="main-header">Utah Land & Property</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">A Member of the Luxury Collection</div>', unsafe_allow_html=True)
    
    _, col_mid, _ = st.columns([1, 0.5, 1])
    with col_mid:
        key = st.text_input("CLIENT ACCESS KEY", type="password")
        if st.button("ENTER PORTAL"):
            st.session_state.authenticated = True
            st.rerun()
    st.stop()

# --- 5. DASHBOARD ---
st.markdown('<div class="main-header">Utah Land & Property</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Exclusive Asset Portfolio</div>', unsafe_allow_html=True)

col_info, col_assets = st.columns([1.5, 1], gap="large")

with col_info:
    st.markdown(f"""
        <div class="prop-card">
            <div class="label-gold">Current Offering</div>
            <h2 class="serif" style="margin-top:0;">{D["address"]}</h2>
            <hr>
            <div style="display: flex; justify-content: space-between; margin-top: 20px;">
                <div>
                    <div class="label-gold">Listing Price</div>
                    <div class="price-display">${D["price"]:,.0f}</div>
                </div>
                <div style="text-align: right;">
                    <div class="label-gold">Property Status</div>
                    <div style="font-weight: 600; color: #27ae60;">ACTIVE / PRIVATE</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
            <div class="prop-card" style="padding: 25px;">
                <div class="label-gold">Seller Equity</div>
                <div class="serif" style="font-size: 28px; color: var(--bhhs-cabernet);">${D["equity"]:,.0f}</div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
            <div class="prop-card" style="padding: 25px;">
                <div class="label-gold">Assignment Fee</div>
                <div class="serif" style="font-size: 28px; color: var(--bhhs-cabernet);">${D["fee"]:,.0f}</div>
            </div>
        """, unsafe_allow_html=True)

with col_assets:
    st.markdown('<div class="label-gold" style="margin-bottom:20px;">Secure Client Documents</div>', unsafe_allow_html=True)
    
    # Checkbox style list
    for item in ["Government Identification", "Verification of Funds", "Purchase Addendum"]:
        st.markdown(f"""
            <div style="padding: 15px; border-bottom: 1px solid #EEE; display: flex; align-items: center;">
                <span style="color: var(--bhhs-cabernet); margin-right: 15px;">◈</span>
                <span style="font-size: 13px; font-weight: 400;">{item}</span>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    with st.container():
        st.file_uploader("Upload Document", label_visibility="collapsed")
        st.button("SUBMIT TO VAULT")

st.sidebar.markdown('<div class="label-gold">Session Management</div>', unsafe_allow_html=True)
if st.sidebar.button("LOGOUT"):
    st.session_state.authenticated = False
    st.rerun()
