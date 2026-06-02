import streamlit as st
import streamlit.components.v1 as components
import os
import json
from library import SHIELD_LIBRARY

# --- 1. PAGE SETUP ---
st.set_page_config(
    page_title="Utah Land & Property | Secure Asset Portal",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. PERSISTENCE ENGINE ---
DATA_FILE = "data/shields_2026.json"

def get_deal_data():
    with open(DATA_FILE, "r") as f: return json.load(f)

def update_status(parcel_id, new_status):
    data = get_deal_data()
    if parcel_id in data:
        data[parcel_id]["status"] = new_status
        with open(DATA_FILE, "w") as f: json.dump(data, f, indent=4)

# --- 3. SESSION STATE ---
if "active_parcel" not in st.session_state: st.session_state.active_parcel = None

# --- 4. HTML LAYOUT (THE DASHBOARD) ---
# We inject the current status into the HTML dynamically
current_status = "Initial Review"
if st.session_state.active_parcel:
    deal_data = get_deal_data().get(st.session_state.active_parcel, {})
    current_status = deal_data.get("status", "Initial Review")

html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        :root {{ --bhhs-cabernet: #631D33; }}
        /* ... YOUR ORIGINAL CSS ... */
    </style>
</head>
<body>
    <div id="dashboard-view" class="visible p-12">
        <div class="flex justify-between border-b pb-8">
            <div class="text-sm font-bold uppercase">Status: <span id="deal-status" class="text-red-900">{current_status}</span></div>
            <div class="flex gap-4">
                <button onclick="parent.postMessage('trigger_upload', '*')" class="bg-gray-100 px-6 py-2">Upload</button>
                <button onclick="parent.postMessage('trigger_esign', '*')" class="bg-[#631D33] text-white px-6 py-2">E-Sign</button>
            </div>
        </div>
    </div>
    <script>
        window.addEventListener("message", (event) => {{
            if(event.data.type === 'update') document.getElementById('deal-status').innerText = event.data.status;
        }});
    </script>
</body>
</html>
"""

# --- 5. LOGIC BRIDGE ---
components.html(html_content, height=600)

# This block listens to the HTML buttons and updates the JSON
if "last_event" not in st.session_state: st.session_state.last_event = None

# Sidebar for file handling
with st.sidebar:
    st.subheader("Transaction Management")
    uploaded_file = st.file_uploader("Upload Docs")
    if uploaded_file:
        update_status(st.session_state.active_parcel, "Documents Uploaded")
        st.success("Status Updated: Documents Uploaded")
        st.rerun()

    if st.button("Mark E-Sign Pending"):
        update_status(st.session_state.active_parcel, "E-Sign Pending")
        st.rerun()
