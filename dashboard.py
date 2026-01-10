import streamlit as st
from streamlit_autorefresh import st_autorefresh
import os
import glob

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

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_role" not in st.session_state:
    st.session_state.user_role = None

# ── 2. AUTHENTICATION GATE ──────────────────────────────────────────────────
if not st.session_state.authenticated:
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&family=Oswald:wght@500;700&display=swap');
        .stApp { background-color: #f8f9fa !important; }
        header, footer, [data-testid="stHeader"] { display: none !important; }
        .viewport-top-container { margin-top: -10vh; text-align: center; width: 100%; }
        .brand-title { font-family: 'Inter', sans-serif !important; font-size: clamp(42px, 10vw, 78px) !important; font-weight: 900 !important; color: #1a3c6d !important; letter-spacing: -1.5px !important; margin-bottom: 0px !important; line-height: 1.0 !important; }
        .brand-subtitle { font-family: 'Oswald', sans-serif !important; font-size: 1.35rem !important; color: #6b7280 !important; letter-spacing: 3px !important; font-weight: 500 !important; margin-top: 5px !important; margin-bottom: 2rem !important; }
        .framework-text { color: #4b5563 !important; font-size: 1.05rem !important; max-width: 800px !important; margin: 0 auto 2.5rem !important; line-height: 1.7 !important; font-family: 'Inter', sans-serif !important; }
        .pulse-lock { height: 12px; width: 12px; background: #10b981; border-radius: 50%; display: inline-block; margin-right: 12px; box-shadow: 0 0 12px rgba(16,185,129,0.5); animation: pulse 2s infinite; vertical-align: middle; }
        @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(16,185,129,0.7); } 70% { box-shadow: 0 0 0 12px rgba(16,185,129,0); } 100% { box-shadow: 0 0 0 0 rgba(16,185,129,0); } }
        .access-text { font-family: 'Oswald', sans-serif !important; font-size: 1.1rem !important; color: #1a3c6d !important; font-weight: 700 !important; letter-spacing: 2px !important; vertical-align: middle; }
    </style>
    """, unsafe_allow_html=True)

    # Combined Access Lines & Bolded Framework Text
    hero_html = """
    <div class="viewport-top-container">
        <div class="brand-title">Utah Land & Property</div>
        <div class="brand-subtitle">Strategic Asset Protection Framework</div>
        <div class="framework-text">
            <strong>Privacy Creation Preservation • Creative Land & Real Estate Deal Structure</strong>
        </div>
        <div style="margin-bottom: 2rem;">
            <span class="pulse-lock"></span>
            <span class="access-text">SECURE CLIENT PORTAL — ENCRYPTED ACCESS ONLY</span>
        </div>
    </div>
    """
    st.markdown(hero_html, unsafe_allow_html=True)

    _, col_mid, _ = st.columns([1, 1.4, 1])
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

# ── 3. PROTECTED CONTENT ──────────────────────────────────────────────────
else:
    role = st.session_state.user_role
    
    # CSS to center the main dashboard content
    st.markdown("""
        <style>
            .block-container { text-align: center; }
            .stButton > button { display: block; margin: 0 auto; }
            [data-testid="stFileUploader"] { width: 50%; margin: 0 auto; }
            [data-testid="stHorizontalBlock"] { justify-content: center; }
        </style>
    """, unsafe_allow_html=True)

    # Center-aligned Header
    st.title(f"{role} Dashboard")
    
    if st.button("Secure Logout", type="secondary"):
        st.session_state.authenticated = False
        st.rerun()

    st.markdown("---")

    # --- PROPERTY GALLERY (Centered & Error-Protected) ---
    st.subheader("Property Visuals")
    
    valid_extensions = ('.png', '.jpg', '.jpeg', '.webp', '.PNG', '.JPG', '.JPEG')
    images = [f for f in glob.glob("vault/property_images/*") if f.endswith(valid_extensions)]
    
    if images:
        # Using a nested column structure to keep images centered
        _, img_col, _ = st.columns([0.1, 0.8, 0.1])
        with img_col:
            cols = st.columns(4)
            for idx, img_path in enumerate(images):
                try:
                    cols[idx % 4].image(img_path, use_container_width=True)
                except:
                    continue
    else:
        st.info("No property images available.")

    st.markdown("---")

    # --- ROLE-SPECIFIC ACCESS ---
    if role == "Buyer":
        st.subheader("Action Required: Documents for Signature")
        buyer_docs = os.listdir("vault/buyer_docs")
        if buyer_docs:
            for f_name in buyer_docs:
                with open(f"vault/buyer_docs/{f_name}", "rb") as f_obj:
                    st.download_button(f"📄 Download & Sign: {f_name}", f_obj, file_name=f_name)
        else:
            st.success("No pending documents for signature.")
    else:
        # Management Logic
        st.subheader("Document Upload & Archival")
        
        c1, c2 = st.columns(2)
        with c1:
            target = st.radio("Destination", ["General Vault", "Buyer's Signature Folder"], horizontal=True)
        with c2:
            if role in ["Admin", "Agent"]:
                upload_kind = st.radio("Asset Type", ["Document", "Property Image"], horizontal=True)
            else:
                upload_kind = "Document"

        uploaded_files = st.file_uploader("Drop Assets Here", accept_multiple_files=True)

        if uploaded_files:
            for file in uploaded_files:
                dest = "vault/property_images" if upload_kind == "Property Image" else (
                    "vault/buyer_docs" if target == "Buyer's Signature Folder" else "vault/general"
                )
                with open(os.path.join(dest, file.name), "wb") as f:
                    f.write(file.getbuffer())
            st.success(f"Archived {len(uploaded_files)} assets.")
            st.rerun()

    if role == "Admin":
        with st.expander("Admin Master View"):
            st.json(glob.glob("vault/**/*", recursive=True))

    st.markdown(f"**Authenticated as:** {role}")
