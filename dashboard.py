import streamlit as st
from streamlit_autorefresh import st_autorefresh
import os
import glob
import pandas as pd
from datetime import datetime
from cryptography.fernet import Fernet

# ── 1. CONFIG & ENCRYPTION ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Utah Land & Property",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st_autorefresh(interval=600000, key="ulp_refresh")

# Initialize Encryption logic
if "secret_key" not in st.secrets:
    ENCR_KEY = b'6_Wb7R-5N5_W_h_Z9F-4Qp3o9-G7_X_z1H-8I_w_9k0=' 
else:
    ENCR_KEY = st.secrets["secret_key"].encode()

fernet = Fernet(ENCR_KEY)

# ── 2. BRANDING & STYLING (GLOBAL - FORCED DARK TEXT) ───────────────────────
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&family=Oswald:wght@500;700&display=swap');
        
        /* Force background and global text color */
        .stApp { 
            background-color: #f8f9fa !important; 
            color: #1a1a1a !important; 
        }
        
        /* Force all headers to Black */
        h1, h2, h3, h4, p, span, label, .stMarkdown {
            color: #1a1a1a !important;
            font-family: 'Inter', sans-serif;
        }

        header, footer, [data-testid="stHeader"] { display: none !important; }
        
        .viewport-top-container { 
            display: flex; flex-direction: column; justify-content: center; 
            align-items: center; min-height: 40vh; padding-top: 50px; 
            text-align: center; width: 100%; 
        }
        
        .brand-title { 
            font-family: 'Inter', sans-serif !important; font-size: clamp(38px, 8vw, 78px) !important; 
            font-weight: 900 !important; color: #1a3c6d !important; letter-spacing: -1.5px !important; 
            margin-bottom: 0px !important; line-height: 1.0 !important; 
        }
        
        .brand-subtitle { 
            font-family: 'Oswald', sans-serif !important; font-size: clamp(1rem, 3vw, 1.35rem) !important; 
            color: #4b5563 !important; letter-spacing: 3px !important; font-weight: 500 !important; 
            margin-top: 10px !important; margin-bottom: 1.5rem !important; 
        }

        .pulse-lock { 
            height: 12px; width: 12px; background: #10b981; border-radius: 50%; 
            display: inline-block; margin-right: 12px; 
            box-shadow: 0 0 12px rgba(16,185,129,0.5); animation: pulse 2s infinite; 
        }
        
        @keyframes pulse { 
            0% { box-shadow: 0 0 0 0 rgba(16,185,129,0.7); } 
            70% { box-shadow: 0 0 0 12px rgba(16,185,129,0); } 
            100% { box-shadow: 0 0 0 0 rgba(16,185,129,0); } 
        }
        
        /* Card Styling for Activity Feed */
        .recent-file-card { 
            background: #ffffff; padding: 15px; border-radius: 12px; 
            border: 1px solid #d1d5db; margin-bottom: 12px; 
            box-shadow: 0 2px 4px rgba(0,0,0,0.05); text-align: left;
            color: #1a1a1a !important;
        }

        /* Fix visibility of Tab labels */
        button[data-baseweb="tab"] p {
            color: #1a1a1a !important;
            font-weight: 600 !important;
        }
        
        /* Fix Input Text Color */
        input {
            color: #1a1a1a !important;
        }
    </style>
""", unsafe_allow_html=True)

# ── 3. CORE LOGIC ────────────────────────────────────────────────────────────
DISCLOSURE_FILE = "vault/general/deal_structure.txt"
AUDIT_FILE = "vault/general/audit_log.csv"

for folder in ["vault/general", "vault/buyer_docs", "vault/property_images"]:
    os.makedirs(folder, exist_ok=True)

def logger(user, action, details):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = pd.DataFrame([[timestamp, user, action, str(details)]], columns=["Timestamp", "User", "Action", "Details"])
    log_entry.to_csv(AUDIT_FILE, mode='a', header=not os.path.exists(AUDIT_FILE), index=False)

def save_encrypted(file_path, data):
    encrypted_data = fernet.encrypt(data)
    with open(file_path, "wb") as f: f.write(encrypted_data)

def read_encrypted(file_path):
    with open(file_path, "rb") as f: return fernet.decrypt(f.read())

def load_disclosure():
    if os.path.exists(DISCLOSURE_FILE):
        with open(DISCLOSURE_FILE, "r") as f: return f.read()
    return "Standard Disclosure: Secure Underwriting in Progress."

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# ── 4. THE UI FLOW ───────────────────────────────────────────────────────────
if not st.session_state.authenticated:
    st.markdown("""
        <div class="viewport-top-container">
            <div class="brand-title">Utah Land & Property</div>
            <div class="brand-subtitle">Strategic Asset Protection Framework</div>
            <div style="margin-bottom: 2rem;"><span class="pulse-lock"></span><span class="access-text" style="color:#1a3c6d;">SECURE CLIENT PORTAL ENCRYPTED ACCESS ONLY</span></div>
        </div>
    """, unsafe_allow_html=True)
    
    _, col_mid, _ = st.columns([1, 1.6, 1])
    with col_mid:
        u_id = st.text_input("User ID", placeholder="Username", label_visibility="collapsed")
        u_pwd = st.text_input("Key", type="password", placeholder="Access Key", label_visibility="collapsed")
        if st.button("Access Portal", use_container_width=True, type="primary"):
            users = st.secrets.get("users", {})
            if u_id in users and str(users[u_id]["key"]) == u_pwd:
                st.session_state.authenticated = True
                st.session_state.user_id = u_id
                st.session_state.user_role = users[u_id]["role"]
                logger(u_id, "Login", "Success")
                st.rerun()
            else: st.error("Access Denied")

else:
    # ── 5. AUTHENTICATED DASHBOARD ──────────────────────────────────────────
    role = st.session_state.user_role
    user_id = st.session_state.user_id

    st.title(f"{role} Portal")
    st.warning(f"🔔 **Deal Structure:** {load_disclosure()}")
    
    # Logout in sidebar for clean UI
    if st.sidebar.button("Secure Logout"):
        st.session_state.authenticated = False
        st.rerun()

    # --- SHARED ACTIVITY VIEW ---
    st.subheader("Latest Activity")
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
            feed_cols[i].markdown(f'''
                <div class="recent-file-card">
                    <strong>{fname[:22]}...</strong><br>
                    <small style="color:#4b5563;">{ftype.title()} | {dt}</small>
                </div>
            ''', unsafe_allow_html=True)

    st.markdown("---")

    # --- ROLE LOGIC ---
    if role == "Admin":
        t1, t2, t3 = st.tabs(["Push Disclosure", "Assign Files", "System Audit"])
        
        with t1:
            st.write("### Update Deal Structure Text")
            new_disc = st.text_area("Disclosure Content", value=load_disclosure(), height=150)
            if st.button("Update Everyone"):
                with open(DISCLOSURE_FILE, "w") as f: f.write(new_disc)
                st.success("Disclosure updated.")
                st.rerun()

        with t2:
            st.write("### Encrypt & Assign Files")
            target = st.text_input("Target User ID (Must match exactly)")
            up_files = st.file_uploader("Upload Docs for Buyer", accept_multiple_files=True)
            if st.button("Secure & Assign") and up_files and target:
                for f in up_files:
                    save_encrypted(os.path.join("vault/buyer_docs", f"ENCR_{target}_{f.name}"), f.getbuffer())
                st.success(f"Files assigned to {target}")
                logger(user_id, "Admin Upload", f"To: {target}")

        with t3:
            st.write("### Security Log")
            if os.path.exists(AUDIT_FILE):
                st.table(pd.read_csv(AUDIT_FILE).tail(15))

    elif role == "Buyer":
        with st.expander("📊 Financial Underwriting Pre-Screen", expanded=True):
            inc = st.number_input("Monthly Income", value=5000, min_value=1)
            debt = st.number_input("Monthly Debt", value=1500, min_value=0)
            if st.button("Log Analysis"):
                logger(user_id, "Underwriting", f"DTI: {(debt/inc)*100:.1f}%")
                st.success("Analysis captured for review.")
        
        st.subheader("Your Secure Documents")
        # Isolation: Only show files with this user's ID
        docs = [f for f in os.listdir("vault/buyer_docs") if user_id in f]
        if docs:
            for d in docs:
                data = read_encrypted(os.path.join("vault/buyer_docs", d))
                st.download_button(f"📄 Download {d.split('_', 2)[-1]}", data, file_name=d)
        else:
            st.info("No documents released for your ID yet.")

    # Property Visuals Section
    st.markdown("---")
    st.subheader("Property Visuals")
    images = [f for f in os.listdir("vault/property_images") if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if images:
        cols = st.columns(4)
        for i, img in enumerate(images):
            cols[i % 4].image(os.path.join("vault/property_images", img), use_container_width=True)
