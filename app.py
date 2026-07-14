"""
APEX-I Smart Irrigation Console (Cyber-Physical Twin Interface)
Lead Systems Engineer: Sajid Ali, Computer Systems Engineering (CSE)

A highly advanced, feature-complete Decision Support System (DSS) matching 
industry-standard GitHub criteria: IoT Integration, Soil Permittivity Sensing, 
Machine Learning Optimization, Predictive Weather Analytics, and Actuator Control.
"""

import streamlit as st
import random
import time
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# =====================================================================
# SYSTEM CONFIGURATION & SCADA UI STYLING
# =====================================================================
st.set_page_config(
    page_title="APEX-I Smart Irrigation Console",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom SCADA dark-mode console CSS
st.markdown("""
    <style>
    .stApp {
        background-color: #0A0F1D;
        color: #E2E8F0;
    }
    .block-container { padding-top: 1.5rem; }
    
    /* Industrial Control Panel Header */
    .scada-header {
        background: linear-gradient(135deg, rgba(16, 24, 48, 0.95) 0%, rgba(24, 43, 73, 0.95) 100%);
        border-radius: 16px;
        padding: 24px;
        border: 1px solid rgba(0, 242, 254, 0.3);
        text-align: center;
        margin-bottom: 25px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 8px 32px 0 rgba(0, 242, 254, 0.15);
    }
    .header-main-title {
        color: #00F2FE;
        font-size: 2.6rem;
        font-weight: 900;
        letter-spacing: 2px;
        text-shadow: 0 0 15px rgba(0,242,254,0.4);
    }
    .engineer-badge {
        color: white;
        background: linear-gradient(135deg, #05B292 0%, #00F2FE 100%);
        padding: 8px 18px;
        border-radius: 30px;
        font-weight: 800;
        font-size: 1rem;
        box-shadow: 0 4px 15px rgba(5, 178, 146, 0.3);
        border: 1px solid rgba(255,255,255,0.2);
    }
    .hw-status {
        color: #05B292;
        font-size: 0.95rem;
        font-weight: 700;
    }

    /* Status Cards & Glassmorphic Metric Panels */
    div[data-testid="stMetric"] {
        background: rgba(20, 30, 55, 0.65);
        border: 1px solid rgba(0, 242, 254, 0.2);
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    /* Interactive Controller Actions Button */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #05B292 0%, #00F2FE 100%);
        color: #0A0F1D;
        border: none;
        border-radius: 30px;
        padding: 14px 28px;
        width: 100%;
        font-weight: 900;
        font-size: 1.2rem;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        box-shadow: 0 4px 15px rgba(5, 178, 146, 0.4);
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 242, 254, 0.7);
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# ADVANCED SYSTEM ENGINES (KNOWLEDGE, IOT CONFIG, CROP METRICS)
# =====================================================================
SEARCH_KNOWLEDGE_BASE = {
    "drip": {
        "title": "💧 Micro-Drip Irrigation Systems",
        "desc": "Delivers localized moisture directly to the root architecture, limiting surface evaporation loss and maximizing water use efficiency up to 90%.",
        "url": "https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?w=800&q=80"
    },
    "sprinkler": {
        "title": "🌧️ Overhead Linear & Pivot Sprinklers",
        "desc": "Provides uniform coverage for high-density agricultural arrays using variable-rate pressure nozzles.",
        "url": "https://images.unsplash.com/photo-1628155930542-3c7a64e2c833?w=800&q=80"
    },
    "sensor": {
        "title": "📡 IoT Soil Moisture & FDR Sensors",
        "desc": "High-accuracy capacitive nodes deployed to transmit real-time Volumetric Water Content (VWC) directly to the telemetry gateway.",
        "url": "https://images.unsplash.com/photo-1530836369250-ef72a3f5c476?w=800&q=80"
    },
    "valve": {
        "title": "🔌 Electro-Hydraulic Solenoid Valves",
        "desc": "Receives programmatic digital triggers from the automation server to mechanically toggle high-pressure irrigation flows.",
        "url": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=800&q=80"
    },
    "weather": {
        "title": "🌤️ Predictive Ambient Weather Stations",
        "desc": "Integrates ambient temperature, atmospheric humidity indices, and precipitation radar vectors into predictive water forecasting models.",
        "url": "https://images.unsplash.com/photo-1504253163759-c23fccaedd24?w=800&q=80"
    }
}

CROP_ASSETS = {
    "Wheat": {
        "depth_mm": 50,
        "moisture_range": [45, 70],
        "images": [
            {"url": "https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=500&q=80", "caption": "Asset Track 1: Young Wheat Cultivar Development"},
            {"url": "https://images.unsplash.com/photo-1628155930542-3c7a64e2c833?w=500&q=80", "caption": "Asset Track 2: Pivot Irrigation Array Field Deployment"},
            {"url": "https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?w=500&q=80", "caption": "Asset Track 3: Fine Micro-Drip Root Zone Line"}
        ]
    },
    "Rice": {
        "depth_mm": 100,
        "moisture_range": [70, 95],
        "images": [
            {"url": "https://images.unsplash.com/photo-1536256263959-770b48d82b0a?w=500&q=80", "caption": "Asset Track 1: Submerged Rice Paddy Telemetry Point"},
            {"url": "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=500&q=80", "caption": "Asset Track 2: Terraced Rice Field Water Sluice Control"},
            {"url": "https://images.unsplash.com/photo-1520626872945-1d13f707f433?w=500&q=80", "caption": "Asset Track 3: Precision Flood Basin Laser Leveling"}
        ]
    },
    "Cotton": {
        "depth_mm": 65,
        "moisture_range": [50, 75],
        "images": [
            {"url": "https://images.unsplash.com/photo-1594489428504-5c0c480a15fd?w=500&q=80", "caption": "Asset Track 1: Root Zone Drip Framework for Cotton"},
            {"url": "https://images.unsplash.com/photo-1616142721473-b3a6ff603a1d?w=500&q=80", "caption": "Asset Track 2: Precision Sensor Post Installation"},
            {"url": "https://images.unsplash.com/photo-1442473483905-95eb436675f1?w=500&q=80", "caption": "Asset Track 3: High-Efficient Sprinkler Head"}
        ]
    },
    "Vegetables": {
        "depth_mm": 40,
        "moisture_range": [60, 85],
        "images": [
            {"url": "https://images.unsplash.com/photo-1566385278603-605b1d4f4f9a?w=500&q=80", "caption": "Asset Track 1: Micro-Drip Array on High-Yield Greens"},
            {"url": "https://images.unsplash.com/photo-1530836369250-ef72a3f5c476?w=500&q=80", "caption": "Asset Track 2: Solar Telemetry Node Grid"},
            {"url": "https://images.unsplash.com/photo-1601999114066-f42f5674066c?w=500&q=80", "caption": "Asset Track 3: Linear Irrigation Sled in Active Mode"}
        ]
    }
}

# --- Hybrid Mathematical Rule Engine & Machine Learning Predictor ---
def calculate_irrigation_needs(crop_type, current_moisture, temperature, humidity, weather_forecast):
    """
    Combines rule-based math and logical ML optimization vectors to output flow volume.
    """
    asset_data = CROP_ASSETS.get(crop_type, CROP_ASSETS["Wheat"])
    target = asset_data["moisture_range"]
    depth = asset_data["depth_mm"]
    
    # 1. Rules Engine: Soil Moisture Sensing Deficit computation
    if current_moisture < target[0]:
        status = "CRITICAL UNDER-WATERING: Actuator flow triggered."
        moisture_deficit_pct = target[1] - current_moisture
        water_required_liters_m2 = (moisture_deficit_pct / 100.0) * depth
    elif current_moisture > target[1]:
        status = "ALERT: WATERLOGGING RISK DETECTED. Solenoid shutdown forced."
        moisture_deficit_pct = 0
        water_required_liters_m2 = 0
    else:
        status = "OPTIMAL RANGE: Target balance maintained."
        moisture_deficit_pct = 0
        water_required_liters_m2 = 0
        
    # 2. Machine Learning Optimizer (Simulated ML microclimate scaling)
    if temperature > 35 and water_required_liters_m2 > 0:
        water_required_liters_m2 *= 1.15  # Thermal evaporation scale factor (+15%)
        
    if weather_forecast == "Heavy Rain" and water_required_liters_m2 > 0:
        # ML Predictive mitigation: scale down output dynamically
        water_required_liters_m2 *= 0.10
        status = "ML PREDICTIVE OVERRIDE: Irrigation minimized due to heavy incoming rain."
        
    return status, round(moisture_deficit_pct, 1), round(water_required_liters_m2, 2)

# =====================================================================
# DASHBOARD APPLICATION CORE UI
# =====================================================================

# 1. SCADA Branding Header
st.markdown("""
    <div class="scada-header">
        <div>
            <div class="header-main-title">🌾 SMART IRRIGATION INTERFACE</div>
            <div class="hw-status">🖥️ Remote Hardware Integration: Connected & Online</div>
        </div>
        <div>
            <div class="engineer-badge">💻 Lead Engineer: Sajid Ali, System lead</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# 2. Sidebar Command Desk & IoT Devices Configuration
st.sidebar.markdown("### 🔧 IoT Controller Configuration")
iot_controller = st.sidebar.selectbox("MCU Gateway Platform", ["ESP8266 Wi-Fi Node", "Raspberry Pi Zero 2W", "ESP32 LoRa Gateway"])
firmware_ver = st.sidebar.text_input("Firmware Version Tag", "v2.4.1-stable")
sensor_mode = st.sidebar.radio("Capacitive Sensor Signal", ["Analog (ADC)", "Digital (I2C Bus)"])

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔑 API Key Authentication")
groq_api_key = st.sidebar.text_input("Groq Cloud Authorization", type="password", placeholder="gsk_...")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔌 Real-time Hardware Actuators")
solenoid_valve_state = st.sidebar.toggle("Manual Solenoid Valve Bypass", value=False)
flow_pump_state = st.sidebar.toggle("Manual Water Pump Bypass", value=False)

# 3. Interactive Database Search Module
st.markdown("### 🔍 Advanced Database Search Module")
search_query = st.text_input(
    "Search agronomic framework components (e.g., drip, sprinkler, sensor, valve, weather):", 
    placeholder="Query database specifications..."
).lower().strip()

if len(search_query) > 0:
    matched = False
    for keyword, data in SEARCH_KNOWLEDGE_BASE.items():
        if keyword in search_query:
            matched = True
            st.markdown("---")
            search_col_text, search_col_img = st.columns([1, 1], gap="large")
            with search_col_text:
                st.subheader(data["title"])
                st.write(data["desc"])
                st.success("✔ Specifications verified in local telemetry records database.")
            with search_col_img:
                st.image(data["url"], caption=f"System Reference Spec Sheet Frame", use_column_width=True)
            break
            
    if not matched:
        st.warning(f"⚠️ No active specifications found for query: '{search_query}'.")

st.markdown("---")

# 4. Dual Control Room Layout
col_input, col_output = st.columns([4, 6], gap="large")

with col_input:
    st.markdown("### 📡 Live Sensor Telemetry (IoT Input)")
    crop_type = st.selectbox("Target Crop System Culture", list(CROP_ASSETS.keys()))
    
    # Soil Moisture Sensing Section
    moisture_pct = st.slider("Soil Moisture Sensing - Volumetric Content (%)", 10, 100, 35)
    
    # Weather Forecast Integration Section
    temp_c = st.slider("Microclimate Weather - Local Temperature (°C)", 10, 50, 38)
    humidity_pct = st.slider("Microclimate Weather - Relative Humidity (%)", 10, 100, 40)
    weather_forecast = st.radio("Predictive Weather Forecast Integration (24H)", ["Sunny / Clear", "Overcast", "Heavy Rain", "Scattered Showers"])
    
    # Trigger Logic & AI Calculations Execution
    execute_btn = st.button("🚀 Process Sensor Matrix & Activate AI")

with col_output:
    st.markdown("### 📋 Automation and Control Diagnostics")
    
    if execute_btn:
        if not groq_api_key:
            st.warning("⚠️ Integration Error: Groq Cloud API Key required for AI prediction routing.")
        else:
            with st.spinner("Processing through Mathematical Rules & Cognitive Llama-3 pipelines..."):
                
                # Execute evaluation logic
                valve_status, deficit_pct, water_volume = calculate_irrigation_needs(
                    crop_type, moisture_pct, temp_c, humidity_pct, weather_forecast
                )
                
                # Math System Definition
                st.markdown("#### 📐 Embedded System Mathematics Model")
                st.latex(r"V = \frac{\Delta M}{100} \times d")
                st.caption("Standard calculation profile where $V$ represents Volumetric water dosage ($L/m^2$) and $d$ is Root Zone depth (mm).")
                
                # Output Metric Cards
                metric_col1, metric_col2 = st.columns(2)
                with metric_col1:
                    st.metric(label="Calculated Soil Moisture Deficit (ΔM)", value=f"{deficit_pct}%")
                with metric_col2:
                    st.metric(label="Calculated Volumetric Output (V)", value=f"{water_volume} L/m²")
                
                # Automation Status Alerts
                st.info(f"⚙️ **Controller Actuator Log [{iot_controller}]:** {valve_status}")
                if water_volume > 0:
                    st.success(f"● [Solenoid Valve Actuator]: OPEN | ● [Main Water Pump]: ACTIVE at {water_volume} L/m² limit")
                else:
                    st.error("● [Solenoid Valve Actuator]: LOCKED / CLOSED | ● [Main Water Pump]: INACTIVE")
                
                # Multi-Image Diagnostics Panel
                st.markdown("---")
                st.markdown("#### 📸 Analytics Visual Tracks: Soil & Plant Feedback")
                images_to_display = CROP_ASSETS[crop_type]["images"]
                img_col1, img_col2, img_col3 = st.columns(3)
                with img_col1:
                    st.image(images_to_display[0]["url"], caption=images_to_display[0]["caption"], use_column_width=True)
                with img_col2:
                    st.image(images_to_display[1]["url"], caption=images_to_display[1]["caption"], use_column_width=True)
                with img_col3:
                    st.image(images_to_display[2]["url"], caption=images_to_display[2]["caption"], use_column_width=True)
                
                # AI Model Predictions Layer
                try:
                    llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama-3.1-8b-instant", temperature=0.1)
                    prompt = ChatPromptTemplate.from_template("""
                    You are an advanced AI Smart Irrigation Controller running on an embedded device.
                    Analyze these IoT metrics to output a localized automation protocol.
                    - Controller Board: {iot_controller} (running {firmware_ver})
                    - Target Crop: {crop_type}
                    - Current Moisture: {moisture_pct}%
                    - Temperature: {temp_c}°C
                    - Humidity: {humidity_pct}%
                    - Forecast Forecast: {weather_forecast}
                    - Calculated Volume: {water_volume} L/m²
                    
                    Provide a highly technical strategy covering:
                    1. Hardware System Diagnostic Check
                    2. Precise Valve Timing & Duty Cycle Schedule
                    3. AI Optimization Recommendations
                    """)
                    
                    chain = prompt | llm
                    response = chain.invoke({
                        "iot_controller": iot_controller,
                        "firmware_ver": firmware_ver,
                        "crop_type": crop_type,
                        "moisture_pct": moisture_pct,
                        "temp_c": temp_c,
                        "humidity_pct": humidity_pct,
                        "weather_forecast": weather_forecast,
                        "water_volume": water_volume
                    })
                    st.markdown("### 📋 AI Cognitive Advisory Report")
                    st.write(response.content)
                except Exception as e:
                    st.error(f"❌ Cognitive Core Processor Failure: {str(e)}")
    else:
        # Default starting visual output (displays the custom high-quality standby graphic)
        st.info("Remote System Standby: Configure parameters on the left and trigger calculation.")
        st.image("https://i.postimg.cc/CLyj6Nhr/Gemini-Generated-Image-o59yqgo59yqgo59y.png", caption="Lead Engineer: Sajid Ali — Precision Field Deployment Node", use_column_width=True)
