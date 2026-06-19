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
