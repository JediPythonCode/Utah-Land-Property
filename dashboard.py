import streamlit as st
import textwrap
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# --- 1. CONFIG & REFRESH ---
st.set_page_config(page_title="Utah Land & Property", layout="wide", initial_sidebar_state="collapsed")
st_autorefresh(interval=10000, key="ulp_sync_ping")

# --- 2. AUTHENTICATION GATE & STYLING ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_role = None

# LOGIC INSERT: Initialize Transaction State
if "checklist_step" not in st.session_state:
    st.session_state.checklist_step = 1
if "uploaded_docs" not in st.session_state:
    st.session_state.uploaded_docs = []

if not st.session_state.authenticated:
    # [EXISTING AUTH LOGIC REMAINS - NO CHANGES]
    pillar_icons = [
        '<svg viewBox="0 0 24 24" width="80" height="80" stroke="#1d428a" stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>',
        '<svg viewBox="0 0 24 24" width="80" height="80" stroke="#1d428a" stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>',
        '<svg viewBox="0 0 24 24" width="80" height="80" stroke="#1d428a" stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>',
        '<svg viewBox="0 0 24 24" width="80" height="80" stroke="#1d428a" stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>',
    
    ]
    icon_stack = "".join([f'<div class="flip-logo" style="animation-delay: {i * 2}s;">{svg}</div>' for i, svg in enumerate(pillar_icons)])

    st.markdown(f'''
    <style>
        @import url("https://fonts.googleapis.com/css2?family=Inter:wght@900&family=Oswald:wght@700&display=swap");
        .stApp {{ background-color: #FFFFFF !important; }}
        header, footer, [data-testid="stHeader"] {{ display: none !important; }}
        .ulp-auth-title {{ font-family: "Inter", sans-serif; font-size: clamp(32px, 12vw, 80px); font-weight: 900; color: #1d428a; letter-spacing: -4px; line-height: 1.0; margin-bottom: 10px; text-align: center; text-transform: uppercase; }}
        .logo-container {{ position: relative; height: 140px; display: flex; justify-content: center; align-items: center; margin: 10px 0; }}
        .flip-logo {{ position: absolute; opacity: 0; animation: logoFlip {len(pillar_icons)*3}s infinite; }}
        @keyframes logoFlip {{ 0% {{ opacity: 0; transform: scale(0.8); }} 1% {{ opacity: 1; transform: scale(1); }} 30% {{ opacity: 1; }} 33% {{ opacity: 0; transform: scale(1.05); }} 100% {{ opacity: 0; }} }}
        .sync-box {{ text-align: center; margin-bottom: 30px; }}
        .pulse-dot {{ height: 10px; width: 10px; background-color: #00ff41; border-radius: 50%; display: inline-block; margin-right: 8px; box-shadow: 0 0 10px #00ff41; animation: pulse-green 1.5s infinite; }}
        @keyframes pulse-green {{ 0% {{ box-shadow: 0 0 0px 0px rgba(0, 255, 65, 0.7); }} 70% {{ box-shadow: 0 0 0px 10px rgba(0, 255, 65, 0); }} 100% {{ box-shadow: 0 0 0px 0px rgba(0, 255, 65, 0); }} }}
        .sync-label {{ font-family: "Oswald", sans-serif; font-size: 15px; color: #1d428a; letter-spacing: 2px; font-weight: bold; }}
        [data-testid="stColumn"] [data-testid="stVerticalBlock"] {{ align-items: center !important; justify-content: center !important; text-align: center !important; }}
        div.stButton > button {{ background-color: #1d428a !important; color: #FFFFFF !important; font-family: 'Oswald', sans-serif !important; font-weight: 700 !important; text-transform: uppercase !important; letter-spacing: 2px !important; padding: 18px 45px !important; border: 2px solid #1d428a !important; transition: all 0.3s ease-in-out !important; margin: 15px auto !important; display: inline-block !important; }}
        input {{ text-align: center !important; }}
    </style>
    <div style="padding: 10vh 5% 0 5%; text-align: center;">
        <div class="ulp-auth-title">Utah Land & Property</div>
        <div class="logo-container">{icon_stack}</div>
        <div class="sync-box"><span class="pulse-dot"></span><span class="sync-label">Maximum privacy. Maximum protection. Strategic land ownership in Utah.</span></div>
    </div>
    ''', unsafe_allow_html=True)

    _, col_mid, _ = st.columns([1, 2, 1])
    with col_mid:
        with st.container(border=True):
            input_key = st.text_input("Security Key", type="password", placeholder="ENTER PRIVATE ACCESS KEY", label_visibility="collapsed")
            if st.button("Secure Access Terminal"):
                try:
                    user_db = st.secrets["users"]
                    found_user = False
                    for username, profile in user_db.items():
                        if input_key == str(profile["key"]):
                            st.session_state.authenticated = True
                            st.session_state.user_role = profile["role"]
                            found_user = True
                            st.rerun()
                    if not found_user: st.error("ACCESS DENIED: INVALID KEY")
                except KeyError: st.error("SYSTEM ERROR: User database not found.")
    st.stop()

# --- 3. INTERNAL DASHBOARD STYLE ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@900&family=Oswald:wght@700&display=swap');
        .stApp { background-color: #FFFFFF !important; }
        .ulp-header { font-family: 'Inter', sans-serif; font-size: clamp(40px, 12vw, 85px) !important; font-weight: 900 !important; color: #1d428a !important; letter-spacing: -4px; line-height: 0.85; margin-bottom: 5px; text-align: center; text-transform: uppercase; }
        .intel-header { background: linear-gradient(to right, #bf953f, #fcf6ba, #b38728, #fbf5b7, #aa771c) !important; -webkit-background-clip: text !important; -webkit-text-fill-color: transparent !important; font-family: 'Inter', sans-serif !important; font-weight: 900 !important; font-size: clamp(35px, 12vw, 65px) !important; text-align: center !important; text-transform: uppercase; }
        .gold-card { background-color: #FDD017 !important; background-image: url("https://www.transparenttextures.com/patterns/carbon-fibre.png") !important; border-top: 6px solid #1a1a1a !important; border-radius: 0px 20px 0px 20px !important; padding: 25px !important; text-align: center !important; margin-bottom: 15px; box-shadow: 0 12px 25px rgba(0,0,0,0.3) !important; min-height: 380px; }
        .m-title-white { color: #ffffff !important; font-family: 'Inter', sans-serif !important; font-weight: 900 !important; font-size: 24px !important; text-transform: uppercase !important; margin: 15px 0 !important; text-shadow: 2px 2px 4px rgba(0,0,0,0.5) !important; }
        .tech-pill { background: #111; border: 1px solid #bf953f; color: #fcf6ba; padding: 4px 10px; border-radius: 4px; font-family: 'Oswald'; font-size: 11px; margin: 2px; display: inline-block; }
    </style>
""", unsafe_allow_html=True)

# --- 4. DASHBOARD CONTENT ---
role = st.session_state.user_role
st.markdown(f'''<div style="text-align: center;"><h1 class="ulp-header">Utah Land & Property</h1><div style="font-family: 'Oswald'; color: #1d428a; letter-spacing: 2px;">TERMINAL ACCESS: {role} LEVEL</div></div>''', unsafe_allow_html=True)
st.markdown("""<div style="text-align:center; padding: 40px 0;"><h1 class="intel-header">Asset Intelligence</h1></div>""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('''<div class="gold-card"><div style="background: #1a1a1a; color: #00ff41; padding: 2px 12px; border-radius: 4px; font-family: 'Oswald'; font-size: 10px; letter-spacing: 2px; margin-bottom: 10px; border: 1px solid #00ff41; display: inline-block;">SYNC ACTIVE</div><div style="font-size: 50px;">🛡️</div><span class="m-title-white">Summit Layered Trust</span><div style="background: #111111; border-radius: 8px; padding: 20px; width: 100%; margin-top: 15px; border: 1px solid #333;"><div style="font-family:Oswald; font-size:10px; color:#00ff41; font-weight:bold; letter-spacing:1px;">PROTECTION</div><div style="font-family: 'Oswald'; font-size: 20px; font-weight: 900; color: #ffffff;">MAXIMUM</div></div></div>''', unsafe_allow_html=True)

with col2:
    st.markdown('''<div class="gold-card"><div style="background: #1a1a1a; color: #bf953f; padding: 2px 12px; border-radius: 4px; font-family: 'Oswald'; font-size: 10px; letter-spacing: 2px; margin-bottom: 10px; border: 1px solid #bf953f; display: inline-block;">FLOW ANALYTICS</div><div style="font-size: 50px;">📈</div><span class="m-title-white">Strategic Deal Flow</span><div style="background: #111111; border-radius: 8px; padding: 15px; width: 100%; margin-top: 15px; border: 1px solid #333; text-align: left;"><div class="tech-pill">TotalExpert CRM</div><div class="tech-pill">SNapp POS</div><div class="tech-pill">DocMagic eClose</div><div class="tech-pill">Encompass LOS</div></div></div>''', unsafe_allow_html=True)

with col3:
    status_color = "#00ff41" if st.session_state.checklist_step > 2 else "#bf953f"
    st.markdown(f'''<div class="gold-card"><div style="background: #1a1a1a; color: #ffffff; padding: 2px 12px; border-radius: 4px; font-family: 'Oswald'; font-size: 10px; letter-spacing: 2px; margin-bottom: 10px; border: 1px solid #ffffff; display: inline-block;">PORTAL V3.0</div><div style="font-size: 50px;">🏢</div><span class="m-title-white">Transaction Hub</span><div style="background: #111111; border-radius: 8px; padding: 15px; width: 100%; margin-top: 15px; border: 1px solid #333; text-align: center;"><div style="color:{status_color}; font-family:'Oswald'; font-size:12px;">PIPELINE STEP {st.session_state.checklist_step}/4</div><div style="color:white; font-family:'Inter'; font-weight:900; font-size:18px;">SECURE VAULT ACTIVE</div></div></div>''', unsafe_allow_html=True)

# --- 5. UNIFIED TRANSACTION & BUYER PORTAL TERMINAL (REFACTORED FOR CLEAN UI/UX) ---
st.divider()
st.subheader("🛠️ Transaction & Buyer Portal Terminal")

# --- Initialize Central Deal State ---
if "deal_state" not in st.session_state:
    st.session_state.deal_state = {
        "deal_id": "DL-" + datetime.now().strftime("%Y%m%d%H%M%S"),
        "status": "Lead",
        "property": {
            "address": "123 Example Rd, Utah",
            "3d_tour_url": "https://example.com/3d-tour"
        },
        "buyer": {"name": "TBD", "pre_approval": False},
        "agent": {"name": st.session_state.user_role},
        "documents": [],
        "checklist": [
            {"task": "Prequalification", "status": "Pending"},
            {"task": "Offer & Contract", "status": "Pending"},
            {"task": "Loan Underwriting", "status": "Pending"},
            {"task": "Digital Closing", "status": "Pending"},
        ],
        "financials": {"loan_amount": 0, "closing_costs": 0, "monthly_payment": 0},
    }

deal = st.session_state.deal_state

# --- Layout: Checklist & Document Vault Side-by-Side ---
col1, col2 = st.columns([1, 1], gap="large")

# --- Checklist Column ---
with col1:
    st.markdown("### 📋 Transaction Checklist")
    for idx, task in enumerate(deal["checklist"], 1):
        completed = task["status"] == "Completed"
        st.checkbox(task["task"], value=completed, key=f"deal_task_{idx}", disabled=True)

    # Action Buttons
    adv_col, reset_col = st.columns(2)
    with adv_col:
        if st.button("✅ Advance Next Task"):
            for task in deal["checklist"]:
                if task["status"] != "Completed":
                    task["status"] = "Completed"
                    # Update canonical deal status
                    if task["task"] == "Prequalification": deal["status"] = "PreApproval"
                    elif task["task"] == "Offer & Contract": deal["status"] = "UnderContract"
                    elif task["task"] == "Loan Underwriting": deal["status"] = "Closing"
                    elif task["task"] == "Digital Closing": deal["status"] = "Completed"
                    break
            st.session_state.deal_state = deal
            st.success("Task completed! Deal state updated.")
            st.rerun()
    with reset_col:
        if st.button("🔄 Reset Deal"):
            for task in deal["checklist"]:
                task["status"] = "Pending"
            deal["status"] = "Lead"
            st.session_state.deal_state = deal
            st.warning("Deal reset to initial state.")
            st.rerun()

# --- Document Vault Column ---
with col2:
    st.markdown("### 📂 Secure Document Vault")
    uploaded_file = st.file_uploader("Upload financial or property documents", type=['pdf', 'jpg', 'png'])
    if uploaded_file:
        doc_entry = {
            "name": uploaded_file.name,
            "uploaded_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        deal["documents"].append(doc_entry)
        st.session_state.deal_state = deal
        st.success(f"Uploaded: {uploaded_file.name}")

    if deal["documents"]:
        with st.expander("Vault Inventory"):
            for doc in deal["documents"]:
                st.write(f"📄 {doc['name']} — Uploaded: {doc['uploaded_at']}")

# --- Real-Time Deal Status ---
st.markdown("### 🔄 Deal Status Tracker")
status_colors = {
    "Lead": "🟡",
    "PreApproval": "🟢",
    "UnderContract": "🔵",
    "Closing": "🟠",
    "Completed": "✅"
}
status_text = status_colors.get(deal["status"], "🟡") + " " + deal["status"].replace("_", " ")
st.info(f"Current Deal Status: {status_text}")

# --- Financial Overview ---
st.markdown("### 💰 Financial Calculator")
deal["financials"]["loan_amount"] = st.number_input("Loan Amount ($)", min_value=0, value=deal["financials"]["loan_amount"])
deal["financials"]["closing_costs"] = st.number_input("Closing Costs ($)", min_value=0, value=deal["financials"]["closing_costs"])

if deal["financials"]["loan_amount"] > 0 and deal["financials"]["closing_costs"] >= 0:
    principal = deal["financials"]["loan_amount"]
    interest_rate = 6.5 / 100 / 12
    months = 30 * 12
    monthly_payment = principal * (interest_rate * (1 + interest_rate) ** months) / ((1 + interest_rate) ** months - 1)
    deal["financials"]["monthly_payment"] = monthly_payment
    st.success(f"Estimated Monthly Payment: ${monthly_payment:,.2f}")

# --- Persist Deal State ---
st.session_state.deal_state = deal



# --- 6. LOGOUT ---
if st.sidebar.button("Terminate Session"):
    st.session_state.authenticated = False
    st.rerun()
