import streamlit as st
import pandas as pd
from datetime import datetime

# Page configuration setup
st.set_page_config(page_title="Autonomous Revenue Intelligence Lab", layout="wide")

st.title("🏨 Autonomous Revenue Guardrail Lab")
st.markdown("""
### MTD/OTB vs. Forecast Dynamic Pricing Architecture
*An operational framework testing automated month-by-month agentic pricing adjustments backed by deterministic safety circuit breakers.*
""")

st.markdown("---")

# --- 1. Property Metadata & Global Currency Setup ---
st.subheader("📍 Step 1: Define Property Profile & Currency Layer")
col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    city = st.text_input("Destination City / Market Location", value="Salalah")
with col_m2:
    country = st.text_input("Destination Country", value="Oman")
with col_m3:
    # Expanded Comprehensive Multi-Region Currency Selector (Asian, Middle East, Europe)
    currency_options = {
        "USD ($) - United States Dollar": {"symbol": "$", "floor": 135.00, "factor": 1.0},
        "OMR (𐎱) - Omani Rial": {"symbol": "OMR ", "floor": 52.00, "factor": 0.38},
        "AED (د.إ) - UAE Dirham": {"symbol": "AED ", "floor": 500.00, "factor": 3.67},
        "SAR (ر.س) - Saudi Riyal": {"symbol": "SAR ", "floor": 500.00, "factor": 3.75},
        "QAR (ر.ق) - Qatari Riyal": {"symbol": "QAR ", "floor": 500.00, "factor": 3.64},
        "KWD (د.ك) - Kuwaiti Dinar": {"symbol": "KWD ", "floor": 41.00, "factor": 0.31},
        "BHD (.د) - Bahraini Dinar": {"symbol": "BHD ", "floor": 51.00, "factor": 0.38},
        "THB (฿) - Thai Baht (Asia)": {"symbol": "฿", "floor": 4500.00, "factor": 36.50},
        "SGD ($) - Singapore Dollar": {"symbol": "SGD $", "floor": 180.00, "factor": 1.35},
        "MYR (RM) - Malaysian Ringgit": {"symbol": "RM ", "floor": 600.00, "factor": 4.70},
        "IDR (Rp) - Indonesian Rupiah": {"symbol": "Rp ", "floor": 2200000.00, "factor": 16400.00},
        "LKR (Rs) - Sri Lankan Rupee": {"symbol": "LKR Rs ", "floor": 40000.00, "factor": 300.00},
        "INR (₹) - Indian Rupee": {"symbol": "₹", "floor": 11000.00, "factor": 83.30},
        "JPY (¥) - Japanese Yen": {"symbol": "¥", "floor": 20000.00, "factor": 155.00},
        "CNY (¥) - Chinese Yuan": {"symbol": "CNY ¥", "floor": 950.00, "factor": 7.25},
        "EUR (€) - Euro (Europe)": {"symbol": "€", "floor": 125.00, "factor": 0.92},
        "GBP (£) - British Pound": {"symbol": "£", "floor": 105.00, "factor": 0.79}
    }
    selected_currency_key = st.selectbox("Select Operational Currency Tier", options=list(currency_options.keys()))
    currency_symbol = currency_options[selected_currency_key]["symbol"]
    currency_scale = currency_options[selected_currency_key]["factor"]
    currency_base_floor = currency_options[selected_currency_key]["floor"]

st.markdown("#### 🏢 Property Identity & Competitive Set Mapping")

# --- STEP 1 LIVE VERIFICATION SCANNER ---
if "compset_grid_df" not in st.session_state:
    default_compset_rows = {
        "Compset Index": [f"0{i}. Compset Name" for i in range(1, 9)],
        "Hotel Identity Name": ["Grand Plaza Resort", "Ocean View Boutique", "Metropolitan Hub", "", "", "", "", ""]
    }
    st.session_state.compset_grid_df = pd.DataFrame(default_compset_rows)

active_compset_check = [r["Hotel Identity Name"].strip() for _, r in st.session_state.compset_grid_df.iterrows() if r["Hotel Identity Name"].strip()]
compset_verification = f"✅ {len(active_compset_check)} Competitor(s) Mapped" if active_compset_check else "📝 Awaiting Compset Entry"
location_verification = "✅ Location Saved" if city.strip() and country.strip() else "📝 Awaiting Location"

# Display Step 1 Verification Panel
st.markdown(f"**Profile Status Tracking Verification Panel:** &nbsp;&nbsp;&nbsp;&nbsp; {location_verification} &nbsp;&nbsp;|&nbsp;&nbsp; {compset_verification}")

col_prop1, col_prop2 = st.columns([1, 1])
with col_prop1:
    user_hotel = st.text_input("Your Property Name (Subject Hotel)", value="My Resort & Spa")

with col_prop2:
    st.write("📋 **Map Competitive Set Names (Up to 8 Properties):**")
    edited_
