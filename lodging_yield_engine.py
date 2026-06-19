import streamlit as st
import pandas as pd
from datetime import datetime

# Page configuration setup
st.set_page_config(page_title="Autonomous Revenue Intelligence Lab", layout="wide")

# --- 🔒 SECURE PASSWORD GATEKEEPER LOOP ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def check_login():
    """Verifies access password string input directly"""
    if st.session_state["pass_input"] == "Gayan2026":
        st.session_state.authenticated = True
    else:
        st.error("🚨 Access Denied: Invalid System Password Token.")

if not st.session_state.authenticated:
    st.title("🔒 Enterprise Security Gateway")
    st.markdown("### Autonomous Revenue Guardrail Lab System Lock")
    st.text_input(
        "Enter authorized credential token to access matrix framework:", 
        type="password", 
        key="pass_input", 
        on_change=check_login
    )
    st.stop()  
# ------------------------------------------

# --- ALL ENGINE OPERATIONS EXECUTE BELOW ONLY IF AUTHENTICATED ---
st.title("🏨 Autonomous Revenue Guardrail Lab")
st.markdown("""
### MTD/OTB vs. Forecast Dynamic Pricing Architecture
*An operational framework testing automated month-by-month agentic pricing adjustments backed by deterministic safety circuit breakers.*
""")

st.markdown("---")

# --- 1. Property Metadata & Global Currency Setup ---
st.subheader("📍 Step 1: Define Property Profile & Currency Layer")

# Reset Function for Step 1
def clear_step_1_profile():
    st.session_state["city_input"] = ""
    st.session_state["country_input"] = ""
    st.session_state["subject_hotel_input"] = ""
    default_compset_rows = {
        "Compset Index": [f"0{i}. Compset Name" for i in range(1, 9)],
        "Hotel Identity Name": ["", "", "", "", "", "", "", ""]
    }
    st.session_state.compset_grid_df = pd.DataFrame(default_compset_rows)

if st.button("🗑️ Reset Profile & Compset (Wipe Step 1 Data)"):
    clear_step_1_profile()
    st.rerun()

col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    city = st.text_input("Destination City / Market Location", value="Salalah", key="city_input")
with col_m2:
    country = st.text_input("Destination Country", value="Oman", key="country_input")
with col_m3:
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

if "compset_grid_df" not in st.session_state:
    default_compset_rows = {
        "Compset Index": [f"0{i}. Compset Name" for i in range(1, 9)],
        "Hotel Identity Name": ["Grand Plaza Resort", "Ocean View Boutique", "Metropolitan Hub", "", "", "", "", ""]
    }
    st.session_state.compset_grid_df = pd.DataFrame(default_compset_rows)

col_prop1, col_prop2 = st.columns([1, 1])
with col_prop1:
    user_hotel = st.text_input("Your Property Name (Subject Hotel)", value="My Resort & Spa", key="subject_hotel_input")

with col_prop2:
    st.write("📋 **Map Competitive Set Names (Up to 8 Properties):**")
    edited_compset_grid = st.data_editor(
        st.session_state.compset_grid_df,
        num_rows="fixed",
        use_container_width=True,
        key="compset_grid_editor"
    )
    st.session_state.compset_grid_df = edited_compset_grid
    
    active_compset = []
    for _, row in edited_compset_grid.iterrows():
        val = row["Hotel Identity Name"]
        if val is not None:
            val_str = str(val).strip()
            if val_str != "" and val_str.lower() != "none":
                active_compset.append(val_str)
    compset_count = len(active_compset)

compset_verification = f"✅ {compset_count} Competitor(s) Mapped" if compset_count > 0 else "📝 Awaiting Compset Entry"
location_verification = "✅ Location Saved" if city.strip() and country.strip() else "📝 Awaiting Location"
hotel_verification = "✅ Hotel Name Saved" if user_hotel.strip() else "📝 Awaiting Hotel Name"

st.markdown(f"**Profile Status Tracking Verification Panel:** &nbsp;&nbsp;&nbsp;&nbsp; {location_verification} &nbsp;&nbsp;|&nbsp;&nbsp; {hotel_verification} &nbsp;&nbsp;|&nbsp;&nbsp; {compset_verification}")

# --- 2. Dynamic Forward 3-Month Matrix Calendar Calculations ---
current_month_name = datetime.now().strftime("%B")
months_list = [current_month_name]
current_month_num = datetime.now().month

for i in range(1, 3):
    future_month = datetime(2026, ((current_month_num + i - 1) % 12) + 1, 1)
    months_list.append(future_month.strftime("%B"))

st.markdown("---")

# --- 3. Structured Data Metrics Input Grid (MTD/OTB vs Forecast Rows) ---
st.subheader(f"📊 Step 2: Input Internal Performance Metrics ({currency_symbol})")
st.write("Track active pacing data alongside expected full-month forecast thresholds to generate context-aware AI parameters:")

row_labels = [
    f"{months_list[0]} (Current MTD Actuals)",
    f"{months_list[0]} (Full Month Forecast Target)",
    f"{months_list[1]} (On-The-Books / OTB Pace)",
    f"{months_list[1]} (Full Month Forecast Target)",
    f"{months_list[2]} (On-The-Books / OTB Pace)",
    f"{months_list[2]} (Full Month Forecast Target)"
]

default_pacing_data = {
    "Operational Tracking Layer": row_labels,
    "Room Nights": [800, 1200, 950, 1450, 600, 1500],
    "Revenue": [
        114000.0 * currency_scale, 
        180000.0 * currency_scale, 
        161500.0 * currency_scale, 
        246500.0 * currency_scale, 
        108000.0 * currency_scale, 
        270000.0 * currency_scale
    ]
}

# Fix: Ensure the data framework handles state switches without hiding subsequent elements
if "pacing_metrics_df" not in st.session_state or st.session_state.get("prev_currency_state") != selected_currency_key:
    st.session_state.pacing_metrics_df = pd.DataFrame(default_pacing_data)
    st.session_state.prev_currency_state = selected_currency_key

edited_pace_df = st.data_editor(
    st.session_state.pacing_metrics_df,
    num_rows="fixed",
    use_container_width=True,
    key="pace_vs_forecast_editor"
)
st.session_state.pacing_metrics_df = edited_pace_df

status_icons = []
for i in range(3):
    p_rn = edited_pace_df.iloc[i * 2]["Room Nights"]
    f_rn = edited_pace_df.iloc[(i * 2) + 1]["Room Nights"]
    if p_rn > 0 and f_rn > 0:
        status_icons.append(f"**{months_list[i]}:** ✅ Entered & Logged")
    else:
        status_icons.append(f"**{months_list[i]}:** 📝 Awaiting Entry")

st.markdown(f"**Metrics Status Tracking Verification Panel:** &nbsp;&nbsp;&nbsp;&nbsp; {status_icons[0]} &nbsp;&nbsp;|&nbsp;&nbsp; {status_icons[1]} &nbsp;&nbsp;|&nbsp;&nbsp; {status_icons[2]}")

if st.button("🗑️ Clear Metrics Grid (Reset Sheet Values)"):
    blank_pacing = {
        "Operational Tracking Layer": row_labels,
        "Room Nights": [0] * 6,
        "Revenue": [0.0] * 6
    }
    st.session_state.pacing_metrics_df = pd.DataFrame(blank_pacing)
    st.rerun()

st.markdown("---")

# --- 4. Month-by-Month Structured AI Revenue Diagnostics ---
st.subheader("📈 Step 3: Month-by-Month RM Analysis & Agentic Safety Loop")

is_salalah = city.lower().strip() == "salalah"
has_valid_data_rendered = False

for i in range(3):
    m_name = months_list[i]
    is_current_month = (i == 0)
    
    pace_row = edited_pace_df.iloc[i * 2]
    fore_row = edited_pace_df.iloc[(i * 2) + 1]
    
    pace_rn, pace_rev = pace_row["Room Nights"], pace_row["Revenue"]
    fore_rn, fore_rev = fore_row["Room Nights"], fore_row["Revenue"]
    
    if fore_rn > 0 and fore_rev > 0:
        has_valid_data_rendered = True
        forecast_adr = fore_rev / fore_rn
        rn_capture_pct = (pace_rn / fore_rn) * 100
        rev_capture_pct = (pace_rev / fore_rev) * 100 if fore_rev > 0 else 0.0
        
        is_high
