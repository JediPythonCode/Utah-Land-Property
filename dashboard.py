from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import pandas as pd
import pydeck as pdk
import streamlit as st

# Page Configuration - Wide layout matching a premium real estate portal
st.set_page_config(
    page_title=(
        "Millcreek UT Real Estate & Homes For Sale | Utah Land & Property"
    ),
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom Styling - Modern, clean UI variables and refined CSS
st.markdown(
    """
    <style>
    :root {
        --primary-color: #006aff;
        --primary-hover: #0051cc;
        --bg-main: #ffffff;
        --bg-subtle: #f8fafc;
        --border-color: #e2e8f0;
        --text-main: #0f172a;
        --text-muted: #64748b;
    }
    
    .stApp {
        background-color: var(--bg-main) !important;
        color: var(--text-main) !important;
        font-family: "Open Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }
    .main {
        background-color: var(--bg-main) !important;
        color: var(--text-main) !important;
        padding-top: 0px !important;
    }
    
    /* Top Navbar */
    .z-navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 14px 28px;
        border-bottom: 1px solid var(--border-color);
        background-color: var(--bg-main);
        margin-bottom: 0px;
    }
    .z-nav-left, .z-nav-right {
        display: flex;
        gap: 24px;
        align-items: center;
        font-size: 0.92rem;
        font-weight: 600;
        color: var(--primary-color);
    }
    .z-nav-left span, .z-nav-right span {
        cursor: pointer;
    }
    .z-nav-left span:hover, .z-nav-right span:hover {
        color: var(--primary-hover);
        text-decoration: underline;
    }
    .z-logo-center {
        font-size: 1.8rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        color: var(--text-main);
        text-transform: uppercase;
        font-family: "Playfair Display", Georgia, serif;
    }
    
    /* Listing Cards */
    .z-card {
        background-color: var(--bg-main);
        border: 1px solid var(--border-color);
        border-radius: 10px;
        overflow: hidden;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .z-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -2px rgba(0, 0, 0, 0.04);
    }
    .z-card-img-container {
        position: relative;
    }
    .z-card-img {
        width: 100%;
        height: 210px;
        object-fit: cover;
    }
    .z-badge {
        position: absolute;
        top: 12px;
        left: 12px;
        background-color: rgba(15, 23, 42, 0.85);
        color: white;
        padding: 5px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.3px;
    }
    .z-card-body {
        padding: 18px;
    }
    .z-price {
        font-size: 1.4rem;
        font-weight: 700;
        color: var(--text-main);
        margin-bottom: 6px;
    }
    .z-details {
        font-size: 0.88rem;
        color: #334155;
        margin-bottom: 8px;
    }
    .z-address {
        font-size: 0.85rem;
        color: var(--text-muted);
        margin-bottom: 6px;
    }
    .z-broker {
        font-size: 0.72rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        font-weight: 700;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# Load Property Dataset matching Millcreek, UT real estate inventory
@st.cache_data
def load_zillow_data():
  data = [
      {
          "id": "UT-MIL-0101",
          "title": "Millcreek Modern Residential Parcel",
          "type": "Land / Development",
          "city": "Millcreek, UT",
          "price": 285000,
          "beds": 0,
          "baths": 0,
          "sqft": 9147,
          "status": "Equitable Interest Available",
          "address": "4646 S Quail Park Dr E #C, Millcreek, UT 84117",
          "broker": "UTAH LAND & PROPERTY INC.",
          "image": (
              "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80"
          ),
          "lat": 40.6977,
          "lon": -111.8550,
      },
      {
          "id": "UT-MIL-0102",
          "title": "Millcreek Elmwood Single Family Home",
          "type": "House for sale",
          "city": "Millcreek, UT",
          "price": 625000,
          "beds": 5,
          "baths": 2,
          "sqft": 2446,
          "status": "Showcase",
          "address": "718 E Elgin Ave, Millcreek, UT 84106",
          "broker": "OMADA REAL ESTATE",
          "image": (
              "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=800&q=80"
          ),
          "lat": 40.7012,
          "lon": -111.8670,
      },
      {
          "id": "UT-MIL-0103",
          "title": "Millbert Avenue Residence",
          "type": "House for sale",
          "city": "Salt Lake City, UT",
          "price": 650000,
          "beds": 5,
          "baths": 2,
          "sqft": 2852,
          "status": "2 days on market",
          "address": "1010 E Millbert Ave S, Salt Lake City, UT 84106",
          "broker": "SUMMIT SOTHEBY'S INTERNATIONAL REALTY",
          "image": (
              "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=800&q=80"
          ),
          "lat": 40.7045,
          "lon": -111.8590,
      },
      {
          "id": "UT-DRP-0204",
          "title": "Draper Commercial Parking Buffer Parcel",
          "type": "Commercial Land",
          "city": "Draper, UT",
          "price": 145000,
          "beds": 0,
          "baths": 0,
          "sqft": 4791,
          "status": "Direct Acquisition",
          "address": "12300 S Fort St, Draper, UT 84020",
          "broker": "UTAH LAND & PROPERTY INC.",
          "image": (
              "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80"
          ),
          "lat": 40.5243,
          "lon": -111.8631,
      },
  ]
  return pd.DataFrame(data)


df = load_zillow_data()


# Helper Function for Automated Email Dispatch
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
    User Notes / Terms: {user_message}
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


# --- TOP NAVIGATION BAR ---
st.markdown(
    """
    <div class="z-navbar">
        <div class="z-nav-left">
            <span>Buy</span>
            <span>Rent</span>
            <span>Sell</span>
            <span>Get a mortgage</span>
            <span>Find an agent</span>
        </div>
        <div class="z-logo-center">
            UTAH LAND & PROPERTY INC.
        </div>
        <div class="z-nav-right">
            <span>Manage rentals</span>
            <span>Advertise</span>
            <span>Get help</span>
            <span style="background-color: #006aff; color: white; padding: 8px 18px; border-radius: 6px; font-weight: 600;">Sign in</span>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

# --- INTERACTIVE FILTER & SEARCH BAR (Native Streamlit UI Widgets) ---
st.markdown(
    "<div style='padding: 12px 24px 0px 24px; background-color: #ffffff;'>",
    unsafe_allow_html=True,
)
f_col1, f_col2, f_col3, f_col4, f_col5, f_col6 = st.columns(
    [2.2, 1, 1, 1, 1, 1]
)

with f_col1:
  search_query = st.text_input(
      "Location Search", value="Millcreek, UT", label_visibility="collapsed"
  )
with f_col2:
  status_filter = st.selectbox(
      "Status", ["For sale", "All Statuses"], label_visibility="collapsed"
  )
with f_col3:
  price_filter = st.selectbox(
      "Price Range", ["Any Price", "Under $300k", "$300k - $700k"], label_visibility="collapsed"
  )
with f_col4:
  beds_filter = st.selectbox(
      "Beds", ["Beds & baths", "3+ Beds", "5+ Beds"], label_visibility="collapsed"
  )
with f_col5:
  type_filter = st.selectbox(
      "Property Type", ["Property type", "House", "Land / Commercial"], label_visibility="collapsed"
  )
with f_col6:
  save_btn = st.button("Save search", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<hr style='margin: 10px 0px 20px 0px; border-color: #e2e8f0;'>", unsafe_allow_html=True)

# --- FILTER LOGIC APPLIED TO DATAFRAME ---
filtered_df = df.copy()
if price_filter == "Under $300k":
  filtered_df = filtered_df[filtered_df["price"] <= 300000]
elif price_filter == "$300k - $700k":
  filtered_df = filtered_df[(filtered_df["price"] > 300000) & (filtered_df["price"] <= 700000)]

if beds_filter == "3+ Beds":
  filtered_df = filtered_df[filtered_df["beds"] >= 3]
elif beds_filter == "5+ Beds":
  filtered_df = filtered_df[filtered_df["beds"] >= 5]

if type_filter == "House":
  filtered_df = filtered_df[filtered_df["type"].str.contains("House", case=False, na=False)]
elif type_filter == "Land / Commercial":
  filtered_df = filtered_df[filtered_df["type"].str.contains("Land|Commercial", case=False, na=False)]

# --- SPLIT LAYOUT: MAP (LEFT) & LISTINGS CARDS (RIGHT) ---
map_col, listings_col = st.columns([1.1, 1.3], gap="medium")

with map_col:
  st.markdown(
      "<div style='font-size: 1.1rem; font-weight: 700; margin-bottom: 10px;"
      " color: #0f172a;'>Interactive Asset & Property Map</div>",
      unsafe_allow_html=True,
  )

  map_data = filtered_df[["lat", "lon"]].rename(
      columns={"lat": "latitude", "lon": "longitude"}
  )

  layer = pdk.Layer(
      "ScatterplotLayer",
      data=map_data,
      get_position="[longitude, latitude]",
      get_color="[0, 106, 255, 230]",
      get_radius=650,
      pickable=True,
      auto_highlight=True,
  )

  # Dynamic view centering based on active subset
  lat_center = filtered_df["lat"].mean() if not filtered_df.empty else 40.6977
  lon_center = filtered_df["lon"].mean() if not filtered_df.empty else -111.8550

  view_state = pdk.ViewState(
      latitude=lat_center, longitude=lon_center, zoom=11.5, pitch=0
  )

  r = pdk.Deck(
      layers=[layer],
      initial_view_state=view_state,
      map_style="light",
      tooltip={"text": "Utah Land & Property Asset Portfolio Location"},
  )
  st.pydeck_chart(r, use_container_width=True)

with listings_col:
  st.markdown(
      "<div style='font-size: 1.2rem; font-weight: 700; margin-bottom: 4px;"
      " color: #0f172a;'>Millcreek UT Real Estate & Homes For Sale</div>"
      f"<div style='font-size: 0.88rem; color: #64748b; margin-bottom: 15px;'>{len(filtered_df)}"
      " matching properties found</div>",
      unsafe_allow_html=True,
  )

  if filtered_df.empty:
    st.info("No properties match the selected filter criteria. Please adjust your filters.")
  else:
    grid_col1, grid_col2 = st.columns(2, gap="small")

    for i, (_, row) in enumerate(filtered_df.iterrows()):
      target_col = grid_col1 if i % 2 == 0 else grid_col2
      with target_col:
        st.markdown(
            f"""
                <div class="z-card">
                    <div class="z-card-img-container">
                        <img src="{row['image']}" class="z-card-img">
                        <div class="z-badge">{row['status']}</div>
                    </div>
                    <div class="z-card-body">
                        <div class="z-price">${row['price']:,}</div>
                        <div class="z-details"><b>{row['beds']}</b> bds &nbsp;|&nbsp; <b>{row['baths']}</b> ba &nbsp;|&nbsp; <b>{row['sqft']:,}</b> sqft &nbsp;|&nbsp; {row['type']}</div>
                        <div class="z-address">{row['address']}</div>
                        <div class="z-broker">{row['broker']}</div>
                    </div>
                </div>
            """,
            unsafe_allow_html=True,
        )

        with st.expander(f"Inquire / Escrow Dispatch ({row['id']})"):
          user_email = st.text_input(
              "Your Email", key=f"z_email_{row['id']}", placeholder="name@domain.com"
          )
          user_msg = st.text_area(
              "Terms / Contingencies",
              key=f"z_msg_{row['id']}",
              placeholder="Enter earnest money or inspection timelines...",
          )
          if st.button("Submit to Escrow", key=f"z_btn_{row['id']}"):
            if user_email:
              send_escrow_dispatch(row["id"], row["title"], user_email, user_msg)
              st.success("Workflow successfully dispatched to escrow!")
            else:
              st.error("Please enter a valid email address.")

# --- FOOTER LEGAL NOTICE ---
st.markdown(
    """
    <div style="font-size: 0.75rem; color: #64748b; text-align: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid #eaeaea;">
        Notice: Utah Land & Property Inc. operates independently as a private investment firm. All property management functions and asset transactions are executed in compliance with applicable Utah real estate statutes (Utah Code Ann. § 57-1 et seq. and § 61-2f-1 et seq.).
    </div>
""",
    unsafe_allow_html=True,
)
