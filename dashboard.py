import streamlit as st
import base64
import json
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# --- 1. CONFIG & REFRESH ---
st.set_page_config(page_title="Utah Land & Property | Asset Terminal", layout="wide", initial_sidebar_state="collapsed")
st_autorefresh(interval=15000, key="ulp_global_sync")

# --- 2. ADVANCED DATA PERSISTENCE ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_role = None

# Initialize Deal Memory
if "current_deal" not in st.session_state:
    st.session_state.current_deal = {
        "deal_id": "DEAL-001",
        "price": 330000.00,
        "seller_equity": 20000.00,
        "assignment_fee": 15000.00,
        "vault": [],
        "notes": []
    }

if "deal_history" not in st.session_state:
    st.session_state.deal_history = []

# --- 3. LOGIN GATEWAY ---
if not st.session_state.authenticated:
    st.markdown(f'''
        <style>
        @import url("https://fonts.googleapis.com/css2?family=Inter:wght@900&family=Oswald:wght@700&display=swap");
        .stApp {{ background-color: #FFFFFF !important; }}
        .ulp-auth-title {{ font-family: "Inter", sans-serif; font-size: 60px; font-weight: 900; color: #1d428a; text-align: center; text-transform: uppercase; margin-top: 15vh; }}
        div.stButton > button {{ background-color: #1d428a !important; color: white !important; width: 100%; height: 50px; font-family: 'Oswald'; font-size: 20px; }}
        </style>
        <div class="ulp-auth-title">Utah Land & Property</div>
    ''', unsafe_allow_html=True)
    
    _, col_mid, _ = st.columns([1, 1, 1])
    with col_mid:
        with st.container(border=True):
            input_key = st.text_input("SECURITY KEY", type="password")
            if st.button("AUTHORIZE"):
                try:
                    user_db = st.secrets["users"]
                    for username, profile in user_db.items():
                        if input_key == str(profile["key"]):
                            st.session_state.authenticated = True
                            st.session_state.user_role = profile["role"]
                            st.rerun()
                    st.error("ACCESS DENIED")
                except: st.error("DATABASE ERROR")
    st.stop()

# --- 4. DASHBOARD STYLE ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=Oswald:wght@500;700&display=swap');
        .stApp { background-color: #ffffff !important; }
        .bento-card { background: #ffffff; padding: 25px; border-radius: 12px; border: 1px solid #e2e8f0; margin-bottom: 20px; }
        .hero-bento { background: #1d428a; color: #ffffff; padding: 35px; border-radius: 12px; }
        .ulp-title-main { font-family: 'Inter', sans-serif; font-size: 38px; font-weight: 900; color: #1d428a; text-transform: uppercase; }
        .hub-header { font-family: 'Inter', sans-serif; font-size: 28px; font-weight: 900; color: #1d428a; border-bottom: 4px solid #1d428a; display: inline-block; margin-bottom: 20px; }
        .label-text { font-family: 'Oswald'; font-size: 12px; color: #64748b; text-transform: uppercase; font-weight: 700; }
        .hero-label { font-family: 'Oswald'; font-size: 12px; color: #cbd5e1; text-transform: uppercase; }
        .stMarkdown p { color: #1e293b !important; }
    </style>
""", unsafe_allow_html=True)

# --- 5. ADMIN COMMAND CENTER (NEW DEAL & SAVE LOGIC) ---
role = st.session_state.user_role
if role == "admin":
    with st.expander("🛠️ ADMIN: DEAL MANAGEMENT TERMINAL", expanded=True):
        m1, m2, m3 = st.columns([1,1,1])
        
        # Create New Deal
        if m1.button("➕ START NEW DEAL"):
            # Save current to history first
            st.session_state.deal_history.append(st.session_state.current_deal.copy())
            # Reset current
            st.session_state.current_deal = {
                "deal_id": f"DEAL-{datetime.now().strftime('%m%d%H%M')}",
                "price": 0.0, "seller_equity": 0.0, "assignment_fee": 0.0, "vault": [], "notes": []
            }
            st.rerun()
            
        # Save Current Deal
        if m2.button("💾 SAVE CURRENT PROGRESS"):
            st.toast("Current Deal State Cached Successfully")
            
        # View Last Deal
        if m3.button("📂 RECALL PREVIOUS DEAL"):
            if st.session_state.deal_history:
                st.session_state.current_deal = st.session_state.deal_history[-1]
                st.rerun()

        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        edt_price = c1.number_input("Contract Sales Price", value=float(st.session_state.current_deal["price"]))
        edt_equity = c2.number_input("Seller Equity (Reduces Price)", value=float(st.session_state.current_deal["seller_equity"]))
        edt_fee = c3.number_input("Utah Land & Property Assignment Fee", value=float(st.session_state.current_deal["assignment_fee"]))
        
        if st.button("PUSH UPDATED FIGURES TO ALL USERS", use_container_width=True):
            st.session_state.current_deal["price"] = edt_price
            st.session_state.current_deal["seller_equity"] = edt_equity
            st.session_state.current_deal["assignment_fee"] = edt_fee
            st.rerun()

# --- 6. MATH & UI ---
D = st.session_state.current_deal
AITD_BAL = D["price"] - D["seller_equity"]

st.markdown(f'<div class="ulp-title-main">Utah Land & Property</div>', unsafe_allow_html=True)
st.markdown(f"**CURRENT TRANSACTION ID:** {D['deal_id']} | **ROLE:** {role.upper()}")

col_hero, col_side = st.columns([2, 1])
with col_hero:
    st.markdown(f"""<div class="hero-bento"><div class="hero-label">AITD PRINCIPAL BALANCE</div><div style="font-family: 'Inter'; font-size: 56px; font-weight: 900; color:white !important;">${AITD_BAL:,.2f}</div><div style="height: 1px; background: rgba(255,255,255,0.2); margin: 25px 0;"></div><div style="display: flex; justify-content: space-between;"><div style="color:white !important;"><div class="hero-label">ORIGINAL SALES PRICE</div><div style="font-size:24px; font-weight:700;">${D['price']:,.2f}</div></div><div style="text-align:right; color:white !important;"><div class="hero-label">SELLER EQUITY PAYMENT</div><div style="font-size:24px; font-weight:700;">${D['seller_equity']:,.2f}</div></div></div></div>""", unsafe_allow_html=True)

with col_side:
    st.markdown(f"""<div class="bento-card"><div class="label-text">UTAH LAND & PROPERTY ASSIGNMENT FEE</div><div style="font-size:28px; font-weight:700; color:#1d428a;">${D['assignment_fee']:,.2f}</div><p style='font-size:10px;'>*Fixed Service Fee</p></div>""", unsafe_allow_html=True)

# --- 7. COMMUNICATION & PDF PUSH ---
st.markdown('<div class="hub-header">Transaction Communication Hub</div>', unsafe_allow_html=True)

v_col, n_col = st.columns([1.5, 1])
with v_col:
    with st.container(border=True):
        st.markdown("<p class='label-text'>Universal Vault & Settlement Exports</p>", unsafe_allow_html=True)
        
        if role == "admin":
            if st.button("📄 GENERATE & PUSH SETTLEMENT PDF TO ALL PARTIES", use_container_width=True):
                report = (
                    f"OFFICIAL SETTLEMENT INSTRUCTIONS - UTAH LAND & PROPERTY\n"
                    f"Deal ID: {D['deal_id']} | Date: {datetime.now().strftime('%Y-%m-%d')}\n"
                    f"--------------------------------------------------\n"
                    f"SALES PRICE:          ${D['price']:,.2f}\n"
                    f"SELLER EQUITY:        -${D['seller_equity']:,.2f}\n"
                    f"AITD PRINCIPAL:       ${AITD_BAL:,.2f}\n"
                    f"--------------------------------------------------\n"
                    f"ASSIGNMENT FEE:       ${D['assignment_fee']:,.2f}\n"
                )
                D["vault"].append({"name": f"Settlement_{D['deal_id']}.txt", "content": report, "user": "ADMIN"})
                st.success("PDF/Settlement instructions pushed to all parties.")

        for i, doc in enumerate(D["vault"]):
            v1, v2 = st.columns([4, 1])
            v1.write(f"📁 **{doc['name']}** (Admin)")
            b64 = base64.b64encode(doc['content'].encode()).decode()
            v2.markdown(f'<a href="data:file/txt;base64,{b64}" download="{doc["name"]}" style="color:#1d428a; font-weight:bold;">PRINT/PDF</a>', unsafe_allow_html=True)

with n_col:
    with st.container(border=True):
        st.markdown("<p class='label-text'>Live Deal Notes</p>", unsafe_allow_html=True)
        new_note = st.text_input("Enter update...", key="note_in")
        if st.button("Add Note"):
            D["notes"].insert(0, f"{datetime.now().strftime('%H:%M')} ({role.upper()}): {new_note}")
            st.rerun()
        for n in D["notes"]:
            st.markdown(f"<p style='font-size:12px; border-bottom:1px solid #f1f5f9; padding:5px;'>{n}</p>", unsafe_allow_html=True)

# --- 8. LOGOUT ---
if st.sidebar.button("TERMINATE SESSION"):
    st.session_state.authenticated = False
    st.rerun()
