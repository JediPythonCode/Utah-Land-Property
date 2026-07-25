from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import pandas as pd
import pydeck as pdk
import streamlit as st

# Page Configuration - Wide layout mimicking a professional real estate portal
st.set_page_config(
    page_title="Utah Real Estate & Land For Sale | Utah Land & Property",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom Styling: Slightly off-white Zillow UI background, ultra-sticky map pane matching scroll height, clean boundary separation
st.markdown(
    """
    <style>
    :root {
        --primary-color: #006aff;
        --primary-hover: #004080;
        --bg-main: #f4f5f7;
        --bg-card: #ffffff;
        --border-color: #dcdcdc;
        --text-main: #2b2b2b;
        --text-muted: #666666;
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
    
    /* Sticky Top Header Container */
    .sticky-header-container {
        position: sticky;
        top: 0;
        z-index: 999;
        background-color: #ffffff;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    }

    /* Top Navbar */
    .z-navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 24px;
        border-bottom: 1px solid var(--border-color);
        background-color: #ffffff;
    }
    .z-nav-left, .z-nav-right {
        display: flex;
        gap: 20px;
        align-items: center;
        font-size: 0.92rem;
        font-weight: 500;
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
        font-size: 1.9rem;
        font-weight: 900;
        letter-spacing: -0.5px;
        color: #111111;
        text-transform: uppercase;
        font-family: "Playfair Display", Georgia, serif;
    }
    
    /* Main Split Layout Containers with Zero Dead Space & True Stickiness */
    .portal-container {
        display: flex;
        width: 100%;
        background-color: var(--bg-main);
        padding-top: 10px;
        align-items: flex-start;
    }
    .map-pane {
        position: sticky;
        top: 145px; /* Sticks right below the sticky header */
        height: calc(100vh - 165px);
        width: 100%;
        padding: 16px;
        background-color: #ffffff;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        border: 1px solid #e0e0e0;
        margin: 10px 6px 10px 12px;
        display: flex;
        flex-direction: column;
    }
    .map-pane iframe, .map-pane div[data-testid="stPyDeckChart"] {
        flex-grow: 1;
    }
    .listings-pane {
        width: 100%;
        padding: 16px 24px 16px 16px;
        background-color: var(--bg-main);
        max-height: calc(100vh - 165px);
        overflow-y: auto;
        margin: 10px 12px 10px 6px;
    }
    
    /* Listing Cards */
    .z-card {
        background-color: var(--bg-card);
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
        height: 180px;
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
        padding: 14px;
    }
    .z-contract-price {
        font-size: 1.3rem;
        font-weight: 800;
        color: #006aff;
        margin-bottom: 2px;
    }
    .z-underlying-price {
        font-size: 0.9rem;
        font-weight: 600;
        color: #444444;
        margin-bottom: 6px;
    }
    .z-details {
        font-size: 0.85rem;
        color: #333333;
        margin-bottom: 6px;
    }
    .z-address {
        font-size: 0.82rem;
        color: #666666;
        margin-bottom: 4px;
    }
    .z-broker {
        font-size: 0.72rem;
        color: #888888;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# Expanded Utah Property Database with 15 Contracts for Sale (Equitable Interest Assignments & Underlying Purchase Prices)
@st.cache_data
def load_utah_property_database():
  data = [
      {
          "id": "UT-MIL-0101",
          "title": "Millcreek Modern Residential Parcel",
          "type": "Contract for Sale / Land",
          "city": "Millcreek, UT",
          "contract_price": 28500,
          "underlying_price": 285000,
          "beds": 0,
          "baths": 0,
          "sqft": 9147,
          "status": "Equitable Interest Available",
          "address": "4646 S Quail Park Dr E #C, Millcreek, UT 84117",
          "broker": "UTAH LAND & PROPERTY INC.",
          "image": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80",
          "lat": 40.6977,
          "lon": -111.8550,
      },
      {
          "id": "UT-MIL-0102",
          "title": "Millcreek Elmwood Contract Assignment",
          "type": "Contract for Sale / House",
          "city": "Millcreek, UT",
          "contract_price": 45000,
          "underlying_price": 625000,
          "beds": 5,
          "baths": 2,
          "sqft": 2446,
          "status": "Showcase",
          "address": "718 E Elgin Ave, Millcreek, UT 84106",
          "broker": "OMADA REAL ESTATE",
          "image": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=800&q=80",
          "lat": 40.7012,
          "lon": -111.8670,
      },
      {
          "id": "UT-SLC-0103",
          "title": "Millbert Avenue Purchase Agreement",
          "type": "Contract for Sale / House",
          "city": "Salt Lake City, UT",
          "contract_price": 52000,
          "underlying_price": 650000,
          "beds": 5,
          "baths": 2,
          "sqft": 2852,
          "status": "2 days on market",
          "address": "1010 E Millbert Ave S, Salt Lake City, UT 84106",
          "broker": "SUMMIT SOTHEBY'S INTERNATIONAL REALTY",
          "image": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=800&q=80",
          "lat": 40.7045,
          "lon": -111.8590,
      },
      {
          "id": "UT-DRP-0204",
          "title": "Draper Commercial Buffer REPC Assignment",
          "type": "Contract for Sale / Commercial",
          "city": "Draper, UT",
          "contract_price": 15000,
          "underlying_price": 145000,
          "beds": 0,
          "baths": 0,
          "sqft": 4791,
          "status": "Direct Acquisition",
          "address": "12300 S Fort St, Draper, UT 84020",
          "broker": "UTAH LAND & PROPERTY INC.",
          "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
          "lat": 40.5243,
          "lon": -111.8631,
      },
      {
          "id": "UT-PRO-0301",
          "title": "Provo Riverfront Purchase Contract",
          "type": "Contract for Sale / Land",
          "city": "Provo, UT",
          "contract_price": 35000,
          "underlying_price": 410000,
          "beds": 0,
          "baths": 0,
          "sqft": 12500,
          "status": "New Listing",
          "address": "1850 N University Pkwy, Provo, UT 84604",
          "broker": "UTAH LAND & PROPERTY INC.",
          "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
          "lat": 40.2542,
          "lon": -111.6608,
      },
      {
          "id": "UT-OGD-0401",
          "title": "Ogden Historic Bench REPC",
          "type": "Contract for Sale / House",
          "city": "Ogden, UT",
          "contract_price": 38000,
          "underlying_price": 485000,
          "beds": 4,
          "baths": 3,
          "sqft": 3100,
          "status": "Price Improvement",
          "address": "1420 25th St, Ogden, UT 84401",
          "broker": "WASATCH HOMES",
          "image": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80",
          "lat": 41.2230,
          "lon": -111.9738,
      },
      {
          "id": "UT-PARK-0501",
          "title": "Park City Mountain View Townhome Contract",
          "type": "Contract for Sale / Townhouse",
          "city": "Park City, UT",
          "contract_price": 95000,
          "underlying_price": 1250000,
          "beds": 3,
          "baths": 4,
          "sqft": 2400,
          "status": "Exclusive",
          "address": "Park Meadows Townhomes, Park City, UT 84060",
          "broker": "SUMMIT SOTHEBY'S",
          "image": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=800&q=80",
          "lat": 40.6461,
          "lon": -111.4980,
      },
      {
          "id": "UT-STG-0601",
          "title": "St. George Red Rock Master REPC",
          "type": "Contract for Sale / Commercial",
          "city": "St. George, UT",
          "contract_price": 75000,
          "underlying_price": 890000,
          "beds": 0,
          "baths": 0,
          "sqft": 45000,
          "status": "Entitled Land",
          "address": "SunRiver Pkwy, St. George, UT 84790",
          "broker": "UTAH LAND & PROPERTY INC.",
          "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
          "lat": 37.0952,
          "lon": -113.5610,
      },
      {
          "id": "UT-LEH-0701",
          "title": "Lehi Silicon Slopes Purchase Agreement",
          "type": "Contract for Sale / Mixed-Use",
          "city": "Lehi, UT",
          "contract_price": 60000,
          "underlying_price": 750000,
          "beds": 4,
          "baths": 3,
          "sqft": 3400,
          "status": "Active",
          "address": "3300 N Ashton Blvd, Lehi, UT 84043",
          "broker": "MOUNTAINLAND REALTY",
          "image": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=800&q=80",
          "lat": 40.4153,
          "lon": -111.8398,
      },
      {
          "id": "UT-SLC-0801",
          "title": "Sugar House Bungalow Assignment",
          "type": "Contract for Sale / House",
          "city": "Salt Lake City, UT",
          "contract_price": 42000,
          "underlying_price": 540000,
          "beds": 3,
          "baths": 2,
          "sqft": 1850,
          "status": "New Listing",
          "address": "2100 S Highland Dr, Salt Lake City, UT 84106",
          "broker": "UTAH LAND & PROPERTY INC.",
          "image": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80",
          "lat": 40.7215,
          "lon": -111.8565,
      },
      {
          "id": "UT-MUR-0901",
          "title": "Murray Metro Condominium REPC",
          "type": "Contract for Sale / Condo",
          "city": "Murray, UT",
          "contract_price": 12000,
          "underlying_price": 245000,
          "beds": 2,
          "baths": 1,
          "sqft": 950,
          "status": "Equitable Interest Available",
          "address": "4800 S State St, Murray, UT 84107",
          "broker": "WASATCH HOMES",
          "image": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=800&q=80",
          "lat": 40.6678,
          "lon": -111.8902,
      },
      {
          "id": "UT-WVC-1001",
          "title": "West Valley Family Estate Contract",
          "type": "Contract for Sale / House",
          "city": "West Valley City, UT",
          "contract_price": 34000,
          "underlying_price": 460000,
          "beds": 4,
          "baths": 2,
          "sqft": 2100,
          "status": "Active",
          "address": "3600 S Redwood Rd, West Valley City, UT 84119",
          "broker": "MOUNTAINLAND REALTY",
          "image": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=800&q=80",
          "lat": 40.6970,
          "lon": -111.9380,
      },
      {
          "id": "UT-SAN-1101",
          "title": "Sandy Foothills Townhome REPC",
          "type": "Contract for Sale / Townhouse",
          "city": "Sandy, UT",
          "contract_price": 28000,
          "underlying_price": 395000,
          "beds": 3,
          "baths": 2,
          "sqft": 1650,
          "status": "Price Improvement",
          "address": "10000 S State St, Sandy, UT 84070",
          "broker": "OMADA REAL ESTATE",
          "image": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=800&q=80",
          "lat": 40.5820,
          "lon": -111.8900,
      },
      {
          "id": "UT-MID-1201",
          "title": "Midvale Central Station Land Contract",
          "type": "Contract for Sale / Land",
          "city": "Midvale, UT",
          "contract_price": 22000,
          "underlying_price": 290000,
          "beds": 0,
          "baths": 0,
          "sqft": 6500,
          "status": "Direct Acquisition",
          "address": "7500 S State St, Midvale, UT 84047",
          "broker": "UTAH LAND & PROPERTY INC.",
          "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
          "lat": 40.6120,
          "lon": -111.8904,
      },
      {
          "id": "UT-BOV-1301",
          "title": "Bountiful Bench View REPC Assignment",
          "type": "Contract for Sale / House",
          "city": "Bountiful, UT",
          "contract_price": 49000,
          "underlying_price": 580000,
          "beds": 4,
          "baths": 3,
          "sqft": 2700,
          "status": "Exclusive",
          "address": "500 S Main St, Bountiful, UT 84010",
          "broker": "SUMMIT SOTHEBY'S",
          "image": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80",
          "lat": 40.8870,
          "lon": -111.8800,
      },
  ]
  return pd.DataFrame(data)


df = load_utah_property_database()


# Helper Function for Automated Email / Offer Dispatch
def send_offer_dispatch(
    property_id, property_title, recipient_email, offer_terms
):
  smtp_server = "smtp.gmail.com"
  port = 587
  sender_email = st.secrets.get("EMAIL_USER", "your-email@domain.com")
  sender_password = st.secrets.get("EMAIL_PASS", "your-app-password")

  subject = f"Official Offer / Escrow Submission: {property_id}"
  body = f"""
    Automated Transaction & Offer Workflow Dispatch:
    Property ID: {property_id}
    Asset Title: {property_title}
    Submitter Contact: {recipient_email}
    Offer Terms & Conditions: {offer_terms}
    ---
    Notice: Utah Land & Property Inc. - Secure Escrow & Offer Routing Engine.
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


# --- EYE-CATCHING HERO BANNER IMAGE (HOME & LAND) ---
st.markdown(
    """
    <div style="width: 100%; height: 210px; overflow: hidden; position: relative; margin-bottom: 0px;">
        <img src="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1600&q=85" style="width: 100%; height: 100%; object-fit: cover; filter: brightness(0.9);">
        <div style="position: absolute; bottom: 18px; left: 30px; color: white; background: rgba(0,0,0,0.6); padding: 8px 16px; border-radius: 6px; font-family: 'Playfair Display', Georgia, serif;">
            <div style="font-size: 1.4rem; font-weight: 700; letter-spacing: 0.5px;">Utah Real Estate Contracts & Equitable Interest Portfolios</div>
            <div style="font-size: 0.85rem; font-weight: 400; opacity: 0.9;">Secure REPC assignments and purchase contracts across Utah cities.</div>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

# --- STICKY HEADER WRAPPER (Navbar + Filter Bar) ---
st.markdown("<div class='sticky-header-container'>", unsafe_allow_html=True)

# --- TOP NAVIGATION BAR ---
st.markdown(
    """
    <div class="z-navbar">
        <div class="z-nav-left">
            <span>Buy Contracts</span>
            <span>Assign</span>
            <span>Sell</span>
            <span>Get a mortgage</span>
            <span style="color: #004080; font-weight: 700;">Submit an Offer</span>
        </div>
        <div class="z-logo-center">
            UTAH LAND & PROPERTY INC.
        </div>
        <div class="z-nav-right">
            <span>Manage Contracts</span>
            <span>Advertise</span>
            <span>Get help</span>
            <span style="background-color: #006aff; color: white; padding: 8px 18px; border-radius: 6px; font-weight: 600;">Sign in</span>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

# --- ZILLOW-STYLE VAST UTAH CITY & FILTER SEARCH BAR ---
st.markdown(
    "<div style='padding: 12px 24px; background-color: #ffffff; border-bottom: 1px solid #e5e5e5;'>",
    unsafe_allow_html=True,
)
f_col1, f_col2, f_col3, f_col4, f_col5, f_col6 = st.columns(
    [2.2, 1, 1, 1, 1, 1]
)

all_locations = [
    "All Utah Cities",
    "Millcreek, UT",
    "Salt Lake City, UT",
    "Draper, UT",
    "Provo, UT",
    "Ogden, UT",
    "Park City, UT",
    "St. George, UT",
    "Lehi, UT",
    "Murray, UT",
    "West Valley City, UT",
    "Sandy, UT",
    "Midvale, UT",
    "Bountiful, UT",
]

with f_col1:
  selected_location = st.selectbox(
      "Utah City Search", all_locations, label_visibility="collapsed"
  )
with f_col2:
  status_filter = st.selectbox(
      "Status", ["Contracts for Sale", "All Statuses"], label_visibility="collapsed"
  )
with f_col3:
  price_filter = st.selectbox(
      "Contract Price",
      ["Any Price", "Under $30k", "$30k - $60k", "Over $60k"],
      label_visibility="collapsed",
  )
with f_col4:
  beds_filter = st.selectbox(
      "Beds",
      ["Beds & baths", "2+ Beds", "3+ Beds", "4+ Beds"],
      label_visibility="collapsed",
  )
with f_col5:
  type_filter = st.selectbox(
      "Contract Type",
      ["Property type", "House", "Land / Development", "Townhouse", "Condo"],
      label_visibility="collapsed",
  )
with f_col6:
  save_btn = st.button("Save search", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)  # End of sticky-header-container

# --- FILTER LOGIC ---
filtered_df = df.copy()
if selected_location != "All Utah Cities":
  filtered_df = filtered_df[
      filtered_df["city"].str.lower() == selected_location.lower()
  ]

if price_filter == "Under $30k":
  filtered_df = filtered_df[filtered_df["contract_price"] <= 30000]
elif price_filter == "$30k - $60k":
  filtered_df = filtered_df[
      (filtered_df["contract_price"] > 30000)
      & (filtered_df["contract_price"] <= 60000)
  ]
elif price_filter == "Over $60k":
  filtered_df = filtered_df[filtered_df["contract_price"] > 60000]

if beds_filter == "2+ Beds":
  filtered_df = filtered_df[filtered_df["beds"] >= 2]
elif beds_filter == "3+ Beds":
  filtered_df = filtered_df[filtered_df["beds"] >= 3]
elif beds_filter == "4+ Beds":
  filtered_df = filtered_df[filtered_df["beds"] >= 4]

if type_filter != "Property type":
  filtered_df = filtered_df[
      filtered_df["type"].str.contains(type_filter, case=False, na=False)
  ]

# --- PORTAL LAYOUT WITH STICKY SIDE MAP & NO DEAD SPACE ---
st.markdown("<div class='portal-container'>", unsafe_allow_html=True)

map_container, listings_container = st.columns([1, 1], gap="small")

# Left Pane: Ultra-Sticky Map View filling vertical space seamlessly
with map_container:
  st.markdown("<div class='map-pane'>", unsafe_allow_html=True)
  location_title = (
      selected_location
      if selected_location != "All Utah Cities"
      else "Utah Statewide"
  )
  st.markdown(
      f"<div style='font-size: 1.05rem; font-weight: 700; margin-bottom: 8px; color: #111;'>{location_title} Real Estate Contracts Map</div>",
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
      get_radius=800,
      pickable=True,
      auto_highlight=True,
  )

  lat_center = (
      filtered_df["lat"].mean() if not filtered_df.empty else 40.6977
  )
  lon_center = (
      filtered_df["lon"].mean() if not filtered_df.empty else -111.8550
  )
  zoom_level = 11 if selected_location != "All Utah Cities" else 7

  view_state = pdk.ViewState(
      latitude=lat_center, longitude=lon_center, zoom=zoom_level, pitch=0
  )

  r = pdk.Deck(
      layers=[layer],
      initial_view_state=view_state,
      map_style="light",
      tooltip={"text": "Utah Land & Property Equitable Interest Contract"},
  )
  st.pydeck_chart(r, use_container_width=True)
  st.markdown("</div>", unsafe_allow_html=True)

# Right Pane: Property Listings Cards with independent scrolling matching container height
with listings_container:
  st.markdown("<div class='listings-pane'>", unsafe_allow_html=True)
  st.markdown(
      f"<div style='font-size: 1.15rem; font-weight: 700; margin-bottom: 4px; color: #111;'>{location_title} Real Estate Contracts For Sale</div>"
      f"<div style='font-size: 0.85rem; color: #666; margin-bottom: 12px;'>{len(filtered_df)} contracts found</div>",
      unsafe_allow_html=True,
  )

  if filtered_df.empty:
    st.info("No contracts found matching your search criteria in this region.")
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
                        <div class="z-contract-price">Contract: ${row['contract_price']:,}</div>
                        <div class="z-underlying-price">Property Value: ${row['underlying_price']:,}</div>
                        <div class="z-details"><b>{row['beds']}</b> bds &nbsp;|&nbsp; <b>{row['baths']}</b> ba &nbsp;|&nbsp; <b>{row['sqft']:,}</b> sqft</div>
                        <div class="z-address">{row['address']}</div>
                        <div class="z-broker">{row['broker']}</div>
                    </div>
                </div>
            """,
            unsafe_allow_html=True,
        )

        with st.expander(f"Submit Offer / Terms ({row['id']})"):
          user_email = st.text_input(
              "Your Email",
              key=f"z_email_{row['id']}",
              placeholder="name@domain.com",
          )
          offer_terms = st.text_area(
              "Offer Terms & Conditions",
              key=f"z_msg_{row['id']}",
              placeholder=(
                  "Enter contract purchase price, assignment fee, or escrow"
                  " contingencies..."
              ),
          )
          if st.button("Submit Official Offer", key=f"z_btn_{row['id']}"):
            if user_email:
              send_offer_dispatch(row["id"], row["title"], user_email, offer_terms)
              st.success("Offer successfully dispatched to escrow!")
            else:
              st.error("Please enter a valid email address.")

  st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# --- FOOTER LEGAL NOTICE ---
st.markdown(
    """
    <div style="font-size: 0.72rem; color: #64748b; text-align: center; margin-top: 20px; padding-bottom: 20px; border-top: 1px solid #eaeaea;">
Notice: Utah Land & Property Inc. is a private investment firm and is not a licensed real estate broker or agent.
We do not represent third parties in the purchase, sale, or management of outside real estate.
Pursuant to the exemption under Utah Code § 61-2f-202, all property management functions are executed solely by individuals,
operating as regular salaried employees of the specific legal entities that own the underlying real estate assets.
    </div>
""",
    unsafe_allow_html=True,
)
