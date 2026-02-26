import streamlit as st
import streamlit.components.v1 as components
import os
from datetime import datetime
from automation_engine import generate_utah_addendum
from library import SHIELD_LIBRARY

# --- 1. PAGE SETUP ---
st.set_page_config(
    page_title="Utah Land & Property | Secure Asset Portal",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed" 
)

# --- 2. SESSION STATE (TRACKS LOGIN) ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# --- 3. CSS: NO GAPS & CONDITIONAL SIDEBAR ---
# We hide the sidebar trigger button completely until authenticated
hide_sidebar_style = """
    <style>
        #MainMenu, footer, header {visibility: hidden;}
        .block-container { padding: 0rem !important; max-width: 100% !important; }
        [data-testid="stSidebar"] { 
            background-color: #631D33 !important; 
            color: white !important; 
        }
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] label { color: white !important; }
        .stButton>button { background-color: #D4AF37 !important; color: black !important; font-weight: bold; width: 100%; }
    </style>
"""
if not st.session_state["authenticated"]:
    hide_sidebar_style += "[data-testid='collapsedControl'] {display: none;}"

st.markdown(hide_sidebar_style, unsafe_allow_html=True)

# --- 4. LOGIC PREP ---
SECRET_PASSWORD = st.secrets.get("acquisition_password", "gold2026")
contracts_list = ["REPC"] + [k for k in SHIELD_LIBRARY.keys() if k != "REPC"]

# --- 5. AUTHENTICATION / HERO VIEW ---
if not st.session_state["authenticated"]:
    # This only shows the login screen
    html_login = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Montserrat:wght@300;400;600&display=swap" rel="stylesheet">
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            :root {{ --bhhs-cabernet: #631D33; --overlay: rgba(0, 0, 0, 0.45); }}
            body, html {{ margin:0; padding:0; font-family:'Montserrat', sans-serif; overflow:hidden; }}
            .hero-container {{ position:relative; height:100vh; width:100vw; background-image: linear-gradient(var(--overlay), var(--overlay)), url('https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&q=80&w=2070'); background-size:cover; background-position:center; display:flex; flex-direction:column; align-items:center; justify-content:center; color:white; text-align:center; }}
            .action-bar {{ background:white; padding:0.5rem; display:flex; width:90%; max-width:900px; box-shadow:0 10px 40px rgba(0,0,0,0.4); }}
            .action-input {{ flex-grow:1; border:none; padding:1.2rem 2rem; font-size:1rem; color:#333; outline:none; }}
            .action-button {{ background:var(--bhhs-cabernet); color:white; padding:0 2.5rem; text-transform:uppercase; letter-spacing:2px; font-size:0.8rem; font-weight:600; border:none; }}
            .disclaimer {{ font-size:12px; font-weight:bold; color:white; margin-top: 2rem; max-width: 800px; line-height: 1.4; }}
        </style>
    </head>
    <body>
        <section class="hero-container">
            <header class="absolute top-0 left-0 p-10">
                <div class="text-2xl font-bold font-serif tracking-tight">UTAH LAND & PROPERTY</div>
            </header>
            <div class="z-10 px-6 text-center flex flex-col items-center">
                <h1 class="text-7xl font-serif font-bold mb-2">Precision Acquisition.</h1>
                <p class="text-[0.9rem] uppercase tracking-[6px] mb-12 font-300">The Gold Standard in Utah Land Asset Strategy.</p>
                <form action="/" method="get" class="action-bar" onsubmit="window.parent.postMessage({{type: 'login', password: document.getElementById('pw').value}}, '*')">
                    <input type="password" id="pw" class="action-input" placeholder="Enter Acquisition ID...">
                    <button type="button" onclick="parent.postMessage({{type: 'login', pw: document.getElementById('pw').value}}, '*')" class="action-button">Enter Vault</button>
                </form>
                <p class="disclaimer">Utah Land & Property Inc, are not licensed real estate agents or brokers. We are investment professionals. All activity is monitored and compliant with Utah regulations.</p>
            </div>
        </section>
    </body>
    </html>
    """
    # Streamlit bridge for login
    from streamlit_javascript import st_javascript
    login_event = st_javascript("""
        window.addEventListener('message', function(e) {
            if (e.data.type === 'login') {
                window.parent.postMessage({type: 'auth_success', pw: e.data.pw}, '*');
            }
        });
    """)
    
    # Simple Streamlit input to handle the auth redirect
    auth_check = st.text_input("Vault Security Check (Repeat Password to Confirm)", type="password")
    if auth_check == SECRET_PASSWORD:
        st.session_state["authenticated"] = True
        st.rerun()
    else:
        components.html(html_login, height=1000)

# --- 6. POST-LOGIN DASHBOARD ---
else:
    # Sidebar is now visible
    with st.sidebar:
        st.title("🏔️ PRINTER TRAY")
        sel_date = st.date_input("Contract Date", datetime.now())
        st.markdown("---")
        f_n = st.text_input("Seller", value="Owen")
        f_a = st.text_input("Address")
        f_p = st.text_input("Parcel ID")
        f_t = st.text_area("Docs (e.g., REPC)")
        
        if st.button("GENERATE PDF"):
            deal_data = {"seller_name": f_n, "address": f_a, "parcel_id": f_p, "repc_date": sel_date.strftime("%m/%d/%Y")}
            pdf = generate_utah_addendum(deal_data, [c.strip() for c in f_t.split(",")])
            if pdf:
                with open(pdf, "rb") as f:
                    st.download_button("📥 DOWNLOAD", f, file_name=f"REPC_{f_n}.pdf")

    # Main Dashboard UI
    html_dash = f"""
    <div style="padding: 5rem; background: #fcfcfc; min-height: 100vh; font-family: Montserrat;">
        <h2 style="font-family: 'Playfair Display'; font-size: 2rem;">Acquisition Dashboard</h2>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 40px; margin-top: 40px;">
            <div style="background: white; padding: 40px; border: 1px solid #eee;">
                <h3 style="margin-bottom: 20px;">Property Details</h3>
                <p>Verify all data points. Once synced, use the <b>Cabernet Sidebar</b> on the left to finalize the date and print.</p>
            </div>
            <div style="background: white; padding: 40px; border: 1px solid #eee;">
                <h3>Status</h3>
                <p style="color: green; font-weight: bold;">VAULT ACTIVE</p>
            </div>
        </div>
    </div>
    """
    st.markdown(html_dash, unsafe_allow_html=True)
