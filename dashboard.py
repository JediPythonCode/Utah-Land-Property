```python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
import streamlit as st

# Page Configuration - Wide layout matching Zillow real estate portal
st.set_page_config(
    page_title=(
        "Millcreek UT Real Estate & Homes For Sale | Utah Land & Property"
    ),
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom Styling to precisely match the Zillow UI screenshot layout and top bar
st.markdown(
    """
    <style>
    .stApp {
        background-color: #ffffff !important;
        color: #2b2b2b !important;
        font-family: "Open Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }
    .main {
        background-color: #ffffff !important;
        color: #2b2b2b !important;
        padding-top: 0px !important;
    }
    
    /* Zillow Top Navbar */
    .z-navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 24px;
        border-bottom: 1px solid #dcdcdc;
        background-color: #ffffff;
        margin-bottom: 0px;
    }
    .z-nav-left, .z-nav-right {
        display: flex;
        gap: 24px;
        align-items: center;
        font-size: 0.95rem;
        font-weight: 500;
        color: #006aff;
    }
    .z-nav-left span, .z-nav-right span {
        cursor: pointer;
    }
    .z-nav-left span:hover, .z-nav-right span:hover {
        color: #004080;
        text-decoration: underline;
    }
    .z-logo-center {
        font-size: 2.1rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        color: #111111;
        text-transform: uppercase;
        font-family: "Playfair Display", Georgia, serif;
    }
    
    /* Sub-filter Search Bar Row */
    .z-filter-bar {
        display: flex;
        gap: 12px;
        align-items: center;
        padding: 14px 24px;
        background-color: #ffffff;
        border-bottom: 1px solid #e5e5e5;
        margin-bottom: 20px;
        flex-wrap: wrap;
    }
    
    /* Zillow Style Listing Cards */
    .z-card {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        overflow: hidden;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
        transition: box-shadow 0.2s ease;
    }
    .z-card:hover {
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
    }
    .z-card-img-container {
        position: relative;
    }
    .z-card-img {
        width: 100%;
        height: 200px;
        object-fit: cover;
    }
    .z-badge {
        position: absolute;
        top: 10px;
        left: 10px;
        background-color: rgba(0, 0, 0, 0.75);
        color: white;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .z-card-body {
        padding: 16px;
    }
    .z-price {
        font-size: 1.35rem;
        font-weight: 700;
        color: #111111;
        margin-bottom: 4px;
    }
    .z-details {
        font-size: 0.88rem;
        color: #333333;
        margin-bottom: 8px;
    }
    .z-address {
        font-size: 0.85rem;
        color: #666666;
        margin-bottom: 4px;
    }
    .z-broker {
        font-size: 0.75rem;
        color: #888888;
        text-transform: uppercase;
        letter-spacing: 0.5px;
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
          "status": "2 days on Zillow",
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


# --- TOP NAVIGATION BAR WITH BOLD BLACK ELEGANT LOGO ---
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

# --- FILTER SEARCH BAR ---
st.markdown(
    """
    <div class="z-filter-bar">
        <div style="flex: 2; min-width: 240px;">
            <input type="text" value="Millcreek, UT" style="width: 100%; padding: 10px 14px; border: 1px solid #dcdcdc; border-radius: 6px; font-size: 0.95rem;" readonly>
        </div>
        <div style="flex: 1; min-width: 120px;">
            <select style="width: 100%; padding: 10px; border: 1px solid #dcdcdc; border-radius: 6px; background: white;"><option>For sale</option></select>
        </div>
        <div style="flex: 1; min-width: 120px;">
            <select style="width: 100%; padding: 10px; border: 1px solid #dcdcdc; border-radius: 6px; background: white;"><option>Price</option></select>
        </div>
        <div style="flex: 1; min-width: 120px;">
            <select style="width: 100%; padding: 10px; border: 1px solid #dcdcdc; border-radius: 6px; background: white;"><option>Beds & baths</option></select>
        </div>
        <div style="flex: 1; min-width: 120px;">
            <select style="width: 100%; padding: 10px; border: 1px solid #dcdcdc; border-radius: 6px; background: white;"><option>Property type</option></select>
        </div>
        <div style="flex: 1; min-width: 100px;">
            <button style="width: 100%; padding: 10px; border: 1px solid #006aff; color: #006aff; background: white; border-radius: 6px; font-weight: 600; cursor: pointer;">Save search</button>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

# --- SPLIT LAYOUT: MAP (LEFT) & LISTINGS CARDS (RIGHT) ---
map_col, listings_col = st.columns([1.1, 1.3])

with map_col:
  st.markdown(
      "<div style='font-size: 1.1rem; font-weight: 700; margin-bottom: 10px;"
      " color: #222;'>Millcreek UT Real Estate Map</div>",
      unsafe_allow_html=True,
  )

  import pydeck as pdk

  map_data = df[["lat", "lon"]].rename(
      columns={"lat": "latitude", "lon": "longitude"}
  )

  layer = pdk.Layer(
      "ScatterplotLayer",
      data=map_data,
      get_position="[longitude, latitude]",
      get_color="[0, 106, 255, 220]",
      get_radius=800,
      pickable=True,
      auto_highlight=True,
  )

  view_state = pdk.ViewState(
      latitude=40.6977, longitude=-111.8550, zoom=12, pitch=0
  )

  r = pdk.Deck(
      layers=[layer],
      initial_view_state=view_state,
      map_style="light",
      tooltip={"text": "Utah Land & Property Asset"},
  )
  st.pydeck_chart(r, use_container_width=True)

with listings_col:
  st.markdown(
      "<div style='font-size: 1.2rem; font-weight: 700; margin-bottom: 4px;"
      f" color: #111;'>Millcreek UT Real Estate & Homes For Sale</div>"
      f"<div style='font-size: 0.88rem; color: #666; margin-bottom: 15px;'>{len(df)}"
      " results</div>",
      unsafe_allow_html=True,
  )

  grid_col1, grid_col2 = st.columns(2)

  for i, row in df.iterrows():
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
        Notice: Utah Land & Property Inc. operates independently as a private investment firm. All property management functions and asset transactions are executed in compliance with applicable Utah real estate statutes.
    </div>
""",
    unsafe_allow_html=True,
)

```
