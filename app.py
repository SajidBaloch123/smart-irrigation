"""
AI-Powered Smart Irrigation Assistant
Unified Hydro-AI Control Room & Chatbot

Lead Systems Engineer: Engineer Sajid Ali
"""

import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# =====================================================================
# SYSTEM CONFIGURATION & UI STYLING
# =====================================================================
st.set_page_config(
    page_title="AI-Powered Smart Irrigation Assistant",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Obsidian Slate UI styling
st.markdown("""
    <style>
    .stApp {
        background-color: #0A0F1D;
        color: #FFFFFF;
    }
    .block-container { padding-top: 1.5rem; }
    
    /* Premium Title Card */
    .ux-header {
        background: linear-gradient(135deg, rgba(20, 35, 60, 0.95) 0%, rgba(10, 20, 40, 0.95) 100%);
        border-radius: 12px;
        padding: 25px;
        border: 1px solid rgba(0, 242, 254, 0.3);
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 8px 32px 0 rgba(0, 242, 254, 0.15);
    }
    .header-main-title {
        color: #00F2FE;
        font-size: 2.5rem;
        font-weight: 900;
        letter-spacing: 2px;
        text-shadow: 0 0 15px rgba(0,242,254,0.4);
    }
    .system-status-sub {
        color: #05B292;
        font-size: 1.1rem;
        font-weight: 700;
        margin-top: 5px;
        letter-spacing: 1px;
    }
    .engineer-badge {
        background: rgba(5, 178, 146, 0.15);
        color: #00F2FE;
        padding: 6px 20px;
        border-radius: 20px;
        font-weight: 800;
        display: inline-block;
        font-size: 0.95rem;
        border: 1px solid #05B292;
        margin-top: 12px;
        box-shadow: 0 0 15px rgba(5, 178, 146, 0.2);
    }

    /* Interactive Sidebar Widgets */
    .sidebar-widget {
        background: rgba(20, 30, 55, 0.6);
        border: 1px solid rgba(5, 178, 146, 0.2);
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
    }

    /* Custom styles for chat messages to fit the dark theme */
    .stChatMessage {
        background-color: rgba(20, 30, 55, 0.6) !important;
        border: 1px solid rgba(5, 178, 146, 0.15) !important;
        border-radius: 10px !important;
        margin-bottom: 10px !important;
    }

    /* FORCE ALL RESULT WORDING & CHAT TEXT TO BE WHITE (INSTEAD OF SILVER) */
    .stChatMessage p, 
    .stChatMessage li, 
    .stChatMessage h1, 
    .stChatMessage h2, 
    .stChatMessage h3, 
    .stChatMessage h4, 
    .stChatMessage code,
    .stChatMessage span {
        color: #FFFFFF !important;
    }

    /* Force input fields to have black text on white backgrounds */
    div[data-testid="stTextInput"] input {
        color: #000000 !important;
        background-color: #FFFFFF !important;
    }
    div[data-testid="stChatInput"] textarea {
        color: #000000 !important;
        background-color: #FFFFFF !important;
    }
    /* Style placeholder text for input fields */
    div[data-testid="stTextInput"] input::placeholder {
        color: #555555 !important;
    }
    div[data-testid="stChatInput"] textarea::placeholder {
        color: #555555 !important;
    }
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# MAIN HEADER WITH PROFESSIONAL TITLE & ENGINEER SIGNATURE
# =====================================================================
st.markdown("""
    <div class="ux-header">
        <div class="header-main-title">🌾 AI-POWERED SMART IRRIGATION ASSISTANT</div>
        <div class="system-status-sub">Smart Irrigation Conversational Assistant & Interface Prototyper</div>
        <div class="engineer-badge">💻 Lead Engineer: Sajid Ali, System lead</div>
    </div>
""", unsafe_allow_html=True)

# =====================================================================
# SIDEBAR CONTROL DESK
# =====================================================================
st.sidebar.markdown("### 🔑 Gateway Authorization")
groq_api_key = st.sidebar.text_input("Groq Cloud API Key", type="password", placeholder="gsk_...")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🏷️ Quick Topic Presets")
st.sidebar.write("Clicking these will clear current history and start a focused topic discussion.")

# Quick buttons to automatically seed chats about the 5 major topics
if st.sidebar.button("🌱 Soil Moisture Sensing"):
    st.session_state.messages = [
        {"role": "assistant", "content": "Let's discuss **Soil Moisture Sensing**. I can explain how FDR/TDR capacitive sensors measure relative permittivity and volumetric water content to prevent under-watering."}
    ]
if st.sidebar.button("🌤️ Weather Forecast Integration"):
    st.session_state.messages = [
        {"role": "assistant", "content": "Let's discuss **Weather Forecast Integration**. Ask me how our system uses local predictive parameters (like impending heavy storms) to postpone irrigation cycles and save water."}
    ]
if st.sidebar.button("🧠 ML Optimization"):
    st.session_state.messages = [
        {"role": "assistant", "content": "Let's discuss **Machine Learning Optimization**. I can explain how we use regression modeling to adjust crop water dosage based on ambient humidity and temperature evaporation indexes."}
    ]
if st.sidebar.button("📱 Remote Monitoring & Control"):
    st.session_state.messages = [
        {"role": "assistant", "content": "Let's discuss **Remote Monitoring & Control**. Ask me how web dashboards act as cyber-physical twins for ESP32 and Raspberry Pi hardware gateways."}
    ]
if st.sidebar.button("🔌 Automation and Control Actuators"):
    st.session_state.messages = [
        {"role": "assistant", "content": "Let's discuss **Automation & Control Actuators**. Ask me about the mechanics of 12V solenoid flow-control valves, pump relay triggers, and automated safety overrides."}
    ]

# Clear history button
st.sidebar.markdown("---")
if st.sidebar.button("🗑️ Clear Chat History"):
    st.session_state.messages = []

# =====================================================================
# DUAL DASHBOARD GRID
# =====================================================================
col_left_panel, col_right_chat = st.columns([4, 6], gap="large")

# --- LEFT PANEL: Live Controls & Centralized Keywords ---
with col_left_panel:
    st.markdown("### 📊 Active Control Panel")
    
    # Visual, clean card displaying your centralized keywords beautifully in the middle
    st.markdown("""
        <div style="background: rgba(5, 178, 146, 0.1); border: 1px solid rgba(5, 178, 146, 0.3); border-radius: 10px; padding: 15px; margin-bottom: 20px; text-align: center;">
            <p style="color: #05B292; font-weight: bold; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1px; font-size: 0.9rem;">
                Core Telemetry Framework Topics
            </p>
            <span style="color: #FFFFFF; font-size: 0.95rem; font-weight: bold; display: block; margin: 3px 0;">🌱 Soil Moisture Sensing</span>
            <span style="color: #FFFFFF; font-size: 0.95rem; font-weight: bold; display: block; margin: 3px 0;">🌤️ Weather Forecasting</span>
            <span style="color: #FFFFFF; font-size: 0.95rem; font-weight: bold; display: block; margin: 3px 0;">🧠 Machine Learning Optimization</span>
            <span style="color: #FFFFFF; font-size: 0.95rem; font-weight: bold; display: block; margin: 3px 0;">📱 Remote Monitoring & Control</span>
            <span style="color: #FFFFFF; font-size: 0.95rem; font-weight: bold; display: block; margin: 3px 0;">🔌 Automation and Control Actuators</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("#### ⚡ Real-Time Telemetry Inputs")
    crop_type = st.selectbox("Target Crop System Culture", ["Wheat", "Rice", "Cotton", "Vegetables"])
    moisture_pct = st.slider("Soil Moisture Sensing - Volumetric Content (%)", 10, 100, 35)
    temp_c = st.slider("Microclimate Weather - Local Temperature (°C)", 10, 50, 38)
    humidity_pct = st.slider("Microclimate Weather - Relative Humidity (%)", 10, 100, 40)
    weather_forecast = st.radio("Predictive Weather Forecast Integration (24H)", ["Sunny / Clear", "Overcast", "Heavy Rain", "Scattered Showers"])

# --- RIGHT PANEL: Professional Chatbot Interface & Standby Logo Image ---
with col_right_chat:
    st.markdown("### 💬 System Assistant & Chat Interface")

    # Welcome card featuring your standing image (The Logo / Standby Image)
    welcome_html = f"""
    <div style="text-align: center; padding: 10px;">
        <h3 style="color: #00F2FE; margin-bottom: 5px;">APEX HYDRO-AI Systems Active</h3>
        <p style="color: #FFFFFF; font-size: 1rem; margin-bottom: 15px;">
            Interactive Systems Engineering Control Room & Conversational Companion.
        </p>
    </div>
    """

    # Initialize session state for holding messages if empty
    if "messages" not in st.session_state or len(st.session_state.messages) == 0:
        st.session_state.messages = [
            {
                "role": "assistant", 
                "content": welcome_html,
                "show_logo": True  # Flag to render the field photo standby logo
            }
        ]

    # Display all messages in history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"], unsafe_allow_html=True)
            # If this is the starting message, load your standing field image right below it!
            if msg.get("show_logo"):
                st.image(
                    "https://i.postimg.cc/CLyj6Nhr/Gemini-Generated-Image-o59yqgo59yqgo59y.png", 
                    caption="Lead Engineer: Sajid Ali — Precision Field Deployment Node", 
                    use_column_width=True
                )

    # Accept user chat input
    user_input = st.chat_input("Type your smart irrigation query here...")

    if user_input:
        # 1. Display user's message in the thread
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # 2. Generate and display assistant's response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            # Scenario A: User has provided a valid Groq API key
            if groq_api_key:
                try:
                    with st.spinner("Analyzing telemetry query and drafting response..."):
                        llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama-3.1-8b-instant", temperature=0.2)
                        
                        # Package the chat history into a structured format
                        history_str = ""
                        for msg in st.session_state.messages[:-1]:  # Exclude the latest user message
                            history_str += f"{msg['role'].capitalize()}: {msg['content']}\n"
                            
                        prompt = ChatPromptTemplate.from_template("""
                        You are the AI-Powered Smart Irrigation Assistant Chatbot, an advanced agronomic AI assistant integrated into a Smart Irrigation Control Room.
                        The system is designed by Lead Systems Engineer Sajid Ali.
                        
                        Answer the user's query professionally, drawing on systems engineering, IoT, microcontrollers, and agronomy. Keep answers concise, highly structured, and directly related to smart farming automation.
                        
                        Recent conversation history:
                        {history_str}
                        
                        User query: {user_input}
                        """)
                        
                        chain = prompt | llm
                        response = chain.invoke({"history_str": history_str, "user_input": user_input})
                        assistant_response = response.content
                        message_placeholder.markdown(assistant_response)
                except Exception as e:
                    assistant_response = f"⚠️ **AI Core Error:** I encountered an issue processing your request: `{str(e)}`. Please check your API key configuration."
                    message_placeholder.markdown(assistant_response)
                    
            # Scenario B: No API key (Runs a smart agricultural simulator response)
            else:
                with st.spinner("Processing telemetry database simulations..."):
                    query_lower = user_input.lower()
                    
                    # Intelligent keyword mapping fallback
                    if "moisture" in query_lower or "sensor" in query_lower or "soil" in query_lower:
                        assistant_response = (
                            "### 📡 Capacitive Soil Moisture Sensing Insight\n"
                            "Our system utilizes **Frequency Domain Reflectometry (FDR)** sensors. "
                            "Unlike traditional resistive sensors which corrode quickly, FDR probes measure the "
                            "dielectric permittivity of the surrounding soil to determine its precise Volumetric Water Content (VWC).\n\n"
                            "**Standard Configuration:**\n"
                            "* **Calibration High (100% water):** ~450mV sensor output\n"
                            "* **Calibration Low (Dry Air):** ~820mV sensor output\n\n"
                            "To integrate this live with hardware, we route the sensor's analog output pin to an ADC channel on your ESP32 board."
                        )
                    elif "weather" in query_lower or "forecast" in query_lower or "rain" in query_lower:
                        assistant_response = (
                            "### 🌤️ Weather Forecast Integration Dynamics\n"
                            "This dashboard simulates automated integration with weather API endpoints. "
                            "By analyzing upcoming atmospheric pressure declines and relative humidity metrics, "
                            "the system predicts impending precipitation.\n\n"
                            "**Automation Protocol:**\n"
                            "If the 24-hour weather prediction forecasts **heavy rain (>70% probability)**, "
                            "the controller initiates an **Automation Override**, locking out scheduled solenoid triggers to save resources and prevent root rot."
                        )
                    elif "machine" in query_lower or "ml" in query_lower or "optimization" in query_lower:
                        assistant_response = (
                            "### 🧠 Machine Learning Evaporative Scaling\n"
                            "We employ linear and regression analytics models to optimize water deployment schedules. "
                            "Standard irrigation algorithms use static thresholds, which cause water waste. "
                            "Our ML engine adjusts the target watering volume dynamically using current atmospheric data.\n\n"
                            "**ML Rule Example:**\n"
                            "Target Volume Adjustment = V * (1 + Evaporation Scaling Factor)\n"
                            "When ambient temperature exceeds 35°C with low relative humidity, the algorithm increases flow by 15% to mitigate direct evaporation losses."
                        )
                    elif "remote" in query_lower or "monitoring" in query_lower or "control" in query_lower:
                        assistant_response = (
                            "### 📱 Remote Monitoring Architecture (Cyber-Physical Twin)\n"
                            "The interface acts as a remote dashboard. Telemetry is transmitted "
                            "from edge devices via **MQTT (Message Queuing Telemetry Transport)** or RESTful API protocols.\n\n"
                            "**Connection Framework:**\n"
                            "1. **ESP32 Node** collects sensor data.\n"
                            "2. Payload is formatted in JSON and pushed to the cloud broker.\n"
                            "3. This Streamlit dashboard pulls and displays active sensor logs, keeping users updated in real-time."
                        )
                    elif "actuator" in query_lower or "valve" in query_lower or "pump" in query_lower:
                        assistant_response = (
                            "### 🔌 Automation Actuator & Override Control\n"
                            "The console is engineered to send digital high/low signals to electronic switches.\n\n"
                            "**Actuator Loop Flow:**\n"
                            "* **Trigger Condition:** Soil Moisture < Threshold (40%)\n"
                            "* **Command Sent:** GPIO digital HIGH pin write (relay closed)\n"
                            "* **Actuator Response:** **12V Solenoid Valve** opens, allowing hydraulic flow.\n\n"
                            "The system also features physical bypass toggles on the sidebar so operators can force valves open/closed instantly during maintenance."
                        )
                    else:
                        # Generic response guiding the user to topics
                        assistant_response = (
                            "I am ready to discuss any aspects of our precision irrigation framework! "
                            "Please ask me a question about **Soil Moisture Probes**, **Weather API Delays**, **ML Water Scaling**, "
                            "**Remote Web Interfaces**, or **Solenoid Relay Valves**.\n\n"
                            "*(To unlock the fully conversational, custom AI assistant, simply enter your Groq Cloud API key in the sidebar dashboard!)*"
                        )
                        
                    # Display response
                    message_placeholder.markdown(assistant_response)
                    
            # Save the assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
