import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Utah Land & Property.Com",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom Styling for Precision Light-Theme Match
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
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
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
    .badge-tag.open-house {
        background-color: #0284c7;
    }
    .badge-tag.commercial {
        background-color: #047857;
    }
    .badge-tag.premier {
        background-color: #b45309;
    }
    
    /* Action Buttons */
    .stButton>button {
        background-color: #b48a60 !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: 500 !important;
        padding: 6px 16px !important;
    }
    .stButton>button:hover {
        background-color: #9c7550 !important;
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
    </style>
""",
    unsafe_allow_html=True,
)


# Property Dataset
@st.cache_data
def load_portal_data():
  data = [
      {
          "id": "UT-MIL-0101",
          "title": "34 Mountain Peak Dr",
          "type": "Residential",
          "city": "Millcreek, UT",
          "price": 1380000,
          "beds": "4 Beds | 2.5 Baths | 3,500 sqft",
          "status": "NEW",
          "image": (
              "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80"
          ),
          "lat": 40.6977,
          "lon": -111.8550,
      },
      {
          "id": "UT-PRK-0312",
          "title": "149 Blackfoot Ln",
          "type": "Townhome",
          "city": "Clearfield, UT",
          "price": 995000,
          "beds": "3 Beds | 1 Bath | 2,200 sqft",
          "status": "OPEN HOUSE",
          "image": (
              "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=800&q=80"
          ),
          "lat": 41.1136,
          "lon": -112.2575,
      },
      {
          "id": "UT-DRP-0204",
          "title": "Lot B, Tech Center Dr",
          "type": "Commercial Land",
          "city": "Draper, UT",
          "price": 7999000,
          "beds": "5 Acres",
          "status": "COMMERCIAL LAND",
          "image": (
              "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80"
          ),
          "lat": 40.5243,
          "lon": -111.8631,
      },
      {
          "id": "UT-MON-0499",
          "title": "Alpine Summit Estate",
          "type": "Premier",
          "city": "Park City, UT",
          "price": 8450000,
          "beds": "10 Beds | 10 Baths | 9,000 sqft",
          "status": "PREMIER",
          "image": (
              "https://images.unsplash.com/photo-1613490493576-7fde63acd811?auto=format&fit=crop&w=800&q=80"
          ),
          "lat": 40.6461,
          "lon": -111.4980,
      },
  ]
  return pd.DataFrame(data)


df = load_portal_data()

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
            <h1 style="font-family: Georgia, serif; font-size: 2.5rem; font-weight: normal; margin-bottom: 10px; color: #ffffff;">Your Key to Utah's Premium<br>Land & Properties.</h1>
            <p style="font-size: 0.95rem; color: #e2e8f0; max-width: 600px; margin: 0;">Your gateway to premier Utah land opportunities and bespoke real estate assets designed for discerning buyers and strategic investors.</p>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

# --- FILTER CONTROLS BAR ---
fcol1, fcol2, fcol3, fcol4 = st.columns(4)

with fcol1:
  location_filter = st.selectbox(
      "Location", ["All Locations", "Millcreek, UT", "Draper, UT", "Park City, UT"]
  )
with fcol2:
  price_filter = st.selectbox(
      "Price Range",
      ["All Prices", "Under $1,000,000", "$1M - $5M", "$5M+"],
  )
with fcol3:
  type_filter = st.selectbox(
      "Property Type", ["All Types", "Residential", "Townhome", "Commercial Land", "Premier"]
  )
with fcol4:
  search_area_btn = st.text_input(
      "Search Area", placeholder="Draw a Search Area..."
  )

st.markdown("<br>", unsafe_allow_html=True)

# --- SPLIT LAYOUT: MAP (LEFT) & LISTINGS (RIGHT) ---
map_col, listings_col = st.columns([1.1, 1.2])

with map_col:
  st.markdown(
      "<h3 style='font-size: 1.1rem; font-weight: 600; margin-bottom: 10px; color:"
      " #222;'>Interactive Region Map</h3>",
      unsafe_allow_html=True,
  )
  map_data = df[["lat", "lon"]].rename(
      columns={"lat": "latitude", "lon": "longitude"}
  )
  st.map(map_data, zoom=8, use_container_width=True)

with listings_col:
  st.markdown(
      f"<h3 style='font-size: 1.1rem; font-weight: 600; margin-bottom: 10px; color:"
      f" #222;'>Featured Listings ({len(df)})</h3>",
      unsafe_allow_html=True,
  )

  # Render 2x2 Grid of Property Cards
  for i in range(0, len(df), 2):
    row_cols = st.columns(2)
    for j in range(2):
      if i + j < len(df):
        item = df.iloc[i + j]
        with row_cols[j]:
          badge_class = ""
          if item["status"] == "OPEN HOUSE":
            badge_class = "open-house"
          elif item["status"] == "COMMERCIAL LAND":
            badge_class = "commercial"
          elif item["status"] == "PREMIER":
            badge_class = "premier"

          st.markdown(
              f"""
                        <div class="property-card">
                            <img src="{item['image']}" class="card-img">
                            <div class="card-body">
                                <span class="badge-tag {badge_class}">{item['status']}</span>
                                <h4 style="margin: 4px 0; font-size: 1.15rem; color: #111; font-weight: 700;">${item['price']:,}</h4>
                                <div style="font-size: 0.85rem; font-weight: 600; color: #333;">{item['title']}</div>
                                <div style="font-size: 0.78rem; color: #666; margin-bottom: 10px;">{item['beds']}</div>
                            </div>
                        </div>
                    """,
              unsafe_allow_html=True,
          )
          if st.button("View Details", key=f"btn_{item['id']} bukan"):
            st.success(f"Loading files for {item['title']}...")

# --- WOOD-TEXTURE FOOTER ---
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
    </div>
""",
    unsafe_allow_html=True,
)
