import streamlit as st
import streamlit.components.v1 as components
import os
import pypdf
from datetime import datetime, timedelta

# --- 1. PAGE SETUP ---
st.set_page_config(
    page_title="Utah Land & Property | Secure Asset Portal",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. ENGINE (THE SERIOUS MATTER) ---
def generate_asset_packet(deal_data, selected_contracts):
    output_files = []
    # Stochastic deadlines for 2026
    today = datetime(2026, 2, 26)
    dd_deadline = (today + timedelta(days=14)).strftime("%m/%d/%Y")
    settlement = (today + timedelta(days=30)).strftime("%m/%d/%Y")

    field_mapping = {
        "Seller": deal_data['seller_name'],
        "Buyer": "Utah Land & Property Inc",
        "Property Address": deal_data['address'],
        "Tax ID Parcel No": deal_data['parcel'],
        "Date": "02/26/2026",
        "Due Diligence Deadline": dd_deadline,
        "Settlement Deadline": settlement,
        "Addendum No": "1"
    }

    for contract in selected_contracts:
        # Use the exact paths you uploaded to GitHub
        if "REPC" in contract:
            template_path = "forms/utah_repc_template.pdf"
        else:
            template_path = "forms/utah_blank_addendum.pdf"

        if not os.path.exists(template_path):
            continue

        output_path = f"{contract}_{deal_data['seller_name'].replace(' ', '_')}.pdf"
        
        reader = pypdf.PdfReader(template_path)
        writer = pypdf.PdfWriter()

        for page in reader.pages:
            writer.add_page(page)
            writer.update_page_form_field_values(writer.pages[-1], field_mapping)

        with open(output_path, "wb") as f:
            writer.write(f)
        output_files.append(output_path)
    
    return output_files[0] if output_files else None

# --- 3. UI STYLE & AUTH ---
SECRET_PASSWORD = st.secrets.get("acquisition_password", "gold2026")

st.markdown("""
    <style>
        #MainMenu, footer, header {visibility: hidden;}
        .block-container {padding: 0;}
        [data-testid="stAppViewContainer"] { background-color: #fcfcfc; }
        [data-testid="stSidebar"] { background-color: #1a1a1a; border-left: 1px solid #333; }
        .stButton>button { background-color: #631D33 !important; color: white !important; width: 100%; border-radius: 0; height: 50px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- 4. THE DESIGN (KEEPING YOUR EXACT HTML/CSS) ---
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
.glass-card {{ background:white; border:1px solid #e5e7eb; box-shadow:0 4px 15px rgba(0,0,0,0.03); padding: 3rem; }}
.visible {{ display:block !important; opacity:1 !important; }}
label {{ font-size:10px; text-transform:uppercase; font-weight:bold; color:#6b7280; }}
input, select {{ font-size:14px; padding:0.5rem; border:1px solid #d1d5db; border-radius:5px; width:100%; color: black; }}
.disclaimer {{ font-size:12px; font-weight:bold; color:white; }}
</style>
</head>
<body>
<section id="hero-section" class="hero-container">
    <header class="absolute top-0 left-0 p-10">
        <div class="text-2xl font-bold font-serif tracking-tight">UTAH LAND & PROPERTY</div>
    </header>
    <div class="z-10 px-6 text-center">
        <h1 class="text-7xl font-serif font-bold mb-2">Precision Acquisition.</h1>
        <p class="text-[0.9rem] uppercase tracking-[6px] mb-12 font-300">The Gold Standard in Utah Land Asset Strategy.</p>
        <div class="action-bar mx-auto">
            <input type="password" id="main-search" class="action-input" placeholder="Enter Acquisition ID...">
            <button onclick="handleLogin()" class="action-button">Enter Vault</button>
        </div>
    </div>
    <p class="mt-6 disclaimer">Utah Land & Property Inc. Activity monitored and compliant.</p>
</section>

<section id="dashboard-view" class="min-h-screen bg-[#FDFDFD] pb-24">
    <div class="max-w-7xl mx-auto px-10 mt-16 grid grid-cols-1 lg:grid-cols-2 gap-10">
        <div class="glass-card flex flex-col">
            <h2 class="font-serif text-3xl mb-8">Property & Contract Details</h2>
            <div class="space-y-4">
                <div><label>Seller Name</label><input type="text" id="s-name" value="Owen"></div>
                <div><label>Property Address</label><input type="text" id="s-addr" placeholder="Enter Utah Address"></div>
                <div><label>Parcel ID</label><input type="text" id="s-parcel" placeholder="Enter Parcel ID"></div>
                <div>
                    <label>Select Contracts</label>
                    <select id="s-contracts" multiple size="4">
                        <option value="REPC" selected>REPC</option>
                        <option value="ADDENDUM">ADDENDUM</option>
                    </select>
                </div>
                <div class="pt-6">
                    <button onclick="syncToSidebar()" class="w-full bg-[var(--bhhs-cabernet)] text-white py-4 font-bold uppercase tracking-[2px] text-xs">Preview & Sync to Printer</button>
                </div>
            </div>
        </div>
        <div class="glass-card">
            <h2 class="font-serif text-3xl mb-8">Contract Preview</h2>
            <textarea id="preview-box" rows="12" class="w-full border p-4 font-mono text-sm" readonly></textarea>
        </div>
    </div>
</section>

<script>
function handleLogin() {{
    const entered = document.getElementById('main-search').value;
    if(entered === "{SECRET_PASSWORD}") {{
        document.getElementById('hero-section').style.display = 'none';
        document.getElementById('dashboard-view').classList.add('visible');
    }} else {{ alert('Invalid Acquisition ID'); }}
}}

function syncToSidebar() {{
    const name = document.getElementById('s-name').value;
    const addr = document.getElementById('s-addr').value;
    const parcel = document.getElementById('s-parcel').value;
    const date = "02/26/2026";
    
    document.getElementById('preview-box').value = "VERIFIED ASSET PACKET\\nDATE: " + date + "\\nSELLER: " + name + "\\nADDR: " + addr + "\\nPARCEL: " + parcel + "\\nSTATUS: SYNCED";
    alert("Data Synced. Open Sidebar to Print.");
}}
</script>
</body>
</html>
"""

components.html(html_content, height=1000, scrolling=True)

# --- 5. SIDEBAR ---
with st.sidebar:
    st.markdown("### 🏔️ SECURE PRINTER TRAY")
    st.info("Ensure the fields below match your dashboard preview.")
    
    f_name = st.text_input("Confirm Seller", value="Owen")
    f_addr = st.text_input("Confirm Address")
    f_parcel = st.text_input("Confirm Parcel ID")
    f_type = st.multiselect("Docs", ["REPC", "ADDENDUM"], default=["REPC"])

    if st.button("EXECUTE BINDING & DOWNLOAD"):
        if f_name and f_addr:
            deal_data = {"seller_name": f_name, "address": f_addr, "parcel": f_parcel}
            try:
                final_path = generate_asset_packet(deal_data, f_type)
                if final_path:
                    with open(final_path, "rb") as f:
                        st.download_button("📥 DOWNLOAD FINALIZED PDF", f, file_name=final_path)
            except Exception as e:
                st.error(f"Mapping Error: {e}")
