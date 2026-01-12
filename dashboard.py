import base64
import numpy_financial as npf
from streamlit_autorefresh import st_autorefresh
import streamlit as st
import io

# --- 1. SECURITY UTILITIES ---
def get_verified_file_type(content):
    if content.startswith(b'%PDF'): return 'pdf'
    if content.startswith(b'\xff\xd8\xff'): return 'jpg'
    if content.startswith(b'\x89PNG\r\n\x1a\n'): return 'png'
    return None

def scan_for_malware(content):
    dangerous = [b"<script", b"eval(", b"exec(", b"system(", b"0x"]
    return not any(p in content.lower() for p in dangerous)

# --- 2. CONFIG ---
st.set_page_config(page_title="Utah Land & Property", layout="wide", initial_sidebar_state="expanded")
st_autorefresh(interval=10000, key="ulp_sync_ping")

# --- 3. SESSION & DATA ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_role" not in st.session_state:
    st.session_state.user_role = None

if "current_deal" not in st.session_state:
    st.session_state.current_deal = {
        "address": "PRIVATE ASSET: UNVETTED", 
        "price": 330000.0, 
        "seller_equity": 20000.0, 
        "assignment_fee": 15000.0, 
        "interest_rate": 6.5, 
        "hoa_monthly": 0.0,
        "vault": [], 
        "property_images": []
    }

D = st.session_state.current_deal

# --- 4. CSS (LOCKED ORIGINAL STYLE) ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=Oswald:wght@500;700&display=swap');
        .stApp { background-color: #ffffff !important; }
        
        /* HEADER BRANDING */
        .main-header { font-family: 'Inter', sans-serif; font-size: 75px; font-weight: 900; color: #1d428a; text-align: center; line-height: 0.8; margin-bottom: 10px; }
        .sub-header { font-family: 'Oswald', sans-serif; font-size: 20px; font-weight: 700; color: #1d428a; text-align: center; text-transform: uppercase; letter-spacing: 3px; margin-bottom: 40px; }
        
        /* TEXT STYLING */
        .blue-label { color: #1d428a !important; font-family: 'Oswald', sans-serif; font-weight: 700; text-transform: uppercase; font-size: 14px; margin-bottom: 5px; display: block; }
        .big-value { color: #1d428a !important; font-family: 'Inter', sans-serif; font-weight: 900; font-size: 38px; line-height: 1; margin-bottom: 20px; display: block; }
        .checklist-item { color: #1d428a !important; font-family: 'Oswald', sans-serif; font-weight: 700; font-size: 18px; margin-bottom: 12px; }
        
        /* BUTTONS */
        div.stButton > button { background-color: #1d428a !important; color: white !important; font-family: 'Oswald', sans-serif !important; font-weight: 700; height: 60px !important; border-radius: 4px; border: none; width: 100%; }
        
        /* FORMS */
        label, [data-testid="stWidgetLabel"] p { color: #1d428a !important; font-weight: 700 !important; font-family: 'Oswald', sans-serif !important; }
    </style>
""", unsafe_allow_html=True)

# --- 5. AUTHENTICATION GATEWAY ---
if not st.session_state.authenticated:
    st.markdown('<div style="height: 10vh;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="main-header">UTAH LAND & PROPERTY</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Asset Protection ● Maximum Privacy ● Anonymous Holdings</div>', unsafe_allow_html=True)
    
    _, col_mid, _ = st.columns([1, 0.4, 1])
    with col_mid:
        access_key = st.text_input("Access Key", type="password", label_visibility="collapsed", placeholder="ENTER KEY")
        if st.button("AUTHORIZE SESSION"):
            if "users" in st.secrets:
                for user, profile in st.secrets["users"].items():
                    if access_key == str(profile["key"]):
                        st.session_state.authenticated = True
                        st.session_state.user_role = str(profile["role"]).lower()
                        st.rerun()
            st.error("INVALID KEY")
    st.stop()

# --- 6. LOGIC & MATH ---
EQ_BUYER_BAL = D["price"] - D["seller_equity"]
REQUIRED_DOCS = ["Government ID", "Proof of Funds", "Bank Statement (Last 2 Mo)", "Purchase Agreement (Signed)"]
uploaded_types = [doc['type'] for doc in D['vault']]

# --- 7. ADMIN TERMINAL ---
if st.session_state.user_role == "admin":
    with st.sidebar:
        st.markdown('<p class="blue-label">Admin Control Panel</p>', unsafe_allow_html=True)
        D["price"] = st.number_input("Sale Price", value=float(D["price"]))
        D["seller_equity"] = st.number_input("Seller Equity", value=float(D["seller_equity"]))
        st.divider()
        st.markdown('<p class="blue-label">Upload Property Images</p>', unsafe_allow_html=True)
        img_up = st.file_uploader("Select Photos", type=['jpg', 'png'], accept_multiple_files=True)
        if st.button("SAVE CHANGES & PHOTOS"):
            if img_up:
                D["property_images"] = [img.getvalue() for img in img_up]
            st.rerun()

# --- 8. DASHBOARD ---
st.markdown('<div class="main-header">UTAH LAND & PROPERTY</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Asset Protection ● Maximum Privacy ● Anonymous Holdings</div>', unsafe_allow_html=True)

# PROPERTY GALLERY (TOP REVEAL)
if D["property_images"]:
    cols = st.columns(len(D["property_images"]) if len(D["property_images"]) < 4 else 4)
    for i, img in enumerate(D["property_images"]):
        cols[i % 4].image(img, use_container_width=True)
    st.divider()

col_left, col_right = st.columns([2, 1], gap="large")

with col_left:
    st.markdown('<span class="blue-label">Sale Price</span>', unsafe_allow_html=True)
    st.markdown(f'<span class="big-value">${D["price"]:,.2f}</span>', unsafe_allow_html=True)
    
    st.markdown('<span class="blue-label">Downpayment (Seller Equity)</span>', unsafe_allow_html=True)
    st.markdown(f'<span class="big-value">${D["seller_equity"]:,.2f}</span>', unsafe_allow_html=True)
    
    st.markdown('<span class="blue-label">Equity Buyer Balance</span>', unsafe_allow_html=True)
    st.markdown(f'<span class="big-value">${EQ_BUYER_BAL:,.2f}</span>', unsafe_allow_html=True)
    
    st.markdown('<span class="blue-label">Assignment Fee</span>', unsafe_allow_html=True)
    st.markdown(f'<span class="big-value">${D["assignment_fee"]:,.2f}</span>', unsafe_allow_html=True)

with col_right:
    st.markdown('<span class="blue-label">Onboarding Tracker</span>', unsafe_allow_html=True)
    completed = sum(1 for req in REQUIRED_DOCS if req in uploaded_types)
    st.progress(completed / len(REQUIRED_DOCS))
    
    for req in REQUIRED_DOCS:
        status = "✅" if req in uploaded_types else "❌"
        st.markdown(f'<div class="checklist-item">{status} {req}</div>', unsafe_allow_html=True)
    
    st.divider()
    
    with st.form("secure_vault_form", clear_on_submit=True):
        st.markdown('<span class="blue-label">Secure Document Upload</span>', unsafe_allow_html=True)
        dtype = st.selectbox("Category", REQUIRED_DOCS)
        file = st.file_uploader("Choose File", type=['pdf','jpg','png'])
        if st.form_submit_button("VALIDATE & SUBMIT"):
            if file:
                fb = file.getvalue()
                if get_verified_file_type(fb) and scan_for_malware(fb):
                    D["vault"].append({"type": dtype, "content": fb})
                    st.rerun()
                else:
                    st.error("Invalid/Unsafe File Structure")

if st.sidebar.button("LOGOUT"):
    st.session_state.authenticated = False
    st.rerun()
