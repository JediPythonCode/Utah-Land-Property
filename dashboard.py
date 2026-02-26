import streamlit as st
import streamlit.components.v1 as components
import os
import json

# --- 1. CORE LOGIC ---
try:
    from library import SHIELD_LIBRARY
    from automation_engine import generate_utah_addendum
except ImportError:
    SHIELD_LIBRARY = {"FinCEN_2026": "Active", "Assignment_Gator": "Active"}
    def generate_utah_addendum(d, s): return "temp.pdf"

# --- 2. LOAD ACQUISITION IDS FROM SECRETS ---
ACQ_IDS = st.secrets.get("acquisition_ids", {})

# --- 3. PAGE SETUP ---
st.set_page_config(
    page_title="Utah Land & Property | Secure Asset Portal",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit default UI
st.markdown("""
    <style>
        #MainMenu, footer, header {visibility: hidden;}
        .block-container {padding: 0;}
        [data-testid="stAppViewContainer"] { background-color: #fcfcfc; }
    </style>
""", unsafe_allow_html=True)

# --- 4. LOGIN / PASSWORD CHECK ---
acq_id = st.text_input("Enter Acquisition ID...", type="default")
login_success = False

if acq_id:
    if acq_id in ACQ_IDS:
        login_success = True
        st.success(f"Access granted for {acq_id}")
    else:
        st.error("❌ Invalid Acquisition ID")

# Only show dashboard if login successful
if login_success:
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
            :root {{ --bhhs-cabernet: #631D33; --overlay: rgba(0, 0, 0, 0.45); }}
            body, html {{ margin: 0; padding: 0; font-family: 'Montserrat', sans-serif; background-color: #fcfcfc; color: #1a1a1a; overflow-x: hidden; }}
            .glass-card {{ background: white; border: 1px solid #e5e7eb; box-shadow: 0 4px 15px rgba(0,0,0,0.03); }}
            .accent-border {{ border-left: 5px solid var(--bhhs-cabernet); }}
        </style>
    </head>
    <body>
        <section id="dashboard-view" class="min-h-screen bg-[#FDFDFD] pb-24">
            <nav class="bg-white border-b border-gray-100 px-10 py-8 flex justify-between items-center sticky top-0 z-50">
                <div class="flex flex-col">
                    <div class="text-[var(--bhhs-cabernet)] font-serif font-bold text-2xl tracking-tight">PRIVATE CLIENT PORTFOLIO</div>
                    <div class="text-[10px] uppercase tracking-[4px] text-gray-400 mt-1">ID: {acq_id}</div>
                </div>
            </nav>

            <div class="max-w-7xl mx-auto px-10 mt-16">
                <div class="grid grid-cols-1 md:grid-cols-3 gap-10 mb-16">
                    <div class="glass-card accent-border p-10">
                        <div class="text-[10px] uppercase tracking-[3px] text-gray-400 mb-2 font-bold">Projected Asset Value</div>
                        <div class="text-4xl font-serif font-bold text-[var(--bhhs-cabernet)]">$8,740,200</div>
                        <div class="text-[10px] text-emerald-600 mt-3 font-bold tracking-widest uppercase">Stochastic Model Active</div>
                    </div>
                    <div class="glass-card p-10">
                        <div class="text-[10px] uppercase tracking-[3px] text-gray-400 mb-2 font-bold">Land Utilization</div>
                        <div class="text-4xl font-serif font-bold">18.42 AC</div>
                    </div>
                    <div class="glass-card p-10">
                        <div class="text-[10px] uppercase tracking-[3px] text-gray-400 mb-2 font-bold">Market Liquidity</div>
                        <div class="text-4xl font-serif font-bold">Premium</div>
                    </div>
                </div>

                <div class="grid grid-cols-1 lg:grid-cols-2 gap-10">
                    <div class="glass-card p-12 h-[500px] flex flex-col">
                        <h2 class="font-serif text-3xl mb-8">Stochastic Trajectory</h2>
                        <canvas id="stochasticChart"></canvas>
                    </div>
                    
                    <div class="glass-card p-12">
                        <h2 class="font-serif text-3xl mb-8">Shield Execution Engine</h2>
                        <div class="space-y-6">
                             <div>
                                <label class="text-[10px] uppercase font-bold text-gray-400">Seller Name</label>
                                <input type="text" id="seller-name-input" value="Owen" class="w-full border-b border-gray-200 py-2 outline-none font-bold text-lg">
                             </div>
                             <div>
                                <label class="text-[10px] uppercase font-bold text-gray-400">Property Address</label>
                                <input type="text" id="property-address-input" placeholder="Enter Utah Address..." class="w-full border-b border-gray-200 py-2 outline-none font-bold text-lg">
                             </div>
                             <div>
                                <label class="text-[10px] uppercase font-bold text-gray-400">Active Logic Shields</label>
                                <div class="flex flex-wrap gap-2 mt-2">
                                    {"".join([f'<div class="bg-gray-100 text-[9px] px-3 py-1 rounded-full text-gray-600 font-bold border border-gray-200 uppercase">{k}</div>' for k in shield_keys])}
                                </div>
                             </div>
                             <div class="pt-6">
                                <button onclick="handleExecution()" class="w-full bg-[var(--bhhs-cabernet)] text-white py-4 font-bold uppercase tracking-[2px] text-xs">Execute Secure Addendum</button>
                             </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <script>
            function handleExecution() {{
                const name = document.getElementById('seller-name-input').value;
                const addr = document.getElementById('property-address-input').value;
                window.parent.postMessage({{ type: 'execute_contract', seller: name, address: addr }}, '*');
                alert("Contract logic bound for: " + name + "\\nProceed to sidebar for download.");
            }}

            function initChart() {{
                const ctx = document.getElementById('stochasticChart').getContext('2d');
                new Chart(ctx, {{
                    type: 'line',
                    data: {{
                        labels: ['M1', 'M2', 'M3', 'M4', 'M5', 'M6'],
                        datasets: [{{ data: [8.74, 8.85, 8.80, 8.92, 9.10, 9.25], borderColor: '#631D33', tension: 0.4 }}]
                    }},
                    options: {{ responsive: true, maintainAspectRatio: false }}
                }});
            }}

            initChart();
        </script>
    </body>
    </html>
    """

    # Render the dashboard
    components.html(html_content, height=1000, scrolling=True)

    # --- 5. SIDEBAR ENGINE & PDF GENERATION ---
    with st.sidebar:
        st.markdown("### 🏔️ SECURE PRINTER TRAY")
        st.info("Fill out the 'Property Address' in the dashboard, then click Execute. Your file will appear here.")
        
        with st.expander("Stochastic Engine Settings", expanded=True):
            final_seller = st.text_input("Confirm Seller", "Owen")
            final_addr = st.text_input("Confirm Address", "")
        
        if st.button("Generate & Download PDF"):
            if not final_addr:
                st.error("Address Required.")
            else:
                data = {"seller": final_seller, "address": final_addr, "addendum_no": "1"}
                path = generate_utah_addendum(data, shield_keys)
                
                if os.path.exists(path):
                    with open(path, "rb") as f:
                        st.download_button(
                            label="CLICK TO SAVE FINAL PDF",
                            data=f,
                            file_name=f"Addendum_{final_seller}.pdf",
                            mime="application/pdf"
                        )
