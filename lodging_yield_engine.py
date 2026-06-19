import streamlit as st
import pandas as pd

# Set up page configurations
st.set_page_config(page_title="Autonomous Revenue Intelligence Lab", layout="wide")

st.title("🏨 Autonomous Revenue Guardrail Lab")
st.markdown("""
### Multi-User Hospitality Performance & Safety Matrix
*An open-source blueprint for verifying autonomous AI pricing decisions against deterministic operational guardrails.*
""")

# --- 1. Global Inputs (City & Country) ---
col_meta1, col_meta2 = st.columns(2)
with col_meta1:
    city = st.text_input("📍 Destination City / Market Location", value="Salalah")
with col_meta2:
    country = st.text_input("🌍 Destination Country", value="Oman")

st.markdown("---")

# --- 2. Session State Setup for Multi-User / Clear Data Stability ---
# We use standard dictionary templates to prevent multi-user session state conflicts on Streamlit Cloud
default_data = {
    "Hotel Name": ["My Property (Subject)", "Grand Plaza Resort", "Ocean View Boutique", "Metropolitan Hub"],
    "3-Month Room Nights": [1200, 1450, 980, 1100],
    "3-Month Revenue ($)": [180000.0, 246500.0, 176400.0, 143000.0]
}

if "market_data" not in st.session_state:
    st.session_state.market_data = pd.DataFrame(default_data)

# --- 3. Interactive Data Table ---
st.subheader("📊 Step 1: Input Comp Set Performance Data")
st.write(f"Adjust values below to calculate fair market shares for **{city}, {country}**:")

# Clear Data Action Function
def clear_table():
    blank_data = {
        "Hotel Name": ["My Property (Subject)", "", "", ""],
        "3-Month Room Nights": [0, 0, 0, 0],
        "3-Month Revenue ($)": [0.0, 0.0, 0.0, 0.0]
    }
    st.session_state.market_data = pd.DataFrame(blank_data)

# Clear Data Button UI Elements
if st.button("🗑️ Clear Table Data (Reset for your Hotel)"):
    clear_table()
    st.rerun()

# Render the interactive grid safely isolated inside session state
edited_df = st.data_editor(
    st.session_state.market_data, 
    num_rows="dynamic", 
    use_container_width=True,
    key="editor_grid"
)
# Update session storage silently as they modify cells
st.session_state.market_data = edited_df

st.markdown("---")

# --- 4. Live Commercial Intelligence Engine Math ---
st.subheader("📈 Step 2: Live Engine Outputs & Revenue Metrics")

# Prevent zero division errors if user clears out data entirely
total_nights = edited_df["3-Month Room Nights"].sum()
total_rev = edited_df["3-Month Revenue ($)"].sum()

if total_nights > 0 and total_rev > 0:
    # Basic ADR calculations
    edited_df["Calculated ADR ($)"] = edited_df["3-Month Revenue ($)"] / edited_df["3-Month Room Nights"]
    edited_df["Calculated ADR ($)"] = edited_df["Calculated ADR ($)"].fillna(0.0)
    
    market_avg_adr = total_rev / total_nights
    subject_hotel = edited_df.iloc[0]
    subject_adr = subject_hotel["Calculated ADR ($)"] if subject_hotel["3-Month Room Nights"] > 0 else 0.0
    
    # Calculate Market Share Percentages
    edited_df["Room Night Share (%)"] = (edited_df["3-Month Room Nights"] / total_nights) * 100
    edited_df["Revenue Share (%)"] = (edited_df["3-Month Revenue ($)"] / total_rev) * 100

    # Display the processed summary framework to the user
    st.dataframe(
        edited_df[["Hotel Name", "Calculated ADR ($)", "Room Night Share (%)", "Revenue Share (%)"]], 
        use_container_width=True
    )

    # Core high-level cards
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric(label="Market Average ADR", value=f"${market_avg_adr:.2f}")
    with c2:
        st.metric(label="Your Property ADR", value=f"${subject_adr:.2f}")
    with c3:
        st.metric(label="Your Market Revenue Share", value=f"{edited_df.iloc[0]['Revenue Share (%)']:.1f}%")

    # --- 5. The Agentic Safety Loop (The Value Proposition) ---
    st.markdown("---")
    st.subheader("🤖 Step 3: Autonomous Pricing & Agentic Guardrail Execution")
    
    # Simulate an AI agent attempting to optimize next month's rate aggressively
    proposed_agent_rate = market_avg_adr * 1.15 
    
    # Define a strict, hardcoded revenue safety floor boundary line
    DETERMINISTIC_SAFETY_FLOOR = 135.00
    
    st.write(f"**Scenario Simulator:** An autonomous pricing agent reads your market matrix for **{city}** and proposes an automated rack rate adjustment to **${proposed_agent_rate:.2f}**.")
    
    if proposed_agent_rate < DETERMINISTIC_SAFETY_FLOOR:
        st.error(f"🚨 **Circuit Breaker Status: BREACH BLOCKED!** The AI agent's optimization rate of ${proposed_agent_rate:.2f} falls below your system's absolute floor parameter of ${DETERMINISTIC_SAFETY_FLOOR:.2f}. Execution tokens revoked. System rolled back to safe baseline.")
    else:
        st.success(f"✅ **Circuit Breaker Status: SECURE / APPROVED.** Proposed rate of ${proposed_agent_rate:.2f} passes all mathematical safety loops. Authorized to stream directly to distribution APIs (SynXis/OPERA Cloud).")

else:
    st.info("💡 Please enter hotel names, room nights, and revenue values into the table above to compute live revenue management metrics.")
