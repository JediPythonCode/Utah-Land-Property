import streamlit as st
import base64
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# --- 1. CORE SYSTEM CONFIG ---
st.set_page_config(page_title="Utah Land & Property", layout="wide", initial_sidebar_state="collapsed")
st_autorefresh(interval=15000, key="ulp_sync_ping")

# --- 2. PERSISTENT STATE MANAGEMENT (FIXES ADMIN EDITING) ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_role" not in st.session_state:
    st.session_state.user_role = None

# Initialize Deal Values in Session State so edits stick
if "price" not in st.session_state:
    st.session_state.price = 330000.00
if "equity" not in st.session_state:
    st.session_state.equity = 20000.00
if "fee" not in st.session_state:
    st.session_state.fee = 15000.00
if "vault" not in st.session_state:
    st.session_state.vault = []
if "notes" not in st.session_state:
    st.session_state.notes = []
if "deal_id" not in st.session_state:
    st.session_state.deal_id = "DEAL-PRIMARY"

# --- 3. THE CENTERED LOGIN (CSS OVERRIDE) ---
if not st.session_state.authenticated:
    st.markdown("""
        <style>
        @import url("https://fonts.googleapis.com/css2?family=Inter:wght@900&family=Oswald:wght@700&display=swap");
        .stApp { background-color: #FFFFFF !important; }
        header, footer, [data-testid="stHeader"] { display: none !important; }
        
        /* THE SPINE - PERFECT CENTER */
        .login-spine {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            width: 100%;
            margin-top: 15vh;
        }
        .ulp-title {
            font-family: "Inter", sans-serif;
            font-size: clamp(30px, 8vw, 70px);
            font-weight: 900;
            color: #1d428a;
            letter-spacing: -3px;
            text-transform: uppercase;
            margin-bottom: 10px;
        }
        .sync-label {
            font-family: "Oswald", sans-serif;
            font-size: 14px;
            color: #1d428a;
            letter-spacing: 2px;
            margin-bottom: 30px;
        }
        
        /* FORCE WIDGET ALIGNMENT */
        div[data-testid="stVerticalBlock"] > div {
            display: flex;
            justify-content: center;
        }
        .stTextInput, .stButton {
            width: 380px !important;
        }
        button {
            background-color: #1d428a !important;
            color: white !important;
            font-family: "Oswald", sans-serif !important;
            border-radius: 0px !important;
            height: 55px !important;
            width: 100% !important;
            border: 2px solid #1d428a !important;
            text-transform: uppercase !important;
            letter-spacing: 2px !important;
        }
        input {
            text-align: center !important;
            border-radius: 0px !important;
            border: 2px solid #1d428a !important;
            height: 50px !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="login-spine"><div class="ulp-title">Utah Land & Property</div><div class="sync-label">Maximum privacy. Maximum protection.</div></div>', unsafe_allow_html=True)
    
    # Logic to handle centering the actual widgets
    _, col_center, _ = st.columns([1, 1, 1])
    with col_center:
        key = st.text_input("Key", type="password", placeholder="ENTER PRIVATE ACCESS KEY", label_visibility="collapsed")
        if st.button("Secure Access Terminal"):
            try:
                users = st.secrets["users"]
                for u, p in users.items():
                    if key == str(p["key"]):
                        st.session_state.authenticated = True
                        st.session_state.user_role = p["role"]
                        st.rerun()
                st.error("INVALID KEY")
            except: st.error("DATABASE ERROR")
    st.stop()

# --- 4. INTERNAL DASHBOARD ---
st.markdown("""
    <style>
    .ulp-header { font-family: 'Inter'; font-size: 32px; font-weight: 900; color: #1d428a; text-transform: uppercase; margin-bottom: 20px; }
    .hero-box { background: #1d428a; padding: 30px; border-radius: 10px; color: white; }
    .bento { background: #f8fafc; padding: 20px; border-radius: 10px; border: 1px solid #e2e8f0; }
    .label { font-family: 'Oswald'; font-size: 12px; color: #64748b; text-transform: uppercase; letter-spacing: 1px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="ulp-header">Utah Land & Property</div>', unsafe_allow_html=True)

# --- 5. ADMIN COMMAND CENTER (FULLY FUNCTIONAL) ---
if st.session_state.user_role == "admin":
    with st.expander("ADMIN TERMINAL: EDIT DEAL / GENERATE DOCUMENTS", expanded=True):
        a1, a2, a3 = st.columns(3)
        
        # Edit Values
        st.session_state.price = a1.number_input("Purchase Price", value=st.session_state.price)
        st.session_state.equity = a2.number_input("Seller Equity Credit", value=st.session_state.equity)
        st.session_state.fee = a3.number_input("Assignment Fee", value=st.session_state.fee)
        
        # Actions
        b1, b2, b3 = st.columns(3)
        if b1.button("REFRESH DASHBOARD"):
            st.rerun()
            
        if b2.button("GENERATE SETTLEMENT PDF"):
            aitd = st.session_state.price - st.session_state.equity
            doc_text = f"UTAH LAND & PROPERTY SETTLEMENT\nPrice: ${st.session_state.price:,.2f}\nEquity: ${st.session_state.equity:,.2f}\nAITD: ${aitd:,.2f}\nFee: ${st.session_state.fee:,.2f}"
            st.session_state.vault.append({"name": f"Settlement_{datetime.now().strftime('%H%M')}.txt", "content": doc_text})
            st.success("Document added to Vault")

        if b3.button("RESET TO NEW DEAL"):
            st.session_state.price = 330000.0
            st.session_state.equity = 20000.0
            st.session_state.fee = 15000.0
            st.session_state.deal_id = f"DEAL-{datetime.now().strftime('%m%d%H%M')}"
            st.rerun()

# --- 6. LIVE CALCULATIONS ---
aitd_principal = st.session_state.price - st.session_state.equity

c1, c2 = st.columns([2, 1])
with c1:
    st.markdown(f"""
        <div class="hero-box">
            <div class="label" style="color: #cbd5e1;">AITD Principal Balance</div>
            <div style="font-size: 50px; font-weight: 900;">${aitd_principal:,.2f}</div>
            <hr style="opacity: 0.2;">
            <div style="display: flex; justify-content: space-between;">
                <div><div class="label" style="color: #cbd5e1;">Sales Price</div><div style="font-size: 20px;">${st.session_state.price:,.2f}</div></div>
                <div><div class="label" style="color: #cbd5e1;">Seller Equity</div><div style="font-size: 20px;">${st.session_state.equity:,.2f}</div></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
        <div class="bento">
            <div class="label">Assignment Fee</div>
            <div style="font-size: 30px; font-weight: 700; color: #1d428a;">${st.session_state.fee:,.2f}</div>
            <div style="font-size: 11px; margin-top: 10px;">Payable to: Utah Land & Property, LLC</div>
        </div>
    """, unsafe_allow_html=True)

# --- 7. VAULT & NOTES ---
st.markdown("### Transaction Hub")
v1, v2 = st.columns([1, 1])
with v1:
    st.markdown('<div class="label">Document Vault</div>', unsafe_allow_html=True)
    for doc in st.session_state.vault:
        b64 = base64.b64encode(doc['content'].encode()).decode()
        st.markdown(f"📄 {doc['name']} - [Download](data:file/txt;base64,{b64})")

with v2:
    st.markdown('<div class="label">Deal Updates</div>', unsafe_allow_html=True)
    note = st.text_input("Add Note", label_visibility="collapsed")
    if st.button("Post Update") and note:
        st.session_state.notes.insert(0, f"{datetime.now().strftime('%H:%M')}: {note}")
        st.rerun()
    for n in st.session_state.notes:
        st.write(n)

if st.sidebar.button("EXIT SESSION"):
    st.session_state.authenticated = False
    st.rerun()
