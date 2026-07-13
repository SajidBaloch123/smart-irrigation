import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# Page Configuration for Ultra-Wide Modern Console
st.set_page_config(
    page_title="APEX-I Smart Irrigation Console",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Advanced CSS Glassmorphic Styling & Neon Accents ---
st.markdown("""
    <style>
    /* Dark Slate Background */
    .stApp {
        background-color: #0B111E;
        color: #E2E8F0;
    }
    .block-container { padding-top: 1.5rem; }
    
    /* Sleek Glassmorphic Header */
    .premium-header {
        background: linear-gradient(135deg, rgba(20, 30, 48, 0.95) 0%, rgba(36, 59, 85, 0.95) 100%);
        border-radius: 16px;
        padding: 30px;
        border: 1px solid rgba(0, 242, 254, 0.25);
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 8px 32px 0 rgba(0, 242, 254, 0.15);
    }
    .header-main-title {
        color: #00F2FE;
        font-size: 2.8rem;
        font-weight: 900;
        letter-spacing: 2px;
        margin-bottom: 5px;
        text-shadow: 0 0 15px rgba(0,242,254,0.4);
    }
    .header-subtitle {
        color: #05B292;
        font-size: 1.1rem;
        font-weight: 700;
        letter-spacing: 4px;
        text-transform: uppercase;
        margin-bottom: 15px;
    }
    .engineer-signature {
        background: rgba(5, 178, 146, 0.15);
        color: #00F2FE;
        padding: 8px 24px;
        border-radius: 30px;
        font-weight: 800;
        display: inline-block;
        font-size: 1rem;
        border: 1px solid #05B292;
        box-shadow: 0 0 15px rgba(5, 178, 146, 0.2);
    }
    
    /* Interactive Metric Panels */
    div[data-testid="stMetric"] {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(0, 242, 254, 0.15);
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }
    
    /* Premium Action Button */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #05B292 0%, #00F2FE 100%);
        color: #0B111E;
        border: none;
        border-radius: 30px;
        padding: 14px;
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

# --- Dynamic Search Engine Knowledge Base ---
SEARCH_DB = {
    "drip irrigation": {
        "title": "💧 Micro-Drip Irrigation Framework",
        "desc": "Delivers targeted water and nutrients directly to plant root zones, mitigating run-off and optimizing water conservation by up to 60%.",
        "image": "https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?w=800&q=80"
    },
    "sprinkler": {
        "title": "🌧️ Center-Pivot Overhead Irrigation",
        "desc": "Automated overhead nozzle networks designed for uniform, large-scale moisture delivery across high-density crop fields.",
        "image": "https://images.unsplash.com/photo-1628155930542-3c7a64e2c833?w=800&q=80"
    },
    "soil sensor": {
        "title": "📡 IoT Soil Moisture Probes",
        "desc": "FDR/TDR sensor modules measuring relative permittivity of soil structures to transmit live volumetric water content (VWC).",
        "image": "https://images.unsplash.com/photo-1530836369250-ef72a3f5c476?w=800&q=80"
    },
    "weather station": {
        "title": "🌤️ Ambient Microclimate Telemetry",
        "desc": "Integrates atmospheric pressure, relative humidity, UV indices, and rain tipping-bucket data into predictive algorithm models.",
        "image": "https://images.unsplash.com/photo-1504253163759-c23fccaedd24?w=800&q=80"
    },
    "solenoid valve": {
        "title": "🔌 Electro-Hydraulic Flow Control",
        "desc": "12V-24V solenoid actuators receiving digital switch triggers to mechanically toggle irrigation pipeline flow.",
        "image": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=800&q=80"
    }
}

# --- Multi-Image Analytical Data Asset Map ---
CROP_ASSETS = {
    "Wheat": {
        "depth_mm": 50,
        "moisture_range": [45, 70],
        "images": [
            {"url": "https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=500&q=80", "caption": "Analytical View: Crop Foliage Matrix"},
            {"url": "https://images.unsplash.com/photo-1500937386664-56d1dfef3854?w=500&q=80", "caption": "Field View: Active Zone Sensor Grid"},
            {"url": "https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?w=500&q=80", "caption": "Irrigation: Root-Zone Sub-Surface Lines"}
        ]
    },
    "Rice": {
        "depth_mm": 100,
        "moisture_range": [70, 95],
        "images": [
            {"url": "https://images.unsplash.com/photo-1536256263959-770b48d82b0a?w=500&q=80", "caption": "Analytical View: Saturated Paddy Levels"},
            {"url": "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=500&q=80", "caption": "Field View: Hydraulic Canal Inflow Gate"},
            {"url": "https://images.unsplash.com/photo-1520626872945-1d13f707f433?w=500&q=80", "caption": "Irrigation: Flooded Irrigation Basin"}
        ]
    },
    "Cotton": {
        "depth_mm": 65,
        "moisture_range": [50, 75],
        "images": [
            {"url": "https://images.unsplash.com/photo-1594489428504-5c0c480a15fd?w=500&q=80", "caption": "Analytical View: Crop Sprout Density"},
            {"url": "https://images.unsplash.com/photo-1616142721473-b3a6ff603a1d?w=500&q=80", "caption": "Field View: Core Monitoring Pole Node"},
            {"url": "https://images.unsplash.com/photo-1442473483905-95eb436675f1?w=500&q=80", "caption": "Irrigation: High-Efficiency Lateral Spray"}
        ]
    },
    "Vegetables": {
        "depth_mm": 40,
        "moisture_range": [60, 85],
        "images": [
            {"url": "https://images.unsplash.com/photo-1566385278603-605b1d4f4f9a?w=500&q=80", "caption": "Analytical View: Canopy Thermal Map"},
            {"url": "https://images.unsplash.com/photo-1530836369250-ef72a3f5c476?w=500&q=80", "caption": "Field View: Solarized Node Installation"},
            {"url": "https://images.unsplash.com/photo-1601999114066-f42f5674066c?w=500&q=80", "caption": "Irrigation: Pressure-Compensating Drip Line"}
        ]
    }
}

# --- Calculation Engine ---
def calculate_irrigation_needs(crop_type, current_moisture, temperature):
    asset_data = CROP_ASSETS.get(crop_type, CROP_ASSETS["Wheat"])
    target = asset_data["moisture_range"]
    depth = asset_data["depth_mm"]
    
    if current_moisture < target[0]:
        status = "CRITICAL LIMIT: Solenoid Open Command Sent."
        moisture_deficit_pct = target[1] - current_moisture
        water_required_liters_m2 = (moisture_deficit_pct / 100.0) * depth
    elif current_moisture > target[1]:
        status = "ALERT: Waterlogging risk detected. Discharge active."
        moisture_deficit_pct = 0
        water_required_liters_m2 = 0
    else:
        status = "SYSTEM STABLE: Equilibrium maintained. Valves offline."
        moisture_deficit_pct = 0
        water_required_liters_m2 = 0
        
    if temperature > 35 and water_required_liters_m2 > 0:
        water_required_liters_m2 *= 1.15
        
    return status, round(moisture_deficit_pct, 1), round(water_required_liters_m2, 2)

# --- Header Interface ---
st.markdown("""
    <div class="premium-header">
        <div class="header-main-title">🌾 APEX-I SMART IRRIGATION CONSOLE</div>
        <div class="header-subtitle">Advanced IoT Cloud Telemetry & AI Decision Engine</div>
        <div class="engineer-signature">💻 Lead Engineer: Sajid Ali, System lead</div>
    </div>
""", unsafe_allow_html=True)

# --- Sidebar Management Desk ---
st.sidebar.markdown("### 🛠️ Hardware Command Desk")
groq_api_key = st.sidebar.text_input("Groq API Authorization", type="password", placeholder="gsk_...")
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Network Gateway Logs")
st.sidebar.success("● Telemetry Channel 1 [Wheat]: ACTIVE")
st.sidebar.success("● Telemetry Channel 2 [Rice]: ACTIVE")
st.sidebar.info("● Telemetry Channel 3 [Cotton]: STANDBY")

# --- Interactive AI Search Section ---
st.markdown("### 🔍 Advanced Database Search Module")
search_query = st.text_input("Search Agronomic terms (e.g., drip irrigation, soil sensor, weather station, sprinkler, solenoid valve):").lower().strip()

if search_query:
    matched = False
    for key, data in SEARCH_DB.items():
        if key in search_query:
            matched = True
            search_col_text, search_col_img = st.columns([1, 1], gap="medium")
            with search_col_text:
                st.markdown(f"### {data['title']}")
                st.write(data['desc'])
                st.success("✔ Database Query Successful. Visual matching retrieved below:")
            with search_col_img:
                st.image(data['image'], caption=f"System Resource Graphic: {data['title']}", use_column_width=True)
            break
    if not matched:
        st.warning("⚠️ No specific match found. Showing dynamic real-time telemetry field database backup:")
        st.image("https://images.unsplash.com/photo-1500937386664-56d1dfef3854?w=800&q=80", caption="Active Agriculture Field Deployment Frame", use_column_width=True)
st.markdown("---")

# --- Dual Console Layout ---
col_controls, col_display = st.columns([4, 6], gap="large")

with col_controls:
    st.markdown("### 📡 Active Sensor Array Controls")
    crop_type = st.selectbox("Crop Target Matrix", list(CROP_ASSETS.keys()))
    moisture_pct = st.slider("Soil Volumetric Moisture Content (%)", 10, 100, 35)
    temp_c = st.slider("Ambient Temperature (°C)", 10, 50, 38)
    humidity_pct = st.slider("Atmospheric Relative Humidity (%)", 10, 100, 40)
    weather_forecast = st.radio("Predictive Radar Outlook (24H)", ["Sunny / Clear", "Overcast / Storm Front", "Imminent Rainfall", "Scattered Showers"])
    execute_btn = st.button("🚀 Process Sensor Matrix & Activate AI")

with col_display:
    st.markdown("### 📋 Automation Diagnostics Panel")
    
    if execute_btn:
        if not groq_api_key:
            st.error("❌ Authorization Error: Invalid or missing Groq API key in the command deck.")
        else:
            with st.spinner("Compiling high-density analytical logs and rendering multi-grid imagery..."):
                valve_status, deficit_pct, water_volume = calculate_irrigation_needs(crop_type, moisture_pct, temp_c)
                
                # Metrics Outputs
                m_col1, m_col2 = st.columns(2)
                with m_col1:
                    st.metric(label="Detected Soil Moisture Deficit", value=f"{deficit_pct}%")
                with m_col2:
                    st.metric(label="Automated Volumetric Output", value=f"{water_volume} L/m²")
                
                st.info(f"💾 **PLC System Switch Log:** {valve_status}")
                
                # Multi-Image Analytical Gallery
                st.markdown("#### 📊 Dynamic Diagnostic Image Gallery")
                images_list = CROP_ASSETS[crop_type]["images"]
                img_col1, img_col2, img_col3 = st.columns(3)
                with img_col1:
                    st.image(images_list[0]["url"], caption=images_list[0]["caption"], use_column_width=True)
                with img_col2:
                    st.image(images_list[1]["url"], caption=images_list[1]["caption"], use_column_width=True)
                with img_col3:
                    st.image(images_list[2]["url"], caption=images_list[2]["caption"], use_column_width=True)
                
                # Groq LLM Diagnostics Logic
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
                    st.markdown("### 📋 AI Agronomic Advisory Report")
                    st.write(response.content)
                except Exception as e:
                    st.error(f"❌ AI Processor Error: {str(e)}")
    else:
        st.info("System Standby: Awaiting sensor matrix triggers. Adjust parameters on the left to activate.")
        # Beautiful high-tech agriculture placeholder image
        st.image("https://images.unsplash.com/photo-1500937386664-56d1dfef3854?w=1200&auto=format&fit=crop&q=80", caption="System Status: Field Node A — Optimal Stability Telemetry (Sajid Ali, System lead)", use_column_width=True)
