import base64
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
import streamlit as st
from PIL import Image

# --- 1. CONFIG & REFRESH ---
st.set_page_config(page_title="Utah Land & Property", layout="wide", initial_sidebar_state="collapsed")
st_autorefresh(interval=10000, key="ulp_sync_ping")

# --- 2. DATA PERSISTENCE ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_role = None

if "current_deal" not in st.session_state:
    st.session_state.current_deal = {
        "deal_id": "DEAL-PRIMARY",
        "address": "4646 S Quail Park Drive #C, Millcreek Utah 84117",
        "seller_name": "John Doe",
        "buyer_name": "Jane Smith",
        "price": 330000.00,
        "seller_equity": 20000.00,
        "assignment_fee": 15000.00,
        "instr_title": "Standard Title Search Required.", 
        "instr_escrow": "Hold Earnest Money in neutral account.", 
        "instr_servicer": "AITD Servicing setup through [Company Name].",
        "disclosures": ["Property sold As-Is."],
        "vault": [], "images": []
    }

# --- 3. THE "DEEP CLEAN" CSS (Hiding Streamlit/GitHub & Branding) ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=Oswald:wght@500;700&display=swap');
        
        /* HIDE STREAMLIT BRANDING */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display:none;}
        [data-testid="stHeader"] {background: rgba(0,0,0,0);}
        
        .stApp { background-color: #ffffff !important; }

        /* Auth UI Components */
        .branding-text { color: #1d428a !important; font-family: 'Oswald', sans-serif; font-weight: 700; font-size: 18px; text-transform: uppercase; letter-spacing: 1.5px; display: inline-block; vertical-align: middle; }
        .blink-indicator { height: 12px; width: 12px; background-color: #00ff00; border-radius: 50%; display: inline-block; margin-right: 12px; vertical-align: middle; box-shadow: 0 0 10px #00ff00; animation: blink 1.2s infinite; }
        @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.2; } 100% { opacity: 1; } }

        /* Button & Input Geometry */
        div.stButton > button { background-color: #1d428a !important; color: white !important; border: 2px solid #1d428a !important; border-radius: 4px !important; height: 56px !important; width: 100% !important; font-family: 'Oswald', sans-serif !important; font-weight: 700 !important; text-transform: uppercase !important; }
        [data-testid="stTextInput"] input { height: 56px !important; background-color: #1d428a !important; border: 2px solid #1d428a !important; border-radius: 4px !important; text-align: center !important; font-size: 18px !important; font-weight: 700 !important; color: white !important; }

        /* Classy Buyer Dashboard Elements */
        .buyer-card { background: #f8fafc; padding: 25px; border-radius: 10px; border: 1px solid #e2e8f0; margin-bottom: 20px; }
        .buyer-label { font-family: 'Oswald', sans-serif; color: #64748b; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; }
        .buyer-value { font-family: 'Inter', sans-serif; color: #1d428a; font-size: 24px; font-weight: 900; }
        
        /* Admin Elements */
        .admin-header-bar { background-color: #1d428a; color: white !important; padding: 16px; text-align: center; border-radius: 4px; font-family: 'Inter', sans-serif; font-weight: 900; font-size: 22px; text-transform: uppercase; margin-bottom: 30px; }
        .admin-label { font-family: 'Oswald', sans-serif !important; color: #1d428a !important; font-weight: 700 !important; text-transform: uppercase !important; font-size: 13px !important; display: block; margin-top: 15px; }
    </style>
""", unsafe_allow_html=True)

# --- 4. AUTH PAGE ---
if not st.session_state.authenticated:
    st.markdown('<div style="height: 15vh;"></div><div style="font-family:Inter; font-size:clamp(40px, 10vw, 75px); font-weight:900; color:#1d428a; text-align:center; line-height:0.9; margin-bottom:15px;">UTAH LAND & PROPERTY</div>', unsafe_allow_html=True)
    st.markdown('<div class="branding-container" style="text-align:center;"><span class="blink-indicator"></span><span class="branding-text">Asset protection ● Maximum privacy ● Anonymous holdings</span></div>', unsafe_allow_html=True)
    
    _, col_mid, _ = st.columns([1, 0.45, 1])
    with col_mid:
        input_key = st.text_input("Access Key", type="password", placeholder="ENTER ACCESS KEY", label_visibility="collapsed")
        st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
        if st.button("Authorize Session"):
            # Check Admin or Buyer keys in secrets
            try:
                for user, profile in st.secrets["users"].items():
                    if input_key == str(profile["key"]):
                        st.session_state.authenticated = True
                        st.session_state.user_role = str(profile["role"]).lower()
                        st.rerun()
                st.error("ACCESS DENIED")
            except: st.error("Config Error")
    st.stop()

# --- 5. DATA SYNC ---
role = st.session_state.user_role
D = st.session_state.current_deal
AITD_BAL = D["price"] - D["seller_equity"]

# --- 6. ADMIN TERMINAL ---
if role == "admin":
    st.markdown('<div class="admin-header-bar">ADMIN: STRATEGIC DEAL JACKET</div>', unsafe_allow_html=True)
    
    with st.expander("Property Details & Financials", expanded=True):
        c1, c2 = st.columns(2)
        D["address"] = c1.text_input("Address", value=D["address"])
        D["deal_id"] = c2.text_input("Deal ID", value=D["deal_id"])
        f1, f2, f3 = st.columns(3)
        D["price"] = f1.number_input("Contract Price", value=float(D["price"]))
        D["seller_equity"] = f2.number_input("Seller Equity Credit", value=float(D["seller_equity"]))
        D["assignment_fee"] = f3.number_input("Assignment Fee", value=float(D["assignment_fee"]))

    with st.expander("Media Vault: Property Gallery"):
        uploaded_files = st.file_uploader("Upload Property Images", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])
        if uploaded_files:
            D["images"] = [Image.open(x) for x in uploaded_files]

    if st.button("UPDATE MASTER DASHBOARD"):
        st.success("Deal Updated Successfully")
        st.rerun()

# --- 7. BUYER PERSPECTIVE PORTAL (Classy Presentation) ---
if role == "buyer" or role == "admin":
    if role == "buyer":
        st.markdown(f'<div style="font-family:Inter; font-size:42px; font-weight:900; color:#1d428a; margin-bottom:5px;">EXECUTIVE SUMMARY</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="font-family:Oswald; font-size:18px; color:#64748b; margin-bottom:30px;">{D["address"]}</div>', unsafe_allow_html=True)

    # Image Gallery
    if D["images"]:
        st.markdown('<div style="font-family:Oswald; font-size:14px; color:#1d428a; margin-bottom:10px;">PROPERTY GALLERY</div>', unsafe_allow_html=True)
        cols = st.columns(3)
        for idx, img in enumerate(D["images"]):
            cols[idx % 3].image(img, use_container_width=True)

    # Financial presentation
    st.markdown("---")
    b1, b2, b3 = st.columns(3)
    b1.markdown(f'<div class="buyer-card"><div class="buyer-label">Contract Price</div><div class="buyer-value">${D["price"]:,.2f}</div></div>', unsafe_allow_html=True)
    b2.markdown(f'<div class="buyer-card"><div class="buyer-label">Seller Equity Credit</div><div class="buyer-value">${D["seller_equity"]:,.2f}</div></div>', unsafe_allow_html=True)
    b3.markdown(f'<div class="buyer-card" style="background:#1d428a; color:white;"><div class="buyer-label" style="color:rgba(255,255,255,0.7)">AITD Principal</div><div class="buyer-value" style="color:white;">${AITD_BAL:,.2f}</div></div>', unsafe_allow_html=True)

    # Disclosures & Instructions
    st.markdown('<div style="font-family:Oswald; font-size:14px; color:#1d428a;">STRATEGIC DISCLOSURES</div>', unsafe_allow_html=True)
    for disc in D["disclosures"]:
        if disc:
            st.info(f"✔️ {disc}")

# --- 8. LOGOUT ---
if st.sidebar.button("Terminiate Session"):
    st.session_state.authenticated = False
    st.rerun()
