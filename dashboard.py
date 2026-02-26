import streamlit as st
import streamlit.components.v1 as components
import os
import json

# --- 1. CORE LOGIC ---
try:
    from library import SHIELD_LIBRARY
    from automation_engine import generate_utah_addendum
except ImportError:
    # fallback for dev
    SHIELD_LIBRARY = {
        "Active Logic Shields": "Active",
        "Assignment_Gator": "Active",
        "Marketing_Rights": "Active",
        "SubTo_Disclosure": "Active",
        "Non_Agency_61_2f": "Active",
        "Market_Value_Disclaimer": "Active",
        "FinCEN_2026": "Active",
        "BOI_Compliance": "Active",
        "Legacy_Unit_SNDA": "Active",
        "Shared_Parking_REA": "Active",
        "As_Is_Condition": "Active",
        "Condition_Claims_Release": "Active",
        "Seller_Defect_Disclosure": "Active",
        "Equitable_Interest_Only": "Active",
        "Recording_Prohibition": "Active",
        "Seller_Title_Warranty": "Active",
        "Closing_Cooperation": "Active",
        "Unrestricted_Assignment": "Active",
        "Closing_Extension_Option": "Active",
        "Buyer_Default_Limited_Remedy": "Active",
        "Seller_Indemnification": "Active",
        "Governing_Law_Utah": "Active",
        "Prevailing_Party_Attorney_Fees": "Active",
        "Entire_Agreement": "Active",
        "Severability": "Active",
        "Time_Is_Essence": "Active",
        "Electronic_Signatures": "Active",
        "Force_Majeure_2026": "Active",
        "Bankruptcy_Warranty": "Active",
        "Commission_Waiver": "Active"
    }

    def generate_utah_addendum(data, shields):
        # dummy PDF for testing
        return "temp.pdf"

# --- 2. PAGE SETUP ---
st.set_page_config(
    page_title="Utah Land & Property | Secure Asset Portal",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 3. PASSWORD SECRET ---
SECRET_PASSWORD = st.secrets.get("acquisition_password", "defaultpassword")

# Hide Streamlit default UI
st.markdown("""
    <style>
        #MainMenu, footer, header {visibility: hidden;}
        .block-container {padding: 0;}
        [data-testid="stAppViewContainer"] { background-color: #fcfcfc; }
    </style>
""", unsafe_allow_html=True)

# --- 4. HTML DASHBOARD ---
shield_keys = list(SHIELD_LIBRARY.keys())

# Contract options: REPC first
contracts = ["REPC"] + [k for k in shield_keys]

html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Montserrat:wght@300;400;600&display=swap" rel="stylesheet">
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
:root {{ --bhhs-cabernet: #631D33; --overlay: rgba(0,0,0,0.35); }}
body, html {{ margin:0; padding:0; font-family: 'Montserrat', sans-serif; background-color:#fcfcfc; overflow-x:hidden; }}
.hero-container {{
    position: relative;
    height: 100vh;
    width: 100%;
    background-image: linear-gradient(var(--overlay), var(--overlay)), url('https://images.unsplash.com/photo-1572120360610-d971b9b6399d?auto=format&fit=crop&w=2070&q=80');
    background-size: cover;
    background-position: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: white;
    text-align: center;
    transition: transform 0.8s cubic-bezier(0.4,0,0.2,1), opacity 0.6s ease;
}}
.action-bar {{ background:white; padding:0.5rem; display:flex; width:90%; max-width:900px; box-shadow:0 10px 40px rgba(0,0,0,0.4); }}
.action-input {{ flex-grow:1; border:none; padding:1.2rem 2rem; font-size:1rem; color:#333; outline:none; }}
.action-button {{ background:var(--bhhs-cabernet); color:white; padding:0 2.5rem; text-transform:uppercase; letter-spacing:2px; font-size:0.8rem; font-weight:600; cursor:pointer; border:none; }}
#portal-overlay {{ position: fixed; inset:0; background: rgba(99,29,51,0.98); z-index:100; display:none; flex-direction:column; align-items:center; justify-content:center; color:white; backdrop-filter:blur(10px); }}
.portal-card {{ background:white; padding:3.5rem; width:100%; max-width:480px; text-align:center; color:#333; }}
#dashboard-view {{ display:none; opacity:0; transition: opacity 1s ease-in-out; }}
.glass-card {{ background:white; border:1px solid #e5e7eb; box-shadow:0 4px 15px rgba(0,0,0,0.03); }}
.accent-border {{ border-left:5px solid var(--bhhs-cabernet); }}
.fade-out-up {{ transform: translateY(-100%); opacity:0; }}
.visible {{ display:block !important; opacity:1 !important; }}
.contract-list input {{ margin-right:0.5rem; }}
</style>
</head>
<body>
<section id="hero-section" class="hero-container">
    <header class="absolute top-0 w-full p-10 flex justify-between items-center">
        <div class="flex flex-col text-left">
            <div class="text-2xl font-bold font-serif tracking-tight">UTAH LAND & PROPERTY</div>
            <div class="text-[0.65rem] uppercase tracking-[3px]">Acquisition, Investment, Development</div>
        </div>
    </header>
    <div class="z-10 px-6">
        <h1 class="text-7xl font-serif font-bold mb-2">Precision Acquisition.</h1>
        <p class="text-[0.9rem] uppercase tracking-[6px] mb-6 font-300">The Gold Standard in Utah Land Asset Strategy.</p>
        <p class="text-[10px] mb-12 text-gray-200">Utah Land & Property Inc, are not licensed real estate agents or real estate brokers. We are investment professionals. All activity is monitored and compliant with Utah state regulations.</p>
        <div class="action-bar mx-auto">
            <input type="password" id="main-search" class="action-input" placeholder="Enter Acquisition ID...">
            <button onclick="togglePortal()" class="action-button">Access Vault</button>
        </div>
    </div>
</section>

<section id="dashboard-view" class="min-h-screen bg-[#FDFDFD] pb-24">
    <div class="max-w-7xl mx-auto px-10 mt-16">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-10 mb-16">
            <div class="glass-card p-12">
                <h2 class="font-serif text-3xl mb-8">Contract Execution Center</h2>
                <div>
                    <label class="text-[10px] uppercase font-bold text-gray-400">Seller Name</label>
                    <input type="text" id="seller-name-input" value="Owen" class="w-full border-b border-gray-200 py-2 outline-none font-bold text-lg mb-4">
                </div>
                <div>
                    <label class="text-[10px] uppercase font-bold text-gray-400">Property Address</label>
                    <input type="text" id="property-address-input" placeholder="Enter Utah Address..." class="w-full border-b border-gray-200 py-2 outline-none font-bold text-lg mb-4">
                </div>
                <div>
                    <label class="text-[10px] uppercase font-bold text-gray-400">Parcel ID</label>
                    <input type="text" id="parcel-id-input" placeholder="Parcel ID..." class="w-full border-b border-gray-200 py-2 outline-none font-bold text-lg mb-4">
                </div>
                <div>
                    <label class="text-[10px] uppercase font-bold text-gray-400">Select Contracts / Addenda</label>
                    <div class="contract-list flex flex-col gap-2 mt-2">
                        {"".join([f'<label><input type="checkbox" class="contract-checkbox" value="{c}">{c}</label>' for c in contracts])}
                    </div>
                </div>
                <div class="pt-6">
                    <button onclick="handleExecution()" class="w-full bg-[var(--bhhs-cabernet)] text-white py-4 font-bold uppercase tracking-[2px] text-xs">Execute & Preview</button>
                </div>
            </div>
            <div class="glass-card p-12">
                <h2 class="font-serif text-3xl mb-8">Contract Preview Center</h2>
                <textarea id="preview-area" class="w-full h-[400px] border border-gray-200 p-4 font-mono text-xs"></textarea>
            </div>
        </div>
    </div>
</section>

<div id="portal-overlay">
    <div class="portal-card shadow-2xl">
        <div class="text-[var(--bhhs-cabernet)] font-serif text-3xl mb-3">Private Access Vault</div>
        <p class="text-[10px] uppercase tracking-[3px] text-gray-400 mb-12">Authorized Client Entrance Only</p>
        <button onclick="handleLogin()" class="w-full bg-[var(--bhhs-cabernet)] text-white py-4 font-bold uppercase">Enter Secure Portal</button>
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
    const name = document.getElementById('seller-name-input').value;
    const addr = document.getElementById('property-address-input').value;
    const parcel = document.getElementById('parcel-id-input').value;
    const selected = Array.from(document.querySelectorAll('.contract-checkbox'))
                        .filter(c => c.checked)
                        .map(c => c.value);
    const preview = `Seller: ${name}\\nAddress: ${addr}\\nParcel ID: ${parcel}\\nSelected Contracts: ${selected.join(', ')}`;
    document.getElementById('preview-area').value = preview;

    window.parent.postMessage({{
        type: 'execute_contract',
        seller: name,
        address: addr,
        parcel: parcel,
        contracts: selected
    }}, '*');
    alert("Contracts prepared for preview. Proceed to sidebar for PDF generation.");
}}
</script>
</body>
</html>
"""

# --- 5. RENDER HTML ---
components.html(html_content, height=1000, scrolling=True)

# --- 6. SIDEBAR PDF ENGINE ---
with st.sidebar:
    st.markdown("### 💰 SECURE PRINTER TRAY")
    st.info("Fill out inputs in the dashboard, select contracts, then click Execute & Preview to populate preview. Your PDF will appear here.")
    
    with st.expander("Stochastic Engine Settings", expanded=True):
        final_seller = st.text_input("Confirm Seller", "Owen")
        final_addr = st.text_input("Confirm Address", "")
        final_parcel = st.text_input("Confirm Parcel ID", "")
        selected_contracts = st.text_area("Selected Contracts", "")

    if st.button("Generate & Download PDF"):
        if not final_addr:
            st.error("Address Required.")
        elif not selected_contracts.strip():
            st.error("Select at least one contract.")
        else:
            data = {
                "seller": final_seller,
                "address": final_addr,
                "parcel": final_parcel,
                "contracts": selected_contracts.splitlines(),
                "addendum_no": "1"
            }
            path = generate_utah_addendum(data, shield_keys)
            if os.path.exists(path):
                with open(path, "rb") as f:
                    st.download_button(
                        label="CLICK TO SAVE FINAL PDF",
                        data=f,
                        file_name=f"Addendum_{final_seller}.pdf",
                        mime="application/pdf"
                    )
