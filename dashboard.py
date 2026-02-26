import streamlit as st
import streamlit.components.v1 as components
import os

# --- 1. CORE LOGIC ---
try:
    from library import SHIELD_LIBRARY
    from automation_engine import generate_utah_addendum
except ImportError:
    # fallback for dev
    SHIELD_LIBRARY = {k: "Active" for k in [
        "Active Logic Shields","Assignment_Gator","Marketing_Rights","SubTo_Disclosure",
        "Non_Agency_61_2f","Market_Value_Disclaimer","FinCEN_2026","BOI_Compliance",
        "Legacy_Unit_SNDA","Shared_Parking_REA","As_Is_Condition","Condition_Claims_Release",
        "Seller_Defect_Disclosure","Equitable_Interest_Only","Recording_Prohibition",
        "Seller_Title_Warranty","Closing_Cooperation","Unrestricted_Assignment",
        "Closing_Extension_Option","Buyer_Default_Limited_Remedy","Seller_Indemnification",
        "Governing_Law_Utah","Prevailing_Party_Attorney_Fees","Entire_Agreement",
        "Severability","Time_Is_Essence","Electronic_Signatures","Force_Majeure_2026",
        "Bankruptcy_Warranty","Commission_Waiver"
    ]}
    def generate_utah_addendum(data, shields):
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

# Hide Streamlit UI completely
st.markdown("""
    <style>
        #MainMenu, footer, header {visibility: hidden;}
        .block-container {padding: 0;}
        [data-testid="stAppViewContainer"] { background-color: #fcfcfc; }
    </style>
""", unsafe_allow_html=True)

# --- 4. LOGIN ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.markdown("""
    <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:100vh;background-image: linear-gradient(rgba(0,0,0,0.45), rgba(0,0,0,0.45)), url('https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&q=80&w=2070'); background-size:cover; background-position:center;">
        <h1 style="color:white;font-family:'Playfair Display', serif;font-size:4rem;margin-bottom:1rem;">Precision Acquisition.</h1>
        <p style="color:white;text-transform:uppercase;letter-spacing:6px;">The Gold Standard in Utah Land Asset Strategy.</p>
        <form method="post">
            <input type="password" name="acq_pass" placeholder="Enter Acquisition ID..." style="padding:1rem 2rem;margin-top:2rem;font-size:1rem;border:none;border-radius:5px;">
            <button type="submit" style="padding:1rem 3rem;margin-top:1rem;background:#631D33;color:white;border:none;text-transform:uppercase;letter-spacing:2px;font-weight:600;cursor:pointer;">Access Vault</button>
        </form>
        <p style="color:white;font-size:10px;margin-top:2rem;">Utah Land & Property Inc, are not licensed real estate agents or real estate brokers. We are investment professionals. All activity is monitored and compliant with Utah state regulations.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check password
    if st.experimental_get_query_params().get("acq_pass"):
        entered = st.experimental_get_query_params().get("acq_pass")[0]
        if entered == SECRET_PASSWORD:
            st.session_state['authenticated'] = True
            st.experimental_rerun()
    elif st.session_state.get('authenticated') == False:
        st.stop()  # stop rendering dashboard until authenticated

# --- 5. DASHBOARD LAYOUT ---
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
:root {{ --bhhs-cabernet: #631D33; }}
body, html {{ margin:0; padding:0; font-family:'Montserrat', sans-serif; background-color:#fcfcfc; color:#1a1a1a; overflow-x:hidden; }}
.hero-container {{ display:none; }}
.glass-card {{ background:white; border:1px solid #e5e7eb; box-shadow:0 4px 15px rgba(0,0,0,0.03); }}
label {{ font-size:10px; text-transform:uppercase; font-weight:bold; color:#6b7280; }}
input, select, textarea {{ font-size:14px; padding:0.5rem; border:1px solid #d1d5db; border-radius:5px; width:100%; }}
.action-button {{ background:var(--bhhs-cabernet); color:white; padding:0.5rem 1rem; border:none; text-transform:uppercase; font-weight:600; cursor:pointer; }}
</style>
</head>
<body>
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
                    <button onclick="handleExecution()" class="w-full action-button">Preview & Bind Contracts</button>
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
}}
</script>
</body>
</html>
"""

# Render HTML
components.html(html_content, height=1000, scrolling=True)

# --- 6. SIDEBAR PDF ENGINE ---
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
            data = {
                "seller_first": final_seller.split()[0],
                "seller_last": " ".join(final_seller.split()[1:]) if len(final_seller.split())>1 else "",
                "address": final_addr,
                "parcel": final_parcel,
                "repc_date": "02/26/2026",
                "addendum_no": "1"
            }
            path = generate_utah_addendum(data, contracts_list_final)
            if os.path.exists(path):
                with open(path, "rb") as f:
                    st.download_button(
                        label="CLICK TO SAVE FINAL PDF",
                        data=f,
                        file_name=f"Addendum_{final_seller}.pdf",
                        mime="application/pdf"
                    )
