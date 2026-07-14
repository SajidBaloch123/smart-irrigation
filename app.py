"""
Smart Irrigation Control Console
Systems Engineering Framework

This module implements a core software gateway for an intelligent, rule-based
Decision Support System (DSS). It features a mathematical computation engine 
for water volume requirements alongside an LLM cognitive reasoning tracker.
"""

import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# =====================================================================
# PAGE CONFIGURATION & SCADA UI STYLING
# =====================================================================
st.set_page_config(
    page_title="Smart Irrigation System",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Dark Mode SCADA UI Styling
st.markdown("""
    <style>
    .stApp {
        background-color: #0A0F1D;
        color: #E2E8F0;
    }
    .block-container { padding-top: 1.5rem; }
    
    /* System Control Header Panel */
    .scada-header {
        background: linear-gradient(135deg, rgba(16, 24, 48, 0.95) 0%, rgba(24, 43, 73, 0.95) 100%);
        border-radius: 12px;
        padding: 20px;
        border: 1px solid rgba(0, 242, 254, 0.3);
        text-align: center;
        margin-bottom: 25px;
    }
    .header-main-title {
        color: #00F2FE;
        font-size: 2.4rem;
        font-weight: 900;
        letter-spacing: 1px;
    }
    .system-status-sub {
        color: #05B292;
        font-size: 0.95rem;
        font-weight: 700;
        margin-top: 5px;
    }

    /* KPI Metric Displays */
    div[data-testid="stMetric"] {
        background: rgba(20, 30, 55, 0.65);
        border: 1px solid rgba(0, 242, 254, 0.2);
        border-radius: 10px;
        padding: 12px;
    }
    
    /* Interactive Process Controls Button */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #05B292 0%, #00F2FE 100%);
        color: #0A0F1D;
        border: none;
        border-radius: 25px;
        padding: 12px 24px;
        width: 100%;
        font-weight: 900;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 242, 254, 0.5);
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# CORE CONFIGURATION SCHEMAS
# =====================================================================
CROP_METRICS = {
    "Crop_Type_A": {"depth_mm": 50, "moisture_range": [45, 70]},
    "Crop_Type_B": {"depth_mm": 100, "moisture_range": [70, 95]},
    "Crop_Type_C": {"depth_mm": 65, "moisture_range": [50, 75]}
}

# =====================================================================
# MATHEMATICAL DETERMINISTIC RULES ENGINE
# =====================================================================
def calculate_hydraulic_dosage(crop_type, current_moisture, temperature):
    """
    Computes volumetric water distribution requirements based on current deficit profiles.
    """
    config = CROP_METRICS.get(crop_type, CROP_METRICS["Crop_Type_A"])
    target = config["moisture_range"]
    depth = config["depth_mm"]
    
    if current_moisture < target[0]:
        status_log = "CRITICAL HYDRAULIC DEFICIT: Automated valve loop open triggered."
        moisture_deficit_pct = target[1] - current_moisture
        # Volumetric Math Model: Deficit Ratio * Plant Root Zone Depth
        water_volume_liters_m2 = (moisture_deficit_pct / 100.0) * depth
    elif current_moisture > target[1]:
        status_log = "CRITICAL SATURATION WARNING: Solenoid override locked out."
        moisture_deficit_pct = 0
        water_required_liters_m2 = 0
        water_volume_liters_m2 = 0
    else:
        status_log = "EQUILIBRIUM MAINTAINED: System operating in baseline criteria."
        moisture_deficit_pct = 0
        water_volume_liters_m2 = 0
        
    # Microclimate Environmental Factor Scaling
    if temperature > 35 and water_volume_liters_m2 > 0:
        water_volume_liters_m2 *= 1.15
        
    return status_log, round(moisture_deficit_pct, 1), round(water_volume_liters_m2, 2)

# =====================================================================
# INTERFACE CONTROL ROOM
# =====================================================================
st.markdown("""
    <div class="scada-header">
        <div class="header-main-title">🚜 SMART IRRIGATION INTERFACE</div>
        <div class="system-status-sub">Distributed SCADA Environment Console — Telemetry Pipeline Active</div>
    </div>
""", unsafe_allow_html=True)

# Sidebar System Configuration Layout
st.sidebar.markdown("### 🔑 Gateway Authorization")
groq_api_key = st.sidebar.text_input("Groq API Cloud Key", type="password", placeholder="gsk_...")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔌 Actuator Diagnostics")
solenoid_relay = st.sidebar.checkbox("Manual Valve Bypass", value=False)
pump_relay = st.sidebar.checkbox("Manual Pump Bypass", value=False)

# Main Dashboard Processing Matrix Split
col_controls, col_diagnostics = st.columns([4, 6], gap="large")

with col_controls:
    st.markdown("### 📡 Live Sensor Telemetry Array")
    selected_crop = st.selectbox("Target Cultivation Profile", list(CROP_METRICS.keys()))
    live_moisture = st.slider("Soil Volumetric Moisture Content (%)", 10, 100, 35)
    live_temp = st.slider("Ambient Environmental Temperature (°C)", 10, 50, 38)
    live_humidity = st.slider("Relative Atmospheric Humidity (%)", 10, 100, 45)
    weather_forecast = st.radio("Predictive Forecast Vectors", ["Clear / Optimal", "Overcast Sky", "Imminent Rainfall"])
    
    compute_matrix_btn = st.button("🚀 Process Telemetry & Initialize AI Analytics")

with col_diagnostics:
    st.markdown("### 📋 Automation Diagnostics Panel")
    
    if compute_matrix_btn:
        if not groq_api_key:
            st.warning("⚠️ Configuration Alert: Valid API verification key required for AI analytical tasks.")
        else:
            with st.spinner("Processing local rule metrics and spawning AI tracks..."):
                # Run rule calculations
                valve_log, deficit, total_volume = calculate_hydraulic_dosage(selected_crop, live_moisture, live_temp)
                
                # Render System Math Variables
                st.markdown("#### 📐 Engineering Mathematics Model")
                st.latex(r"V = \frac{\Delta M}{100} \times d")
                st.caption("Standard system formula tracking Volumetric Water Dosage ($V$), Moisture Deficit ($\Delta M$), and Depth ($d$).")
                
                # Print Analytical Metric Blocks
                metric_col1, metric_col2 = st.columns(2)
                with metric_col1:
                    st.metric(label="Calculated Moisture Deficit (ΔM)", value=f"{deficit}%")
                with metric_col2:
                    st.metric(label="Hydraulic Water Volume Output (V)", value=f"{total_volume} L/m²")
                    
                st.info(f"⚙️ **System Log:** {valve_log}")
                
                # Execute Cloud LLM Strategy Tracking Pipeline
                try:
                    llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama-3.1-8b-instant", temperature=0.1)
                    prompt = ChatPromptTemplate.from_template("""
                    You are an advanced AI Smart Irrigation Controller.
                    Analyze the following real-time field telemetry metrics to output an operational strategy.
                    - Crop Zone: {selected_crop}
                    - Moisture Content: {live_moisture}%
                    - Temp: {live_temp}°C
                    - Humidity: {live_humidity}%
                    - Forecast Outlook: {weather_forecast}
                    - Calculated Flow: {total_volume} L/m²
                    
                    Provide a concise, technical deployment strategy highlighting Hardware Diagnostics, Valve Timing Windows, and System Safety Overrides.
                    """)
                    
                    chain = prompt | llm
                    response = chain.invoke({
                        "selected_crop": selected_crop,
                        "live_moisture": live_moisture,
                        "live_temp": live_temp,
                        "live_humidity": live_humidity,
                        "weather_forecast": weather_forecast,
                        "total_volume": total_volume
                    })
                    st.markdown("### 📋 AI Cognitive Strategy Report")
                    st.write(response.content)
                except Exception as e:
                    st.error(f"❌ AI Computing Error encountered: {str(e)}")
    else:
        st.info("System Standby Track: Awaiting live sensor telemetry data vectors. Configure parameters on the left to activate.")
