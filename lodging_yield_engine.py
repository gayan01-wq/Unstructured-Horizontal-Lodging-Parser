import streamlit as st
import pandas as pd
from datetime import datetime

# Set up page configurations
st.set_page_config(page_title="Autonomous Revenue Intelligence Lab", layout="wide")

st.title("🏨 Autonomous Revenue Guardrail Lab")
st.markdown("""
### Global Multi-Currency Enterprise Performance & Safety Matrix
*An open-source blueprint for verifying autonomous AI pricing decisions against deterministic operational guardrails.*
""")

st.markdown("---")

# --- 1. Dynamic Market & Global Currency Setup ---
st.subheader("📍 Step 1: Define Property Location & Currency Protocol")
col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    city = st.text_input("Destination City / Market Location", value="Salalah")
with col_m2:
    country = st.text_input("Destination Country", value="Oman")
with col_m3:
    # Comprehensive Multi-Region Currency Selector
    currency_options = {
        "USD ($) - United States Dollar": {"symbol": "$", "floor": 135.00, "factor": 1.0},
        "OMR (𐎱.regular) - Omani Rial": {"symbol": "OMR ", "floor": 52.00, "factor": 0.38},
        "AED (د.إ) - UAE Dirham": {"symbol": "AED ", "floor": 500.00, "factor": 3.67},
        "SAR (ر.س) - Saudi Riyal": {"symbol": "SAR ", "floor": 500.00, "factor": 3.75},
        "EUR (€) - Euro (Europe)": {"symbol": "€", "floor": 125.00, "factor": 0.92},
        "GBP (£) - British Pound": {"symbol": "£", "floor": 105.00, "factor": 0.79},
        "THB (฿) - Thai Baht (Asia)": {"symbol": "฿", "floor": 4500.00, "factor": 36.50},
        "SGD ($) - Singapore Dollar": {"symbol": "SGD $", "floor": 180.00, "factor": 1.35},
        "INR (₹) - Indian Rupee": {"symbol": "₹", "floor": 11000.00, "factor": 83.30},
        "JPY (¥) - Japanese Yen": {"symbol": "¥", "floor": 20000.00, "factor": 155.00}
    }
    selected_currency_key = st.selectbox("Select Operational Currency Tier", options=list(currency_options.keys()))
    
    # Extract dynamic symbols and currency conversion scales
    currency_symbol = currency_options[selected_currency_key]["symbol"]
    currency_scale = currency_options[selected_currency_key]["factor"]
    currency_base_floor = currency_options[selected_currency_key]["floor"]

col_prop1, col_prop2 = st.columns(2)
with col_prop1:
    user_hotel = st.text_input("Your Property Name (Subject Hotel)", value="My Resort & Spa")
with col_prop2:
    compset_input = st.text_input("Enter Competitor Hotel Names (Separate with commas)", 
                                  value="Grand Plaza Resort, Ocean View Boutique, Metropolitan Hub")

# Process raw text strings into arrays
compset_list = [name.strip() for name in compset_input.split(",") if name.strip()]
all_hotels = [user_hotel] + compset_list

# --- 2. Dynamic Forward 3-Month Date Tracker ---
current_month_name = datetime.now().strftime("%B")
months_list = [current_month_name]
current_month_num = datetime.now().month

for i in range(1, 3):
    future_month = datetime(2026, (current_month_num + i - 1) % 12 + 1, 1)
    months_list.append(future_month.strftime("%B"))

# Define header string components dynamically using selected currency identifiers
col_m1_rn, col_m1_rev = f"{months_list[0]} Room Nights", f"{months_list[0]} Revenue ({currency_symbol})"
col_m2_rn, col_m2_rev = f"{months_list[1]} Room Nights", f"{months_list[1]} Revenue ({currency_symbol})"
col_m3_rn, col_m3_rev = f"{months_list[2]} Room Nights", f"{months_list[2]} Revenue ({currency_symbol})"

st.markdown("---")

# --- 3. Dynamic Data Isolation Session States ---
default_grid_data = {
    "Hotel Name": all_hotels,
    col_m1_rn: [1200 if idx == 0 else 1100 + (idx * 50) for idx in range(len(all_hotels))],
    col_m1_rev: [180000.0 * currency_scale if idx == 0 else (150000.0 + (idx * 20000)) * currency_scale for idx in range(len(all_hotels))],
    col_m2_rn: [1450 if idx == 0 else 1300 + (idx * 40) for idx in range(len(all_hotels))],
    col_m2_rev: [246500.0 * currency_scale if idx == 0 else (210000.0 + (idx * 25000)) * currency_scale for idx in range(len(all_hotels))],
    col_m3_rn: [1500 if idx == 0 else 1400 + (idx * 60) for idx in range(len(all_hotels))],
    col_m3_rev: [270000.0 * currency_scale if idx == 0 else (240000.0 + (idx * 30000)) * currency_scale for idx in range(len(all_hotels))]
}

# Clear out session state if currency or hotel configuration fields change
if ("prev_currency" not in st.session_state or st.session_state.prev_currency != selected_currency_key or
    "user_hotel_prev" not in st.session_state or st.session_state.user_hotel_prev != user_hotel or
    "compset_prev" not in st.session_state or st.session_state.compset_prev != compset_input):
    st.session_state.market_df = pd.DataFrame(default_grid_data)
    st.session_state.prev_currency = selected_currency_key
    st.session_state.user_hotel_prev = user_hotel
    st.session_state.compset_prev = compset_input

st.subheader("📊 Step 2: Input Forward 3-Month Comp Set Performance Data")
st.write(f"Adjust values below to evaluate metric profiles inside the **{currency_symbol}** fiscal layer:")

def clear_all_metrics():
    blank_data = {
        "Hotel Name": all_hotels,
        col_m1_rn: [0] * len(all_hotels), col_m1_rev: [0.0] * len(all_hotels),
        col_m2_rn: [0] * len(all_hotels), col_m2_rev: [0.0] * len(all_hotels),
        col_m3_rn: [0] * len(all_hotels), col_m3_rev: [0.0] * len(all_hotels)
    }
    st.session_state.market_df = pd.DataFrame(blank_data)

if st.button("🗑️ Clear Table Data (Reset Sheet Values)"):
    clear_all_metrics()
    st.rerun()

edited_df = st.data_editor(st.session_state.market_df, num_rows="fixed", use_container_width=True, key="market_grid_currency_editor")
st.session_state.market_df = edited_df

st.markdown("---")

# --- 4. Live Globalized Revenue Calculations ---
st.subheader("📈 Step 3: Recalculated Market Share & Generation Metrics")

total_rn_3mo = edited_df[[col_m1_rn, col_m2_rn, col_m3_rn]].sum().sum()
total_rev_3mo = edited_df[[col_m1_rev, col_m2_rev, col_m3_rev]].sum().sum()

if total_rn_3mo > 0 and total_rev_3mo > 0:
    edited_df["Total Room Nights"] = edited_df[[col_m1_rn, col_m2_rn, col_m3_rn]].sum(axis=1)
    edited_df[f"Total Revenue ({currency_symbol})"] = edited_df[[col_m1_rev, col_m2_rev, col_m3_rev]].sum(axis=1)
    
    edited_df[f"3-Mo ADR ({currency_symbol})"] = edited_df[f"Total Revenue ({currency_symbol})"] / edited_df["Total Room Nights"]
    edited_df[f"3-Mo ADR ({currency_symbol})"] = edited_df[f"3-Mo ADR ({currency_symbol})"].fillna(0.0)
    
    market_avg_adr = total_rev_3mo / total_rn_3mo
    subject_adr = edited_df.iloc[0][f"3-Mo ADR ({currency_symbol})"]
    
    edited_df["Room Night Share (%)"] = (edited_df["Total Room Nights"] / total_rn_3mo) * 100
    edited_df["Revenue Share (%)"] = (edited_df[f"Total Revenue ({currency_symbol})"] / total_rev_3mo) * 100
    
    st.dataframe(
        edited_df[["Hotel Name", "Total Room Nights", f"Total Revenue ({currency_symbol})", f"3-Mo ADR ({currency_symbol})", "Room Night Share (%)", "Revenue Share (%)"]],
        use_container_width=True
    )
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric(label=f"Market Compiled ADR ({currency_symbol})", value=f"{currency_symbol}{market_avg_adr:.2f}")
    with c2:
        st.metric(label=f"Your Compiled ADR ({currency_symbol})", value=f"{currency_symbol}{subject_adr:.2f}")
    with c3:
        st.metric(label="Your Accumulated Revenue Share", value=f"{edited_df.iloc[0]['Revenue Share (%)']:.1f}%")

    # --- 5. Advanced Context-Aware Market Intelligence Engine ---
    st.markdown("---")
    st.subheader("🤖 Step 4: Autonomous Pricing & Agentic Guardrail Execution")
    
    is_salalah = city.lower().strip() == "salalah"
    is_summer_khareef = any(m in ["June", "July", "August", "September"] for m in months_list)
    
    st.markdown("#### 🎯 Market Condition & Macro Demand Diagnostics")
    if is_salalah and is_summer_khareef:
        st.info(f"""
        **📍 Location Context:** {city}, {country} (Dhofar Monsoon Season window detected).  
        **📈 Market Demand Dynamics:** High micro-climate seasonality variance. The localized Indian Ocean Monsoon (*Khareef*) shifts temperatures down to 20-27°C, driving extreme regional tourism inflows while the rest of the GCC experiences temperatures above 43°C.  
        **🛠️ Tactical Rate Adjustments:** Inventory remains highly constrained. Maintain aggressive yield positions, minimize deep group discounting channels, and ensure dynamic rate protection.
        """)
        deterministic_floor = currency_base_floor * 1.15
        ai_aggression_factor = 1.25
    else:
        st.info(f"""
        **📍 Location Context:** {city}, {country} ({months_list[0]}-{months_list[2]} window).  
        **📈 Market Demand Dynamics:** Steady-state destination cycle. Occupancy distributed across standard corporate accounts and local leisure segments.  
        **🛠️ Tactical Rate Adjustments:** Focus optimization protocols on shoulder-day displacement strategies. Ensure public rack rate tracking aligns cleanly with core competitive index medians.
        """)
        deterministic_floor = currency_base_floor
        ai_aggression_factor = 1.10

    # Calculate dynamic pricing simulation parameters
    proposed_rate = market_avg_adr * ai_aggression_factor
    
    st.markdown("#### 🛡️ Circuit Breaker Gateway Validation")
    st.write(f"An autonomous AI distribution agent attempts to optimize your properties pricing architecture. Proposed rate push: **{currency_symbol}{proposed_rate:.2f}**")
    
    if proposed_rate < deterministic_floor:
        st.error(f"🚨 **Circuit Breaker Status: BREACH REJECTED!** The AI agent's proposed optimization rate of {currency_symbol}{proposed_rate:.2f} violates your localized operational safety floor limits of {currency_symbol}{deterministic_floor:.2f}. Automated execution payload revoked. System rolled back to safe baseline positions.")
    else:
        st.success(f"✅ **Circuit Breaker Status: AUTHORIZED.** The proposed optimization rate of {currency_symbol}{proposed_rate:.2f} passes all deterministic security validations. Execution token cleared for direct distribution stream API synchronization (SynXis / OPERA Cloud).")

else:
    st.info("💡 Please ensure your hotel profile properties, room nights, and revenue values contain data to trigger the live market analytics loop.")
