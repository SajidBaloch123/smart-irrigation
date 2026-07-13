import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# Set up page layout style (Advanced Industrial View)
st.set_page_config(
    page_title="APEX-I Smart Irrigation Console",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Premium Glassmorphism & Cyberpunk Neon UI Customization ---
st.markdown("""
    <style>
    /* Deep Space Background */
    .stApp {
        background-color: #0A0F1D;
        color: #E2E8F0;
    }
    .block-container { padding-top: 1.5rem; }
    
    /* Neon Lead Engineer Header Card */
    .lead-engineer-card {
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
    .lead-credentials {
        color: white;
        background: linear-gradient(135deg, #05B292 0%, #00F2FE 100%);
        padding: 8px 18px;
        border-radius: 30px;
        font-weight: 800;
        font-size: 1rem;
        box-shadow: 0 4px 15px rgba(5, 178, 146, 0.3);
        border: 1px solid rgba(255,255,255,0.2);
    }
    .hw-gateways {
        color: #05B292;
        font-size: 0.95rem;
        font-weight: 700;
        letter-spacing: 1px;
        margin-top: 5px;
        text-align: left;
    }

    /* Glass Panels for Inputs and Displays */
    div[data-testid="stMetric"] {
        background: rgba(20, 30, 55, 0.6);
        border: 1px solid rgba(0, 242, 254, 0.15);
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    /* Glowing Action Buttons with Pulse effect */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #05B292 0%, #00F2FE 100%);
        color: #0A0F1D;
        border: none;
        border-radius: 30px;
        padding: 14px 28px;
        width: 100%;
        font-weight: 900;
        font-size: 1.2rem;
        letter-spacing: 1px;
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

# --- Advanced Visual Knowledge Base (Dynamic Search Engine) ---
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

# --- NEW: Advanced Database Search & Visual Query Engine ---
st.markdown("### 🔍 Advanced Database Search Module")
search_query = st.text_input(
    "Type to search agronomic framework terms (e.g., drip, sprinkler, sensor, valve, weather):", 
    placeholder="Search telemetry components..."
).lower().strip()

if search_query:
    matched = False
    for keyword, data in SEARCH_KNOWLEDGE_BASE.items():
        if keyword in search_query:
            matched = True
            st.markdown("---")
            search_col_text, search_col_img = st.columns([1, 1], gap="large")
            with search_col_text:
                st.subheader(data["title"])
                st.write(data["desc"])
                st.success(f"✔ Live telemetry search match: Database records verified.")
            with search_col_img:
                st.image(data["url"], caption=f"Component Reference: {data['title']}", use_column_width=True)
            break
    if not matched:
        st.warning("⚠️ No specific match found. Showing current custom system standby node:")
        st.image("https://i.postimg.cc/CLyj6Nhr/Gemini-Generated-Image-o59yqgo59yqgo59y.png", caption="Custom Lead Node Backup Display", use_column_width=True)
st.markdown("---")

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
                
                # --- Enhanced Multi-Image Output Section ---
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
        # --- Standby Visual (Custom Lead Node Wallpaper) ---
        st.info("System in Active-Standby Mode. Configure inputs on the left and execute to generate diagnostics.")
        st.image("https://i.postimg.cc/CLyj6Nhr/Gemini-Generated-Image-o59yqgo59yqgo59y.png", caption="Lead Engineer: Sajid Ali — Precision Field Deployment", use_column_width=True)
