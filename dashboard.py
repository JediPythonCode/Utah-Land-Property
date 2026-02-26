import streamlit as st
import streamlit.components.v1 as components
import os
from automation_engine import generate_utah_addendum
from library import SHIELD_LIBRARY

# --- 1. PAGE SETUP ---
st.set_page_config(
    page_title="Utah Land & Property | Secure Asset Portal",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. PASSWORD ---
SECRET_PASSWORD = st.secrets.get("acquisition_password", "defaultpassword")

# --- 3. HIDE STREAMLIT UI ---
st.markdown("""
    <style>
        #MainMenu, footer, header {visibility: hidden;}
        .block-container {padding: 0;}
        [data-testid="stAppViewContainer"] { background-color: #fcfcfc; }
    </style>
""", unsafe_allow_html=True)

# --- 4. SHIELDS AND CONTRACTS ---
shield_keys = list(SHIELD_LIBRARY.keys())
contracts_list = ["REPC"] + [k for k in SHIELD_LIBRARY.keys() if k != "REPC"]

# --- 5. HTML LAYOUT ---
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
#dashboard-view {{ display:none; opacity:0; transition: opacity 1s ease-in-out; }}
.glass-card {{ background:white; border:1px solid #e5e7eb; box-shadow:0 4px 15px rgba(0,0,0,0.03); }}
.fade-out-up {{ transform:translateY(-100%); opacity:0; }}
.visible {{ display:block !important; opacity:1 !important; }}
label {{ font-size:10px; text-transform:uppercase; font-weight:bold; color:#6b7280; }}
input, select {{ font-size:14px; padding:0.5rem; border:1px solid #d1d5db; border-radius:5px; width:100%; }}
.disclaimer {{ font-size:12px; font-weight:bold; color:white; }}
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
            <button onclick="handleLogin()" class="action-button">Enter Vault</button>
        </div>
    </div>
    <p class="mt-6 disclaimer">Utah Land & Property Inc, are not licensed real estate agents or brokers. We are investment professionals. All activity is monitored and compliant with Utah regulations.</p>
</section>

<section id="dashboard-view" class="min-h-screen bg-[#FDFDFD] pb-24">
    <div class="max-w-7xl mx-auto px-10 mt-16 grid grid-cols-1 lg:grid-cols-2 gap-10">
        <div class="glass-card p-12 flex flex-col">
            <h2 class="font-serif text-3xl mb-8">Property & Contract Details</h2>
            <div class="space-y-4">
                <div>
                    <label>Seller Name</label>
                    <input type="text" id="seller-name-input" value="Owen">
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

<script>
const SECRET_PASSWORD = "{SECRET_PASSWORD}";

function handleLogin() {{
    const entered = document.getElementById('main-search').value;
    if(entered !== SECRET_PASSWORD) {{
        alert('Invalid Acquisition ID');
        return;
    }}
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
    const selected = Array.from(document.getElementById('contracts-select').selectedOptions).map(opt => opt.value);
    if(!addr || !name){{
        alert("Seller name and address are required.");
        return;
    }}
    const preview = "Seller: " + name + "\\nAddress: " + addr + "\\nParcel ID: " + parcel + "\\nSelected Contracts: " + selected.join(', ');
    document.getElementById('preview-area').value = preview;

    // send to Streamlit sidebar for PDF generation
    window.parent.postMessage({{type:'execute_contract', seller:name, address:addr, parcel:parcel, contracts:selected}}, '*');
    alert("Preview generated. Confirm in sidebar to download PDF.");
}}
</script>
</body>
</html>
"""

# --- 6. RENDER HTML ---
components.html(html_content, height=1000, scrolling=True)

# --- 7. SIDEBAR PDF ENGINE ---
with st.sidebar:
    st.markdown("### 🏔️ SECURE PRINTER TRAY")
    st.info("Preview contracts above, then click below to generate your PDF.")

    final_seller = st.text_input("Confirm Seller", "Owen")
    final_addr = st.text_input("Confirm Address", "")
    final_parcel = st.text_input("Confirm Parcel ID", "")
    final_contracts = st.text_area("Confirm Contracts Selected (comma separated)")

    if st.button("Generate & Download PDF"):
        if not final_addr or not final_seller:
            st.error("Seller Name and Address are required.")
        elif not final_contracts.strip():
            st.error("Please select at least one contract.")
        else:
            contracts_list_final = [c.strip() for c in final_contracts.split(",")]
            # Prepare deal data
            deal_data = {
                "seller_first": final_seller.split()[0],
                "seller_last": " ".join(final_seller.split()[1:]) if len(final_seller.split())>1 else "",
                "address": final_addr,
                "repc_date": "02/26/2026",
                "addendum_no": "1",
                "acceptance_date": "03/01/2026",
                "acceptance_time": "5:00 PM"
            }
            try:
                pdf_path = generate_utah_addendum(deal_data, contracts_list_final)
                if os.path.exists(pdf_path):
                    with open(pdf_path, "rb") as f:
                        st.download_button(
                            label="CLICK TO SAVE FINAL PDF",
                            data=f,
                            file_name=f"Addendum_{final_seller}.pdf",
                            mime="application/pdf"
                        )
            except Exception as e:
                st.error(f"Error generating PDF: {e}")
