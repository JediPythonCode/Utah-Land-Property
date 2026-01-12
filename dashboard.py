import base64
import numpy_financial as npf
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
import streamlit as st
from PIL import Image
import io
import re

# --- 1. CONFIG ---
st.set_page_config(page_title="Utah Land & Property", layout="wide", initial_sidebar_state="collapsed")
st_autorefresh(interval=10000, key="ulp_sync_ping")

# --- 2. DATA PERSISTENCE (STARTS BLANK) ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_role = None
    st.session_state.verified_by_admin = False

if "current_deal" not in st.session_state:
    st.session_state.current_deal = {
        "deal_id": "", "address": "", "seller_name": "", "buyer_name": "",
        "price": 0.0, 
        "seller_equity": 20000.00,   # Downpayment
        "assignment_fee": 15000.00,  # Utah Land & Property Fee
        "interest_rate": 0.0, "hoa_monthly": 0.0,
        "instr_title": "", "instr_escrow": "", "instr_servicer": "",
        "vault": [], "images": []
    }

D = st.session_state.current_deal

# --- 3. CSS (CENTERING & BRANDING) ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=Oswald:wght@500;700&display=swap');
        #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
        .stApp { background-color: #ffffff !important; }
        
        /* Branding Styles */
        .branding-container { text-align: center; margin-bottom: 20px; }
        .branding-text { color: #1d428a !important; font-family: 'Oswald', sans-serif; font-weight: 700; font-size: 18px; text-transform: uppercase; letter-spacing: 1.5px; }
        
        /* Auth Centering Logic */
        [data-testid="stVerticalBlock"] > div:has(input[type="password"]) {
            text-align: center !important;
        }
        
        div.stButton > button { 
            background-color: #1d428a !important; color: white !important; border: 2px solid #1d428a !important; 
            border-radius: 4px !important; height: 56px !important; width: 100% !important; 
            font-family: 'Oswald', sans-serif !important; font-weight: 700 !important; text-transform: uppercase !important; 
        }
        
        [data-testid="stTextInput"] input { 
            height: 56px !important; background-color: #1d428a !important; border: 2px solid #1d428a !important; 
            border-radius: 4px !important; text-align: center !important; font-size: 18px !important; 
            font-weight: 700 !important; color: white !important; 
        }

        .admin-header-bar { background-color: #1d428a; color: white !important; padding: 16px; text-align: center; border-radius: 4px; font-family: 'Inter', sans-serif; font-weight: 900; font-size: 22px; text-transform: uppercase; margin-bottom: 30px; }
        .buyer-card { background: #f1f5f9; padding: 20px; border-left: 5px solid #1d428a; border-radius: 4px; margin-bottom: 10px; }
        .buyer-label { font-family: 'Oswald', sans-serif; color: #1d428a; font-size: 11px; text-transform: uppercase; }
        .buyer-value { font-family: 'Inter', sans-serif; color: #1d428a; font-size: 26px; font-weight: 900; }
        .pmt-card { background: #1d428a; color: white; padding: 18px; border-radius: 4px; text-align: center; margin-bottom: 12px; }
    </style>
""", unsafe_allow_html=True)

# --- 4. AUTH PAGE (RESTORED BRANDING) ---
if not st.session_state.authenticated:
    st.markdown('<div style="height: 15vh;"></div><div style="font-family:Inter; font-size:clamp(40px, 10vw, 75px); font-weight:900; color:#1d428a; text-align:center; line-height:0.9; margin-bottom:15px;">UTAH LAND & PROPERTY</div>', unsafe_allow_html=True)
    st.markdown('<div class="branding-container"><span class="branding-text">Asset protection ● Maximum privacy ● Anonymous holdings</span></div>', unsafe_allow_html=True)
    
    _, col_mid, _ = st.columns([1, 0.45, 1])
    with col_mid:
        input_key = st.text_input("Access Key", type="password", placeholder="ENTER ACCESS KEY", label_visibility="collapsed")
        # Centered button inside the same column
        if st.button("Authorize Session"):
            try:
                for user, profile in st.secrets["users"].items():
                    if input_key == str(profile["key"]):
                        st.session_state.authenticated = True
                        st.session_state.user_role = str(profile["role"]).lower()
                        st.rerun()
                st.error("ACCESS DENIED")
            except: 
                st.error("Configuration Error")
    st.stop()

# --- 5. LOGIC & DASHBOARD ---
# Principal ($310k) = Price ($330k) - Seller Equity ($20k)
EQ_BUYER_BAL = D["price"] - D["seller_equity"] if D["price"] > 0 else 0

def calc_monthly_pmt(principal, annual_rate, years):
    if annual_rate <= 0 or years <= 0: return principal / (years * 12) if years > 0 else 0
    return abs(npf.pmt(annual_rate/100/12, years*12, principal))

pi_15, pi_30 = calc_monthly_pmt(EQ_BUYER_BAL, D["interest_rate"], 15), calc_monthly_pmt(EQ_BUYER_BAL, D["interest_rate"], 30)
total_15, total_30 = pi_15 + D["hoa_monthly"], pi_30 + D["hoa_monthly"]

def generate_memo_text():
    return f"""
UTAH LAND & PROPERTY, LLC - DEAL MEMORANDUM
--------------------------------------------------
PROPERTY: {D['address']}
FINANCIAL SUMMARY:
- Sale Price: ${D['price']:,.2f}
- Downpayment (Seller Equity): ${D['seller_equity']:,.2f}
- EQUITY BUYER PRINCIPAL: ${EQ_BUYER_BAL:,.2f}
- Assignment Fee: ${D['assignment_fee']:,.2f}
--------------------------------------------------
    """

# --- 6. ADMIN TERMINAL ---
if st.session_state.user_role == "admin":
    st.markdown('<div class="admin-header-bar">ADMIN: PRIVATE DEAL JACKET</div>', unsafe_allow_html=True)
    
    with st.expander("📁 BUYER VETTING & APPROVAL", expanded=True):
        if not D["vault"]: st.info("No documents uploaded.")
        else:
            for idx, doc in enumerate(D["vault"]):
                v1, v2, v3 = st.columns([3, 1, 1])
                v1.write(f"📄 **{doc['name']}**")
                b64 = base64.b64encode(doc['content'] if isinstance(doc['content'], bytes) else doc['content'].encode()).decode()
                v2.markdown(f'<a href="data:application/octet-stream;base64,{b64}" download="{doc["name"]}"><button style="width:100%; cursor:pointer; height:30px !important; font-size:10px !important;">VIEW</button></a>', unsafe_allow_html=True)
                if v3.button("DEL", key=f"del_{idx}"): D["vault"].pop(idx); st.rerun()
        if st.button("✅ REVEAL ADDRESS TO BUYER"): st.session_state.verified_by_admin = True; st.rerun()
        if st.button("🔒 LOCK ADDRESS"): st.session_state.verified_by_admin = False; st.rerun()

    with st.container(border=True):
        st.write("### MANUAL DATA ENTRY")
        c1, c2, c3, c4 = st.columns([2, 1, 0.7, 0.7])
        a_addr = c1.text_input("Address", value=D["address"])
        a_id = c2.text_input("Deal ID", value=D["deal_id"])
        a_rate = c3.number_input("Rate", value=float(D["interest_rate"]))
        a_hoa = c4.number_input("HOA", value=float(D["hoa_monthly"]))
        f1, f2, f3 = st.columns(3)
        a_price = f1.number_input("Price", value=float(D["price"]))
        a_equity = f2.number_input("Downpayment (Equity)", value=float(D["seller_equity"]))
        a_fee = f3.number_input("Assignment Fee", value=float(D["assignment_fee"]))

        st.markdown("### STRATEGIC INSTRUCTIONS")
        i1, i2, i3 = st.columns(3)
        a_title, a_escrow, a_servicer = i1.text_area("Title Search", value=D["instr_title"]), i2.text_area("Escrow Holder", value=D["instr_escrow"]), i3.text_area("Mortgage Servicer", value=D["instr_servicer"])

        if st.button("SAVE & UPDATE PORTAL"):
            D.update({"address": a_addr, "deal_id": a_id, "interest_rate": a_rate, "hoa_monthly": a_hoa, "price": a_price, "seller_equity": a_equity, "assignment_fee": a_fee, "instr_title": a_title, "instr_escrow": a_escrow, "instr_servicer": a_servicer})
            st.rerun()

# --- 7. BUYER PORTAL ---
st.markdown("---")
show_data = st.session_state.user_role == "admin" or st.session_state.verified_by_admin

if show_data and D["address"]:
    st.markdown(f'<div style="font-family:Inter; font-size:36px; font-weight:900; color:#1d428a; text-transform:uppercase;">{D["address"]}</div>', unsafe_allow_html=True)
    st.download_button("🖨️ GENERATE DEAL MEMO", data=generate_memo_text(), file_name=f"Deal_Memo_{D['deal_id']}.txt", mime="text/plain")
else:
    st.markdown('<div style="font-family:Inter; font-size:36px; font-weight:900; color:#1d428a;">PRIVATE ASSET: UNVETTED</div>', unsafe_allow_html=True)

col_main, col_pmt = st.columns([2, 1])
with col_main:
    p1, p2, p3 = st.columns(3)
    p1.markdown(f'<div class="buyer-card"><div class="buyer-label">Assignment Fee</div><div class="buyer-value">${D["assignment_fee"]:,.2f}</div></div>', unsafe_allow_html=True)
    p2.markdown(f'<div class="buyer-card"><div class="buyer-label">Sale Price</div><div class="buyer-value">${D["price"]:,.2f}</div></div>', unsafe_allow_html=True)
    p3.markdown(f'<div class="buyer-card" style="background:#1d428a;"><div class="buyer-label" style="color:white;">Equity Buyer Principal</div><div class="buyer-value" style="color:white;">${EQ_BUYER_BAL:,.2f}</div></div>', unsafe_allow_html=True)

    if not show_data:
        with st.form("gate"):
            st.markdown("### UPLOAD ID TO UNLOCK ASSET")
            up = st.file_uploader("ID / Proof of Funds", type=['pdf', 'jpg', 'png'])
            if st.form_submit_button("SUBMIT"):
                if up:
                    D["vault"].append({"name": f"BUYER_{up.name}", "content": up.getvalue()})
                    st.success("Submitted for review.")

with col_pmt:
    st.markdown(f'<div class="pmt-card"><div style="font-size:12px; opacity:0.8;">15-YR TOTAL</div><div style="font-size:32px; font-weight:900;">${total_15:,.2f}</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="pmt-card"><div style="font-size:12px; opacity:0.8;">30-YR TOTAL</div><div style="font-size:32px; font-weight:900;">${total_30:,.2f}</div></div>', unsafe_allow_html=True)
    
    if show_data:
        with st.container(border=True):
            st.write("**SETTLEMENT VAULT**")
            for doc in D["vault"]:
                b64 = base64.b64encode(doc['content']).decode()
                st.markdown(f'<a href="data:application/octet-stream;base64,{b64}" download="{doc["name"]}">{doc["name"]} (PRINT)</a>', unsafe_allow_html=True)

if st.sidebar.button("LOGOUT"): st.session_state.authenticated = False; st.rerun()
