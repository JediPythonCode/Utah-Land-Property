import base64
import io
import hashlib
from datetime import datetime

import streamlit as st
from streamlit_autorefresh import st_autorefresh
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas

# --------------------------------------------------
# 1. CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Utah Land & Property",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st_autorefresh(interval=10000, key="ulp_sync_ping")

# --------------------------------------------------
# 2. SESSION + SHARED DEAL STORE
# --------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_role = None

if "shared_deals" not in st.session_state:
    st.session_state.shared_deals = {}

if "active_deal_id" not in st.session_state:
    st.session_state.active_deal_id = "DEAL-PRIMARY"


def deal_hash(deal: dict):
    payload = f"{deal['price']}{deal['seller_equity']}{deal['assignment_fee']}"
    return hashlib.md5(payload.encode()).hexdigest()


if st.session_state.active_deal_id not in st.session_state.shared_deals:
    st.session_state.shared_deals[st.session_state.active_deal_id] = {
        "deal_id": st.session_state.active_deal_id,
        "price": 330000.0,
        "seller_equity": 20000.0,
        "assignment_fee": 15000.0,
        "vault": [],
        "notes": [],
        "version": ""
    }

D = st.session_state.shared_deals[st.session_state.active_deal_id]

# --------------------------------------------------
# 3. AUTH TERMINAL (FIXED CENTER + SINGLE CLICK)
# --------------------------------------------------
if not st.session_state.authenticated:

    st.markdown("""
    <style>
    @import url("https://fonts.googleapis.com/css2?family=Inter:wght@900&family=Oswald:wght@700&display=swap");
    header, footer { display:none !important; }

    section.main > div { padding-top: 0 !important; }
    [data-testid="stVerticalBlock"] { gap: 0 !important; }

    .main-auth-container {
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
    }

    .ulp-auth-title {
        font-family: Inter;
        font-size: clamp(36px, 8vw, 84px);
        font-weight: 900;
        color: #1d428a;
        letter-spacing: -4px;
        margin-bottom: 10px;
        text-transform: uppercase;
    }

    .sync-box {
        margin: 20px 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .pulse-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: #00ff41;
        box-shadow: 0 0 10px #00ff41;
        animation: pulse 1.5s infinite;
    }

    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(0,255,65,.7); }
        70% { box-shadow: 0 0 0 10px rgba(0,255,65,0); }
        100% { box-shadow: 0 0 0 0 rgba(0,255,65,0); }
    }

    div.stButton > button {
        background:#1d428a;
        color:white;
        font-family:Oswald;
        letter-spacing:2px;
        text-transform:uppercase;
        padding:14px;
        width:100%;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="main-auth-container">
        <div class="ulp-auth-title">Utah Land & Property</div>
        <div class="sync-box">
            <span class="pulse-dot"></span>
            <span style="font-family:Oswald;letter-spacing:2px;">Secure Access Terminal</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([1.3, 1, 1.3])
    with col:
        key_input = st.text_input(
            "Security Key",
            type="password",
            placeholder="ENTER PRIVATE ACCESS KEY",
            label_visibility="collapsed"
        )

        if st.button("Authorize Session", disabled=st.session_state.get("auth_lock", False)):
            st.session_state.auth_lock = True
            try:
                for _, profile in st.secrets["users"].items():
                    if key_input == str(profile["key"]):
                        st.session_state.authenticated = True
                        st.session_state.user_role = profile["role"]
                        st.session_state.auth_lock = False
                        st.rerun()
                st.error("ACCESS DENIED")
                st.session_state.auth_lock = False
            except:
                st.error("SYSTEM ERROR: CHECK SECRETS")
                st.session_state.auth_lock = False

    st.stop()

# --------------------------------------------------
# 4. USER AUTO-SYNC
# --------------------------------------------------
role = st.session_state.user_role
if role != "admin":
    if "local_version" not in st.session_state:
        st.session_state.local_version = D["version"]

    if D["version"] != st.session_state.local_version:
        st.session_state.local_version = D["version"]
        st.toast("🔄 Deal Updated by Admin")
        st.rerun()

# --------------------------------------------------
# 5. ADMIN DEAL CONTROL
# --------------------------------------------------
if role == "admin":
    with st.expander("🛡️ ADMIN DEAL MANAGEMENT", expanded=False):
        c1, c2, c3 = st.columns(3)
        p = c1.number_input("Sales Price", value=D["price"])
        e = c2.number_input("Seller Equity", value=D["seller_equity"])
        f = c3.number_input("ULP Assignment Fee", value=D["assignment_fee"])

        if st.button("🔁 RESTRUCTURE & PUSH LIVE", use_container_width=True):
            D["price"], D["seller_equity"], D["assignment_fee"] = p, e, f
            D["version"] = deal_hash(D)
            st.toast("Deal pushed live")
            st.rerun()

# --------------------------------------------------
# 6. CORE DASHBOARD
# --------------------------------------------------
AITD = D["price"] - D["seller_equity"]

st.markdown(f"## Utah Land & Property")
st.caption(f"SESSION: {D['deal_id']} | ROLE: {role.upper()}")

c1, c2 = st.columns([2, 1])
with c1:
    st.metric("AITD Principal Balance", f"${AITD:,.2f}")
with c2:
    st.metric("ULP Assignment Fee", f"${D['assignment_fee']:,.2f}")

# --------------------------------------------------
# 7. TRANSACTION HUB
# --------------------------------------------------
st.markdown("### Transaction Hub")

v_col, n_col = st.columns([1.5, 1])

with v_col:
    if role == "admin" and st.button("📄 GENERATE PDF SETTLEMENT"):
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=LETTER)
        w, h = LETTER

        c.setFont("Helvetica-Bold", 18)
        c.drawString(72, h - 72, "Utah Land & Property – Settlement Summary")

        c.setFont("Helvetica", 12)
        y = h - 140
        for line in [
            f"Deal ID: {D['deal_id']}",
            f"Sales Price: ${D['price']:,.2f}",
            f"Seller Equity Credit: ${D['seller_equity']:,.2f}",
            f"AITD Balance: ${AITD:,.2f}",
            f"ULP Assignment Fee: ${D['assignment_fee']:,.2f}",
            "",
            f"Generated: {datetime.now().strftime('%m/%d/%Y %H:%M')}"
        ]:
            c.drawString(72, y, line)
            y -= 22

        c.showPage()
        c.save()
        buffer.seek(0)

        D["vault"].append({
            "name": f"Settlement_{D['deal_id']}.pdf",
            "content": buffer.read()
        })

        st.success("PDF Generated")

    for doc in D["vault"]:
        b64 = base64.b64encode(doc["content"]).decode()
        st.markdown(
            f'<a href="data:application/pdf;base64,{b64}" download="{doc["name"]}">📥 {doc["name"]}</a>',
            unsafe_allow_html=True
        )

with n_col:
    note = st.text_input("Add Note", label_visibility="collapsed")
    if st.button("Post") and note:
        D["notes"].insert(0, f"{datetime.now().strftime('%H:%M')} – {note}")
        st.rerun()

    for n in D["notes"]:
        st.markdown(f"- {n}")

# --------------------------------------------------
# 8. LOGOUT
# --------------------------------------------------
if st.sidebar.button("LOGOUT"):
    st.session_state.authenticated = False
    st.rerun()
