import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# Set up page layout style
st.set_page_config(
    page_title="Smart Irrigation System",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom premium styling (integrated branding)
st.markdown("""
    <style>
    .block-container { padding-top: 1.5rem; }
    
    /* System Lead Header Card */
    .lead-engineer-card {
        background: rgba(15, 32, 39, 0.9);
        border-radius: 12px;
        padding: 18px;
        border: 2px solid #05B292;
        text-align: center;
        margin-bottom: 25px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .header-main-title {
        color: #00F2FE;
        font-size: 2.2rem;
        font-weight: 800;
        text-shadow: 0 0 10px rgba(0,242,254,0.3);
    }
    .lead-credentials {
        color: white;
        background-color: #05B292;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.9rem;
    }
    .hw-gateways {
        color: #00F2FE;
        font-size: 0.85rem;
        margin-top: 5px;
    }

    /* Button styles (Pulse effect) */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #05B292 0%, #00F2FE 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 12px;
        width: 100%;
        font-weight: bold;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(5, 178, 146, 0.4);
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 242, 254, 0.6);
    }
    </style>
""", unsafe_allow_html=True)

# --- Multi-Image Data Structure ---
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

# --- Mathematical Rules Engine ---
def calculate_irrigation_needs(crop_type, current_moisture, temperature, humidity):
    asset_data = CROP_ASSETS.get(crop_type, CROP_ASSETS["Wheat"])
    target = asset_data["moisture_range"]
    depth = asset_data["depth_mm"]
    
    if current_moisture < target[0]:
        status = "CRITICAL UNDER-WATERING: Automatic Valve Trigger Activated"
        moisture_deficit_pct = target[1] - current_moisture
        water_required_liters_m2 = (moisture_deficit_pct / 100.0) * depth
    elif current_moisture > target[1]:
        status = "ALERT: FIELD SATURATED / WATERLOGGING RISK"
        moisture_deficit_pct = 0
        water_required_liters_m2 = 0
    else:
        status = "OPTIMAL STABILITY: Irrigation Cycles Postponed"
        moisture_deficit_pct = 0
        water_required_liters_m2 = 0
        
    if temperature > 35 and water_required_liters_m2 > 0:
        water_required_liters_m2 *= 1.15
        
    return status, round(moisture_deficit_pct, 1), round(water_required_liters_m2, 2)

# --- 1. Top Section: Lead Engineer Branding Card ---
st.markdown("""
    <div class="lead-engineer-card">
        <div>
            <div class="header-main-title">🌾 SMART IRRIGATION INTERFACE</div>
            <div class="hw-gateways">🖥️ Hardware Gateways: Connected (4 Active Nodes)</div>
        </div>
        <div>
            <div class="lead-credentials">💻 Lead Engineer: Sajid Ali, System lead</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Sidebar Setup (Credentials)
st.sidebar.markdown("### 🔑 System Authorization")
groq_api_key = st.sidebar.text_input("Groq API Key", type="password", placeholder="gsk_...")
st.sidebar.markdown("---")
st.sidebar.markdown("### 📡 Hardware Telemetry")
st.sidebar.success("● Node A: Wheat Field (Connected)")
st.sidebar.success("● Node B: Rice Paddy (Connected)")
st.sidebar.success("● Node C: Cotton Field (Connected)")

# Split Dashboard Layout
col_input, col_output = st.columns([4, 6], gap="large")

with col_input:
    st.markdown("### 📊 Live Telemetry Inputs")
    crop_type = st.selectbox("Target Crop Asset", list(CROP_ASSETS.keys()))
    moisture_pct = st.slider("Soil Moisture Content (%)", 10, 100, 35)
    temp_c = st.slider("Field Ambient Temperature (°C)", 10, 50, 38)
    humidity_pct = st.slider("Atmospheric Humidity Ratio (%)", 10, 100, 40)
    weather_forecast = st.radio("Weather Outlook (24H)", ["Sunny / Clear", "Overcast", "Heavy Rain", "Scattered Showers"])
    execute_btn = st.button("🚀 Evaluate & Compute System Logic")

with col_output:
    st.markdown("### 📋 Evaluation Output & Diagnostics")
    
    if execute_btn:
        if not groq_api_key:
            st.warning("⚠️ Setup Error: Groq API Key required for AI analysis module.")
        else:
            with st.spinner("Analyzing telemetry profiles and rendering diagnostics grid..."):
                valve_status, deficit_pct, water_volume = calculate_irrigation_needs(crop_type, moisture_pct, temp_c, humidity_pct)
                
                # Metrics Section
                metric_col1, metric_col2 = st.columns(2)
                with metric_col1:
                    st.metric(label="Calculated Moisture Deficit", value=f"{deficit_pct}%")
                with metric_col2:
                    st.metric(label="Volumetric Water Dosage", value=f"{water_volume} L/m²")
                st.info(f"**System Log:** {valve_status}")
                
                # --- NEW: Enhanced Multi-Image Output Section ---
                st.markdown("---")
                st.markdown("#### 📸 Diagnostics Image Gallery: Multi-Track Analysis")
                images_to_display = CROP_ASSETS[crop_type]["images"]
                img_col1, img_col2, img_col3 = st.columns(3)
                
                # Display 3 separate images for the single crop asset
                with img_col1:
                    st.image(images_to_display[0]["url"], caption=images_to_display[0]["caption"], use_column_width=True)
                with img_col2:
                    st.image(images_to_display[1]["url"], caption=images_to_display[1]["caption"], use_column_width=True)
                with img_col3:
                    st.image(images_to_display[2]["url"], caption=images_to_display[2]["caption"], use_column_width=True)
                # ---------------------------------------------
                
                # LLM reasoning layer
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
                    response = chain.invoke({"crop_type": crop_type, "moisture_pct": moisture_pct, "temp_c": temp_c, "humidity_pct": humidity_pct, "weather_forecast": weather_forecast, "water_volume": water_volume})
                    st.markdown("### 📋 Agronomic Assessment Strategy")
                    st.write(response.content)
                except Exception as e:
                    st.error(f"❌ AI Inference Failure: {str(e)}")
    else:
        # --- NEW Standby Visual (Direct, verified, stunning irrigation image) ---
        st.info("System in Active-Standby Mode. Configure inputs on the left and execute to generate diagnostics.")
        st.image("https://images.unsplash.com/photo-1500937386664-56d1dfef3854?w=1000&auto=format&fit=crop&q=80", caption="System Status: Field Node A — Active Telemetry Standby (Sajid Ali, System lead)", use_column_width=True)
