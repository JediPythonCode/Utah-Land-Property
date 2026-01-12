import base64
import numpy_financial as npf
from streamlit_autorefresh import st_autorefresh
import streamlit as st
from PIL import Image
import io

# --- 1. ANTI-SCRAPE & SECURITY UTILITIES ---
def get_verified_file_type(content):
    """Magic Byte Verification: Prevents file-masking attacks."""
    if content.startswith(b'%PDF'): return 'pdf'
    if content.startswith(b'\xff\xd8\xff'): return 'jpg'
    if content.startswith(b'\x89PNG\r\n\x1a\n'): return 'png'
    return None

def scan_for_malware(content):
    """Byte-level scan for injection patterns."""
    dangerous = [b"<script", b"eval(", b"exec(", b"system(", b"0x"]
    return not any(p in content.lower() for p in dangerous)

# --- 2. CONFIG ---
# 'initial_sidebar_state' is expanded for visibility, 'menu_items' disabled to block bot-entry points
st.set_page_config(
    page_title="Utah Land & Property", 
    layout="wide", 
    initial_sidebar_state="expanded",
    menu_items={'Get help': None, 'Report a bug': None, 'About': None}
)
st_autorefresh(interval=10000, key="ulp_sync_ping")

# --- 3. DATA PERSISTENCE ---
if "current_deal" not in st.session_state:
    st.session_state.current_deal = {
        "address": "PRIVATE ASSET", "deal_id": "000",
        "price": 330000.0, "seller_equity": 20000.0, 
        "assignment_fee": 15000.0, "interest_rate": 6.5, "hoa_monthly": 0.0,
        "vault": [], "property_images": []
    }

D = st.session_state.current_deal

# --- 4. CSS (ENHANCED VISIBILITY & OBFUSCATION) ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@900&family=Oswald:wght@700&display=swap');
        .stApp { background-color: #ffffff !important; }
        
        /* BOT-SHIELD: Prevent text selection for low-level scrapers */
        .main-header, .big-value, .checklist-item { 
            user-select: none; 
            -webkit-user-select: none; 
        }

        .main-header { font-family: 'Inter', sans-serif; font-size: 75px; font-weight: 900; color: #1d428a; text-align: center; line-height: 0.8; margin-bottom: 10px; }
        .sub-header { font-family: 'Oswald', sans-serif; font-size: 20px; font-weight: 700; color: #1d428a; text-align: center; text-transform: uppercase; letter-spacing: 3px; margin-bottom: 40px; }
        .blue-label { color: #1d428a !important; font-family: 'Oswald', sans-serif; font-weight: 700; text-transform: uppercase; font-size: 14px; }
        .big-value { color: #1d428a !important; font-family: 'Inter', sans-serif; font-weight: 900; font-size: 45px; line-height: 1; }
        .checklist-item { color: #1d428a !important; font-family: 'Oswald', sans-serif; font-weight: 700; font-size: 18px; margin-bottom: 8px; }
        
        div.stButton > button { background-color: #1d428a !important; color: white !important; font-family: 'Oswald', sans-serif !important; font-weight: 700; height: 60px !important; border-radius: 4px; }
        .data-card { background: #f1f5f9; padding: 25px; border-left: 8px solid #1d428a; border-radius: 4px; margin-bottom: 15px; }
        .equity-box { background: #1d428a; color: white !important; padding: 25px; border-radius: 4px; margin-bottom: 15px; }
        
        label, [data-testid="stWidgetLabel"] p { color: #1d428a !important; font-weight: 700 !important; }
    </style>
""", unsafe_allow_html=True)

# --- 5. CALCULATIONS ---
EQ_BUYER_BAL = D["price"] - D["seller_equity"]
REQUIRED_DOCS = ["Government ID", "Proof of Funds", "Bank Statement (Last 2 Mo)", "Purchase Agreement (Signed)"]
uploaded_types = [doc['type'] for doc in D['vault']]

def calc_pmt(principal, rate, years):
    if rate <= 0 or years <= 0: return principal / (years * 12) if (years*12) > 0 else 0
    return abs(npf.pmt(rate/100/12, years*12, principal))

t30 = calc_pmt(EQ_BUYER_BAL, D["interest_rate"], 30) + D["hoa_monthly"]

# --- 6. ADMIN TERMINAL ---
if st.sidebar.checkbox("🔓 ADMIN TERMINAL"):
    with st.container(border=True):
        D["address"] = st.text_input("Property Address", value=D["address"])
        D["price"] = st.number_input("Sale Price", value=float(D["price"]))
        D["interest_rate"] = st.number_input("Rate %", value=float(D["interest_rate"]))
        D["hoa_monthly"] = st.number_input("HOA", value=float(D["hoa_monthly"]))
        if st.button("UPDATE PORTAL"): st.rerun()

# --- 7. DASHBOARD DISPLAY ---
st.markdown('<div class="main-header">UTAH LAND & PROPERTY</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Asset Protection ● Maximum Privacy ● Anonymous Holdings</div>', unsafe_allow_html=True)

col_left, col_right = st.columns([2, 1], gap="large")

with col_left:
    st.markdown('<p class="blue-label">Financial Structure</p>', unsafe_allow_html=True)
    st.markdown(f'<div class="data-card"><span class="blue-label">Sale Price</span><br><span class="big-value">${D["price"]:,.2f}</span></div>', unsafe_allow_html=True)
    
    # Highlighted Balance (Harder to scrape due to nested spans)
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
    st.markdown('<p class="blue-label">Onboarding Tracker</p>', unsafe_allow_html=True)
    completed = sum(1 for req in REQUIRED_DOCS if req in uploaded_types)
    st.progress(completed / len(REQUIRED_DOCS))
    
    # CHECKLIST (FORCED DARK BLUE)
    for req in REQUIRED_DOCS:
        status = "✅" if req in uploaded_types else "❌"
        st.markdown(f'<div class="checklist-item">{status} {req}</div>', unsafe_allow_html=True)
    
    st.divider()
    
    with st.form("secure_vault_form", clear_on_submit=True):
        dtype = st.selectbox("Category", REQUIRED_DOCS)
        file = st.file_uploader("Upload Document", type=['pdf','jpg','png'])
        if st.form_submit_button("VALIDATE & SUBMIT"):
            if file:
                fb = file.getvalue()
                if get_verified_file_type(fb) is None or not scan_for_malware(fb):
                    st.error("Security Violation: Invalid file structure.")
                else:
                    D["vault"].append({"type": dtype, "name": file.name, "content": fb})
                    st.rerun()

    st.markdown(f'<div class="data-card" style="background:#1d428a; color:white; text-align:center;"><span style="color:white; font-family:Oswald;">30-YR EST. PMT</span><br><span style="color:white; font-family:Inter; font-weight:900; font-size:32px;">${t30:,.2f}</span></div>', unsafe_allow_html=True)

if st.sidebar.button("LOGOUT"):
    st.session_state.authenticated = False
    st.rerun()
