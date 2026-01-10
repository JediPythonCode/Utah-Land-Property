import base64
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
import streamlit as st

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
        "price": 330000.00,
        "seller_equity": 20000.00,
        "assignment_fee": 15000.00,
        "vault": [],
        "notes": []
    }

# --- 3. THE FIXED & CENTERED AUTHENTICATION ---
if not st.session_state.authenticated:
    st.markdown("""
        <style>
        @import url("https://fonts.googleapis.com/css2?family=Inter:wght@900&family=Oswald:wght@700&display=swap");
        
        /* Forces the entire app content to center perfectly */
        [data-testid="stAppViewBlockContainer"] {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            min-height: 90vh;
        }

        .ulp-auth-title { 
            font-family: "Inter", sans-serif; 
            font-size: clamp(32px, 8vw, 60px); 
            font-weight: 900; 
            color: #1d428a; 
            letter-spacing: -2px; 
            text-transform: uppercase;
            text-align: center;
            margin-bottom: 20px;
        }
        
        .sync-label { 
            font-family: "Oswald", sans-serif; 
            font-size: 14px; 
            color: #1d428a; 
            letter-spacing: 2px; 
            font-weight: bold; 
            text-transform: uppercase;
            text-align: center;
            margin-bottom: 40px;
        }

        /* Styling the button and input to be a specific width */
        div.stButton > button {
            background-color: #1d428a !important;
            color: white !important;
            font-family: 'Oswald', sans-serif !important;
            width: 100% !important;
            padding: 15px !important;
            border-radius: 4px !important;
        }
        
        [data-testid="stTextInput"] {
            width: 100% !important;
            max-width: 400px;
        }
        
        input {
            text-align: center !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="ulp-auth-title">Utah Land & Property</div>', unsafe_allow_html=True)
    st.markdown('<div class="sync-label">Secure Access Terminal</div>', unsafe_allow_html=True)

    # Centered container for the login form
    with st.container():
        input_key = st.text_input("Security Key", type="password", placeholder="ENTER PRIVATE ACCESS KEY", label_visibility="collapsed")
        if st.button("Authorize Session"):
            try:
                user_db = st.secrets["users"]
                for username, profile in user_db.items():
                    if input_key == str(profile["key"]):
                        st.session_state.authenticated = True
                        st.session_state.user_role = profile["role"]
                        st.rerun()
                st.error("ACCESS DENIED")
            except:
                st.error("SYSTEM ERROR: Check Secrets Configuration")
    st.stop()

# --- 4. INTERNAL DASHBOARD STYLING ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=Oswald:wght@500;700&display=swap');
        .stApp { background-color: #ffffff !important; }
        .bento-card { background: #ffffff; padding: 24px; border-radius: 12px; border: 1px solid #e2e8f0; margin-bottom: 20px; }
        .hero-bento { background: #1d428a; color: #ffffff; padding: 30px; border-radius: 12px; }
        .ulp-header { font-family: 'Inter', sans-serif; font-size: 36px; font-weight: 900; color: #1d428a; text-transform: uppercase; }
        .hero-label { font-family: 'Oswald'; font-size: 11px; letter-spacing: 1px; color: #cbd5e1; text-transform: uppercase; }
        .label-text { font-family: 'Oswald'; font-size: 11px; letter-spacing: 1px; color: #475569; text-transform: uppercase; font-weight: 700; }
        .value-text { font-family: 'Inter'; font-size: 26px; font-weight: 700; color: #1d428a; }
    </style>
""", unsafe_allow_html=True)

# --- 5. ADMIN COMMAND CENTER (ALWAYS VISIBLE IF ADMIN) ---
role = st.session_state.user_role
D = st.session_state.current_deal

if role == "admin":
    st.markdown("### 🛡️ ADMIN CONTROL PANEL")
    with st.container(border=True):
        c1, c2, c3 = st.columns(3)
        new_p = c1.number_input("Contract Sales Price", value=float(D["price"]))
        new_e = c2.number_input("Seller Equity", value=float(D["seller_equity"]))
        new_f = c3.number_input("ULP Assignment Fee", value=float(D["assignment_fee"]))
        
        if st.button("PUSH UPDATED FIGURES TO DASHBOARD", use_container_width=True):
            D["price"], D["seller_equity"], D["assignment_fee"] = new_p, new_e, new_f
            st.rerun()
    st.markdown("---")

# --- 6. CORE CALCULATIONS & DASHBOARD ---
AITD_PRINCIPAL = D["price"] - D["seller_equity"]

st.markdown('<div class="ulp-header">Utah Land & Property</div>', unsafe_allow_html=True)
st.caption(f"ACTIVE DEAL: {D['deal_id']} | ROLE: {role.upper()}")

col_hero, col_side = st.columns([2, 1])
with col_hero:
    st.markdown(f"""
        <div class="hero-bento">
            <div class="hero-label">AITD PRINCIPAL BALANCE</div>
            <div style="font-family: 'Inter'; font-size: 56px; font-weight: 900; color: white;">${AITD_PRINCIPAL:,.2f}</div>
            <div style="height: 1px; background: rgba(255,255,255,0.2); margin: 25px 0;"></div>
            <div style="display: flex; justify-content: space-between; color: white;">
                <div><div class="hero-label">ORIGINAL SALES PRICE</div><div style="font-size:24px; font-weight:700;">${D['price']:,.2f}</div></div>
                <div style="text-align:right;"><div class="hero-label">SELLER EQUITY CREDIT</div><div style="font-size:24px; font-weight:700;">${D['seller_equity']:,.2f}</div></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col_side:
    st.markdown(f"""
        <div class="bento-card">
            <div class="label-text">ULP ASSIGNMENT FEE</div>
            <div class="value-text">${D['assignment_fee']:,.2f}</div>
            <p style='font-size:10px; color:#475569; margin-top:5px;'>Payable to Utah Land & Property, LLC at closing.</p>
        </div>
    """, unsafe_allow_html=True)

# --- 7. TRANSACTION HUB ---
v_col, n_col = st.columns([1.5, 1])
with v_col:
    with st.container(border=True):
        st.markdown("<p class='label-text'>Settlement Vault</p>", unsafe_allow_html=True)
        if role == "admin" and st.button("📄 GENERATE MASTER SETTLEMENT SHEET", use_container_width=True):
            instr = f"ULP SETTLEMENT\nPrice: ${D['price']:,.2f}\nEquity: ${D['seller_equity']:,.2f}\nBalance: ${AITD_PRINCIPAL:,.2f}"
            D["vault"].append({"name": f"Settlement_{datetime.now().strftime('%m%d')}.txt", "content": instr})
            st.rerun()

        for doc in D["vault"]:
            v1, v2 = st.columns([4, 1])
            v1.write(f"📁 {doc['name']}")
            b64 = base64.b64encode(doc['content'].encode()).decode()
            v2.markdown(f'<a href="data:file/txt;base64,{b64}" download="{doc["name"]}" style="color:#1d428a; font-weight:bold;">PRINT</a>', unsafe_allow_html=True)

with n_col:
    with st.container(border=True):
        st.markdown("<p class='label-text'>Deal Notes</p>", unsafe_allow_html=True)
        new_note = st.text_input("Add update", key="note_in", label_visibility="collapsed")
        if st.button("Post Note") and new_note:
            D["notes"].insert(0, f"{datetime.now().strftime('%H:%M')}: {new_note}")
            st.rerun()
        for n in D["notes"]:
            st.markdown(f"<p style='font-size:12px; border-bottom:1px solid #eee; padding:5px;'>{n}</p>", unsafe_allow_html=True)

if st.sidebar.button("TERMINATE SESSION"):
    st.session_state.authenticated = False
    st.rerun()
