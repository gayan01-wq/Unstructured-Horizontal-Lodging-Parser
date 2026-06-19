import streamlit as st
import pandas as pd
from datetime import datetime

# Set up page configurations
st.set_page_config(page_title="Autonomous Revenue Intelligence Lab", layout="wide")

st.title("🏨 Autonomous Revenue Guardrail Lab")
st.markdown("""
### Real-World Forward Pricing & Agentic Safety Loop
*An operational revenue dashboard allowing hoteliers to stress-test autonomous AI rate suggestions month-by-month against strict, localized floor parameters.*
""")

st.markdown("---")

# --- 1. Property Metadata & Global Currency Setup ---
st.subheader("📍 Step 1: Define Property Profile & Compset")
col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    city = st.text_input("Destination City / Market Location", value="Salalah")
with col_m2:
    country = st.text_input("Destination Country", value="Oman")
with col_m3:
    currency_options = {
        "USD ($) - United States Dollar": {"symbol": "$", "floor": 135.00, "factor": 1.0},
        "OMR (𐎱.regular) - Omani Rial": {"symbol": "OMR ", "floor": 52.00, "factor": 0.38},
        "AED (د.إ) - UAE Dirham": {"symbol": "AED ", "floor": 500.00, "factor": 3.67},
        "SAR (ر.س) - Saudi Riyal": {"symbol": "SAR ", "floor": 500.00, "factor": 3.75},
        "EUR (€) - Euro (Europe)": {"symbol": "€", "floor": 125.00, "factor": 0.92},
        "GBP (£) - British Pound": {"symbol": "£", "floor": 105.00, "factor": 0.79},
        "THB (฿) - Thai Baht (Asia)": {"symbol": "฿", "floor": 4500.00, "factor": 36.50}
    }
    selected_currency_key = st.selectbox("Select Operational Currency Tier", options=list(currency_options.keys()))
    currency_symbol = currency_options[selected_currency_key]["symbol"]
    currency_scale = currency_options[selected_currency_key]["factor"]
    currency_base_floor = currency_options[selected_currency_key]["floor"]

col_prop1, col_prop2 = st.columns(2)
with col_prop1:
    user_hotel = st.text_input("Your Property Name (Subject Hotel)", value="My Resort & Spa")
with col_prop2:
    compset_input = st.text_input("Enter Competitor Hotel Names (For Market Mapping)", 
                                  value="Grand Plaza Resort, Ocean View Boutique, Metropolitan Hub")

# Process compset names for metadata display
compset_list = [name.strip() for name in compset_input.split(",") if name.strip()]

# --- 2. Dynamic Forward 3-Month Tracker ---
current_month_name = datetime.now().strftime("%B")
months_list = [current_month_name]
current_month_num = datetime.now().month

for i in range(1, 3):
    future_month = datetime(2026, (current_month_num + i - 1) % 12 + 1, 1)
    months_list.append(future_month.strftime("%B"))

st.markdown("---")

# --- 3. Simple Real-World Data Input (Your Hotel Only) ---
st.subheader(f"📊 Step 2: Input Your Property Forward Metrics ({currency_symbol})")
st.write("Enter your hotel's internal targets for the upcoming three-month horizon. Competitor data is kept hidden to match operational realities.")

# Default template values scaled by currency selection
default_user_metrics = {
    "Month Horizon": months_list,
    "Target Room Nights": [1200, 1450, 1500],
    "Target Revenue": [180000.0 * currency_scale, 246500.0 * currency_scale, 270000.0 * currency_scale]
}

if "user_metrics_df" not in st.session_state or st.session_state.get("prev_currency_key") != selected_currency_key:
    st.session_state.user_metrics_df = pd.DataFrame(default_user_metrics)
    st.session_state.prev_currency_key = selected_currency_key

def clear_user_table():
    blank_metrics = {
        "Month Horizon": months_list,
        "Target Room Nights": [0, 0, 0],
        "Target Revenue": [0.0, 0.0, 0.0]
    }
    st.session_state.user_metrics_df = pd.DataFrame(blank_metrics)

if st.button("🗑️ Clear Table Data (Reset Sheet Values)"):
    clear_user_table()
    st.rerun()

# Editable table containing only the user's data rows
edited_user_df = st.data_editor(
    st.session_state.user_metrics_df, 
    num_rows="fixed", 
    use_container_width=True,
    key="user_only_grid_editor"
)
st.session_state.user_metrics_df = edited_user_df

st.markdown("---")

# --- 4. Month-by-Month Structured AI Revenue Diagnostics ---
st.subheader("📈 Step 3: Month-by-Month AI Pricing & Circuit Breaker Execution")

# Check if city is Salalah during Khareef peak season months
is_salalah = city.lower().strip() == "salalah"

# Loop through each month to output structured individual analysis cards
for index, row in edited_user_df.iterrows():
    m_name = row["Month Horizon"]
    m_rn = row["Target Room Nights"]
    m_rev = row["Target Revenue"]
    
    # Avoid mathematical errors if user cleared rows
    if m_rn > 0 and m_rev > 0:
        calculated_adr = m_rev / m_rn
        
        # Determine dynamic demand profiles based on the calendar month name
        is_high_season_month = m_name in ["June", "July", "August", "September"]
        
        if is_salalah and is_high_season_month:
            demand_profile = "CRITICAL / HIGH DEMAND (Khareef Monsoon Window)"
            demand_desc = "The Dhofar monsoon climate brings peak GCC leisure flows. Maximum inventory constraints detected."
            floor_adjusted = currency_base_floor * 1.30  #
