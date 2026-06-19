import streamlit as st
import pandas as pd
from datetime import datetime
import calendar

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
st.subheader("📍 Step 1: Define Property Profile & Capacity Inventory")

# Reset Function for Step 1
def clear_step_1_profile():
    st.session_state["city_input"] = ""
    st.session_state["country_input"] = ""
    st.session_state["subject_hotel_input"] = ""
    st.session_state["total_rooms_input"] = 150
    default_compset_rows = {
        "Compset Index": [f"0{i}. Compset Name" for i in range(1, 9)],
        "Hotel Identity Name": ["", "", "", "", "", "", "", ""],
        "Public Rate (Lighthouse/OTA)": [0.0] * 8
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
        "Hotel Identity Name": ["Grand Plaza Resort", "Ocean View Boutique", "Metropolitan Hub", "", "", "", "", ""],
        "Public Rate (Lighthouse/OTA)": [65.0, 72.0, 58.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    }
    st.session_state.compset_grid_df = pd.DataFrame(default_compset_rows)

col_prop1, col_prop2 = st.columns([1, 1.2])
with col_prop1:
    user_hotel = st.text_input("Your Property Name (Subject Hotel)", value="My Resort & Spa", key="subject_hotel_input")
    # Added capacity anchor
    total_rooms = st.number_input("Total Physical Room Inventory Capacity", min_value=1, value=150, step=1, key="total_rooms_input")

with col_prop2:
    st.write("📋 **Map Competitive Set Names & Current Market Pricing:**")
    edited_compset_grid = st.data_editor(
        st.session_state.compset_grid_df,
        num_rows="fixed",
        use_container_width=True,
        key="compset_grid_editor"
    )
    st.session_state.compset_grid_df = edited_compset_grid
    
    active_compset = []
    compset_rates = []
    for _, row in edited_compset_grid.iterrows():
        val = row["Hotel Identity Name"]
        rate = row["Public Rate (Lighthouse/OTA)"]
        if val is not None:
            val_str = str(val).strip()
            if val_str != "" and val_str.lower() != "none":
                active_compset.append(val_str)
                try:
                    rate_val = float(rate)
                    if rate_val > 0:
                        compset_rates.append(rate_val)
                except (ValueError, TypeError):
                    pass
                    
    compset_count = len(active_compset)
    average_compset_rate = sum(compset_rates) / len(compset_rates) if len(compset_rates) > 0 else 0.0

compset_verification = f"✅ {compset_count} Competitor(s) Mapped" if compset_count > 0 else "📝 Awaiting Compset Entry"
location_verification = "✅ Location Saved" if city.strip() and country.strip() else "📝 Awaiting Location"
hotel_verification = f"✅ Saved ({total_rooms} Rooms)" if user_hotel.strip() else "📝 Awaiting Hotel Name"

st.markdown(f"**Profile Status Tracking Verification Panel:** &nbsp;&nbsp;&nbsp;&nbsp; {location_verification} &nbsp;&nbsp;|&nbsp;&nbsp; {hotel_verification} &nbsp;&nbsp;|&nbsp;&nbsp; {compset_verification}")

# --- 2. Dynamic Forward 3-Month Matrix Calendar Calculations ---
current_datetime = datetime.now()
months_data = [] # List of dicts storing month names, numbers, years, and days in month
current_month_num = current_datetime.month
current_year = current_datetime.year

for i in range(3):
    m_num = ((current_month_num + i - 1) % 12) + 1
    # Adjust year if it wraps past December
    m_year = current_year + 1 if (current_month_num + i > 12) else current_year
    m_name = datetime(m_year, m_num, 1).strftime("%B")
    days_in_m = calendar.monthrange(m_year, m_num)[1]
    months_data.append({"name": m_name, "num": m_num, "year": m_year, "days": days_in_m})

months_list = [m["name"] for m in months_data]

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
    m_info = months_data[i]
    m_name = m_info["name"]
    days_in_month = m_info["days"]
    is_current_month = (i == 0)
    
    pace_row = edited_pace_df.iloc[i * 2]
    fore_row = edited_pace_df.iloc[(i * 2) + 1]
    
    pace_rn, pace_rev = pace_row["Room Nights"], pace_row["Revenue"]
    fore_rn, fore_rev = fore_row["Room Nights"], fore_row["Revenue"]
    
    if fore_rn > 0 and fore_rev > 0:
        has_valid_data_rendered = True
        
        # Calculate dynamic KPIs
        forecast_adr = fore_rev / fore_rn
        rn_capture_pct = (pace_rn / fore_rn) * 100
        rev_capture_pct = (pace_rev / fore_rev) * 100 if fore_rev > 0 else 0.0
        
        # CALCULATE TRUE PROJECTED FULL MONTH OCCUPANCY RATE
        total_available_capacity = total_rooms * days_in_month
        projected_occ_pct = (fore_rn / total_available_capacity) * 100
        pace_occ_pct = (pace_rn / total_available_capacity) * 100
        
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
        
        if average_compset_rate > 0:
            ari_index = (proposed_ai_rate / average_compset_rate) * 100
            ari_string = f"{ari_index:.1f}% (Value Positioning to capture share)" if ari_index < 100 else f"{ari_index:.1f}% (Premium Market Leader Positioning)"
        else:
            ari_string = "N/A (No Competitor Pricing Entered)"

        with st.container():
            st.markdown(f"### 📅 Horizon Period: **{m_name}**")
            col_info, col_guardrail = st.columns([3, 2])
            
            with col_info:
                st.markdown(f"**📈 Market Demand Status:** `{demand_profile}`")
                st.write(f"*{demand_desc}*")
                st.markdown(f"**📊 Pacing Health & Velocity:** `{pace_status}`")
                st.caption("💡 *Note: Rate recommendations are derived dynamically by cross-referencing your internal booking velocity matrix variables against full-month expected forecast baseline targets, modulated by external micro-climate demand constraints.*")
                
                # Dynamic Capacity and Pricing Metrics Display Row
                st.write(f"* **Target Forecast ADR Baseline (Calculated):** {currency_symbol}{forecast_adr:.2f}")
                st.write(f"* **Projected Capacity Occupancy:** `{projected_occ_pct:.1f}% Full Month Occupancy` (Active Pacing: {pace_occ_pct:.1f}%)")
                st.write(f"* **Inventory Materialization ({tracking_label}):** {pace_rn} / {fore_rn} Room Nights ({rn_capture_pct:.1f}% Inventory Committed)")
                st.write(f"* **Revenue Volume Secured:** {currency_symbol}{pace_rev:,.2f} / {currency_symbol}{fore_rev:,.2f} ({rev_capture_pct:.1f}% Revenue Materialized)")
                st.write(f"* **Competitive Landscape Index (ARI):** Proposed strategy positions property at an ARI Index of `{ari_string}` against mapped compset benchmarks.")
                st.write(f"* **Agent Yield Optimization Vector:** `{ai_behavior_label}` targeting an adjustment markup of **{int((ai_markup-1)*100)}%**")
                st.write(f"* **Active Safety Parameter (Circuit Breaker Floor):** {currency_symbol}{floor_adjusted:.2f}")

            with col_guardrail:
                st.write("#### 🛡️ Automated Yield Gatekeeper")
                st.write(f"AI Agent Proposed Public Rack Rate: **{currency_symbol}{proposed_ai_rate:.2f}**")
                
                if proposed_ai_rate < floor_adjusted:
                    st.error(f"🚨 **RATE DEVIATION REJECTED!** The autonomous rate proposal of {currency_symbol}{proposed_ai_rate:.2f} violates your operational safety parameters floor line of {currency_symbol}{floor_adjusted:.2f}. Strategy authorization denied to prevent severe channel dilution. Distribution channels rolled back to secure baseline positions to safeguard yield.")
                else:
                    st.success(f"✅ **Rate is compatible with market conditions.** The dynamic strategy proposal of {currency_symbol}{proposed_ai_rate:.2f} satisfies all deterministic constraints. Automated ARI strategy authorized for real-time channel manager and PMS synchronization.")
            st.markdown("<br>", unsafe_allow_html=True)

if not has_valid_data_rendered:
    st.info("💡 Complete Step 2 above by entering your property's pacing and full month forecast metrics to let the AI logic trigger the individual month-by-month analysis.")
