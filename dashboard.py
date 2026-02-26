import streamlit as st
import streamlit.components.v1 as components
import os
from library import SHIELD_LIBRARY
from automation_engine import generate_utah_addendum

# --- 1. PAGE SETUP ---
st.set_page_config(
    page_title="Utah Land & Property | Secure Asset Portal",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. PASSWORD SECRET ---
SECRET_PASSWORD = st.secrets.get("acquisition_password", "defaultpassword")

# Hide default Streamlit UI
st.markdown("""
    <style>
        #MainMenu, footer, header {visibility: hidden;}
        .block-container {padding: 0;}
        [data-testid="stAppViewContainer"] { background-color: #fcfcfc; }
    </style>
""", unsafe_allow_html=True)

# --- 3. HTML LAYOUT ---
shield_keys = list(SHIELD_LIBRARY.keys())
contracts_list = ["REPC"] + [k for k in SHIELD_LIBRARY.keys() if k != "REPC"]

html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Montserrat:wght@300;400;600&display=swap" rel="stylesheet">
<script src="https://cdn.tailwindcss.com"></script>
<style>
:root {{ --bhhs-cabernet: #631D33; --overlay: rgba(0, 0, 0, 0.45); }}
body, html {{ margin:0; padding:0; font-family:'Montserrat', sans-serif; background-color:#fcfcfc; color:#1a1a1a; overflow-x:hidden; }}
.hero-container {{ position:relative; height:100vh; width:100%; background-image: linear-gradient(var(--overlay), var(--overlay)), url('https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&q=80&w=2070'); background-size:cover; background-position:center; display:flex; flex-direction:column; align-items:center; justify-content:center; color:white; text-align:center; transition: transform 0.8s ease, opacity 0.6s ease; }}
.action-bar {{ background:white; padding:0.5rem; display:flex; width:90%; max-width:900px; box-shadow:0 10px 40px rgba(0,0,0,0.4); }}
.action-input {{ flex-grow:1; border:none; padding:1.2rem 2rem; font-size:1rem; color:#333; outline:none; }}
.action-button {{ background:var(--bhhs-cabernet); color:white; padding:0 2.5rem; text-transform:uppercase; letter-spacing:2px; font-size:0.8rem; font-weight:600; cursor:pointer; border:none; }}
#portal-overlay {{ position:fixed; inset:0; background: rgba(99,29,51,0.95); z-index:100; display:none; flex-direction:column; align-items:center; justify-content:center; color:white; backdrop-filter: blur(10px); }}
.portal-card {{ background:white; padding:3.5rem; width:100%; max-width:480px; text-align:center; color:#333; }}
#dashboard-view {{ display:none; opacity:0; transition: opacity 1s ease-in-out; }}
.glass-card {{ background:white; border:1px solid #e5e7eb; box-shadow:0 4px 15px rgba(0,0,0,0.03); }}
.fade-out-up {{ transform:translateY(-100%); opacity:0; }}
.visible {{ display:block !important; opacity:1 !important; }}
label {{ font-size:10px; text-transform:uppercase; font-weight:bold; color:#6b7280; }}
input, select {{ font-size:14px; padding:0.5rem; border:1px solid #d1d5db; border-radius:5px; width:100%; }}
</style>
</head>
<body>
<section id="hero-section" class="hero-container">
    <header class="absolute top-0 left-0 p-10">
        <div class="text-2xl font-bold font-serif tracking-tight">UTAH LAND & PROPERTY</div>
        <div class="text-[0.65rem] uppercase tracking-[3px]">Acquisition, Investment, Development</div>
    </header>
    <div class="z-10 px-6 text-center">
        <h1 class="text-7xl font-serif font-bold mb-2">Precision Acquisition.</h1>
        <p class="text-[0.9rem] uppercase tracking-[6px] mb-12 font-300">The Gold Standard in Utah Land Asset Strategy.</p>
        <div class="action-bar mx-auto">
            <input type="password" id="main-search" class="action-input" placeholder="Enter Acquisition ID...">
            <button onclick="togglePortal()" class="action-button">Access Vault</button>
        </div>
    </div>
    <p class="mt-6 text-[10px] text-white">Utah Land & Property Inc, are not licensed real estate agents or real estate brokers. We are investment professionals. All activity is monitored and compliant with Utah state regulations.</p>
</section>

<section id="dashboard-view" class="min-h-screen bg-[#FDFDFD] pb-24">
    <div class="max-w-7xl mx-auto px-10 mt-16 grid grid-cols-1 lg:grid-cols-2 gap-10">
        <div class="glass-card p-12 flex flex-col">
            <h2 class="font-serif text-3xl mb-8">Property & Contract Details</h2>
            <div class="space-y-4">
                <div>
                    <label>Seller First Name</label>
                    <input type="text" id="seller-first-input" value="Owen">
                </div>
                <div>
                    <label>Seller Last Name</label>
                    <input type="text" id="seller-last-input" value="[Last Name]">
                </div>
                <div>
                    <label>Property Address</label>
                    <input type="text" id="property-address-input" placeholder="Enter Utah Address">
                </div>
                <div>
                    <label>Parcel ID</label>
                    <input type="text" id="parcel-id-input" placeholder="Enter Parcel ID">
                </div>
                <div>
                    <label>REPC Reference Date</label>
                    <input type="date" id="repc-date-input">
                </div>
                <div>
                    <label>Addendum No.</label>
                    <input type="number" id="addendum-no-input" value="1">
                </div>
                <div>
                    <label>Select Contracts / Addenda</label>
                    <select id="contracts-select" multiple size="10">
                        {''.join([f'<option value="{c}">{c}</option>' for c in contracts_list])}
                    </select>
                </div>
                <div class="pt-6">
                    <button onclick="handleExecution()" class="w-full bg-[var(--bhhs-cabernet)] text-white py-4 font-bold uppercase tracking-[2px] text-xs">Preview & Bind Contracts</button>
                </div>
            </div>
        </div>
        <div class="glass-card p-12">
            <h2 class="font-serif text-3xl mb-8">Preview</h2>
            <textarea id="preview-area" rows="15" class="w-full border p-4" readonly></textarea>
        </div>
    </div>
</section>

<div id="portal-overlay">
    <div class="portal-card shadow-2xl">
        <div class="text-[var(--bhhs-cabernet)] font-serif text-3xl mb-3">Private Access Vault</div>
        <input type="password" id="token" class="w-full border-b border-gray-300 py-3 outline-none mb-4 text-xl text-center" placeholder="••••••••">
        <button onclick="handleLogin()" class="w-full bg-[var(--bhhs-cabernet)] text-white py-4 font-bold uppercase">Enter Secure Portal</button>
        <p class="mt-6 text-[10px] text-gray-500">Utah Land & Property Inc, are not licensed real estate agents or real estate brokers. We are investment professionals. All activity is monitored and compliant with Utah state regulations.</p>
    </div>
</div>

<script>
const SECRET_PASSWORD = "{SECRET_PASSWORD}";

function togglePortal() {{
    const entered = document.getElementById('main-search').value;
    if (entered === SECRET_PASSWORD) {{
        document.getElementById('portal-overlay').style.display = 'flex';
    }} else {{
        alert('Invalid Acquisition ID');
    }}
}}

function handleLogin() {{
    document.getElementById('portal-overlay').style.display = 'none';
    document.getElementById('hero-section').classList.add('fade-out-up');
    setTimeout(() => {{
        document.getElementById('hero-section').style.display = 'none';
        document.getElementById('dashboard-view').classList.add('visible');
    }}, 700);
}}

function handleExecution() {{
    const sellerFirst = document.getElementById('seller-first-input').value;
    const sellerLast = document.getElementById('seller-last-input').value;
    const addr = document.getElementById('property-address-input').value;
    const parcel = document.getElementById('parcel-id-input').value;
    const repcDate = document.getElementById('repc-date-input').value;
    const addendumNo = document.getElementById('addendum-no-input').value;
    const selected = Array.from(document.getElementById('contracts-select').selectedOptions).map(opt => opt.value);

    if(!addr || !sellerFirst){{
        alert("Seller first name and address are required.");
        return;
    }}

    const preview = "Seller: " + sellerFirst + " " + sellerLast + "\\nAddress: " + addr + "\\nParcel ID: " + parcel + "\\nREPC Date: " + repcDate + "\\nAddendum No.: " + addendumNo + "\\nSelected Contracts: " + selected.join(', ');
    document.getElementById('preview-area').value = preview;

    window.parent.postMessage({{
        type:'execute_contract',
        seller_first: sellerFirst,
        seller_last: sellerLast,
        address: addr,
        parcel: parcel,
        repc_date: repcDate,
        addendum_no: addendumNo,
        contracts:selected
    }}, '*');

    alert("Preview generated. Confirm in sidebar to download PDF.");
}}
</script>
</body>
</html>
"""

# --- 4. RENDER HTML ---
components.html(html_content, height=1000, scrolling=True)

# --- 5. SIDEBAR PDF ENGINE ---
with st.sidebar:
    st.markdown("### 🏔️ SECURE PRINTER TRAY")
    st.info("Preview contracts above, then click below to generate your PDF.")

    final_seller_first = st.text_input("Confirm Seller First Name", "Owen")
    final_seller_last = st.text_input("Confirm Seller Last Name", "[Last Name]")
    final_addr = st.text_input("Confirm Address", "")
    final_parcel = st.text_input("Confirm Parcel ID", "")
    repc_date_input = st.text_input("Confirm REPC Date", "")
    addendum_number_input = st.text_input("Confirm Addendum No.", "1")
    final_contracts = st.text_area("Confirm Contracts Selected (comma separated)")

    if st.button("Generate & Download PDF"):
        if not final_addr or not final_seller_first:
            st.error("Seller Name and Address are required.")
        elif not final_contracts.strip():
            st.error("Please select at least one contract.")
        else:
            contracts_list_final = [c.strip() for c in final_contracts.split(",")]
            data = {
                "seller_first": final_seller_first,
                "seller_last": final_seller_last,
                "address": final_addr,
                "repc_date": repc_date_input,
                "addendum_no": addendum_number_input,
                "contracts": contracts_list_final
            }
            path = generate_utah_addendum(data, contracts_list_final)
            if os.path.exists(path):
                with open(path, "rb") as f:
                    st.download_button(
                        label="CLICK TO SAVE FINAL PDF",
                        data=f,
                        file_name=os.path.basename(path),
                        mime="application/pdf"
                    )
