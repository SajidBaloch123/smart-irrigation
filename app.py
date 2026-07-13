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

# Custom premium styling (Dark green, glassmorphism, and custom buttons)
st.markdown("""
    <style>
    .block-container { padding-top: 1.5rem; }
    
    /* Header Card styling */
    .header-card {
        background: rgba(15, 32, 39, 0.85);
        border-radius: 15px;
        padding: 25px;
        border: 2px solid #05B292;
        text-align: center;
        margin-bottom: 20px;
    }
    .header-title {
        color: #00F2FE;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 5px;
        text-shadow: 0 0 10px rgba(0,242,254,0.3);
    }
    .header-subtitle {
        color: #05B292;
        font-size: 1.1rem;
        font-weight: 600;
        letter-spacing: 2px;
        margin-bottom: 15px;
    }
    .engineer-badge {
        background-color: #05B292;
        color: white;
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        font-size: 0.95rem;
        box-shadow: 0 4px 15px rgba(5, 178, 146, 0.3);
    }
    
    /* Button styles */
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

# Dynamic Agricultural Image Mapping
CROP_IMAGES = {
    "Wheat": {
        "url": "https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=800&auto=format&fit=crop&q=80",
        "caption": "Precision Pivotal Irrigation Operating on a Cultivated Wheat Field Asset"
    },
    "Rice": {
        "url": "https://images.unsplash.com/photo-1536256263959-770b48d82b0a?w=800&auto=format&fit=crop&q=80",
        "caption": "Automated Water-Level Regulation and Sluice Controls Active on Rice Terraces"
    },
    "Cotton": {
        "url": "https://images.unsplash.com/photo-1594489428504-5c0c480a15fd?w=800&auto=format&fit=crop&q=80",
        "caption": "Targeted Root-Zone Micro-Drip Irrigation System Deployed for Cotton Rows"
    },
    "Maize": {
        "url": "https://images.unsplash.com/photo-1530595467537-0b5996c41f2d?w=800&auto=format&fit=crop&q=80",
        "caption": "Overhead Sprinkler System Optimizing Moisture Levels on Maize Crops"
    },
    "Vegetables": {
        "url": "https://images.unsplash.com/photo-1566385278603-605b1d4f4f9a?w=800&auto=format&fit=crop&q=80",
        "caption": "Smart Agricultural Drip-Line Framework Active on High-Yield Vegetables"
    }
}

# --- Mathematical Rules Engine ---
def calculate_irrigation_needs(crop_type, current_moisture, temperature, humidity):
    crop_baselines = {
        "Wheat": {"min": 45, "max": 70, "depth_mm": 50},
        "Rice": {"min": 70, "max": 95, "depth_mm": 100},
        "Cotton": {"min": 50, "max": 75, "depth_mm": 65},
        "Maize": {"min": 55, "max": 80, "depth_mm": 60},
        "Vegetables": {"min": 60, "max": 85, "depth_mm": 40}
    }
    
    target = crop_baselines.get(crop_type, {"min": 50, "max": 75, "depth_mm": 50})
    
    if current_moisture < target["min"]:
        status = "CRITICAL UNDER-WATERING: Valve Trigger Activated Automatically"
        moisture_deficit_pct = target["max"] - current_moisture
        water_required_liters_m2 = (moisture_deficit_pct / 100.0) * target["depth_mm"]
    elif current_moisture > target["max"]:
        status = "ALERT: FIELD SATURATED / WATERLOGGING RISK"
        moisture_deficit_pct = 0
        water_required_liters_m2 = 0
    else:
        status = "OPTIMAL STABILITY: No Immediate Watering Required"
        moisture_deficit_pct = 0
        water_required_liters_m2 = 0
        
    if temperature > 35 and water_required_liters_m2 > 0:
        water_required_liters_m2 *= 1.15
        
    return status, round(moisture_deficit_pct, 1), round(water_required_liters_m2, 2)

# --- 1. Wallpaper Header Banner & Developer Branding ---
st.image("https://images.unsplash.com/photo-1628155930542-3c7a64e2c833?w=1400&auto=format&fit=crop&q=80", use_column_width=True)

st.markdown("""
    <div class="header-card">
        <div class="header-title">🌾 SMART IRRIGATION AUTOMATION PLATFORM</div>
        <div class="header-subtitle">IOT PRECISION TELEMETRY & DECISION ENGINE</div>
        <div class="engineer-badge">💻 Developed by: Engineer Sajid Ali</div>
    </div>
""", unsafe_allow_html=True)

# Sidebar Setup (Credentials)
st.sidebar.markdown("### 🔑 System Authorization")
groq_api_key = st.sidebar.text_input("Groq API Key", type="password", placeholder="gsk_...")
st.sidebar.markdown("---")
st.sidebar.markdown("### 🖥️ Hardware Controller Status")
st.sidebar.success("● IoT Node Gateways: Connected")
st.sidebar.success("● Flow Valve Actuators: Ready")

# Split Dashboard Layout
col_input, col_output = st.columns([4, 6], gap="large")

with col_input:
    st.markdown("### 📡 Live Field Telemetry")
    
    crop_type = st.selectbox("Target Crop Culture Asset", list(CROP_IMAGES.keys()))
    moisture_pct = st.slider("Current Soil Moisture Level (%)", 10, 100, 35)
    temp_c = st.slider("Field Ambient Temperature (°C)", 10, 50, 38)
    humidity_pct = st.slider("Atmospheric Humidity Ratio (%)", 10, 100, 40)
    weather_forecast = st.radio(
        "Imminent Weather Forecast (24H)",
        ["Sunny / Clear Sky", "Overcast / High Humidity", "Heavy Rain Expected", "Scattered Showers"]
    )
    
    execute_btn = st.button("🚀 Evaluate & Compute System Logic")

with col_output:
    st.markdown("### 📊 Automated Operations & Agronomist Logs")
    
    if execute_btn:
        if not groq_api_key:
            st.warning("⚠️ Setup Error: Please provide a valid Groq API Key in the sidebar.")
        else:
            with st.spinner("Analyzing telemetry profiles and rendering visual grids..."):
                # 1. Compute empirical values
                valve_status, deficit_pct, water_volume = calculate_irrigation_needs(
                    crop_type, moisture_pct, temp_c, humidity_pct
                )
                
                # Display structural metric cards
                metric_col1, metric_col2 = st.columns(2)
                with metric_col1:
                    st.metric(label="Calculated Moisture Deficit", value=f"{deficit_pct}%")
                with metric_col2:
                    st.metric(label="Volumetric Water Dosage", value=f"{water_volume} L/m²")
                
                st.info(f"**System Automation Log:** {valve_status}")
                
                # 2. Dynamic Output Image Injection
                st.markdown("#### 📸 Telemetry-Matched Action Imagery")
                selected_media = CROP_IMAGES[crop_type]
                st.image(selected_media["url"], caption=selected_media["caption"], use_column_width=True)
                
                # 3. Invoke LLM reasoning track layer
                try:
                    llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama-3.3-70b-versatile", temperature=0.1)
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
                    st.markdown("### 📋 Agronomic Assessment Strategy")
                    st.write(response.content)
                except Exception as e:
                    st.error(f"❌ AI Inference Failure: {str(e)}")
    else:
        # Default starting visual output
        st.info("Awaiting telemetry evaluation command. Configure parameters on the left and click 'Evaluate' to boot calculations.")
st.image("https://i.postimg.cc/CLyj6Nhr/Gemini-Generated-Image-o59yqgo59yqgo59y.png", caption="Lead Engineer: Sajid Ali — Precision Field Deployment", use_column_width=True)
