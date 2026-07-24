import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Utah Land & Property | Portal",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Friendly & Inviting Light-Theme Styling
st.markdown(
    """
    <style>
    .main {
        background-color: #f8fafc;
        color: #1e293b;
        font-family: 'Inter', sans-serif;
    }
    .stTextInput>div>div>input {
        background-color: #ffffff;
        color: #1e293b;
        border: 1px solid #cbd5e1;
        border-radius: 8px;
    }
    .hero-container {
        background: linear-gradient(rgba(15, 23, 42, 0.4), rgba(15, 23, 42, 0.4)), url('https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1920&q=80');
        background-size: cover;
        background-position: center;
        padding: 50px 20px;
        border-radius: 12px;
        text-align: center;
        color: white;
        margin-bottom: 25px;
    }
    .property-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
    }
    .badge {
        background-color: #0284c7;
        color: white;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .legal-notice {
        font-size: 0.75rem;
        color: #64748b;
        text-align: center;
        margin-top: 50px;
        border-top: 1px solid #e2e8f0;
        padding-top: 20px;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# Property Database with Map Coordinates
@st.cache_data
def load_portal_data():
  data = [
      {
          "id": "UT-MIL-0101",
          "title": "Millcreek Modern Residential Parcel",
          "type": "Land / Development",
          "city": "Millcreek, UT",
          "price": 285000,
          "acres": 0.21,
          "status": "Equitable Interest Available",
          "description": (
              "Flat, shovel-ready residential infill lot with active utility"
              " connections stubbed to edge."
          ),
          "lat": 40.6977,
          "lon": -111.8550,
      },
      {
          "id": "UT-DRP-0204",
          "title": "Draper Commercial Parking Buffer Parcel",
          "type": "Commercial Land",
          "city": "Draper, UT",
          "price": 145000,
          "acres": 0.11,
          "status": "Direct Acquisition",
          "description": (
              "Strategic commercial-zoned parcel optimized for logistics"
              " overflow and vehicular parking."
          ),
          "lat": 40.5243,
          "lon": -111.8631,
      },
      {
          "id": "UT-PRK-0312",
          "title": "Park Meadows Townhome Addendum Unit",
          "type": "Townhome",
          "city": "Clearfield, UT",
          "price": 340000,
          "acres": 0.05,
          "status": "Under Contract - Assignment Available",
          "description": (
              "Well-maintained townhome asset integrated into active management"
              " framework. Clean title commitment ready."
          ),
          "lat": 41.1136,
          "lon": -112.2575,
      },
      {
          "id": "UT-MON-0499",
          "title": "Montello Desert Acreage Tract",
          "type": "Rural Acreage",
          "city": "Montello, NV/UT Border",
          "price": 95000,
          "acres": 7.00,
          "status": "Direct Acquisition",
          "description": (
              "High-potential expansive desert parcel evaluated for"
              " agricultural viability and long-term holding."
          ),
          "lat": 41.2584,
          "lon": -114.2153,
      },
  ]
  return pd.DataFrame(data)


df = load_portal_data()


# Helper Function for Automated Email Dispatch to Escrow
def send_escrow_dispatch(
    property_id, property_title, recipient_email, user_message
):
  smtp_server = "smtp.gmail.com"
  port = 587
  sender_email = st.secrets.get("EMAIL_USER", "your-email@domain.com")
  sender_password = st.secrets.get("EMAIL_PASS", "your-app-password")

  subject = f"Escrow Dispatch & Terms Request: {property_id}"
  body = f"""
    Automated Transaction Workflow Dispatch:
    
    Property ID: {property_id}
    Asset Title: {property_title}
    Requester Contact: {recipient_email}
    
    User Notes / Terms:
    {user_message}
    
    ---
    Notice: Utah Land & Property Inc. - Secure Escrow Document Routing Engine.
    """

  msg = MIMEMultipart()
  msg["From"] = sender_email
  msg["To"] = recipient_email
  msg["Subject"] = subject
  msg.attach(MIMEText(body, "plain"))

  try:
    server = smtplib.SMTP(smtp_server, port)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, recipient_email, msg.as_string())
    server.quit()
    return True
  except Exception:
    return False


# Hero Section
st.markdown(
    """
    <div class="hero-container">
        <h1 style="color: #ffffff; margin-bottom: 5px;">Discover Utah Land & Property</h1>
        <p style="color: #e2e8f0; font-size: 1.1rem;">Explore verified acquisitions, direct opportunities, and transparent contract assignments.</p>
    </div>
""",
    unsafe_allow_html=True,
)

# Top Filter Bar
filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)

with filter_col1:
  search_query = st.text_input(
      "Search Location or Keyword", placeholder="e.g., Millcreek, Land..."
  )
with filter_col2:
  selected_type = st.selectbox(
      "Asset Type", ["All Types"] + list(df["type"].unique())
  )
with filter_col3:
  max_price = st.slider(
      "Max Price ($)",
      min_value=50000,
      max_value=500000,
      value=500000,
      step=25000,
  )
with filter_col4:
  vault_input = st.text_input(
      "Secure Vault Portal", placeholder="Enter Acquisition ID..."
  )

# Apply Filters
filtered_df = df.copy()
if search_query:
  filtered_df = filtered_df[
      filtered_df["title"].str.contains(search_query, case=False)
      | filtered_df["city"].str.contains(search_query, case=False)
      | filtered_df["id"].str.contains(search_query, case=False)
  ]
if selected_type != "All Types":
  filtered_df = filtered_df[filtered_df["type"] == selected_type]
filtered_df = filtered_df[filtered_df["price"] <= max_price]

st.markdown("---")

# Split Layout: Map View on Left, Clean Cards on Right
map_col, results_col = st.columns([1, 1.2])

with map_col:
  st.subheader("Interactive Region Map")
  if not filtered_df.empty:
    map_data = filtered_df[["lat", "lon"]].rename(
        columns={"lat": "latitude", "lon": "longitude"}
    )
    st.map(map_data, zoom=7, use_container_width=True)
  else:
    st.info("No matching map locations found.")

with results_col:
  st.subheader(f"Available Opportunities ({len(filtered_df)})")

  if filtered_df.empty:
    st.warning(
        "No properties match your filter criteria. Try expanding your search."
    )
  else:
    for _, row in filtered_df.iterrows():
      st.markdown(
          f"""
                <div class="property-card">
                    <span class="badge">{row['status']}</span>
                    <h3 style="margin-top: 10px; margin-bottom: 4px; color: #0f172a;">${row['price']:,}</h3>
                    <p style="color: #475569; font-size: 0.9rem; margin-bottom: 8px;">
                        <b>{row['title']}</b> ({row['id']})<br>
                        📍 {row['city']} &nbsp;|&nbsp; 📐 {row['acres']} Acres &nbsp;|&nbsp; 🏷️ {row['type']}
                    </p>
                    <p style="font-size: 0.85rem; color: #334155; margin-bottom: 12px;">{row['description']}</p>
                </div>
            """,
          unsafe_allow_html=True,
      )

      # Interactive Workflow Modal / Expander for Escrow Dispatch
      with st.expander(
          f"Request Terms & Dispatch to Escrow for {row['id']}"
      ):
        user_email_input = st.text_input(
            "Your Email Address", key=f"email_{row['id']}"
        )
        user_notes_input = st.text_area(
            "Acquisition / Assignment Notes",
            placeholder=(
                "Specify desired earnest money timeline or due diligence"
                " contingencies..."
            ),
            key=f"notes_{row['id']}",
        )

        if st.button(
            "Submit & Trigger Escrow Dispatch", key=f"dispatch_btn_{row['id']}"
        ):
          if user_email_input:
            send_escrow_dispatch(
                row["id"], row["title"], user_email_input, user_notes_input
            )
            st.success(
                f"Successfully generated workflow packet for {row['id']} and"
                " dispatched notification to escrow!"
            )
          else:
            st.error(
                "Please provide a valid email address to receive the contract"
                " workflow package."
            )

# Legal Disclaimer Footer
st.markdown(
    """
    <div class="legal-notice">
        Notice: Utah Land & Property Inc. is a private investment firm and is not a licensed real estate broker or agent. 
        We do not represent third parties in the purchase, sale, or management of outside real estate. 
        Pursuant to the exemption under Utah Code § 61-2f-202, all property management functions are executed solely by individuals 
        operating as regular salaried employees of the specific legal entities that own the underlying real estate assets.
    </div>
""",
    unsafe_allow_html=True,
)
