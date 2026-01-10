import streamlit as st
from streamlit_autorefresh import st_autorefresh
import os
import glob
from datetime import datetime

# ── 1. CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Utah Land & Property",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st_autorefresh(interval=600000, key="ulp_refresh")

# Ensure vault directories exist
for folder in ["vault/general", "vault/buyer_docs", "vault/property_images"]:
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)

# Initialize Session States
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_role" not in st.session_state:
    st.session_state.user_role = None
if "active_disclosure" not in st.session_state:
    st.session_state.active_disclosure = "Standard Disclosure: All deals subject to final underwriting and title search."

# ── 2. AUTHENTICATION GATE ──────────────────────────────────────────────────
if not st.session_state.authenticated:
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&family=Oswald:wght@500;700&display=swap');
        .stApp { background-color: #f8f9fa !important; }
        header, footer, [data-testid="stHeader"] { display: none !important; }
        .viewport-top-container { display: flex; flex-direction: column; justify-content: center; align-items: center; min-height: 50vh; padding-top: 4%; text-align: center; width: 100%; padding-left: 20px; padding-right: 20px; }
        .brand-title { font-family: 'Inter', sans-serif !important; font-size: clamp(38px, 8vw, 78px) !important; font-weight: 900 !important; color: #1a3c6d !important; letter-spacing: -1.5px !important; margin-bottom: 0px !important; line-height: 1.0 !important; }
        .brand-subtitle { font-family: 'Oswald', sans-serif !important; font-size: clamp(1rem, 3vw, 1.35rem) !important; color: #6b7280 !important; letter-spacing: 3px !important; font-weight: 500 !important; margin-top: 10px !important; margin-bottom: 2rem !important; }
        .framework-text { color: #4b5563 !important; font-size: 1.05rem !important; max-width: 800px !important; margin: 0 auto 2.5rem !important; line-height: 1.7 !important; font-family: 'Inter', sans-serif !important; }
        .pulse-lock { height: 12px; width: 12px; background: #10b981; border-radius: 50%; display: inline-block; margin-right: 12px; box-shadow: 0 0 12px rgba(16,185,129,0.5); animation: pulse 2s infinite; vertical-align: middle; }
        @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(16,185,129,0.7); } 70% { box-shadow: 0 0 0 12px rgba(16,185,129,0); } 100% { box-shadow: 0 0 0 0 rgba(16,185,129,0); } }
        .access-text { font-family: 'Oswald', sans-serif !important; font-size: 0.9rem !important; color: #1a3c6d !important; font-weight: 700 !important; letter-spacing: 2px !important; vertical-align: middle; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""<div class="viewport-top-container"><div class="brand-title">Utah Land & Property</div><div class="brand-subtitle">Strategic Asset Protection Framework</div><div class="framework-text"><strong>Privacy Creation Preservation • Creative Land & Real Estate Deal Structure</strong></div><div style="margin-bottom: 2rem;"><span class="pulse-lock"></span><span class="access-text">SECURE CLIENT PORTAL ENCRYPTED ACCESS ONLY</span></div>""", unsafe_allow_html=True)
    _, col_mid, _ = st.columns([1, 1.6, 1])
    with col_mid:
        pwd = st.text_input("Key", type="password", placeholder="Enter Access Key", label_visibility="collapsed")
        if st.button("Access Portal", use_container_width=True, type="primary"):
            keys_dict = st.secrets.get("access_keys", {})
            if pwd in keys_dict:
                st.session_state.authenticated = True
                st.session_state.user_role = keys_dict[pwd]
                st.rerun()
            else:
                st.error("Invalid Security Key")
    st.markdown("</div>", unsafe_allow_html=True)

# ── 3. PROTECTED CONTENT ──────────────────────────────────────────────────
else:
    role = st.session_state.user_role
    st.markdown("""<style>.block-container { text-align: center; padding-top: 2rem; }.stButton > button { display: block; margin: 0 auto; width: 200px; }[data-testid="stFileUploader"] { width: 100%; max-width: 500px; margin: 0 auto; }.recent-file-card { background: white; padding: 10px; border-radius: 8px; border: 1px solid #ddd; margin-bottom: 10px; font-family: 'Inter'; font-size: 0.9rem; }</style>""", unsafe_allow_html=True)

    # Global Dashboard Header
    st.title(f"{role} Dashboard")
    
    # DEAL STRUCTURE DISCLOSURE (Visible to everyone, controlled by Admin)
    st.warning(f"🔔 **Deal Structure Disclosure:** {st.session_state.active_disclosure}")

    if st.button("Secure Logout"):
        st.session_state.authenticated = False
        st.rerun()

    st.markdown("---")

    # --- 3a. GLOBAL ACTIVITY VIEW ---
    st.subheader("Latest Property Activity")
    all_files = []
    for root, dirs, files in os.walk("vault"):
        for f in files:
            if not f.startswith('.'):
                path = os.path.join(root, f)
                all_files.append((f, os.path.getmtime(path), root.split('/')[-1]))
    all_files.sort(key=lambda x: x[1], reverse=True)

    if all_files:
        feed_cols = st.columns(3)
        for i, (fname, ftime, ftype) in enumerate(all_files[:3]):
            dt = datetime.fromtimestamp(ftime).strftime('%Y-%m-%d %H:%M')
            with feed_cols[i]:
                st.markdown(f"""<div class="recent-file-card"><strong>{fname}</strong><br><span style="color:#666; font-size:0.8rem;">Category: {ftype.replace('_',' ').title()}</span><br><span style="color:#999; font-size:0.7rem;">Uploaded: {dt}</span></div>""", unsafe_allow_html=True)

    # --- 3b. PROPERTY VISUALS ---
    st.subheader("Property Images")
    valid_ext = ('.png', '.jpg', '.jpeg', '.webp')
    images = [f for f in glob.glob("vault/property_images/*") if f.lower().endswith(valid_ext)]
    if images:
        img_cols = st.columns(min(len(images), 4))
        for idx, img_path in enumerate(images):
            img_cols[idx % 4].image(img_path, use_container_width=True)

    st.markdown("---")

    # --- 3c. ROLE-SPECIFIC LOGIC ---
    if role == "Buyer":
        st.subheader("Step 1: Underwriting Pre-Screen")
        with st.expander("📊 Analyze Financial Ratios", expanded=True):
            v1, v2 = st.columns(2)
            inc = v1.number_input("Monthly Income ($)", min_value=1, value=5000)
            debt = v1.number_input("Monthly Debt ($)", min_value=0, value=1500)
            price = v2.number_input("Property Price ($)", min_value=1, value=400000)
            down = v2.number_input("Down Payment ($)", min_value=0, value=80000)
            dti = (debt / inc) * 100
            ltv = ((price - down) / price) * 100
            st.markdown("---")
            r1, r2 = st.columns(2)
            r1.metric("DTI Ratio", f"{dti:.1f}%", delta="Pass" if dti <= 43 else "High", delta_color="normal" if dti <= 43 else "inverse")
            r2.metric("LTV Ratio", f"{ltv:.1f}%", delta="Pass" if ltv <= 80 else "High", delta_color="normal" if ltv <= 80 else "inverse")

        st.subheader("Step 2: Property Aspects & Vetting")
        vet_file = st.file_uploader("Upload Proof of Funds / ID", key="buyer_vet")
        if vet_file:
            with open(os.path.join("vault/general", f"VETTING_{vet_file.name}"), "wb") as f:
                f.write(vet_file.getbuffer())
            st.success("File archived for review.")

        st.subheader("Step 3: Signature Vault")
        docs = os.listdir("vault/buyer_docs")
        if docs:
            for d in docs:
                with open(f"vault/buyer_docs/{d}", "rb") as f:
                    st.download_button(f"📄 Download {d}", f, file_name=d)
        else:
            st.warning("Locked: Awaiting manual vetting for document release.")

    else:
        # ADMIN & AGENT MANAGEMENT
        st.subheader("Management: Deal Structure & Assets")
        
        # DISCLOSURE PUSH TOOL
        with st.expander("📝 Push Deal Disclosures", expanded=True):
            common_disclosures = {
                "Subject-To": "This deal is structured as 'Subject-To' existing financing. Buyer acknowledges existing loan stays in place.",
                "Seller Carry": "Seller Finance / Carry-Back: Terms include a 5-year balloon with a 6% interest rate.",
                "Wholesale/Assignment": "Assignment of Contract: Equitable interest is being sold. All inspections must be completed prior to assignment.",
                "All Cash": "Proof of Funds required. Closing to occur within 10 business days of title clearance.",
                "Privacy Trust": "Property to be held in an Anonymous Land Trust for asset protection and privacy preservation."
            }
            choice = st.selectbox("Select Disclosure Template", list(common_disclosures.keys()))
            custom_note = st.text_area("Custom Addendum", common_disclosures[choice])
            if st.button("Push to Portal Dashboard", type="primary"):
                st.session_state.active_disclosure = custom_note
                st.success("Disclosure updated for all users.")
                st.rerun()

        # UPLOADER
        c1, c2 = st.columns(2)
        with c1: target = st.radio("Folder", ["General", "Buyer Signatures"])
        with c2: upload_kind = st.radio("Type", ["Document", "Image"])

        uploaded_files = st.file_uploader("Select Assets", accept_multiple_files=True)
        if uploaded_files:
            for file in uploaded_files:
                dest = "vault/property_images" if upload_kind == "Image" else ("vault/buyer_docs" if target == "Buyer Signatures" else "vault/general")
                with open(os.path.join(dest, file.name), "wb") as f:
                    f.write(file.getbuffer())
            st.success("Uploaded.")
            st.rerun()

    if role == "Admin":
        with st.expander("System Audit"):
            st.write(glob.glob("vault/**/*", recursive=True))

    st.markdown(f"<small>Authenticated as {role}</small>", unsafe_allow_html=True)
