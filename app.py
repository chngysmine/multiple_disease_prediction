import streamlit as st
import pickle
import os
from streamlit_option_menu import option_menu
from typing import Dict, Tuple, List
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

st.set_page_config(
    page_title="Virtual Health Assistant",
    layout="wide",
    page_icon="🏥",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
    * {
        margin: 0;
        padding: 0;
    }
    
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f1419 0%, #1a1f2e 100%);
        color: #e0e0e0;
    }
    
    /* Professional sidebar styling - Instagram/Facebook style */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1f2e 0%, #0f1419 100%);
        border-right: 1px solid rgba(0, 200, 200, 0.1);
        height: 100vh;
        overflow: hidden !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        gap: 0 !important;
        overflow: hidden !important;
    }
    
    /* Optimize sidebar spacing - remove all padding */
    [data-testid="stSidebar"] > div {
        padding: 0 !important;
        overflow: hidden !important;
        height: 100vh;
        display: flex;
        flex-direction: column;
    }
    
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div {
        overflow: visible !important;
    }
    
    /* Ensure proper flexbox layout for sidebar content */
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        display: flex;
        flex-direction: column;
        height: 100%;
        max-height: 100vh;
        overflow: hidden;
    }
    
    /* Make option menu more compact */
    .css-1d391kg {
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* Hide option menu title/icon if empty */
    .css-1d391kg > div:first-child {
        display: none !important;
    }
    
    /* Remove any inner card/wrapper backgrounds in sidebar */
    [data-testid="stSidebar"] section,
    [data-testid="stSidebar"] .block-container,
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div {
        background: transparent !important;
        box-shadow: none !important;
        border: none !important;
    }
    
    /* Custom scrollbar for navigation if needed */
    .sidebar-nav-container::-webkit-scrollbar {
        width: 4px;
    }
    
    .sidebar-nav-container::-webkit-scrollbar-track {
        background: transparent;
    }
    
    .sidebar-nav-container::-webkit-scrollbar-thumb {
        background: rgba(0, 200, 200, 0.3);
        border-radius: 2px;
    }
    
    .sidebar-nav-container::-webkit-scrollbar-thumb:hover {
        background: rgba(0, 200, 200, 0.5);
    }
    
    .main {
        background: linear-gradient(135deg, #0f1419 0%, #1a1f2e 100%);
        margin-left: 0;
    }
    
    /* Professional header styling - better spacing */
    .sidebar-header {
        background: transparent;
        border-bottom: none;
        padding: 16px 12px;
        text-align: center;
        margin: 0;
        flex-shrink: 0;
    }
    
    .sidebar-header h2 {
        color: #00c8c8;
        margin: 0;
        font-size: 24px;
        font-weight: 700;
        line-height: 1.3;
        margin-bottom: 4px;
    }
    
    .sidebar-header p {
        color: #aaa;
        font-size: 10px;
        margin: 4px 0 0 0;
        font-weight: 400;
        line-height: 1.4;
    }
    
    /* Stat boxes with comfortable spacing */
    .sidebar-stats-container {
        padding: 12px 10px;
        flex-shrink: 0;
    }
    
    /* Better column spacing in stats grid */
    .sidebar-stats-container [data-testid="column"] {
        padding: 0 4px !important;
        margin-bottom: 4px;
    }
    
    /* General sidebar column spacing */
    [data-testid="stSidebar"] [data-testid="column"] {
        padding: 0 4px !important;
    }
    
    /* Ensure proper spacing between stat rows */
    .sidebar-stats-container [data-testid="column"]:first-child,
    .sidebar-stats-container [data-testid="column"]:last-child {
        padding: 0 4px !important;
    }
    
    .sidebar-stat {
        background: linear-gradient(135deg, rgba(0, 200, 200, 0.08) 0%, rgba(0, 150, 150, 0.04) 100%);
        border: 1px solid rgba(0, 200, 200, 0.15);
        border-radius: 8px;
        padding: 12px 8px;
        text-align: center;
        margin: 5px 0;
        height: 100%;
        min-height: 60px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .sidebar-stat h4 {
        color: #aaa;
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin: 0 0 6px 0;
        line-height: 1.3;
    }
    
    .sidebar-stat .value {
        color: #00c8c8;
        font-size: 20px;
        font-weight: 700;
        line-height: 1.2;
    }
    
    /* Better divider spacing */
    .sidebar-divider {
        border-top: 1px solid rgba(0, 200, 200, 0.1);
        margin: 10px 10px;
        flex-shrink: 0;
    }
    
    /* Navigation container with better spacing */
    .sidebar-nav-container {
        flex: 1;
        overflow-y: auto;
        overflow-x: hidden;
        padding: 8px 6px;
    }
    
    /* Recent activity section with comfortable spacing */
    .recent-activity-section {
        padding: 12px 10px;
        flex-shrink: 0;
        border-top: 1px solid rgba(0, 200, 200, 0.1);
        margin-top: auto;
    }
    
    .recent-activity {
        background: rgba(0, 200, 200, 0.05);
        border-left: 2px solid rgba(0, 200, 200, 0.3);
        padding: 8px 10px;
        margin: 6px 0;
        border-radius: 6px;
        font-size: 11px;
        color: #aaa;
        line-height: 1.5;
    }
    
    .recent-activity .disease {
        color: #00c8c8;
        font-weight: 600;
        font-size: 11px;
        margin-bottom: 2px;
    }
    
    .recent-activity .risk {
        font-size: 10px;
        color: #f59f00;
    }
    
    .recent-activity-label {
        color: #aaa;
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin: 0 0 8px 0;
        font-weight: 600;
    }
    
    /* Animated gradient backgrounds */
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    /* Risk level badges with animations */
    .risk-low {
        background: linear-gradient(135deg, rgba(18, 184, 134, 0.15) 0%, rgba(18, 184, 134, 0.05) 100%);
        border-left: 4px solid #12b886;
        border-radius: 12px;
        padding: 20px;
        margin: 16px 0;
        color: #12b886;
        font-weight: 600;
        animation: slideIn 0.5s ease-out;
        box-shadow: 0 4px 12px rgba(18, 184, 134, 0.1);
    }
    
    .risk-mid {
        background: linear-gradient(135deg, rgba(245, 159, 0, 0.15) 0%, rgba(245, 159, 0, 0.05) 100%);
        border-left: 4px solid #f59f00;
        border-radius: 12px;
        padding: 20px;
        margin: 16px 0;
        color: #f59f00;
        font-weight: 600;
        animation: slideIn 0.5s ease-out;
        box-shadow: 0 4px 12px rgba(245, 159, 0, 0.1);
    }
    
    .risk-high {
        background: linear-gradient(135deg, rgba(224, 49, 49, 0.15) 0%, rgba(224, 49, 49, 0.05) 100%);
        border-left: 4px solid #e03131;
        border-radius: 12px;
        padding: 20px;
        margin: 16px 0;
        color: #e03131;
        font-weight: 600;
        animation: slideIn 0.5s ease-out;
        box-shadow: 0 4px 12px rgba(224, 49, 49, 0.1);
    }
    
    /* Enhanced metric cards */
    .metric-card {
        background: linear-gradient(135deg, rgba(0, 200, 200, 0.12) 0%, rgba(0, 150, 150, 0.06) 100%);
        border: 2px solid rgba(0, 200, 200, 0.25);
        border-radius: 16px;
        padding: 28px;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        animation: slideIn 0.6s ease-out;
    }
    
    .metric-card:hover {
        border-color: rgba(0, 200, 200, 0.5);
        background: linear-gradient(135deg, rgba(0, 200, 200, 0.18) 0%, rgba(0, 150, 150, 0.12) 100%);
        transform: translateY(-8px);
        box-shadow: 0 12px 32px rgba(0, 200, 200, 0.2);
    }
    
    .metric-card h3 {
        color: #00c8c8;
        margin-top: 16px;
        font-size: 26px;
        font-weight: 700;
    }
    
    .metric-card p {
        color: #a0a0a0;
        font-size: 14px;
        margin-top: 10px;
        line-height: 1.5;
    }
    
    /* Welcome banner */
    .welcome-banner {
        background: linear-gradient(135deg, #00c8c8 0%, #0099cc 100%);
        border-radius: 16px;
        padding: 40px;
        margin-bottom: 32px;
        color: white;
        box-shadow: 0 8px 32px rgba(0, 200, 200, 0.3);
        animation: slideIn 0.7s ease-out;
    }
    
    .welcome-banner h1 {
        font-size: 36px;
        margin-bottom: 12px;
        font-weight: 800;
    }
    
    .welcome-banner p {
        font-size: 16px;
        opacity: 0.95;
        line-height: 1.6;
    }
    
    /* Input styling */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {
        background-color: #1a1f2e !important;
        border: 2px solid rgba(0, 200, 200, 0.2) !important;
        color: #e0e0e0 !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #00c8c8 !important;
        box-shadow: 0 0 0 3px rgba(0, 200, 200, 0.15) !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #00c8c8 0%, #0099cc 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 14px 32px;
        font-weight: 700;
        font-size: 16px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 24px rgba(0, 200, 200, 0.4);
    }
    
    .stButton > button:active {
        transform: translateY(-1px);
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        border-bottom: 2px solid rgba(0, 200, 200, 0.1);
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(0, 200, 200, 0.05);
        border-radius: 10px;
        color: #a0a0a0;
        padding: 12px 20px;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: rgba(0, 200, 200, 0.25);
        color: #00c8c8;
        font-weight: 600;
    }
    
    /* Section headers */
    .section-header {
        color: #00c8c8;
        font-size: 28px;
        font-weight: 800;
        margin-top: 40px;
        margin-bottom: 24px;
        border-bottom: 3px solid rgba(0, 200, 200, 0.3);
        padding-bottom: 16px;
        animation: slideIn 0.6s ease-out;
    }
    
    /* Recommendation box */
    .recommendation-box {
        background: linear-gradient(135deg, rgba(0, 200, 200, 0.08) 0%, rgba(0, 150, 150, 0.04) 100%);
        border: 2px solid rgba(0, 200, 200, 0.2);
        border-radius: 12px;
        padding: 20px;
        margin: 16px 0;
        line-height: 1.8;
        color: #e0e0e0;
        animation: slideIn 0.5s ease-out;
    }
    
    .success-message {
        background: linear-gradient(135deg, rgba(18, 184, 134, 0.15) 0%, rgba(18, 184, 134, 0.05) 100%);
        border-left: 4px solid #12b886;
        color: #12b886;
        padding: 20px;
        border-radius: 12px;
        margin: 20px 0;
        font-weight: 600;
        animation: slideIn 0.5s ease-out;
    }
    
    .warning-message {
        background: linear-gradient(135deg, rgba(224, 49, 49, 0.15) 0%, rgba(224, 49, 49, 0.05) 100%);
        border-left: 4px solid #e03131;
        color: #e03131;
        padding: 20px;
        border-radius: 12px;
        margin: 20px 0;
        font-weight: 600;
        animation: slideIn 0.5s ease-out;
    }
    
    /* Achievement badge */
    .achievement-badge {
        background: linear-gradient(135deg, rgba(255, 193, 7, 0.15) 0%, rgba(255, 152, 0, 0.05) 100%);
        border: 2px solid rgba(255, 193, 7, 0.3);
        border-radius: 12px;
        padding: 16px;
        margin: 12px 0;
        text-align: center;
        color: #ffc107;
        font-weight: 600;
        animation: slideIn 0.5s ease-out;
    }
    
    /* Progress bar */
    .progress-container {
        background-color: rgba(0, 200, 200, 0.1);
        border-radius: 10px;
        height: 12px;
        overflow: hidden;
        margin: 12px 0;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #00c8c8 0%, #0099cc 100%);
        height: 100%;
        border-radius: 10px;
        transition: width 0.5s ease;
    }
    
    /* Info card */
    .info-card {
        background: linear-gradient(135deg, rgba(0, 200, 200, 0.1) 0%, rgba(0, 150, 150, 0.05) 100%);
        border: 1px solid rgba(0, 200, 200, 0.2);
        border-radius: 12px;
        padding: 20px;
        margin: 16px 0;
        line-height: 1.7;
    }
    
    .stat-box {
        background: linear-gradient(135deg, rgba(0, 200, 200, 0.12) 0%, rgba(0, 150, 150, 0.06) 100%);
        border: 2px solid rgba(0, 200, 200, 0.2);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin: 12px 0;
    }
    
    .stat-box h4 {
        color: #a0a0a0;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
    
    .stat-box .value {
        color: #00c8c8;
        font-size: 32px;
        font-weight: 800;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

working_dir = os.path.dirname(os.path.abspath(__file__))

# Load models
diabetes_model = pickle.load(open(f'{working_dir}/saved_models/diabetes.pkl','rb'))
heart_disease_model = pickle.load(open(f'{working_dir}/saved_models/heart.pkl','rb'))
kidney_disease_model = pickle.load(open(f'{working_dir}/saved_models/kidney.pkl','rb'))

if 'user_predictions' not in st.session_state:
    st.session_state.user_predictions = []
if 'achievements' not in st.session_state:
    st.session_state.achievements = []
if 'health_streak' not in st.session_state:
    st.session_state.health_streak = 0
if 'points' not in st.session_state:
    st.session_state.points = 0

def get_recommendations() -> Dict[str, Dict[str, Dict[str, str]]]:
    """Comprehensive recommendation bank by disease and severity level."""
    return {
        "diabetes": {
            "Low": {
                "diet": "🥗 **Maintain a Balanced Diet**: Focus on whole grains, lean proteins, and plenty of vegetables. Limit sugary drinks and processed foods. Include healthy fats from nuts, seeds, and olive oil. Eat regular meals at consistent times to maintain stable blood sugar levels.",
                "habits": "🚶 **Stay Active**: Aim for 150 minutes of moderate exercise per week (brisk walking, cycling, swimming). Include strength training 2-3 times weekly. Maintain a healthy weight (BMI 18.5-24.9). Get 7-8 hours of quality sleep. Manage stress through meditation or yoga.",
                "when_sick": "😷 **If You Feel Unwell**: Rest and stay hydrated. Monitor your blood sugar if you have a meter. Eat light, nutritious meals. If symptoms persist beyond 3 days or worsen, contact your healthcare provider.",
                "monitoring": "📊 **Regular Check-ups**: Schedule health screenings every 6-12 months. Monitor blood sugar levels if recommended. Keep a health journal to track patterns. Maintain regular contact with your healthcare provider.",
            },
            "Medium": {
                "diet": "🥗 **Controlled Carbohydrate Intake**: Choose low-glycemic index foods. Eat 5-6 small meals daily instead of 3 large ones. Include lean proteins at each meal. Limit refined carbohydrates and sugary foods. Drink plenty of water (2-3 liters daily).",
                "habits": "💪 **Structured Exercise Program**: Engage in 30-45 minutes of moderate activity daily. Include both cardio and resistance training. Monitor your weight weekly. Aim for gradual weight loss if overweight (5-10% reduction). Avoid smoking and limit alcohol.",
                "when_sick": "😷 **Managing Symptoms**: If experiencing dizziness or shakiness, consume 15g of fast-acting carbs (banana, juice). Rest and monitor symptoms. Contact your doctor if symptoms persist for more than 2 hours or worsen.",
                "monitoring": "📊 **Frequent Monitoring**: Check blood sugar 1-2 times weekly (fasting and 2 hours after meals). Get HbA1c tested every 3 months. Schedule regular eye and foot exams. Maintain a detailed health log.",
            },
            "High": {
                "diet": "🥗 **Strict Dietary Management**: Work with a nutritionist for personalized meal planning. Carefully count carbohydrates at each meal. Avoid all sugary beverages and processed foods. Eat consistent portions at regular times. Focus on high-fiber foods and lean proteins.",
                "habits": "💪 **Intensive Lifestyle Modification**: Exercise under medical supervision. Aim for 30-60 minutes of activity daily. Target 5-10% weight loss if overweight. Strictly avoid tobacco and alcohol. Practice stress management daily.",
                "when_sick": "😷 **Emergency Preparedness**: Always carry fast-acting carbs and identification. If experiencing severe symptoms (confusion, loss of consciousness), seek emergency care immediately. Keep emergency contacts readily available.",
                "monitoring": "📊 **Daily Monitoring**: Check blood sugar 3-4 times daily. Take medications exactly as prescribed. Attend all scheduled appointments. Get HbA1c tested every 2-3 months. Monitor for complications regularly.",
            },
        },
        "heart": {
            "Low": {
                "diet": "🥗 **Mediterranean Diet**: Emphasize vegetables, fruits, whole grains, and fish. Use olive oil as primary fat source. Include nuts and legumes. Limit salt to less than 5g daily. Eat fish 2-3 times weekly.",
                "habits": "🚶 **Regular Physical Activity**: Aim for 150 minutes of moderate aerobic activity weekly. Include flexibility and balance exercises. Maintain a healthy weight. Get 7-8 hours of sleep. Manage stress through relaxation techniques.",
                "when_sick": "😷 **Chest Discomfort**: If experiencing unusual chest pain, rest immediately. Monitor for 5-10 minutes. If pain persists or spreads, seek medical attention. Keep aspirin available if recommended by your doctor.",
                "monitoring": "📊 **Preventive Care**: Check blood pressure monthly. Get lipid panel annually. Schedule regular heart health check-ups. Maintain a healthy lifestyle. Track cardiovascular risk factors.",
            },
            "Medium": {
                "diet": "🥗 **Heart-Healthy Eating**: Reduce sodium to less than 3g daily. Limit saturated fats. Increase soluble fiber (oats, beans). Eat lean proteins. Avoid processed and fried foods. Stay well-hydrated.",
                "habits": "💪 **Structured Exercise**: 30-45 minutes of moderate activity 5 days weekly. Include resistance training. Maintain ideal weight. Avoid smoking completely. Limit alcohol consumption.",
                "when_sick": "😷 **Chest Pain Management**: Rest immediately and take prescribed medications. If pain is severe or accompanied by shortness of breath, call emergency services. Chew aspirin if instructed.",
                "monitoring": "📊 **Regular Monitoring**: Check blood pressure weekly. Get lipid levels tested every 3 months. Attend all cardiology appointments. Monitor for warning signs. Keep medication records.",
            },
            "High": {
                "diet": "🥗 **Strict Cardiac Diet**: Very low sodium (<2g daily). Minimal saturated fats. High in potassium-rich foods (if approved). Controlled portion sizes. Frequent small meals. Avoid all processed foods.",
                "habits": "💪 **Cardiac Rehabilitation**: Exercise only under medical supervision. Gradual activity increase as approved. Strict medication adherence. Complete stress management program. Avoid strenuous activities.",
                "when_sick": "😷 **Emergency Protocol**: Severe chest pain, shortness of breath, or dizziness requires immediate emergency care (call 911). Keep emergency medications accessible. Wear medical alert identification.",
                "monitoring": "📊 **Intensive Monitoring**: Daily blood pressure checks. Regular hospital visits as scheduled. Strict medication compliance. Continuous symptom monitoring. Prepare for possible interventions.",
            },
        },
        "kidney": {
            "Low": {
                "diet": "💧 **Kidney-Protective Diet**: Drink adequate water (2-3 liters daily). Moderate protein intake. Limit sodium to 5g daily. Avoid excessive potassium and phosphorus. Eat fresh, whole foods.",
                "habits": "🚶 **Healthy Lifestyle**: Regular moderate exercise (30 minutes daily). Maintain healthy weight. Avoid NSAIDs (ibuprofen, aspirin) unless prescribed. Get 7-8 hours of sleep. Manage blood pressure.",
                "when_sick": "😷 **Monitoring Symptoms**: If experiencing swelling, reduced urination, or fatigue, rest and increase water intake. Contact your doctor if symptoms persist beyond 2 days.",
                "monitoring": "📊 **Regular Testing**: Annual kidney function tests (creatinine, eGFR). Monthly blood pressure checks. Urinalysis annually. Maintain healthy lifestyle habits.",
            },
            "Medium": {
                "diet": "💧 **Controlled Protein Diet**: Moderate protein (0.8-1g per kg body weight). Strict sodium restriction (<3g daily). Monitor potassium and phosphorus intake. Limit processed foods. Stay well-hydrated as advised.",
                "habits": "📊 **Active Monitoring**: Daily weight tracking. Moderate exercise (30 minutes, 5 days weekly). Strict blood pressure control. Medication adherence. Avoid smoking and excessive alcohol.",
                "when_sick": "😷 **Symptom Management**: Nausea, reduced urination, or increased swelling requires immediate medical attention. Adjust fluid intake as directed. Contact your nephrologist promptly.",
                "monitoring": "📊 **Frequent Testing**: Kidney function tests every 3-6 months. Weekly blood pressure monitoring. Regular urinalysis. Specialist appointments as scheduled.",
            },
            "High": {
                "diet": "💧 **Strict Renal Diet**: Very low sodium (<2g daily). Controlled protein (0.6-0.8g per kg). Careful potassium and phosphorus management. Fluid restriction as prescribed. Nutritionist-guided meal planning.",
                "habits": "⚠️ **Intensive Management**: Limited physical activity as approved. Strict medication compliance. Daily fluid and intake monitoring. Prepare for possible dialysis. Avoid all NSAIDs.",
                "when_sick": "😷 **Emergency Care**: Severe symptoms (difficulty breathing, severe swelling, chest pain) require immediate hospitalization. Keep emergency contacts available.",
                "monitoring": "📊 **Intensive Monitoring**: Frequent lab tests (2-4 weeks). Regular specialist visits. Continuous symptom tracking. Prepare for renal replacement therapy.",
            },
        },
    }

def get_health_tips() -> List[str]:
    """Collection of evidence-based health tips."""
    return [
        "💡 Drink water first thing in the morning to boost metabolism and hydration.",
        "💡 Take a 10-minute walk after meals to help regulate blood sugar levels.",
        "💡 Practice deep breathing for 5 minutes daily to reduce stress and improve heart health.",
        "💡 Eat a rainbow of vegetables to ensure diverse nutrient intake.",
        "💡 Get 7-8 hours of quality sleep for optimal health and recovery.",
        "💡 Limit screen time 1 hour before bed to improve sleep quality.",
        "💡 Include omega-3 rich foods (fish, flaxseed) for heart and brain health.",
        "💡 Practice portion control by using smaller plates.",
        "💡 Stay socially connected for better mental and physical health.",
        "💡 Regular health check-ups can catch problems early.",
    ]

def check_achievements(disease: str, risk_level: str) -> List[str]:
    """Check and award achievements based on predictions."""
    new_achievements = []
    
    if risk_level == "Low":
        new_achievements.append(f"🏆 Healthy {disease.title()} Score - Keep up the great work!")
    
    if len(st.session_state.user_predictions) >= 5:
        new_achievements.append("🎯 Health Tracker - Completed 5 predictions!")
    
    if len(st.session_state.user_predictions) >= 10:
        new_achievements.append("⭐ Health Champion - Completed 10 predictions!")
    
    return new_achievements

with st.sidebar:
    # Minimal header
    st.markdown("""
    <div class='sidebar-header'>
        <h2>🏥 VHA</h2>
        <p>Virtual Health Assistant</p>
        <p>AI-Powered Predictions</p>
    </div>
    """, unsafe_allow_html=True)

    # Navigation only
    selected = option_menu(
        "",
        [
            'Dashboard',
            'Diabetes Prediction',
            'Heart Disease Prediction',
            'Kidney Disease Prediction',
            'Health Tips',
            'My Progress',
        ],
        menu_icon='',
        icons=['speedometer2','activity','heart-pulse','droplet','lightbulb','chart-line'],
        default_index=0,
        styles={
            "container": {
                "padding": "8px 0px",
                "background-color": "transparent",
                "margin": "0",
            },
            "icon": {
                "color": "#00c8c8",
                "font-size": "17px",
                "margin-right": "10px",
            },
            "nav-link": {
                "color": "#aaa",
                "font-size": "13px",
                "text-align": "left",
                "margin": "4px 6px",
                "border-radius": "8px",
                "padding": "10px 12px",
                "--hover-color": "rgba(0, 200, 200, 0.15)",
                "transition": "all 0.3s ease",
                "font-weight": "500",
                "line-height": "1.5",
            },
            "nav-link-selected": {
                "background-color": "rgba(0, 200, 200, 0.25)",
                "color": "#00c8c8",
                "font-weight": "600",
            },
        }
    )


def get_probability(model, row) -> Tuple[float, float]:
    """Return (prob_0, prob_1) if possible; otherwise fall back to prediction."""
    try:
        proba = model.predict_proba([row])[0]
        return float(proba[0]), float(proba[1])
    except Exception:
        pred = model.predict([row])[0]
        return (1.0, 0.0) if pred == 0 else (0.0, 1.0)


def prob_to_severity(p1: float) -> Tuple[str, str]:
    """Map probability of class 1 to a (level, css_class)."""
    if p1 < 0.33:
        return "Low", "risk-low"
    if p1 < 0.66:
        return "Medium", "risk-mid"
    return "High", "risk-high"


def render_recommendations(disease_key: str, prob_one: float):
    """Render comprehensive recommendations with tabs for each severity level."""
    level, css = prob_to_severity(prob_one)
    bank = get_recommendations()[disease_key][level]
    
    # Risk level display
    st.markdown(
        f"<div class='{css}'><b>📊 Risk Level:</b> {level} | <b>Probability:</b> {prob_one:.1%}</div>",
        unsafe_allow_html=True
    )
    
    # Recommendations tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🍽️ Diet", "🏃 Habits", "🏥 When Sick", "📋 Monitoring"])
    
    with tab1:
        st.markdown(f"<div class='recommendation-box'>{bank['diet']}</div>", unsafe_allow_html=True)
    
    with tab2:
        st.markdown(f"<div class='recommendation-box'>{bank['habits']}</div>", unsafe_allow_html=True)
    
    with tab3:
        st.markdown(f"<div class='recommendation-box'>{bank['when_sick']}</div>", unsafe_allow_html=True)
    
    with tab4:
        st.markdown(f"<div class='recommendation-box'>{bank['monitoring']}</div>", unsafe_allow_html=True)


if selected == 'Dashboard':
    st.markdown("""
    <div class='welcome-banner'>
        <h1>👋 Welcome to Your Virtual Health Assistant</h1>
        <p>Advanced AI-powered disease prediction and personalized health recommendations. Take control of your health today.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class='stat-box'>
            <h4>Total Predictions</h4>
            <div class='value'>{len(st.session_state.user_predictions)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='stat-box'>
            <h4>Health Points</h4>
            <div class='value'>{st.session_state.points}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='stat-box'>
            <h4>Achievements</h4>
            <div class='value'>{len(st.session_state.achievements)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class='stat-box'>
            <h4>Health Streak</h4>
            <div class='value'>{st.session_state.health_streak}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-header'>🔬 Available Prediction Models</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='metric-card'>
            <div style='font-size: 48px;'>🩺</div>
            <h3>Diabetes</h3>
            <p>Predict your risk of developing diabetes based on health metrics</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='metric-card'>
            <div style='font-size: 48px;'>❤️</div>
            <h3>Heart Disease</h3>
            <p>Assess your cardiovascular health and heart disease risk</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='metric-card'>
            <div style='font-size: 48px;'>💧</div>
            <h3>Kidney Disease</h3>
            <p>Evaluate your kidney function and disease risk</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-header'>📚 How to Use</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='info-card'>
        <h4>Step 1: Select a Disease</h4>
        Choose one of the three disease prediction models from the sidebar menu.
        
        <h4>Step 2: Enter Your Health Data</h4>
        Provide accurate health metrics and medical information. All fields are required for accurate predictions.
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='info-card'>
        <h4>Step 3: Get Your Results</h4>
        Receive your risk assessment and severity level with detailed explanations.
        
        <h4>Step 4: Follow Recommendations</h4>
        Get personalized diet, habits, and monitoring recommendations based on your risk level.
        </div>
        """, unsafe_allow_html=True)


if selected == 'Diabetes Prediction':
    st.markdown("<div class='section-header'>🩺 Diabetes Risk Assessment</div>", unsafe_allow_html=True)
    st.markdown("Enter your health metrics to assess your diabetes risk. All fields are required.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        Pregnancies = st.number_input("Number of Pregnancies", min_value=0, max_value=20, value=0)
    with col2:
        Glucose = st.number_input("Glucose Level (mg/dL)", min_value=0, max_value=300, value=100)
    with col3:
        BloodPressure = st.number_input("Blood Pressure (mmHg)", min_value=0, max_value=200, value=70)
    
    with col1:
        SkinThickness = st.number_input("Skin Thickness (mm)", min_value=0, max_value=100, value=20)
    with col2:
        Insulin = st.number_input("Insulin Level (mIU/L)", min_value=0, max_value=900, value=80)
    with col3:
        BMI = st.number_input("BMI (Body Mass Index)", min_value=10.0, max_value=60.0, value=25.0)
    
    with col1:
        DiabetesPedigreeFunction = st.number_input("Diabetes Pedigree Function", min_value=0.0, max_value=2.5, value=0.5)
    with col2:
        Age = st.number_input("Age (years)", min_value=18, max_value=120, value=30)
    
    if st.button("🔍 Assess Diabetes Risk", use_container_width=True):
        try:
            # Feature engineering
            bmi_val = float(BMI)
            insulin_val = float(Insulin)
            glucose_val = float(Glucose)
            
            NewBMI_Underweight = 1 if bmi_val <= 18.5 else 0
            NewBMI_Overweight = 1 if 18.5 < bmi_val <= 24.9 else 0
            NewBMI_Obesity_1 = 1 if 24.9 < bmi_val <= 29.9 else 0
            NewBMI_Obesity_2 = 1 if 29.9 < bmi_val <= 34.9 else 0
            NewBMI_Obesity_3 = 1 if 34.9 < bmi_val <= 39.9 else 0
            NewBMI_Obesity_4 = 1 if bmi_val > 39.9 else 0
            
            NewInsulinScore_Normal = 1 if 16 <= insulin_val <= 166 else 0
            
            NewGlucose_Low = 1 if glucose_val <= 70 else 0
            NewGlucose_Normal = 1 if 70 < glucose_val <= 99 else 0
            NewGlucose_Overweight = 1 if 99 < glucose_val <= 126 else 0
            NewGlucose_Secret = 1 if glucose_val > 126 else 0
            
            user_input = [
                Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin,
                BMI, DiabetesPedigreeFunction, Age, NewBMI_Underweight,
                NewBMI_Overweight, NewBMI_Obesity_1, NewBMI_Obesity_2,
                NewBMI_Obesity_3, NewInsulinScore_Normal, NewGlucose_Low,
                NewGlucose_Normal, NewGlucose_Overweight, NewGlucose_Secret
            ]
            
            user_input = [float(x) for x in user_input]
            p0, p1 = get_probability(diabetes_model, user_input)
            prediction = 1 if p1 >= 0.5 else 0
            
            st.session_state.user_predictions.append({
                'disease': 'Diabetes',
                'risk': p1,
                'timestamp': datetime.now()
            })
            st.session_state.points += 10
            
            # Check achievements
            level, _ = prob_to_severity(p1)
            achievements = check_achievements('Diabetes', level)
            for achievement in achievements:
                if achievement not in st.session_state.achievements:
                    st.session_state.achievements.append(achievement)
            
            if prediction == 1:
                st.markdown(
                    "<div class='warning-message'><b>⚠️ Alert:</b> You have a higher risk of diabetes. Please consult with a healthcare provider.</div>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    "<div class='success-message'><b>✅ Good News:</b> Your diabetes risk is low. Continue maintaining healthy habits!</div>",
                    unsafe_allow_html=True
                )
            
            render_recommendations("diabetes", p1)
            
            if achievements:
                st.markdown("<div class='section-header'>🏆 New Achievements Unlocked!</div>", unsafe_allow_html=True)
                for achievement in achievements:
                    st.markdown(f"<div class='achievement-badge'>{achievement}</div>", unsafe_allow_html=True)
        
        except ValueError:
            st.error("❌ Please enter valid numeric values for all fields")


if selected == 'Heart Disease Prediction':
    st.markdown("<div class='section-header'>❤️ Heart Disease Risk Assessment</div>", unsafe_allow_html=True)
    st.markdown("Enter your cardiovascular health metrics for an accurate risk assessment.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        age = st.number_input("Age (years)", min_value=18, max_value=120, value=50)
    with col2:
        sex = st.selectbox("Gender", options=[("Female", 0), ("Male", 1)], format_func=lambda x: x[0])
        sex = sex[1]
    with col3:
        cp = st.selectbox("Chest Pain Type", options=[(f"Type {i}", i) for i in range(4)], format_func=lambda x: x[0])
        cp = cp[1]
    
    with col1:
        trestbps = st.number_input("Resting Blood Pressure (mmHg)", min_value=80, max_value=200, value=120)
    with col2:
        chol = st.number_input("Cholesterol (mg/dL)", min_value=100, max_value=400, value=200)
    with col3:
        fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dL", options=[("No", 0), ("Yes", 1)], format_func=lambda x: x[0])
        fbs = fbs[1]
    
    with col1:
        restecg = st.selectbox("Resting ECG Result", options=[(f"Type {i}", i) for i in range(3)], format_func=lambda x: x[0])
        restecg = restecg[1]
    with col2:
        thalach = st.number_input("Max Heart Rate Achieved (bpm)", min_value=60, max_value=220, value=150)
    with col3:
        exang = st.selectbox("Exercise Induced Angina", options=[("No", 0), ("Yes", 1)], format_func=lambda x: x[0])
        exang = exang[1]
    
    with col1:
        oldpeak = st.number_input("ST Depression (0-6)", min_value=0.0, max_value=6.0, value=0.0)
    with col2:
        slope = st.selectbox("ST Slope", options=[(f"Type {i}", i) for i in range(3)], format_func=lambda x: x[0])
        slope = slope[1]
    with col3:
        ca = st.selectbox("Major Vessels (0-4)", options=[(str(i), i) for i in range(5)], format_func=lambda x: x[0])
        ca = ca[1]
    
    with col1:
        thal = st.selectbox("Thalassemia", options=[("Normal", 0), ("Fixed", 1), ("Reversible", 2)], format_func=lambda x: x[0])
        thal = thal[1]
    
    if st.button("🔍 Assess Heart Disease Risk", use_container_width=True):
        try:
            user_input = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]
            user_input = [float(x) for x in user_input]
            p0, p1 = get_probability(heart_disease_model, user_input)
            prediction = 1 if p1 >= 0.5 else 0
            
            st.session_state.user_predictions.append({
                'disease': 'Heart Disease',
                'risk': p1,
                'timestamp': datetime.now()
            })
            st.session_state.points += 10
            
            level, _ = prob_to_severity(p1)
            achievements = check_achievements('Heart Disease', level)
            for achievement in achievements:
                if achievement not in st.session_state.achievements:
                    st.session_state.achievements.append(achievement)
            
            if prediction == 1:
                st.markdown(
                    "<div class='warning-message'><b>⚠️ Alert:</b> You have a higher risk of heart disease. Seek medical consultation immediately.</div>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    "<div class='success-message'><b>✅ Good News:</b> Your heart disease risk is low. Keep up your healthy lifestyle!</div>",
                    unsafe_allow_html=True
                )
            
            render_recommendations("heart", p1)
            
            if achievements:
                st.markdown("<div class='section-header'>🏆 New Achievements Unlocked!</div>", unsafe_allow_html=True)
                for achievement in achievements:
                    st.markdown(f"<div class='achievement-badge'>{achievement}</div>", unsafe_allow_html=True)
        
        except ValueError:
            st.error("❌ Please enter valid values for all fields")


if selected == 'Kidney Disease Prediction':
    st.markdown("<div class='section-header'>💧 Kidney Disease Risk Assessment</div>", unsafe_allow_html=True)
    st.markdown("Provide your kidney health metrics for a comprehensive risk evaluation.")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        age = st.number_input('Age', min_value=18, max_value=120, value=50)
    with col2:
        blood_pressure = st.number_input('Blood Pressure', min_value=60, max_value=200, value=80)
    with col3:
        specific_gravity = st.number_input('Specific Gravity', min_value=1.0, max_value=1.05, value=1.020)
    with col4:
        albumin = st.selectbox('Albumin Level', options=[(str(i), i) for i in range(6)], format_func=lambda x: x[0])
        albumin = albumin[1]
    with col5:
        sugar = st.selectbox('Sugar Level', options=[(str(i), i) for i in range(6)], format_func=lambda x: x[0])
        sugar = sugar[1]
    
    with col1:
        red_blood_cells = st.selectbox('Red Blood Cells', options=[("No", 0), ("Yes", 1)], format_func=lambda x: x[0])
        red_blood_cells = red_blood_cells[1]
    with col2:
        pus_cell = st.selectbox('Pus Cells', options=[("No", 0), ("Yes", 1)], format_func=lambda x: x[0])
        pus_cell = pus_cell[1]
    with col3:
        pus_cell_clumps = st.selectbox('Pus Cell Clumps', options=[("No", 0), ("Yes", 1)], format_func=lambda x: x[0])
        pus_cell_clumps = pus_cell_clumps[1]
    with col4:
        bacteria = st.selectbox('Bacteria', options=[("No", 0), ("Yes", 1)], format_func=lambda x: x[0])
        bacteria = bacteria[1]
    with col5:
        blood_glucose_random = st.number_input('Random Blood Glucose', min_value=50, max_value=500, value=100)
    
    with col1:
        blood_urea = st.number_input('Blood Urea', min_value=10, max_value=200, value=30)
    with col2:
        serum_creatinine = st.number_input('Serum Creatinine', min_value=0.5, max_value=10.0, value=1.0)
    with col3:
        sodium = st.number_input('Sodium', min_value=120, max_value=160, value=140)
    with col4:
        potassium = st.number_input('Potassium', min_value=3.0, max_value=7.0, value=4.5)
    with col5:
        haemoglobin = st.number_input('Hemoglobin', min_value=5.0, max_value=20.0, value=13.0)
    
    with col1:
        packed_cell_volume = st.number_input('Packed Cell Volume', min_value=10, max_value=60, value=40)
    with col2:
        white_blood_cell_count = st.number_input('White Blood Cell Count', min_value=2000, max_value=15000, value=7000)
    with col3:
        red_blood_cell_count = st.number_input('Red Blood Cell Count', min_value=2000000, max_value=8000000, value=5000000)
    with col4:
        hypertension = st.selectbox('Hypertension', options=[("No", 0), ("Yes", 1)], format_func=lambda x: x[0])
        hypertension = hypertension[1]
    with col5:
        diabetes_mellitus = st.selectbox('Diabetes Mellitus', options=[("No", 0), ("Yes", 1)], format_func=lambda x: x[0])
        diabetes_mellitus = diabetes_mellitus[1]
    
    with col1:
        coronary_artery_disease = st.selectbox('Coronary Artery Disease', options=[("No", 0), ("Yes", 1)], format_func=lambda x: x[0])
        coronary_artery_disease = coronary_artery_disease[1]
    with col2:
        appetite = st.selectbox('Appetite', options=[("Good", 0), ("Poor", 1)], format_func=lambda x: x[0])
        appetite = appetite[1]
    with col3:
        peda_edema = st.selectbox('Pedal Edema', options=[("No", 0), ("Yes", 1)], format_func=lambda x: x[0])
        peda_edema = peda_edema[1]
    with col4:
        aanemia = st.selectbox('Anemia', options=[("No", 0), ("Yes", 1)], format_func=lambda x: x[0])
        aanemia = aanemia[1]
    
    if st.button("🔍 Assess Kidney Disease Risk", use_container_width=True):
        try:
            user_input = [
                age, blood_pressure, specific_gravity, albumin, sugar,
                red_blood_cells, pus_cell, pus_cell_clumps, bacteria,
                blood_glucose_random, blood_urea, serum_creatinine, sodium,
                potassium, haemoglobin, packed_cell_volume,
                white_blood_cell_count, red_blood_cell_count, hypertension,
                diabetes_mellitus, coronary_artery_disease, appetite,
                peda_edema, aanemia
            ]
            
            user_input = [float(x) for x in user_input]
            p0, p1 = get_probability(kidney_disease_model, user_input)
            prediction = 1 if p1 >= 0.5 else 0
            
            st.session_state.user_predictions.append({
                'disease': 'Kidney Disease',
                'risk': p1,
                'timestamp': datetime.now()
            })
            st.session_state.points += 10
            
            level, _ = prob_to_severity(p1)
            achievements = check_achievements('Kidney Disease', level)
            for achievement in achievements:
                if achievement not in st.session_state.achievements:
                    st.session_state.achievements.append(achievement)
            
            if prediction == 1:
                st.markdown(
                    "<div class='warning-message'><b>⚠️ Alert:</b> You have a higher risk of kidney disease. Consult a nephrologist.</div>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    "<div class='success-message'><b>✅ Good News:</b> Your kidney disease risk is low. Maintain your healthy habits!</div>",
                    unsafe_allow_html=True
                )
            
            render_recommendations("kidney", p1)
            
            if achievements:
                st.markdown("<div class='section-header'>🏆 New Achievements Unlocked!</div>", unsafe_allow_html=True)
                for achievement in achievements:
                    st.markdown(f"<div class='achievement-badge'>{achievement}</div>", unsafe_allow_html=True)
        
        except ValueError:
            st.error("❌ Please enter valid values for all fields")


if selected == 'Health Tips':
    st.markdown("<div class='section-header'>💡 Daily Health Tips & Education</div>", unsafe_allow_html=True)
    st.markdown("Learn evidence-based health tips to improve your wellbeing.")
    
    tips = get_health_tips()
    
    # Display tips in a grid
    cols = st.columns(2)
    for idx, tip in enumerate(tips):
        with cols[idx % 2]:
            st.markdown(f"<div class='info-card'>{tip}</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='section-header'>📚 Disease Information</div>", unsafe_allow_html=True)
    
    disease_info = {
        "Diabetes": "Diabetes is a chronic condition affecting how your body processes blood glucose. Type 2 diabetes is the most common form, often preventable through lifestyle changes.",
        "Heart Disease": "Heart disease encompasses various conditions affecting the heart and blood vessels. Risk factors include high blood pressure, high cholesterol, smoking, and obesity.",
        "Kidney Disease": "Chronic kidney disease develops gradually and may not show symptoms until advanced stages. Early detection and management can slow progression significantly.",
    }
    
    selected_disease = st.selectbox("Select a Disease to Learn More", list(disease_info.keys()))
    st.markdown(f"<div class='info-card'><h4>{selected_disease}</h4><p>{disease_info[selected_disease]}</p></div>", unsafe_allow_html=True)


if selected == 'My Progress':
    st.markdown("<div class='section-header'>📊 Your Health Journey</div>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class='stat-box'>
            <h4>Total Predictions</h4>
            <div class='value'>{len(st.session_state.user_predictions)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='stat-box'>
            <h4>Health Points</h4>
            <div class='value'>{st.session_state.points}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='stat-box'>
            <h4>Achievements</h4>
            <div class='value'>{len(st.session_state.achievements)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class='stat-box'>
            <h4>Health Streak</h4>
            <div class='value'>{st.session_state.health_streak} days</div>
        </div>
        """, unsafe_allow_html=True)
    
    if st.session_state.achievements:
        st.markdown("<div class='section-header'>🏆 Your Achievements</div>", unsafe_allow_html=True)
        for achievement in st.session_state.achievements:
            st.markdown(f"<div class='achievement-badge'>{achievement}</div>", unsafe_allow_html=True)
    
    if st.session_state.user_predictions:
        st.markdown("<div class='section-header'>📈 Prediction History</div>", unsafe_allow_html=True)
        
        # Create a dataframe for predictions
        predictions_data = []
        for pred in st.session_state.user_predictions:
            level, _ = prob_to_severity(pred['risk'])
            predictions_data.append({
                'Disease': pred['disease'],
                'Risk Level': level,
                'Probability': f"{pred['risk']:.1%}",
                'Date': pred['timestamp'].strftime("%Y-%m-%d %H:%M")
            })
        
        df = pd.DataFrame(predictions_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("📝 No predictions yet. Start by selecting a disease prediction model from the sidebar!")
