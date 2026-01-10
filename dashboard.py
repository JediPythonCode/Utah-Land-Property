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
        "address": "123 Main St, Salt Lake City",
        "seller_name": "John Doe",
        "buyer_name": "Jane Smith",
        "price": 330000.00,
        "seller_equity": 20000.00,
        "assignment_fee": 15000.00,
        "terms": "Subject to existing financing.",
        "instr_title": "", "instr_escrow": "", "instr_servicer": "",
        "disclosures": ["Property sold As-Is."],
        "vault": [], "notes": []
    }

# --- 3. CLEAN CSS (OVERLAP FIX & STEADY-BLUE BUTTONS) ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=Oswald:wght@500;700&display=swap');
        
        /* Global Background */
        .stApp { background-color: #ffffff !important; }

        /* Button Conformity & Hover Effect */
        div.stButton > button {
            background-color: #1d428a !important;
            color: white !important;
            border: 2px solid #1d428a !important;
            border-radius: 4px !important;
            height: 52px !important;
            width: 100% !important;
            font-family: 'Oswald', sans-serif !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            transition: all 0.2s ease;
        }
        div.stButton > button:hover {
            background-color: #1d428a !important;
            color: white !important;
            border: 2px solid white !important; /* White boundary on hover */
            box-shadow: inset 0 0 0 2px #1d428a;
        }

        /* Label legibility (Prevents Overlapping) */
        .admin-label {
            font-family: 'Oswald', sans-serif !important;
            color: #1d428a !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            font-size: 13px !important;
            margin-bottom: 8px !important;
            margin-top: 15px !important;
            display: block !important;
        }

        /* Admin Header Bar */
        .admin-header-bar {
            background-color: #1d428a;
            color: white;
            padding: 15px;
            text-align: center;
            border-radius: 4px;
            font-family: 'Inter', sans-serif;
            font-weight: 900;
            font-size: 20px;
            letter-spacing: 1px;
            margin-bottom: 25px;
            text-transform: uppercase;
        }

        /* Input Conformity */
        input {
            height: 52px !important;
            border: 2px solid #e2e8f0 !important;
            border-radius: 4px !important;
        }
        
        /* Auth Screen Centering */
        [data-testid="stAppViewBlockContainer"] {
            display: flex; flex-direction: column; justify-content: center; align-items: center;
        }
    </style>
""", unsafe_allow_html=True)

# --- 4. LOGIN ---
if not st.session_state.authenticated:
    st.markdown('<div style="font-family:Inter; font-size:60px; font-weight:900; color:#1d428a; text-align:center; margin-bottom:20px;">UTAH LAND & PROPERTY</div>', unsafe_allow_html=True)
    _, col_mid, _ = st.columns([1, 0.6, 1])
    with col_mid:
        input_key = st.text_input("Key", type="password", placeholder="ENTER ACCESS KEY", label_visibility="collapsed")
        if st.button("Authorize Session"):
            try:
                for user, profile in st.secrets["users"].items():
                    if input_key == str(profile["key"]):
                        st.session_state.authenticated = True
                        st.session_state.user_role = str(profile["role"]).lower()
                        st.rerun()
                st.error("ACCESS DENIED")
            except: st.error("Config Error")
    st.stop()

# --- 5. ADMIN TERMINAL ---
role = st.session_state.user_role
D = st.session_state.current_deal

if role == "admin":
    st.markdown('<div class="admin-header-bar">ADMIN: STRATEGIC DEAL JACKET</div>', unsafe_allow_html=True)
    
    with st.container(border=True):
        c1, c2 = st.columns(2)
        c1.markdown('<span class="admin-label">Property Address</span>', unsafe_allow_html=True)
        a_addr = c1.text_input("Addr", value=D["address"], label_visibility="collapsed")
        c2.markdown('<span class="admin-label">Deal ID</span>', unsafe_allow_html=True)
        a_id = c2.text_input("ID", value=D["deal_id"], label_visibility="collapsed")
        
        f1, f2, f3 = st.columns(3)
        f1.markdown('<span class="admin-label">Sales Price</span>', unsafe_allow_html=True)
        a_price = f1.number_input("Price", value=float(D["price"]), label_visibility="collapsed")
        f2.markdown('<span class="admin-label">Seller Equity</span>', unsafe_allow_html=True)
        a_equity = f2.number_input("Equity", value=float(D["seller_equity"]), label_visibility="collapsed")
        f3.markdown('<span class="admin-label">Assignment Fee</span>', unsafe_allow_html=True)
        a_fee = f3.number_input("Fee", value=float(D["assignment_fee"]), label_visibility="collapsed")

        st.markdown('<span class="admin-label">Instructions: Title | Escrow | Servicer</span>', unsafe_allow_html=True)
        i1, i2, i3 = st.columns(3)
        a_title = i1.text_area("Title", value=D["instr_title"], placeholder="Title Instructions", label_visibility="collapsed")
        a_escrow = i2.text_area("Escrow", value=D["instr_escrow"], placeholder="Escrow Instructions", label_visibility="collapsed")
        a_servicer = i3.text_area("Servicer", value=D["instr_servicer"], placeholder="Servicer Instructions", label_visibility="collapsed")

        st.markdown('<span class="admin-label">Buyer Disclosures</span>', unsafe_allow_html=True)
        updated_discs = []
        for i, d in enumerate(D["disclosures"]):
            updated_discs.append(st.text_input(f"Disc {i}", value=d, key=f"d_in_{i}", label_visibility="collapsed"))
        
        if st.button("Add Disclosure Line +"):
            D["disclosures"].append("")
            st.rerun()

        if st.button("UPDATE MASTER DASHBOARD"):
            st.session_state.current_deal.update({
                "address": a_addr, "deal_id": a_id, "price": a_price,
                "seller_equity": a_equity, "assignment_fee": a_fee,
                "instr_title": a_title, "instr_escrow": a_escrow, 
                "instr_servicer": a_servicer, "disclosures": updated_discs
            })
            st.rerun()

# --- 6. DASHBOARD VIEW ---
AITD_PRINCIPAL = D["price"] - D["seller_equity"]
st.markdown(f'<div style="font-family:Inter; font-size:32px; font-weight:900; color:#1d428a; margin-top:20px;">{D["address"]}</div>', unsafe_allow_html=True)

col_main, col_side = st.columns([2, 1])
with col_main:
    st.markdown(f"""
        <div style="background:#1d428a; padding:30px; border-radius:8px; color:white;">
            <div style="font-family:Oswald; font-size:12px; opacity:0.8;">AITD PRINCIPAL BALANCE</div>
            <div style="font-family:Inter; font-size:48px; font-weight:900;">${AITD_PRINCIPAL:,.2f}</div>
        </div>
    """, unsafe_allow_html=True)

with col_side:
    with st.container(border=True):
        st.markdown('<div style="font-family:Oswald; font-size:12px; color:#1d428a;">DISCLOSURES</div>', unsafe_allow_html=True)
        for disc in D["disclosures"]:
            if disc: st.markdown(f"• {disc}")

if st.sidebar.button("LOGOUT"):
    st.session_state.authenticated = False
    st.rerun()
