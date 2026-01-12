import base64
import numpy_financial as npf
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
import streamlit as st

# --- 1. CONFIG ---
st.set_page_config(page_title="Utah Land & Property", layout="wide", initial_sidebar_state="expanded")
st_autorefresh(interval=10000, key="ulp_sync_ping")

# --- 2. DATA PERSISTENCE ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_role = None
    st.session_state.verified_by_admin = False

if "current_deal" not in st.session_state:
    st.session_state.current_deal = {
        "deal_id": "", "address": "", 
        "price": 330000.00, "seller_equity": 20000.00, "assignment_fee": 15000.00,  
        "interest_rate": 0.0, "hoa_monthly": 0.0,
        "instr_title": "", "instr_escrow": "", "instr_servicer": "",
        "vault": [], "property_images": []
    }

D = st.session_state.current_deal

# --- 3. STYLING ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=Oswald:wght@500;700&display=swap');
        .stApp { background-color: #ffffff !important; }
        .blue-text { color: #1d428a !important; font-family: 'Oswald', sans-serif; font-weight: 700; text-transform: uppercase; }
        .big-value { color: #1d428a !important; font-family: 'Inter', sans-serif; font-weight: 900; font-size: 38px; line-height: 1; }
        div.stButton > button { background-color: #1d428a !important; color: white !important; font-family: 'Oswald', sans-serif !important; font-weight: 700; text-transform: uppercase; height: 50px !important; width: 100% !important; }
        .data-card { background: #f1f5f9; padding: 20px; border-left: 6px solid #1d428a; border-radius: 4px; margin-bottom: 15px; }
        .pmt-box { background: #1d428a; color: white !important; padding: 25px; border-radius: 4px; text-align: center; }
        .progress-text { font-family: 'Oswald', sans-serif; font-size: 12px; color: #1d428a; margin-bottom: 5px; }
    </style>
""", unsafe_allow_html=True)

# --- 4. AUTH PAGE ---
if not st.session_state.authenticated:
    st.markdown('<div style="height: 10vh;"></div><h1 style="text-align:center; color:#1d428a; font-family:Inter; font-weight:900; font-size:60px; line-height:0.9;">UTAH LAND & PROPERTY</h1>', unsafe_allow_html=True)
    _, col_mid, _ = st.columns([1, 0.4, 1])
    with col_mid:
        key = st.text_input("Access Key", type="password", placeholder="ENTER KEY", label_visibility="collapsed")
        if st.button("AUTHORIZE"):
            for user, profile in st.secrets["users"].items():
                if key == str(profile["key"]):
                    st.session_state.authenticated, st.session_state.user_role = True, str(profile["role"]).lower()
                    st.rerun()
    st.stop()

# --- 5. LOGIC & PROGRESS ---
EQ_BUYER_BAL = D["price"] - D["seller_equity"]
REQUIRED_DOCS = ["Government ID", "Proof of Funds", "Bank Statement (Last 2 Mo)", "Purchase Agreement (Signed)"]
uploaded_names = [doc['type'] for doc in D['vault']]
completed = sum(1 for req in REQUIRED_DOCS if req in uploaded_names)
progress_perc = completed / len(REQUIRED_DOCS)

def calc_pmt(principal, rate, years):
    if rate <= 0 or years <= 0: return principal / (years * 12) if (years*12) > 0 else 0
    return abs(npf.pmt(rate/100/12, years*12, principal))

t15 = calc_pmt(EQ_BUYER_BAL, D["interest_rate"], 15) + D["hoa_monthly"]
t30 = calc_pmt(EQ_BUYER_BAL, D["interest_rate"], 30) + D["hoa_monthly"]

# --- 6. ADMIN PANEL ---
if st.session_state.user_role == "admin":
    st.markdown('<h2 class="blue-text">ADMIN: PROPERTY & DOC MANAGEMENT</h2>', unsafe_allow_html=True)
    
    with st.expander("📸 PROPERTY IMAGES GALLERY", expanded=False):
        img_up = st.file_uploader("Upload Property Photos", type=['jpg','png','jpeg'], accept_multiple_files=True)
        if st.button("Save Photos"):
            for img in img_up:
                D["property_images"].append({"name": img.name, "content": img.getvalue()})
            st.rerun()
        if D["property_images"]:
            for idx, img in enumerate(D["property_images"]):
                st.image(img["content"], width=200, caption=img["name"])
                if st.button(f"Remove Photo {idx}"): D["property_images"].pop(idx); st.rerun()

    with st.container(border=True):
        st.markdown('<p class="blue-text">MANUAL DATA ENTRY</p>', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        D["address"] = c1.text_input("Address", value=D["address"])
        D["deal_id"] = c2.text_input("Deal ID", value=D["deal_id"])
        D["interest_rate"] = c3.number_input("Rate %", value=float(D["interest_rate"]))
        D["hoa_monthly"] = c4.number_input("HOA", value=float(D["hoa_monthly"]))
        
        f1, f2, f3 = st.columns(3)
        D["price"] = f1.number_input("Sale Price", value=float(D["price"]))
        D["seller_equity"] = f2.number_input("Downpayment (Equity)", value=float(D["seller_equity"]))
        D["assignment_fee"] = f3.number_input("Assignment Fee", value=float(D["assignment_fee"]))
        
        if st.button("UPDATE PORTAL DATA"): st.rerun()
        if st.button("✅ REVEAL TO BUYER"): st.session_state.verified_by_admin = True; st.rerun()

# --- 7. BUYER PORTAL ---
st.markdown("---")
show = st.session_state.user_role == "admin" or st.session_state.verified_by_admin

# Progress Bar
st.markdown(f'<p class="progress-text">BUYER ONBOARDING PROGRESS: {completed}/{len(REQUIRED_DOCS)} DOCUMENTS</p>', unsafe_allow_html=True)
st.progress(progress_perc)

if show:
    st.markdown(f'<h1 class="blue-text">{D["address"]}</h1>', unsafe_allow_html=True)
    if D["property_images"]:
        cols = st.columns(3)
        for i, img in enumerate(D["property_images"]):
            cols[i % 3].image(img["content"], use_container_width=True)

col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown('<p class="blue-text">FINANCIAL SUMMARY</p>', unsafe_allow_html=True)
    st.markdown(f'<div class="data-card"><span class="blue-text">Sale Price</span><br><span class="big-value">${D["price"]:,.2f}</span></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="data-card" style="background:#1d428a;"><span style="color:white; font-family:Oswald; font-weight:700;">EQUITY BUYER BALANCE</span><br><span style="color:white; font-family:Inter; font-weight:900; font-size:38px;">${EQ_BUYER_BAL:,.2f}</span></div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<p class="blue-text">DOCUMENT UPLOAD CENTER</p>', unsafe_allow_html=True)
    with st.form("vault_upload"):
        doc_type = st.selectbox("Select Document Type", REQUIRED_DOCS)
        file = st.file_uploader("Upload File", type=['pdf','jpg','png'])
        if st.form_submit_button("UPLOAD TO SETTLEMENT VAULT"):
            if file:
                D["vault"].append({"type": doc_type, "name": file.name, "content": file.getvalue()})
                st.rerun()

    # Checklist Display
    for req in REQUIRED_DOCS:
        status = "✅" if req in uploaded_names else "❌"
        st.markdown(f"**{status} {req}**")

if st.sidebar.button("LOGOUT"): st.session_state.authenticated = False; st.rerun()
