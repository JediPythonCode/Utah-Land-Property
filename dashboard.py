import os
import streamlit as st
import streamlit.components.v1 as components
from automation_engine import generate_utah_addendum
from library import SHIELD_LIBRARY

# --- 1. PAGE SETUP ---
st.set_page_config(
    page_title="Utah Land & Property | Secure Asset Portal",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- 2. PASSWORD ---
SECRET_PASSWORD = st.secrets.get("acquisition_password", "defaultpassword")

# --- 3. SESSION STATE INITIALIZATION ---
if "authenticated" not in st.session_state:
  st.session_state.authenticated = False
if "form_seller" not in st.session_state:
  st.session_state.form_seller = "Owen"
if "form_address" not in st.session_state:
  st.session_state.form_address = ""
if "form_parcel" not in st.session_state:
  st.session_state.form_parcel = ""
if "form_contracts" not in st.session_state:
  st.session_state.form_contracts = ["REPC"]

# --- 4. HIDE STREAMLIT UI ---
st.markdown(
    """
    <style>
        #MainMenu, footer, header {visibility: hidden;}
        .block-container {padding: 0;}
        [data-testid="stAppViewContainer"] { background-color: #fcfcfc; }
    </style>
""",
    unsafe_allow_html=True,
)

# --- 5. SHIELDS AND CONTRACTS ---
shield_keys = list(SHIELD_LIBRARY.keys())
contracts_list = ["REPC"] + [k for k in SHIELD_LIBRARY.keys() if k != "REPC"]

# --- 6. AUTHENTICATION & LANDING PAGE GATE ---
if not st.session_state.authenticated:
  # Render the gorgeous Tailwind Hero & Login screen via components.html
  login_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Montserrat:wght@300;400;600&display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
    :root {{ --bhhs-cabernet: #631D33; --overlay: rgba(0, 0, 0, 0.45); }}
    body, html {{ margin:0; padding:0; font-family:'Montserrat', sans-serif; background-color:#fcfcfc; color:#1a1a1a; overflow-x:hidden; }}
    .hero-container {{ position:relative; height:100vh; width:100%; background-image: linear-gradient(var(--overlay), var(--overlay)), url('https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&q=80&w=2070'); background-size:cover; background-position:center; display:flex; flex-direction:column; align-items:center; justify-content:center; color:white; text-align:center; }}
    .action-bar {{ background:white; padding:0.5rem; display:flex; width:90%; max-width:900px; box-shadow:0 10px 40px rgba(0,0,0,0.4); }}
    .action-input {{ flex-grow:1; border:none; padding:1.2rem 2rem; font-size:1rem; color:#333; outline:none; }}
    .action-button {{ background:var(--bhhs-cabernet); color:white; padding:0 2.5rem; text-transform:uppercase; letter-spacing:2px; font-size:0.8rem; font-weight:600; cursor:pointer; border:none; }}
    .disclaimer {{ font-size:11px; font-weight:400; color:rgba(255,255,255,0.8); max-width: 800px; line-height: 1.4; margin-top: 0.5rem; }}
    </style>
    </head>
    <body>
    <section id="hero-section" class="hero-container">
        <header class="absolute top-0 left-0 p-10 text-left">
            <div class="text-2xl font-bold font-serif tracking-tight">UTAH LAND & PROPERTY</div>
            <div class="text-[0.65rem] uppercase tracking-[3px]">Acquisition, Investment, Management, Development</div>
        </header>
        <div class="z-10 px-6 text-center">
            <h1 class="text-7xl font-serif font-bold mb-2">Precision Acquisition.</h1>
            <p class="text-[0.9rem] uppercase tracking-[6px] mb-12 font-300">The Gold Standard in Utah Land Asset Strategy.</p>
            <div class="action-bar mx-auto">
                <input type="password" id="main-search" class="action-input" placeholder="Enter Acquisition ID..." onkeypress="if(event.key === 'KeyE' || event.keyCode === 13) handleLogin()">
                <button onclick="handleLogin()" class="action-button">Enter Vault</button>
            </div>
        </div>
        <div class="absolute bottom-10 px-4 text-center flex flex-col items-center">
            <p class="disclaimer">Notice: Utah Land & Property Inc. is a private investment firm and is not a licensed real estate broker or agent. We do not represent third parties in the purchase, sale, or management of outside real estate.</p>
            <p class="disclaimer">Pursuant to the exemption under Utah Code § 61-2f-202, all property management functions are executed solely by individuals, operating as regular salaried employees of the specific legal entities that own the underlying real estate assets.</p>
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
        window.parent.postMessage({{type: 'ul_auth_success'}}, '*');
    }}
    </script>
    </body>
    </html>
    """
  components.html(login_html, height=900, scrolling=False)

  # Check if user tried to login via script communication or let Streamlit handle a native fallback input in sidebar if needed
  col1, col2, col3 = st.columns([1, 2, 1])
  with col2:
    st.markdown("---")
    passthrough_pw = st.text_input(
        "Direct Vault Access (Fallback Key)", type="password"
    )
    if st.button("Unlock Vault"):
      if passthrough_pw == SECRET_PASSWORD:
        st.session_state.authenticated = True
        st.rerun()
      else:
        st.error("Invalid Acquisition ID.")

else:
  # --- 7. DASHBOARD VIEW (POST-AUTHENTICATION) ---

  # Custom HTML/JS Dashboard UI for Data Entry
  dashboard_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Montserrat:wght@300;400;600&display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
    :root {{ --bhhs-cabernet: #631D33; }}
    body, html {{ margin:0; padding:0; font-family:'Montserrat', sans-serif; background-color:#FDFDFD; color:#1a1a1a; }}
    .glass-card {{ background:white; border:1px solid #e5e7eb; box-shadow:0 4px 15px rgba(0,0,0,0.03); border-radius: 8px; }}
    label {{ font-size:10px; text-transform:uppercase; font-weight:bold; color:#6b7280; display: block; margin-bottom: 0.25rem; }}
    input, select, textarea {{ font-size:14px; padding:0.75rem; border:1px solid #d1d5db; border-radius:5px; width:100%; outline: none; }}
    input:focus, select:focus, textarea:focus {{ border-color: var(--bhhs-cabernet); }}
    </style>
    </head>
    <body>
    <div class="max-w-7xl mx-auto px-10 py-12">
        <div class="mb-8 flex justify-between items-center border-b pb-6">
            <div>
                <h2 class="font-serif text-3xl text-[#631D33]">Asset Control Vault</h2>
                <p class="text-xs uppercase tracking-widest text-gray-500 mt-1">Utah Land & Property Inc. — Executive Terminal</p>
            </div>
        </div>
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-10">
            <div class="glass-card p-10 flex flex-col">
                <h3 class="font-serif text-2xl mb-6">Property & Contract Parameters</h3>
                <div class="space-y-4">
                    <div>
                        <label>Seller Name</label>
                        <input type="text" id="seller-name-input" value="{st.session_state.form_seller}">
                    </div>
                    <div>
                        <label>Property Address</label>
                        <input type="text" id="property-address-input" placeholder="Enter Utah Address" value="{st.session_state.form_address}">
                    </div>
                    <div>
                        <label>Parcel ID</label>
                        <input type="text" id="parcel-id-input" placeholder="Enter Parcel ID" value="{st.session_state.form_parcel}">
                    </div>
                    <div>
                        <label>Select Contracts / Addenda (Hold Ctrl/Cmd for multiple)</label>
                        <select id="contracts-select" multiple size="8">
                            {''.join([f'<option value="{c}" {"selected" if c in st.session_state.form_contracts else ""}>{c}</option>' for c in contracts_list])}
                        </select>
                    </div>
                    <div class="pt-4">
                        <button onclick="handleExecution()" class="w-full bg-[var(--bhhs-cabernet)] text-white py-4 font-bold uppercase tracking-[2px] text-xs transition hover:opacity-90 cursor-pointer">Sync & Stage Contract Data</button>
                    </div>
                </div>
            </div>
            <div class="glass-card p-10 flex flex-col">
                <h3 class="font-serif text-2xl mb-6">Live Payload Preview</h3>
                <textarea id="preview-area" rows="14" class="bg-gray-50 font-mono text-xs" readonly>Configure parameters on the left and stage contract data to initialize print tray pipeline.</textarea>
            </div>
        </div>
    </div>
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
        const preview = "--- CONTRACT STAGED ---\\n" +
                        "Seller: " + name + "\\n" +
                        "Address: " + addr + "\\n" +
                        "Parcel ID: " + parcel + "\\n" +
                        "Selected Addenda: " + selected.join(', ');
        document.getElementById('preview-area').value = preview;
        
        // Post data back to Streamlit container context
        window.parent.postMessage({{
            type: 'ul_update_deal',
            seller: name,
            address: addr,
            parcel: parcel,
            contracts: selected
        }}, '*');
        alert("Payload synchronized with Secure Printer Tray.");
    }}
    </script>
    </body>
    </html>
    """
  components.html(dashboard_html, height=750, scrolling=True)

  # --- 8. SIDEBAR PRINTER TRAY ---
  with st.sidebar:
    st.markdown("### 🏔️ SECURE PRINTER TRAY")
    st.info(
        "Manage final parameters and generate immutable document package."
    )

    final_seller = st.text_input(
        "Confirm Seller", value=st.session_state.form_seller
    )
    final_addr = st.text_input(
        "Confirm Address", value=st.session_state.form_address
    )
    final_parcel = st.text_input(
        "Confirm Parcel ID", value=st.session_state.form_parcel
    )

    selected_contracts_input = st.text_area(
        "Confirmed Contracts (comma separated)",
        value=", ".join(st.session_state.form_contracts),
    )

    st.markdown("---")
    if st.button("Generate & Download PDF Package", type="primary"):
      if not final_addr or not final_seller:
        st.error("Seller Name and Address are required.")
      elif not selected_contracts_input.strip():
        st.error("Please specify at least one contract.")
      else:
        contracts_list_final = [
            c.strip() for c in selected_contracts_input.split(",")
        ]
        deal_data = {
            "seller_first": final_seller.split()[0],
            "seller_last": (
                " ".join(final_seller.split()[1:])
                if len(final_seller.split()) > 1
                else ""
            ),
            "address": final_addr,
            "repc_date": "02/26/2026",
            "addendum_no": "1",
            "acceptance_date": "03/01/2026",
            "acceptance_time": "5:00 PM",
        }
        try:
          pdf_path = generate_utah_addendum(deal_data, contracts_list_final)
          if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
              st.download_button(
                  label="📥 CLICK TO SAVE FINAL PDF",
                  data=f,
                  file_name=f"Addendum_{final_seller.replace(' ', '_')}.pdf",
                  mime="application/pdf",
              )
        except Exception as e:
          st.error(f"Error generating PDF: {e}")

    if st.button("Lock Vault / Logout"):
      st.session_state.authenticated = False
      st.rerun()
