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

compset_list = [name.strip() for name in compset_input.split(",") if name.strip()]

# --- 2. Dynamic Forward 3-Month Matrix Calendar Calculations ---
current_month_name = datetime.now().strftime("%B")
months_list = [current_month_name]
current_month_num = datetime.now().month

for i in range(1, 3):
    future_month = datetime(2026, (current_month_num + i - 1) % 12 + 1, 1)
    months_list.append(future_month.strftime("%B"))

st.markdown("---")

# --- 3. Structured Data Metrics Input Grid (MTD/OTB vs Forecast Rows) ---
st.subheader(f"📊 Step 2: Input Internal Performance Metrics ({currency_symbol})")
st.write("Track active pace data alongside expected full-month forecast thresholds to generate context-aware AI parameters:")

# Set up the precise structural rows requested
row_labels = [
    f"{months_list[0]} (Current MTD)",
    f"{months_list[0]} (Full Month Forecast)",
    f"{months_list[1]} (On-The-Books / OTB)",
    f"{months_list[1]} (Full Month Forecast)",
    f"{months_list[2]} (On-The-Books / OTB)",
    f"{months_list[2]} (Full Month Forecast)"
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

if "pacing_metrics_df" not in st.session_state or st.session_state.get("prev_currency_state") != selected_currency_key:
    st.session_state.pacing_metrics_df = pd.DataFrame(default_pacing_data)
    st.session_state.prev_currency_state = selected_currency_key

if st.button("🗑️ Clear Table Data (Reset Sheet Values)"):
    blank_pacing = {
        "Operational Tracking Layer": row_labels,
        "Room Nights": [0] * 6,
        "Revenue": [0.0] * 6
    }
    st.session_state.pacing_metrics_df = pd.DataFrame(blank_pacing)
    st.rerun()

edited_pace_df = st.data_editor(
    st.session_state.pacing_metrics_df,
    num_rows="fixed",
    use_container_width=True,
    key="pace_vs_forecast_editor"
)
st.session_state.pacing_metrics_df = edited_pace_df

st.markdown("---")

# --- 4. Month-by-Month Structured AI Revenue Diagnostics ---
st.subheader("📈 Step 3: Month-by-Month AI Pricing & Circuit Breaker Execution")

is_salalah = city.lower().strip() == "salalah"

# We iterate through our data pairs step-wise (jumping by 2 lines to handle each month's pairing)
for i in range(3):
    m_name = months_list[i]
    is_current_month = (i == 0)
    
    # Extract data pairs from row slices
    pace_row = edited_pace_df.iloc[i * 2]
    fore_row = edited_pace_df.iloc[(i * 2) + 1]
    
    pace_rn, pace_rev = pace_row["Room Nights"], pace_row["Revenue"]
    fore_rn, fore_rev = fore_row["Room Nights"], fore_row["Revenue"]
    
    # Process only if user has filled forecast benchmarks
    if fore_rn > 0 and fore_rev > 0:
        forecast_adr = fore_rev / fore_rn
        pace_adr = pace_rev / pace_rn if pace_rn > 0 else 0.0
        
        # Calculate exactly how much business is already locked in relative to target expectations
        rn_capture_pct = (pace_rn / fore_rn) * 100
        rev_capture_pct = (pace_rev / fore_rev) * 100 if fore_rev > 0 else 0.0
        
        # Dynamic Seasonal Intelligence Injections
        is_high_season_month = m_name in ["June", "July", "August", "September"]
        
        if is_salalah and is_high_season_month:
            demand_profile = "CRITICAL / PEAK SEASON (Khareef Monsoon Window)"
            demand_desc = "The Dhofar monsoon climate brings peak regional leisure flows. Maximum seasonal room constraints active."
            base_floor = currency_base_floor * 1.35
        elif is_high_season_month:
            demand_profile = "ELEVATED DEMAND (Summer Holiday Window)"
            demand_desc = "Standard regional leisure vacation adjustments active. Normal competitive pacing parameters."
            base_floor = currency_base_floor * 1.10
        else:
            demand_profile = "STABLE / STEADY-STATE DESTINATION CYCLE"
            demand_desc = "Standard corporate accounts and stable baseline regional corporate segments anchor inventory."
            base_floor = currency_base_floor

        # --- AI Agent Logic Modulated by Real-World Pacing Capture Lines ---
        # If your room nights capture is running hot ahead of expectations, the AI turns highly aggressive
        if rn_capture_pct > 75:
            pace_status = "ACCELERATED PACING"
            ai_behavior_label = "Aggressive Yield Optimization (Pace exceeding target vector)"
            ai_markup = 1.30  # High velocity gives AI confidence to hike prices 30%
            floor_adjusted = base_floor * 1.15
        elif rn_capture_pct >= 40:
            pace_status = "NORMAL PACING RANGE"
            ai_behavior_label = "Standard Market Positioning (Steady pacing volume)"
            ai_markup = 1.15  # Normal markup
            floor_adjusted = base_floor
        else:
            pace_status = "LAGGING PACE TARGETS"
            ai_behavior_label = "Defensive Occupancy Stimulation (Slow pick-up detected)"
            ai_markup = 0.95  # Drop rate slightly below your baseline to stimulate room booking conversions
            floor_adjusted = base_floor * 0.85  # Lower protection floor to permit baseline filling

        proposed_ai_rate = forecast_adr * ai_markup
        tracking_label = "MTD Actuals" if is_current_month else "OTB Bookings"
        
        with st.container():
            st.markdown(f"### 📅 Horizon Month: **{m_name}**")
            
            col_info, col_guardrail = st.columns([3, 2])
            
            with col_info:
                st.markdown(f"**📈 Dynamic Market Demand Status:** `{demand_profile}`")
                st.write(f"*{demand_desc}*")
                st.markdown(f"**📊 Internal Pacing Health:** `{pace_status}`")
                
                # Render clean structural performance cards inside the text framework
                st.write(f"* **Your Expected Forecast ADR:** {currency_symbol}{forecast_adr:.2f}")
                st.write(f"* **Current {tracking_label} Capture:** {pace_rn} / {fore_rn} Room Nights ({rn_capture_pct:.1f}% Volume Filled)")
                st.write(f"* **Current Revenue Capture Index:** {currency_symbol}{pace_rev:,.2f} / {currency_symbol}{fore_rev:,.2f} ({rev_capture_pct:.1f}% Revenue Secured)")
                st.write(f"* **AI Agent Action Vector:** `{ai_behavior_label}` targeting a rate update adjustment of **{int((ai_markup-1)*100)}%**")
                st.write(f"* **Active Safety Parameter (Circuit Breaker Floor):** {currency_symbol}{floor_adjusted:.2f}")

            with col_guardrail:
                st.write("#### 🛡️ Live Gateway Validation Payload")
                st.write(f"AI Agent Proposed Update: **{currency_symbol}{proposed_ai_rate:.2f}**")
                
                if proposed_ai_rate < floor_adjusted:
                    st.error(f"🚨 **BREACH REJECTED!** The autonomous rate proposal of {currency_symbol}{proposed_ai_rate:.2f} violates your operational safety parameters floor line of {currency_symbol}{floor_adjusted:.2f}. API clearance denied. System rolled back to safe baseline positions to preserve yields.")
                else:
                    st.success(f"✅ **PAYLOAD AUTHORIZED.** The rate adjustment proposal of {currency_symbol}{proposed_ai_rate:.2f} passes all mathematical validation loops. Secure token granted for direct channel synchronization (OPERA Cloud / SynXis).")
            
            st.markdown("<br>", unsafe_allow_html=True)
else:
    if edited_pace_df["Room Nights"].sum() == 0:
        st.info("💡 Complete Step 2 above by entering your property's pacing and full month forecast metrics to let the AI logic trigger the individual month-by-month analysis.")
