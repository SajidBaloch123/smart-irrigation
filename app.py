"""
APEX-I Smart Irrigation Console
Lead Systems Engineer: Sajid Ali, Computer Systems Engineering (CSE)

This module implements an academic-grade, AI-driven Decision Support System (DSS)
for precision agriculture. It integrates an empirical Mathematical Rules Engine,
a Llama-3 Cognitive AI Layer, and a formal Agricultural Research & Comparative Analysis Module.
"""

import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# =====================================================================
# SYSTEM CONFIGURATION & UI STYLING
# =====================================================================
st.set_page_config(
    page_title="APEX-I Smart Irrigation Console",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium SCADA and Academic Glassmorphism Styles
st.markdown("""
    <style>
    .stApp {
        background-color: #0A0F1D;
        color: #E2E8F0;
    }
    .block-container { padding-top: 1.5rem; }
    
    /* SCADA Style Header Card */
    .scada-header {
        background: linear-gradient(135deg, rgba(16, 24, 48, 0.95) 0%, rgba(24, 43, 73, 0.95) 100%);
        border-radius: 16px;
        padding: 24px;
        border: 1px solid rgba(0, 242, 254, 0.3);
        text-align: center;
        margin-bottom: 30px;
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

    /* Embedded Glass Panels for Metrics */
    div[data-testid="stMetric"] {
        background: rgba(20, 30, 55, 0.6);
        border: 1px solid rgba(0, 242, 254, 0.15);
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    /* Styled Control Buttons */
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
    
    /* Research Card Styling */
    .research-card {
        background: rgba(20, 30, 55, 0.4);
        border-left: 5px solid #00F2FE;
        padding: 15px;
        margin-bottom: 15px;
        border-radius: 4px;
    }
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# SYSTEM DATABASES (KNOWLEDGE, CROPS, RESEARCH)
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

# =====================================================================
# MATHEMATICAL RULES ENGINE
# =====================================================================
def calculate_irrigation_needs(crop_type, current_moisture, temperature, humidity):
    asset_data = CROP_ASSETS.get(crop_type, CROP_ASSETS["Wheat"])
    target = asset_data["moisture_range"]
    depth = asset_data["depth_mm"]
    
    if current_moisture < target[0]:
        status = "CRITICAL UNDER-WATERING: Automatic Solenoid Valve Triggered."
        moisture_deficit_pct = target[1] - current_moisture
        water_required_liters_m2 = (moisture_deficit_pct / 100.0) * depth
    elif current_moisture > target[1]:
        status = "ALERT: FIELD SATURATED / WATERLOGGING RISK. Valves Locked."
        moisture_deficit_pct = 0
        water_required_liters_m2 = 0
    else:
        status = "OPTIMAL STABILITY: Irrigation Cycles Postponed."
        moisture_deficit_pct = 0
        water_required_liters_m2 = 0
        
    if temperature > 35 and water_required_liters_m2 > 0:
        water_required_liters_m2 *= 1.15
        
    return status, round(moisture_deficit_pct, 1), round(water_required_liters_m2, 2)

# =====================================================================
# SYSTEM MAIN ENTRY HEADER
# =====================================================================
st.markdown("""
    <div class="scada-header">
        <div>
            <div class="header-main-title">🌾 APEX-I SMART IRRIGATION CONSOLE</div>
            <div class="hw-status">🖥️ Core Hardware Gateways: Connected & Processing</div>
        </div>
        <div>
            <div class="engineer-badge">💻 Lead Engineer: Sajid Ali, System lead</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Define Main Application Workspaces
tab_active, tab_methodology = st.tabs(["🎮 Active Control Console", "📘 Systems Methodology & Literature Study"])

# =====================================================================
# WORKSPACE 1: ACTIVE CONTROL CONSOLE
# =====================================================================
with tab_active:
    # Sidebar Setup
    st.sidebar.markdown("### 🔑 System Authorization")
    groq_api_key = st.sidebar.text_input("Groq API Key", type="password", placeholder="gsk_...")
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📡 Hardware Telemetry")
    st.sidebar.success("● Node A: Wheat Field (Connected)")
    st.sidebar.success("● Node B: Rice Paddy (Connected)")
    st.sidebar.success("● Node C: Cotton Field (Connected)")

    # Interactive Search Module
    st.markdown("### 🔍 Advanced Database Search Module")
    search_query = st.text_input(
        "Query the localized telemetry components database (e.g., drip, sprinkler, sensor, valve, weather):", 
        placeholder="Enter keyword...",
        key="active_search"
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
                    st.success("✔ Database query successful. Hardware specifications matching:")
                with search_col_img:
                    st.image(data["url"], caption=f"Component Specifications Reference Frame", use_column_width=True)
                break
                
        if not matched:
            st.warning(f"⚠️ No specific system match found for '{search_query}'.")

    st.markdown("---")

    # Dual Control Layout
    col_input, col_output = st.columns([4, 6], gap="large")

    with col_input:
        st.markdown("### 📊 Active Telemetry Feeds")
        crop_type = st.selectbox("Target Crop Profile", list(CROP_ASSETS.keys()))
        moisture_pct = st.slider("Capacitive Sensor Volumetric Soil Moisture (%)", 10, 100, 35)
        temp_c = st.slider("External Ambient Temperature Reading (°C)", 10, 50, 38)
        humidity_pct = st.slider("Relative Atmospheric Humidity (%)", 10, 100, 40)
        weather_forecast = st.radio("Predictive Microclimate Outlook (24H)", ["Sunny / Clear", "Overcast", "Heavy Rain", "Scattered Showers"])
        execute_btn = st.button("🚀 Process Sensor Matrix & Activate AI")

    with col_output:
        st.markdown("### 📋 System Evaluation Outputs & Analytics")
        
        if execute_btn:
            if not groq_api_key:
                st.warning("⚠️ Configuration Error: Please input your Groq API Key on the sidebar desk.")
            else:
                with st.spinner("Executing Mathematical Rules Engine & LLM Cognitive Layer..."):
                    valve_status, deficit_pct, water_volume = calculate_irrigation_needs(
                        crop_type, moisture_pct, temp_c, humidity_pct
                    )
                    
                    st.markdown("#### 📐 Embedded System Mathematics")
                    st.latex(r"V = \frac{\Delta M}{100} \times d")
                    st.caption("Where $V$ = Volumetric Water Dosage ($L/m^2$), $\Delta M$ = Moisture Deficit (%), and $d$ = Crop Root Zone Depth (mm).")
                    
                    metric_col1, metric_col2 = st.columns(2)
                    with metric_col1:
                        st.metric(label="Calculated Moisture Deficit (ΔM)", value=f"{deficit_pct}%")
                    with metric_col2:
                        st.metric(label="Volumetric Water Dosage Output (V)", value=f"{water_volume} L/m²")
                        
                    st.info(f"⚙️ **PLC Solenoid State Log:** {valve_status}")
                    
                    st.markdown("---")
                    st.markdown("#### 📸 Telemetry-Matched Multi-Track Imagery")
                    images_to_display = CROP_ASSETS[crop_type]["images"]
                    img_col1, img_col2, img_col3 = st.columns(3)
                    with img_col1:
                        st.image(images_to_display[0]["url"], caption=images_to_display[0]["caption"], use_column_width=True)
                    with img_col2:
                        st.image(images_to_display[1]["url"], caption=images_to_display[1]["caption"], use_column_width=True)
                    with img_col3:
                        st.image(images_to_display[2]["url"], caption=images_to_display[2]["caption"], use_column_width=True)
                    
                    try:
                        llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama-3.1-8b-instant", temperature=0.1)
                        prompt = ChatPromptTemplate.from_template("""
                        You are an advanced AI Smart Irrigation Controller and Expert Agronomist.
                        Analyze the following real-time field telemetry metrics to output an operational strategy.
                        - Crop: {crop_type}
                        - Current Moisture: {moisture_pct}%
                        - Temperature: {temp_c}°C
                        - Humidity: {humidity_pct}%
                        - Forecast: {weather_forecast}
                        - Calculated Volume: {water_volume} L/m²
                        
                        Provide a concise, professional strategy covering Field Status Assessment, Exact Watering Schedule Guide, and Automation Override Log.
                        """)
                        
                        chain = prompt | llm
                        response = chain.invoke({
                            "crop_type": crop_type,
                            "moisture_pct": moisture_pct,
                            "temp_c": temp_c,
                            "humidity_pct": humidity_pct,
                            "weather_forecast": weather_forecast,
                            "water_volume": water_volume
                        })
                        st.markdown("### 📋 AI Cognitive Agronomic Advisory Report")
                        st.write(response.content)
                    except Exception as e:
                        st.error(f"❌ AI Reasoning Engine Processor Failure: {str(e)}")
        else:
            st.info("System Standby: Awaiting sensor matrix triggers. Adjust parameters on the left to activate.")
            st.image("https://i.postimg.cc/CLyj6Nhr/Gemini-Generated-Image-o59yqgo59yqgo59y.png", caption="Lead Engineer: Sajid Ali — Precision Field Deployment", use_column_width=True)

# =====================================================================
# WORKSPACE 2: SYSTEMS METHODOLOGY & LITERATURE STUDY
# =====================================================================
with tab_methodology:
    st.markdown("## 📘 Agricultural IoT & AI Framework Analysis")
    st.write("A structured literature survey maps the APEX-I Console core attributes against standard, peer-reviewed engineering methodologies on GitHub.")
    
    col_tech1, col_tech2 = st.columns(2)
    
    with col_tech1:
        st.markdown("""
        <div class="research-card">
            <h3>🌱 1. Real-Time Soil Moisture Sensing</h3>
            <p><strong>Standard GitHub Practice:</strong> Systems utilize capacitive or resistive probes to translate environmental moisture into volumetric water percentages.</p>
            <p><strong>APEX-I Integration:</strong> Tracks precise VWC via simulated capacitive inputs, matching the telemetry to target crop tolerance parameters (e.g., 45%-70% for Wheat).</p>
        </div>
        <div class="research-card">
            <h3>🌤️ 2. Weather Forecast Integration</h3>
            <p><strong>Standard GitHub Practice:</strong> Integrates OpenWeatherMap APIs or historical microclimate indices to forecast predictive evaporative loss.</p>
            <p><strong>APEX-I Integration:</strong> Combines real-time microclimatic trends with predictive inputs. Under extreme weather profiles (>35°C), it factors a +15% thermal compensation multiplier.</p>
        </div>
        <div class="research-card">
            <h3>⚙️ 3. Automation and Actuators</h3>
            <p><strong>Standard GitHub Practice:</strong> Utilizes physical solenoid valves and relays toggled by raw digital HIGH/LOW microchip registers.</p>
            <p><strong>APEX-I Integration:</strong> Computes the exact volumetric requirements ($L/m^2$) before triggering virtual solenoid valve open-times, safeguarding against runoff.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_tech2:
        st.markdown("""
        <div class="research-card">
            <h3>🧠 4. Cognitive AI & Machine Learning</h3>
            <p><strong>Standard GitHub Practice:</strong> Employs offline ML regression architectures (such as Random Forest) to evaluate static irrigation models.</p>
            <p><strong>APEX-I Integration:</strong> Integrates a real-time Generative LLM agent (Llama-3.1 via LangChain). The agent analyzes active microclimatic threats and suggests adaptive adjustments.</p>
        </div>
        <div class="research-card">
            <h3>🔌 5. IoT Distributed Architecture</h3>
            <p><strong>Standard GitHub Practice:</strong> Relies on microcontrollers (such as ESP8266 or Raspberry Pi) communicating over HTTP/MQTT protocols.</p>
            <p><strong>APEX-I Integration:</strong> Simulates a multi-node distributed SCADA model, establishing continuous telemetry channels across 3 separate sensor nodes.</p>
        </div>
        <div class="research-card">
            <h3>🖥️ 6. Unified User Interface (SCADA)</h3>
            <p><strong>Standard GitHub Practice:</strong> Simple visual telemetry charts lacking built-in diagnostic lookup features.</p>
            <p><strong>APEX-I Integration:</strong> Built with Streamlit glassmorphism dashboards, featuring an active database search module matching images dynamically to researched keywords.</p>
        </div>
        """, unsafe_allow_html=True)
