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
    # Expanded Comprehensive Multi-Region Currency Selector (Asian, Middle East, Europe, Americas)
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
col_prop1, col_prop2 = st.columns([1, 1])

with col_prop1:
    user_hotel = st.text_input("Your Property Name (Subject Hotel)", value="My Resort & Spa")

with col_prop2:
    st.write("📋 **Map Competitive Set Names (Up to 8 Properties):**")
    default_compset_rows = {
        "Compset Index": [f"0{i}. Compset Name" for i in range(1, 9)],
        "Hotel Identity Name": ["Grand Plaza Resort", "Ocean View Boutique", "Metropolitan Hub", "", "", "", "", ""]
    }
    
    if "compset_grid_df" not in st.session_state:
        st.session_state.compset_grid_df = pd.DataFrame(default_compset_rows)
        
    edited_compset_grid = st.data_editor(
        st.session_state.compset_grid_df,
        num_rows="fixed",
        use_container_width=True,
        key="compset_grid_editor"
    )
    st.session_state.compset_grid_df = edited_compset_grid
    active_compset = [row["Hotel Identity Name"].strip() for _, row in edited_compset_grid.iterrows() if row["Hotel Identity Name"].strip()]
    compset_count = len(active_compset)

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

if "pacing_metrics_df" not in st.session_state or st.session_state.get("prev_currency_state") != selected_currency_key:
    st.session_state.pacing_metrics_df = pd.DataFrame(default_pacing_data)
    st.session_state.prev_currency_state = selected_currency_key

# --- DYNAMIC NOTED MARK STATUS CHECKER ---
# Inspect values inside the spreadsheet to instantly calculate user data entry completion flags
status_icons = []
for i in range(3):
    p_rn = st.session_state.pacing_metrics_df.iloc[i * 2]["Room Nights"]
    f_rn = st.session_state.pacing_metrics_df.iloc[(i * 2) + 1]["Room Nights"]
    if p_rn > 0 and f_rn > 0:
        status_icons.append(f"**{months_list[i]}:** ✅ Entered & Logged")
    else:
        status_icons.append(f"**{months_list[i]}:** 📝 Awaiting Entry")

# Display a beautiful entry confirmation status bar right above the interactive table
st.markdown(f"**Data Status Tracking Verification Panel:** &nbsp;&nbsp;&nbsp;&nbsp; {status_icons[0]} &nbsp;&nbsp;|&nbsp;&nbsp; {status_icons[1]} &nbsp;&nbsp;|&nbsp;&nbsp; {status_icons[2]}")

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
st.subheader("📈 Step 3: Month-by-Month RM Analysis & Agentic Safety Loop")

is_salalah = city.lower().strip() == "salalah"

for i in range(3):
    m_name = months_list[i]
    is_current_month = (i == 0)
    
    pace_row = edited_pace_df.iloc[i * 2]
    fore_row = edited_pace_df.iloc[(i * 2) + 1]
    
    pace_rn, pace_rev = pace_row["Room Nights"], pace_row["Revenue"]
    fore_rn, fore_rev = fore_row["Room Nights"], fore_row["Revenue"]
    
    if fore_rn > 0 and fore_rev > 0:
        forecast_adr = fore_rev / fore_rn
        rn_capture_pct = (pace_rn / fore_rn) * 100
        rev_capture_pct = (pace_rev / fore_rev) * 100 if fore_rev > 0 else 0.0
        
        is_high_season_month = m_name in ["June", "July", "August", "September"]
        
        if is_salalah and is_high_season_month:
            demand_profile = "🚨 CRITICAL MARKET COMPRESSION (Khareef Monsoon Horizon)"
            demand_desc = "Extreme seasonal compression driven by structural micro-climate variations. High unconstrained market demand eliminates the risk of inventory spoilage, establishing significant premium pricing power across the sector."
            base_floor = currency_base_floor * 1.35
        elif is_high_season_month:
            demand_profile = "📈 POSITIVE SEASONAL DEMAND VARIANCE"
            demand_desc = "Transient holiday volume driving steady compression cycles. Market pace registers normal elasticity vectors; standard structural distribution tuning recommended."
            base_floor = currency_base_floor * 1.10
        else:
            demand_profile = "⚖️ STEADY-STATE MARKET EQUILIBRIUM"
            demand_desc = "Baseline commercial operations active. High dependence on base corporate accounts and contracted volume. Core strategy should focus on length-of-stay (LOS) controls to mitigate low-rate displacement."
            base_floor = currency_base_floor

        if rn_capture_pct > 75:
            pace_status = "🔥 ACCELERATED BOOKING PACE (POS VELOCITY BREACH)"
            ai_behavior_label = "Aggressive Yield Premiumization (Maximizing ADR Index at the cost of nominal occupancy)"
            ai_markup = 1.30  
            floor_adjusted = base_floor * 1.15
        elif rn_capture_pct >= 40:
            pace_status = "✅ STABLE BOOKING PACE CURVE"
            ai_behavior_label = "Optimal Fair-Share Positioning (Balancing RevPAR Index and RGI projections)"
            ai_markup = 1.15  
            floor_adjusted = base_floor
        else:
            pace_status = "⚠️ LAGGING BOOKING VELOCITY (CAPTURE DEFICIT)"
            ai_behavior_label = "Tactical Occupancy Stimulation (Preventing inventory spoilage and dilution via baseline distribution changes)"
            ai_markup = 0.95  
            floor_adjusted = base_floor * 0.85  

        proposed_ai_rate = forecast_adr * ai_markup
        tracking_label = "MTD" if is_current_month else "OTB"
        
        with st.container():
            st.markdown(f"### 📅 Horizon Period: **{m_name}**")
            
            col_info, col_guardrail = st.columns([3, 2])
            
            with col_info:
                st.markdown(f"**📈 Market Demand Status:** `{demand_profile}`")
                st.write(f"*{demand_desc}*")
                st.markdown(f"**📊 Pacing Health & Velocity:** `{pace_status}`")
                
                st.write(f"* **Target Forecast ADR Baseline:** {currency_symbol}{forecast_adr:.2f}")
                st.write(f"* **Inventory Materialization ({tracking_label}):** {pace_rn} / {fore_rn} Room Nights ({rn_capture_pct:.1f}% Inventory Committed)")
                st.write(f"* **Revenue Volume Secured:** {currency_symbol}{pace_rev:,.2f} / {currency_symbol}{fore_rev:,.2f} ({rev_capture_pct:.1f}% Revenue Materialized)")
                st.write(f"* **Mapped Competitive Landscape:** Cross-referencing pricing vectors against `{compset_count}` active competitor profiles mapped in Step 1.")
                st.write(f"* **Agent Yield Optimization Vector:** `{ai_behavior_label}` targeting an adjustment markup of **{int((ai_markup-1)*100)}%**")
                st.write(f"* **Active Safety Parameter (Circuit Breaker Floor):** {currency_symbol}{floor_adjusted:.2f}")

            with col_guardrail:
                st.write("#### 🛡️ Autonomous Distribution Gateway")
                st.write(f"AI Agent Proposed Public Rate: **{currency_symbol}{proposed_ai_rate:.2f}**")
                
                if proposed_ai_rate < floor_adjusted:
                    st.error(f"🚨 **GATEWAY BREACH BLOCKED!** The autonomous rate adjustment proposal of {currency_symbol}{proposed_ai_rate:.2f} violates your system's deterministic safety floor of {currency_symbol}{floor_adjusted:.2f}. API execution token revoked to avoid rate dilution. Channel rate rolled back to secure baseline thresholds.")
                else:
                    st.success(f"✅ **EXECUTION PAYLOAD CLEARED.** The rate adjustment proposal of {currency_symbol}{proposed_ai_rate:.2f} satisfies all algorithmic validation conditions. Secure ARI instruction package dispatched for live PMS/CRS channel synchronization.")
            
            st.markdown("<br>", unsafe_allow_html=True)
else:
    if edited_pace_df["Room Nights"].sum() == 0:
        st.info("💡 Complete Step 2 above by entering your property's pacing and full month forecast metrics to let the AI logic trigger the individual month-by-month analysis.")
