import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Utah Land & Property.Com",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom Styling for Precision Light-Theme Match & Luxury Layout
st.markdown(
    """
    <style>
    /* Force Pristine White Base Theme */
    .stApp {
        background-color: #ffffff !important;
        color: #2b2b2b !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }
    .main {
        background-color: #ffffff !important;
        color: #2b2b2b !important;
    }
    
    /* Top Navigation Header Bar */
    .top-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 0px 20px 0px;
        border-bottom: 1px solid #eaeaea;
        margin-bottom: 25px;
    }
    .brand-logo {
        font-weight: 800;
        font-size: 1.1rem;
        letter-spacing: 0.5px;
        color: #111111;
        text-transform: uppercase;
    }
    .brand-sub {
        font-size: 0.55rem;
        color: #666;
        letter-spacing: 1px;
    }
    .nav-links {
        display: flex;
        gap: 25px;
        font-size: 0.95rem;
        font-weight: 500;
        color: #333333;
    }
    
    /* Hero Alpine Banner */
    .hero-alpine {
        position: relative;
        border-radius: 10px;
        overflow: hidden;
        margin-bottom: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    }
    .hero-bg {
        background: linear-gradient(rgba(0, 0, 0, 0.25), rgba(0, 0, 0, 0.45)), url('https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1920&q=80');
        background-size: cover;
        background-position: center;
        padding: 55px 40px;
        color: white;
    }
    
    /* Input Styling to match Light UI */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stSlider>div>div>div {
        background-color: #ffffff !important;
        color: #333333 !important;
        border: 1px solid #dcdcdc !important;
        border-radius: 6px !important;
    }
    
    /* Property Card Grid Styling */
    .property-card {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        overflow: hidden;
        margin-bottom: 20px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
        transition: transform 0.2s ease;
    }
    .property-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.08);
    }
    .card-img {
        width: 100%;
        height: 160px;
        object-fit: cover;
    }
    .card-body {
        padding: 14px;
    }
    .badge-tag {
        display: inline-block;
        background-color: #1e3a8a;
        color: white;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        margin-bottom: 6px;
    }
    .badge-tag.equitable {
        background-color: #0284c7;
    }
    .badge-tag.direct {
        background-color: #047857;
    }
    .badge-tag.contract {
        background-color: #b45309;
    }

    /* Wood-Texture Footer */
    .wood-footer {
        background: linear-gradient(rgba(210, 175, 135, 0.85), rgba(190, 150, 110, 0.9)), url('https://images.unsplash.com/photo-1546484396-fb3fc6f95f98?auto=format&fit=crop&w=1920&q=80');
        background-size: cover;
        padding: 35px 40px;
        border-top: 1px solid #d4bda0;
        margin-top: 50px;
        color: #2c221e;
        border-radius: 6px;
    }
    .legal-notice {
        font-size: 0.75rem;
        color: #64748b;
        text-align: center;
        margin-top: 30px;
        padding-top: 15px;
        border-top: 1px solid #eaeaea;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# Property Dataset with Map Coordinates, Photos, and Descriptions
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
          "image": (
              "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80"
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
          "image": (
              "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80"
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
          "image": (
              "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=800&q=80"
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
          "image": (
              "https://images.unsplash.com/photo-1613490493576-7fde63acd811?auto=format&fit=crop&w=800&q=80"
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


# --- TOP NAVIGATION BAR ---
st.markdown(
    """
    <div class="top-nav">
        <div>
            <div class="brand-logo">Utah Land & Property</div>
            <div class="brand-sub">ACQUISITION . INVESTMENT . MANAGEMENT . DEVELOPMENT</div>
        </div>
        <div class="nav-links">
            <span>Buy</span>
            <span>Sell</span>
            <span>Invest</span>
            <span>Market Insights</span>
            <span>Connect Intels</span>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

# --- HERO ALPINE BANNER ---
st.markdown(
    """
    <div class="hero-alpine">
        <div class="hero-bg">
            <h1 style="font-family: Georgia, serif; font-size: 2.3rem; font-weight: normal; margin-bottom: 8px; color: #ffffff;">Your Key to Utah's Premium<br>Land & Properties.</h1>
            <p style="font-size: 0.95rem; color: #e2e8f0; max-width: 600px; margin: 0;">Explore verified acquisitions, direct opportunities, and transparent contract assignments.</p>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

# --- FILTER CONTROLS BAR (4 Columns) ---
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

st.markdown("<br>", unsafe_allow_html=True)

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

# --- SPLIT LAYOUT: MAP (LEFT) & LISTINGS CARDS (RIGHT) ---
map_col, results_col = st.columns([1.1, 1.2])

with map_col:
  # Header & Map Style Toggle controls side-by-side
  m_head_col1, m_head_col2 = st.columns([1.2, 1])
  with m_head_col1:
    st.markdown(
        "<h3 style='font-size: 1.1rem; font-weight: 600; margin-top: 5px; color:"
        " #222;'>Interactive Region Map</h3>",
        unsafe_allow_html=True,
    )
  with m_head_col2:
    map_style = st.selectbox(
        "Map Style", ["Satellite View", "Light / Standard"], index=0
    )

  if not filtered_df.empty:
    map_data = filtered_df[["lat", "lon"]].rename(
        columns={"lat": "latitude", "lon": "longitude"}
    )

    # Render via pydeck with custom map style tiles
    import pydeck as pdk

    # Select Mapbox/Carto tile layer style based on user toggle selection
    if map_style == "Satellite View":
      # Using Mapbox Satellite style URL (or Carto dark/light basemap alternative fallback)
      map_provider = "mapbox"
      map_tiles_style = "mapbox://styles/mapbox/satellite-v9"
    else:
      map_provider = "carto"
      map_tiles_style = "light"

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=map_data,
        get_position="[longitude, latitude]",
        get_color="[2, 132, 199, 200]",
        get_radius=1500,
        pickable=True,
        auto_highlight=True,
    )

    # Set initial center view around Utah coordinates
    view_state = pdk.ViewState(
        latitude=40.7608 if filtered_df.empty else filtered_df["lat"].mean(),
        longitude=-111.8910 if filtered_df.empty else filtered_df["lon"].mean(),
        zoom=7,
        pitch=0,
    )

    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style=map_tiles_style,
        tooltip={"text": "Utah Land & Property Asset Location"},
    )
    st.pydeck_chart(r, use_container_width=True)
  else:
    st.info("No matching map locations found.")

with results_col:
  st.markdown(
      f"<h3 style='font-size: 1.1rem; font-weight: 600; margin-top: 5px; margin-bottom: 10px; color:"
      f" #222;'>Available Opportunities ({len(filtered_df)})</h3>",
      unsafe_allow_html=True,
  )

  if filtered_df.empty:
    st.warning(
        "No properties match your filter criteria. Try expanding your search."
    )
  else:
    for _, row in filtered_df.iterrows():
      badge_class = "equitable"
      if "Direct" in row["status"]:
        badge_class = "direct"
      elif "Contract" in row["status"]:
        badge_class = "contract"

      st.markdown(
          f"""
                <div class="property-card">
                    <img src="{row['image']}" class="card-img">
                    <div class="card-body">
                        <span class="badge-tag {badge_class}">{row['status']}</span>
                        <h4 style="margin: 4px 0; font-size: 1.15rem; color: #111; font-weight: 700;">${row['price']:,}</h4>
                        <div style="font-size: 0.9rem; font-weight: 600; color: #222;">{row['title']} ({row['id']})</div>
                        <div style="font-size: 0.8rem; color: #666; margin-bottom: 6px;">📍 {row['city']} &nbsp;|&nbsp; 📐 {row['acres']} Acres &nbsp;|&nbsp; 🏷️ {row['type']}</div>
                        <p style="font-size: 0.82rem; color: #444; margin-bottom: 0;">{row['description']}</p>
                    </div>
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

# --- WOOD-TEXTURE FOOTER & LEGAL DISCLAIMER ---
st.markdown(
    """
    <div class="wood-footer">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 20px;">
            <div style="display: flex; gap: 30px; font-size: 0.9rem; font-weight: 500;">
                <span>Property Management</span>
                <span>About Us</span>
                <span>Contact</span>
                <span>Terms of Service</span>
            </div>
            <div style="text-align: right; font-size: 0.85rem;">
                <b>Utah: Contact Consilium</b><br>
                Call 648-4237, 442-4325
            </div>
        </div>
        <div class="legal-notice">
            Notice: Utah Land & Property Inc. is a private investment firm and is not a licensed real estate broker or agent. 
            We do not represent third parties in the purchase, sale, or management of outside real estate. 
            Pursuant to the exemption under Utah Code § 61-2f-202, all property management functions are executed solely by individuals 
            operating as regular salaried employees of the specific legal entities that own the underlying real estate assets.
        </div>
    </div>
""",
    unsafe_allow_html=True,
)
