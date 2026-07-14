"""
APEX-I HydroCognitive Interface
Systems Engineering UI/UX Design Console

Lead Systems Engineer: Engineer Sajid Ali

This application serves as an educational and prototyping platform for developing 
user-friendly interfaces in precision agriculture. It integrates live GitHub API 
querying to discover existing open-source solutions alongside interactive UI/UX prototyping tools.
"""

import streamlit as st
import requests

# =====================================================================
# SYSTEM CONFIGURATION & UI STYLING
# =====================================================================
st.set_page_config(
    page_title="APEX-I HydroCognitive Interface",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Obsidian Slate UI styling
st.markdown("""
    <style>
    .stApp {
        background-color: #0A0F1D;
        color: #E2E8F0;
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
        font-size: 2.3rem;
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

    /* Glassmorphic Cards */
    .feature-card {
        background: rgba(20, 30, 55, 0.65);
        border: 1px solid rgba(5, 178, 146, 0.2);
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 15px;
    }
    
    /* Interactive Button Customization */
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
# GITHUB SEARCH UTILITY FUNCTION
# =====================================================================
def query_github_repositories(keyword):
    """
    Queries the GitHub API to find relevant open-source repositories 
    based on agricultural keywords or topics.
    """
    url = f"https://api.github.com/search/repositories?q={keyword}&sort=stars&order=desc"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json().get("items", [])[:5]  # Return top 5 matches
    except Exception:
        pass
    return []

# =====================================================================
# MAIN HEADER WITH NEW PROFESSIONAL TITLE & ENGINEER SIGNATURE
# =====================================================================
st.markdown("""
    <div class="ux-header">
        <div class="header-main-title">🌾 APEX-I HYDROCOGNITIVE INTERFACE</div>
        <div class="system-status-sub">Advanced Interaction Prototyper & Open-Source Discovery Console</div>
        <div class="engineer-badge">💻 Lead Engineer: Sajid Ali, System lead</div>
    </div>
""", unsafe_allow_html=True)

# =====================================================================
# DUAL PANEL LAYOUT
# =====================================================================
col_left, col_right = st.columns([5, 5], gap="large")

with col_left:
    st.markdown("### 🔍 Live GitHub Discovery Engine")
    st.write("Scan GitHub for real-world projects and associated technologies.")
    
    # Pre-defined keyword scan buttons
    search_keywords = ["AI irrigation system", "smart irrigation", "automated irrigation", "precision irrigation"]
    selected_keyword = st.selectbox("Select Core Search Phrase", search_keywords)
    
    custom_search = st.text_input("Or write a custom keyword/topic (e.g., 'smart-irrigation'):")
    query_term = custom_search if custom_search else selected_keyword
    
    if st.button("🔎 Scan GitHub Repositories"):
        with st.spinner(f"Querying GitHub for '{query_term}'..."):
            repos = query_github_repositories(query_term)
            
            if repos:
                st.success(f"Successfully retrieved top open-source projects for '{query_term}':")
                for repo in repos:
                    st.markdown(f"""
                    <div class="feature-card">
                        <h4 style='color: #00F2FE; margin-bottom: 5px;'>🔗 <a href="{repo['html_url']}" target="_blank" style='color: #00F2FE; text-decoration: none;'>{repo['full_name']}</a></h4>
                        <p style='font-size: 0.9rem; margin-bottom: 8px;'>{repo['description'] or 'No description provided.'}</p>
                        <span style='background-color: #05B292; color: #0A0F1D; padding: 3px 8px; border-radius: 12px; font-size: 0.8rem; font-weight: bold;'>⭐ {repo['stargazers_count']} Stars</span>
                        <span style='background-color: #00F2FE; color: #0A0F1D; padding: 3px 8px; border-radius: 12px; font-size: 0.8rem; font-weight: bold; margin-left: 5px;'>🍴 {repo['forks_count']} Forks</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.error("No repositories found or GitHub API limit reached. Try again later.")

with col_right:
    st.markdown("### 🖥️ Interactive UX Prototyper")
    st.write("Configure and preview user-friendly controls designed for system management.")
    
    # 1. Soil Moisture Sensing UI Prototype
    with st.expander("🌱 1. Soil Moisture Sensing Interface"):
        st.caption("How to present real-time soil moisture to a non-technical farmer:")
        moisture_val = st.slider("Simulate Raw Sensor Reading (%)", 0, 100, 38)
        if moisture_val < 40:
            st.error(f"🔴 Current Status: Critical Deficit ({moisture_val}%). High contrast red alerts help users identify immediately.")
        elif moisture_val > 80:
            st.warning(f"🟡 Current Status: Wet Saturated ({moisture_val}%). Yellow indicators denote potential waterlogging risks.")
        else:
            st.success(f"🟢 Current Status: Optimal Zone ({moisture_val}%). Clean green values confirm stable operation.")

    # 2. Weather Forecast Integration UI Prototype
    with st.expander("🌤️ 2. Weather Forecast Integration"):
        st.caption("Designing responsive UI elements based on atmospheric conditions:")
        forecast = st.selectbox("Select Forecast Option", ["Sunny & Dry", "Heavy Storm Imminent", "Mild Overcast"])
        if forecast == "Heavy Storm Imminent":
            st.info("🌧️ UI Strategy: The system displays a clear recommendation to bypass next cycle to conserve resources.")
        else:
            st.info("☀️ UI Strategy: Display simple, bright sunshine icons to indicate upcoming default schedule execution.")

    # 3. Machine Learning (ML) Optimization UI Prototype
    with st.expander("🧠 3. Machine Learning (ML) Optimization"):
        st.caption("Explaining complex ML predictive logic cleanly to users:")
        enable_ml = st.checkbox("Enable Automated ML Optimization Cycles")
        if enable_ml:
            st.code("ML Model: Active Random Forest Regressor\nStrategy: Scaling back flow volume by 12% to compensate for high humidity.", language="text")
        else:
            st.text("System is operating on a standard fixed-interval rules database.")

    # 4. Remote Monitoring & Control UI Prototype
    with st.expander("📱 4. Remote Monitoring & Control"):
        st.caption("Designing visual feedback switches that mirror physical states:")
        mcu_status = st.selectbox("Active Device Connection", ["Online - ESP32 Gateway", "Offline - NodeMCU ESP8266"])
        if mcu_status == "Online - ESP32 Gateway":
            st.success("● Network Connection Latency: 42ms (Highly Responsive)")
        else:
            st.error("❌ Connection Dropped. Presenting manual offline diagnostic buttons.")

    # 5. Automation and Control UI Prototype
    with st.expander("🔌 5. Automation and Control Actuators"):
        st.caption("Safe UI execution models for high-pressure hardware triggers:")
        st.warning("Critical Hardware Actions require explicit manual confirmations to prevent pipeline damage.")
        bypass_lock = st.toggle("Unlock Physical Override Commands")
        if bypass_lock:
            st.button("⚠️ Force Solenoid Valve Open")
