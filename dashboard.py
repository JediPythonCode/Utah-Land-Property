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
    SHIELD_LIBRARY = {"FinCEN_2026": "Active", "Assignment_Gator": "Active"}
    def generate_utah_addendum(data, shields):
        # return a dummy PDF path for testing
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

# --- 4. HERO + LOGIN ---
login_container = st.container()
with login_container:
    st.markdown("<h1 style='text-align:center; font-family: Playfair Display;'>Precision Acquisition.</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; text-transform:uppercase; letter-spacing:2px;'>The Gold Standard in Utah Land Asset Strategy.</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:10px; color:#555;'>Utah Land & Property Inc are not licensed real estate agents or real estate brokers. We are investment professionals. All activity is monitored and compliant with Utah state regulations.</p>", unsafe_allow_html=True)
    acquisition_id = st.text_input("Enter Acquisition ID (Password)", type="password")
    login_button = st.button("Access Dashboard")

if login_button:
    if acquisition_id != SECRET_PASSWORD:
        st.error("Invalid Acquisition ID")
    else:
        # --- 5. DASHBOARD ---
        login_container.empty()  # remove login

        shield_keys = list(SHIELD_LIBRARY.keys())

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
                body, html {{ margin:0; padding:0; font-family:'Montserrat', sans-serif; background-color:#fcfcfc; }}
                .glass-card {{ background:white; border:1px solid #e5e7eb; box-shadow:0 4px 15px rgba(0,0,0,0.03); padding:2rem; }}
                .accent-border {{ border-left:5px solid #631D33; }}
            </style>
        </head>
        <body>
            <div class="max-w-7xl mx-auto px-10 mt-16">
                <div class="grid grid-cols-1 md:grid-cols-3 gap-10 mb-16">
                    <div class="glass-card accent-border">
                        <div class="text-xs uppercase text-gray-400 font-bold">Current Portfolio Value</div>
                        <div class="text-4xl font-serif font-bold text-[#631D33]">$8,740,200</div>
                        <div class="text-xs text-green-600 font-bold tracking-widest uppercase">Performance Tracking Active</div>
                    </div>
                    <div class="glass-card">
                        <div class="text-xs uppercase text-gray-400 font-bold">Land Owned</div>
                        <div class="text-4xl font-serif font-bold">18.42 AC</div>
                    </div>
                    <div class="glass-card">
                        <div class="text-xs uppercase text-gray-400 font-bold">Liquidity Status</div>
                        <div class="text-4xl font-serif font-bold">Premium</div>
                    </div>
                </div>

                <div class="grid grid-cols-1 lg:grid-cols-2 gap-10">
                    <div class="glass-card p-12 h-[500px] flex flex-col">
                        <h2 class="font-serif text-3xl mb-8">Performance Chart</h2>
                        <canvas id="stochasticChart"></canvas>
                    </div>
                    
                    <div class="glass-card p-12">
                        <h2 class="font-serif text-3xl mb-8">Contracts & Shield Engine</h2>
                        <div class="space-y-6">
                             <div>
                                <label class="text-xs uppercase font-bold text-gray-400">Seller Name</label>
                                <input type="text" id="seller-name-input" value="Owen" class="w-full border-b border-gray-200 py-2 outline-none font-bold text-lg">
                             </div>
                             <div>
                                <label class="text-xs uppercase font-bold text-gray-400">Property Address</label>
                                <input type="text" id="property-address-input" placeholder="Enter Utah Address..." class="w-full border-b border-gray-200 py-2 outline-none font-bold text-lg">
                             </div>
                             <div>
                                <label class="text-xs uppercase font-bold text-gray-400">Active Logic Shields</label>
                                <div class="flex flex-wrap gap-2 mt-2">
                                    {"".join([f'<div class="bg-gray-100 text-[9px] px-3 py-1 rounded-full text-gray-600 font-bold border border-gray-200 uppercase">{k}</div>' for k in shield_keys])}
                                </div>
                             </div>
                             <div class="pt-6">
                                <button onclick="handleExecution()" class="w-full bg-[#631D33] text-white py-4 font-bold uppercase tracking-[2px] text-xs">Execute & Generate Contracts</button>
                             </div>
                        </div>
                    </div>
                </div>
            </div>

            <script>
                function initChart() {{
                    const ctx = document.getElementById('stochasticChart').getContext('2d');
                    new Chart(ctx, {{
                        type:'line',
                        data:{{
                            labels:['M1','M2','M3','M4','M5','M6'],
                            datasets:[{{ data:[8.74,8.85,8.80,8.92,9.10,9.25], borderColor:'#631D33', tension:0.4 }}]
                        }},
                        options:{{ responsive:true, maintainAspectRatio:false }}
                    }});
                }}
                initChart();

                function handleExecution(){{
                    const name = document.getElementById('seller-name-input').value;
                    const addr = document.getElementById('property-address-input').value;
                    window.parent.postMessage({{type:'execute_contract', seller:name, address:addr}}, '*');
                    alert("Contracts prepared for: " + name + "\\nCheck the sidebar to view or download.");
                }}
            </script>
        </body>
        </html>
        """

        components.html(html_content, height=1000, scrolling=True)

        # --- 6. SIDEBAR PDF ENGINE ---
        with st.sidebar:
            st.markdown("### 🏔️ SECURE CONTRACT VIEWER & PRINTER TRAY")
            st.info("After executing, your REPC contract is generated first. Optional addenda can be selected. Preview or download below.")

            # Confirm input
            final_seller = st.text_input("Confirm Seller", "Owen")
            final_addr = st.text_input("Confirm Address", "")

            # Select addenda
            addenda_options = st.multiselect("Optional Addenda", ["Addendum A", "Addendum B", "Addendum C"])

            if st.button("Generate & Download PDF"):
                if not final_addr:
                    st.error("Address Required.")
                else:
                    # always generate REPC first
                    data = {"seller": final_seller, "address": final_addr, "addendum_no": "1", "addenda": addenda_options}
                    path = generate_utah_addendum(data, shield_keys)

                    if os.path.exists(path):
                        with open(path, "rb") as f:
                            st.download_button(
                                label="VIEW / SAVE FINAL PDF",
                                data=f,
                                file_name=f"REPC_{final_seller}.pdf",
                                mime="application/pdf"
                            )
