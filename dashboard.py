import base64
import numpy_financial as npf
from streamlit_autorefresh import st_autorefresh
import streamlit as st
import io

# --- 1. CORE SECURITY UTILITIES ---
def get_verified_file_type(content):
    """Magic Byte Verification: Prevents file-masking attacks."""
    if content.startswith(b'%PDF'): return 'pdf'
    if content.startswith(b'\xff\xd8\xff'): return 'jpg'
    if content.startswith(b'\x89PNG\r\n\x1a\n'): return 'png'
    return None

def scan_for_malware(content):
    """Byte-level scan for malicious code signatures."""
    dangerous = [b"<script", b"eval(", b"exec(", b"system(", b"0x"]
    return not any(p in content.lower() for p in dangerous)

# --- 2. CONFIG ---
st.set_page_config(
    page_title="Utah Land & Property", 
    layout="wide", 
    initial_sidebar_state="expanded"
)
st_autorefresh(interval=10000, key="ulp_sync_ping")

# --- 3. SESSION & DATA PERSISTENCE ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_role = None

if "current_deal" not in st.session_state:
    st.session_state.current_deal = {
        "address": "PRIVATE ASSET: UNVETTED", "deal_id": "ULP-001",
        "price": 330000.0, "seller_equity": 20000.0, 
        "assignment_fee": 15000.0, "interest_rate": 6.5, "hoa_monthly": 0.0,
        "vault": [], "property_images": []
    }

D = st.session_state.current_deal

# --- 4. CSS (LARGE BRANDING & ANTI-SCRAPE) ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@900&family=Oswald:wght@700&display=swap');
        .stApp { background-color: #ffffff !important; }
        
        /* HEADER BRANDING */
        .main-header { font-family: 'Inter', sans-serif; font-size: 75px; font-weight: 900; color: #1d428a; text-align: center; line-height: 0.8; margin-bottom: 10px; user-select: none; }
        .sub-header { font-family: 'Oswald', sans-serif; font-size: 20px; font-weight: 700; color: #1d428a; text-align: center; text-transform: uppercase; letter-spacing: 3px; margin-bottom: 40px; }
        
        /* TEXT VISIBILITY */
        .blue-label { color: #1d428a !important; font-family: 'Oswald', sans-serif; font-weight: 700; text-transform: uppercase; font-size: 14px; }
        .big-value { color: #1d428a !important; font-family: 'Inter', sans-serif; font-weight: 900; font-size: 45px; line-height: 1; user-select: none; }
        .checklist-item { color: #1d428a !important; font-family: 'Oswald', sans-serif; font-weight: 700; font-size: 18px; margin-bottom: 12px; }
        
        /* INTERFACE ELEMENTS */
        div.stButton > button { background-color: #1d428a !important; color: white !important; font-family: 'Oswald', sans-serif !important; font-weight: 700; height: 60px !important; border-radius: 4px; }
        .data-card { background: #f1f5f9; padding: 25px; border-left: 8px solid #1d428a; border-radius: 4px; margin-bottom: 15px; }
        .equity-box { background: #1d428a; color: white !important; padding: 25px; border-radius: 4px; margin-bottom: 15px; }
        
        label, [data-testid="stWidgetLabel"] p { color: #1d428a !important; font-weight: 700 !important; }
    </style>
""", unsafe_allow_html=True)

# --- 5. AUTHENTICATION GATEWAY ---
if not st.session_state.authenticated:
    st.markdown('<div style="height: 10vh;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="main-header">UTAH LAND & PROPERTY</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">SECURE ASSET ACCESS TERMINAL</div>', unsafe_allow_html=True)
    
    _, col_mid, _ = st.columns([1, 0.4, 1])
    with col_mid:
        access_key = st.text_input("Enter Access Key", type="password", label_visibility="collapsed", placeholder="PASSWORD")
        if st.button("AUTHORIZE SESSION"):
            # Matches against Streamlit Secrets
            try:
                for user, profile in st.secrets["users"].items():
                    if access_key == str(profile["key"]):
                        st.session_state.authenticated = True
                        st.session_state.user_role = str(profile["role"]).lower()
                        st.rerun()
                st.error("INVALID KEY")
            except:
                st.error("System configuration error: Secrets missing.")
    st.stop()

# --- 6. LOGIC & MATH ---
EQ_BUYER_BAL = D["price"] - D["seller_equity"]
REQUIRED_DOCS = ["Government ID", "Proof of Funds", "Bank Statement (Last 2 Mo)", "Purchase Agreement (Signed)"]
uploaded_types = [doc['type'] for doc in D['vault']]

def calc_pmt(principal, rate, years):
    if rate <= 0 or years <= 0: return principal / (years * 12) if (years*12) > 0 else 0
    return abs(npf.pmt(rate/100/12, years*12, principal))

t30 = calc_pmt(EQ_BUYER_BAL, D["interest_rate"], 30) + D["hoa_monthly"]

# --- 7. ADMIN TERMINAL (IF AUTHORIZED) ---
if st.session_state.user_role == "admin":
    with st.sidebar:
        st.markdown('<p class="blue-label">Admin Management</p>', unsafe_allow_html=True)
        D["address"] = st.text_input("Property Address", value=D["address"])
        D["price"] = st.number_input("Sale Price", value=float(D["price"]))
        D["seller_equity"] = st.number_input("Seller Equity", value=float(D["seller_equity"]))
        D["interest_rate"] = st.number_input("Rate %", value=float(D["interest_rate"]))
        if st.button("SAVE CHANGES"): st.rerun()
        st.divider()

# --- 8. DASHBOARD ---
st.markdown('<div class="main-header">UTAH LAND & PROPERTY</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Asset Protection ● Maximum Privacy ● Anonymous Holdings</div>', unsafe_allow_html=True)

col_left, col_right = st.columns([2, 1], gap="large")

with col_left:
    st.markdown('<p class="blue-label">Financial Structure</p>', unsafe_allow_html=True)
    st.markdown(f'<div class="data-card"><span class="blue-label">Sale Price</span><br><span class="big-value">${D["price"]:,.2f}</span></div>', unsafe_allow_html=True)
    
    # THE HIGHLIGHTED EQUITY BUYER BALANCE
    st.markdown(f'''
        <div class="equity-box">
            <span style="color:white; font-family:Oswald; font-weight:700;">EQUITY BUYER BALANCE</span><br>
            <span class="big-value" style="color:white !important; font-size:55px;">${EQ_BUYER_BAL:,.2f}</span>
        </div>
    ''', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    c1.markdown(f'<div class="data-card"><span class="blue-label">Downpayment</span><br><span class="big-value">${D["seller_equity"]:,.0f}</span></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="data-card"><span class="blue-label">Assignment Fee</span><br><span class="big-value">${D["assignment_fee"]:,.0f}</span></div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<p class="blue-label">Buyer Onboarding Tracker</p>', unsafe_allow_html=True)
    completed = sum(1 for req in REQUIRED_DOCS if req in uploaded_types)
    st.progress(completed / len(REQUIRED_DOCS))
    
    # CHECKLIST (FORCED DARK BLUE VISIBILITY)
    for req in REQUIRED_DOCS:
        status = "✅" if req in uploaded_types else "❌"
        st.markdown(f'<div class="checklist-item">{status} {req}</div>', unsafe_allow_html=True)
    
    st.divider()
    
    with st.form("secure_vault_form", clear_on_submit=True):
        st.markdown('<p class="blue-label">Secure Document Upload</p>', unsafe_allow_html=True)
        dtype = st.selectbox("Category", REQUIRED_DOCS)
        file = st.file_uploader("Upload PDF, JPG, or PNG", type=['pdf','jpg','png'])
        
        if st.form_submit_button("VALIDATE & SUBMIT"):
            if file:
                fb = file.getvalue()
                if get_verified_file_type(fb) is None or not scan_for_malware(fb):
                    st.error("SECURITY ALERT: Invalid or Malicious File detected.")
                else:
                    D["vault"].append({"type": dtype, "name": file.name, "content": fb})
                    st.success("File Verified.")
                    st.rerun()

if st.sidebar.button("LOGOUT"):
    st.session_state.authenticated = False
    st.rerun()
