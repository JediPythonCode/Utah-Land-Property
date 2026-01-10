import streamlit as st
import os
import json
import pandas as pd
from datetime import datetime
from cryptography.fernet import Fernet
from collections.abc import Mapping

# ───────────────── CONFIG ─────────────────
st.set_page_config(
    page_title="Utah Land & Property",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ───────────────── SECRETS LOADING ─────────────────
def load_secrets():
    try:
        secret_key = st.secrets["secret_key"]
        users = st.secrets["users"]

        # IMPORTANT: st.secrets["users"] is NOT a dict, it's a Mapping
        if not isinstance(users, Mapping):
            st.error("🚨 USERS must be a table in secrets.toml")
            st.stop()

        return Fernet(secret_key.encode()), users

    except Exception as e:
        st.error(f"🚨 Secrets load failed: {e}")
        st.stop()

fernet, USER_DB = load_secrets()

# ───────────────── FILE SYSTEM ─────────────────
BASE_DIR = "vault"
BUYER_DIR = os.path.join(BASE_DIR, "buyer_docs")
META_DIR = os.path.join(BASE_DIR, "metadata")
AUDIT_FILE = os.path.join(BASE_DIR, "audit_log.csv")

for d in [BASE_DIR, BUYER_DIR, META_DIR]:
    os.makedirs(d, exist_ok=True)

# ───────────────── HELPERS ─────────────────
def log_event(user, action, detail=""):
    try:
        df = pd.DataFrame(
            [[datetime.now(), user, action, detail]],
            columns=["Time", "User", "Action", "Detail"]
        )
        df.to_csv(
            AUDIT_FILE,
            mode="a",
            header=not os.path.exists(AUDIT_FILE),
            index=False
        )
    except:
        pass  # Never block auth

def encrypt_save(path, data, note=""):
    with open(path, "wb") as f:
        f.write(fernet.encrypt(data))
    with open(os.path.join(META_DIR, os.path.basename(path) + ".json"), "w") as m:
        json.dump({"note": note}, m)

def decrypt_read(path):
    try:
        with open(path, "rb") as f:
            return fernet.decrypt(f.read())
    except:
        return None

def read_note(filename):
    p = os.path.join(META_DIR, filename + ".json")
    if os.path.exists(p):
        with open(p) as f:
            return json.load(f).get("note", "")
    return ""

# ───────────────── SESSION STATE ─────────────────
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# ───────────────── LOGIN ─────────────────
if not st.session_state.authenticated:
    st.title("🔐 Secure Client Portal")

    u = st.text_input("User ID")
    p = st.text_input("Access Key", type="password")

    if st.button("Login"):
        if u in USER_DB and p == str(USER_DB[u]["key"]):
            st.session_state.authenticated = True
            st.session_state.user = u
            st.session_state.role = USER_DB[u]["role"]
            log_event(u, "LOGIN", "SUCCESS")
            st.rerun()
        else:
            log_event(u or "UNKNOWN", "LOGIN", "FAILED")
            st.error("❌ Invalid credentials")

    st.stop()

# ───────────────── DASHBOARD ─────────────────
user = st.session_state.user
role = st.session_state.role

st.sidebar.write(f"👤 {user} ({role})")
if st.sidebar.button("Logout"):
    st.session_state.authenticated = False
    st.rerun()

st.title(f"{role} Dashboard")

# ───────────────── ADMIN ─────────────────
if role == "Admin":
    target = st.text_input("Target User ID")
    note = st.text_input("Note for Buyer")
    uploads = st.file_uploader("Upload Files", accept_multiple_files=True)

    if st.button("Encrypt & Assign") and target and uploads:
        for f in uploads:
            path = os.path.join(BUYER_DIR, f"{target}_{f.name}")
            encrypt_save(path, f.getbuffer(), note)
        log_event(user, "UPLOAD", f"Files for {target}")
        st.success("✅ Files assigned")

# ───────────────── BUYER ─────────────────
if role == "Buyer":
    st.subheader("📁 Your Documents")

    files = [f for f in os.listdir(BUYER_DIR) if f.startswith(user + "_")]

    if not files:
        st.info("No documents assigned yet.")

    for i, f in enumerate(files):
        data = decrypt_read(os.path.join(BUYER_DIR, f))
        note = read_note(f)

        st.write(f"**{f.split('_',1)[1]}**")
        if note:
            st.caption(f"📝 {note}")

        st.download_button(
            "Download",
            data,
            file_name=f.split("_",1)[1],
            key=f"dl{i}"
        )
        st.divider()
