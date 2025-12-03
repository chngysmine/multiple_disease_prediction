import streamlit as st
import streamlit.components.v1 as components
import pickle
import os
from streamlit_option_menu import option_menu
from typing import Dict, Tuple, List
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import nbformat
from nbconvert import HTMLExporter

st.set_page_config(
    page_title="Virtual Health Assistant",
    layout="wide",
    page_icon="🏥",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap');

    :root {
        --ink: #0c111d;
        --jet: #1b1f30;
        --aqua: #5ff4f4;
        --violet: #a855f7;
        --mint: #22d3ee;
        --text: #edf2ff;
        --muted: #8ea2c1;
        --glass: rgba(255,255,255,0.05);
        --border: rgba(255,255,255,0.12);
        --card-grad: linear-gradient(135deg, rgba(95,244,244,0.08), rgba(168,85,247,0.08));
    }

    * {
        font-family: 'Space Grotesk', 'Segoe UI', sans-serif;
    }

    body,
    html,
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at top, rgba(88, 28, 135, 0.35), transparent 45%),
                    radial-gradient(circle at 20% 20%, rgba(34, 211, 238, 0.25), transparent 35%),
                    radial-gradient(circle at 80% 0%, rgba(99, 102, 241, 0.35), transparent 35%),
                    #05070f;
        color: var(--text);
    }

    .main .block-container {
        padding: 2.5rem clamp(1.5rem, 4vw, 4.25rem) 4rem;
        max-width: 1350px;
        margin: 0 auto;
    }

    .section-shell {
        margin-bottom: 2.5rem;
        padding: 2.25rem clamp(1.2rem, 3vw, 2.75rem);
        border-radius: 28px;
        border: 1px solid rgba(255,255,255,0.08);
        background: rgba(9, 12, 22, 0.75);
        box-shadow: 0 25px 55px rgba(3,5,14,0.55);
        position: relative;
        overflow: hidden;
    }

    @media (max-width: 980px) {
        .main .block-container {
            padding: 2rem 1.25rem 3rem;
        }
        .hero {
            padding: 32px;
        }
        .model-card {
            min-height: 200px;
        }
    }

    [data-testid="stSidebar"] {
        background: rgba(5, 7, 15, 0.85);
        backdrop-filter: blur(12px);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }

    [data-testid="stSidebar"] * {
        color: var(--muted);
    }

    .sidebar-header h2 {
        color: var(--text);
        letter-spacing: 2px;
    }

    .sidebar-header p {
        color: var(--muted);
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    .stButton > button,
    .cta-button {
        background: linear-gradient(120deg, #5ff4f4, #a855f7);
        color: #04060d;
        font-weight: 600;
        border: none;
        border-radius: 999px;
        padding: 0.85rem 1.6rem;
        transition: all 0.25s ease;
        box-shadow: 0 15px 45px rgba(117, 219, 255, 0.3);
    }

    .stButton > button:hover,
    .cta-button:hover {
        transform: translateY(-4px) scale(1.01);
        box-shadow: 0 18px 55px rgba(117, 219, 255, 0.5);
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 0.8rem;
        border-bottom: none;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 999px;
        padding: 0.6rem 1.5rem;
        background: rgba(255, 255, 255, 0.06);
        color: var(--muted);
        border: 1px solid transparent;
        transition: all 0.2s ease;
    }

    .stTabs [aria-selected="true"] {
        color: var(--ink);
        background: linear-gradient(120deg, #5ff4f4, #a855f7);
        border-color: transparent;
        font-weight: 600;
    }

    .hero {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 32px;
        padding: 48px;
        margin-bottom: 32px;
        backdrop-filter: blur(18px);
        position: relative;
        overflow: hidden;
    }

    .hero::after {
        content: "";
        position: absolute;
        inset: 0;
        background: radial-gradient(circle at top right, rgba(111, 66, 193, 0.35), transparent 60%);
        opacity: 0.8;
        pointer-events: none;
    }

    .hero h1 {
        font-size: 3rem;
        margin: 0.5rem 0 1rem;
        color: var(--text);
    }

    .hero p {
        color: var(--muted);
        font-size: 1.1rem;
        max-width: 560px;
    }

    .neon-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: rgba(95, 244, 244, 0.18);
        border: 1px solid rgba(95, 244, 244, 0.35);
        border-radius: 999px;
        padding: 0.35rem 1rem;
        font-size: 0.9rem;
        letter-spacing: 1px;
        text-transform: uppercase;
    }

    .hero-actions {
        display: flex;
        gap: 0.8rem;
        flex-wrap: wrap;
        margin-top: 1.5rem;
    }

    .metric-chip {
        padding: 0.6rem 1rem;
        border-radius: 14px;
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: var(--muted);
        font-size: 0.9rem;
    }

    .neo-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        padding: 24px;
        box-shadow: 0 25px 65px rgba(5, 7, 15, 0.55);
        transition: transform 0.4s cubic-bezier(.2, .8, .2, 1);
    }

    .neo-card:hover {
        transform: translateY(-6px);
        border-color: rgba(95, 244, 244, 0.45);
    }

    .neo-card h3 {
        margin-bottom: 0.4rem;
        color: var(--text);
    }

    .neo-card p {
        margin: 0;
        color: var(--muted);
        font-size: 0.95rem;
    }

    .glass-panel {
        padding: 24px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        background: rgba(5, 7, 15, 0.6);
    }

    .section-header {
        font-size: 1.6rem;
        font-weight: 700;
        margin: 2.5rem 0 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }

    .section-header::after {
        content: "";
        flex: 1;
        height: 1px;
        background: linear-gradient(120deg, rgba(95, 244, 244, 0.4), transparent);
    }

    .section-subtitle {
        margin: -1rem 0 1.5rem;
        color: var(--muted);
        max-width: 720px;
    }

    .section-shell::before {
        content: "";
        position: absolute;
        inset: 0;
        background: radial-gradient(circle at top right, rgba(95,244,244,0.08), transparent 60%);
        opacity: 0.7;
        pointer-events: none;
    }

    .section-shell > * {
        position: relative;
        z-index: 1;
    }

    .tip-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 18px;
        margin-top: 1.25rem;
    }

    .tip-card {
        padding: 1rem 1.25rem;
        border-radius: 18px;
        border: 1px solid rgba(255,255,255,0.08);
        background: rgba(255,255,255,0.04);
        box-shadow: inset 0 0 0 1px rgba(255,255,255,0.03);
    }

    .info-panel {
        padding: 1.4rem 1.6rem;
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.08);
        background: rgba(5,8,18,0.85);
        margin-top: 1.25rem;
    }

    .section-shell .stButton {
        margin-top: 0.9rem;
    }

    .result-shell {
        margin-top: 1.5rem;
        padding: 1.5rem;
        border-radius: 24px;
        border: 1px solid rgba(255,255,255,0.08);
        background: rgba(11,14,24,0.9);
        box-shadow: 0 25px 60px rgba(3,5,14,0.5);
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    .timeline {
        position: relative;
        padding-left: 30px;
        border-left: 1px dashed rgba(255,255,255,0.2);
    }

    .timeline-step {
        margin-bottom: 18px;
        padding-left: 12px;
        position: relative;
    }

    .timeline-step::before {
        content: "";
        position: absolute;
        left: -39px;
        top: 6px;
        width: 14px;
        height: 14px;
        border-radius: 50%;
        background: linear-gradient(120deg, #5ff4f4, #a855f7);
        box-shadow: 0 0 18px rgba(95, 244, 244, 0.6);
    }

    .risk-low,
    .risk-mid,
    .risk-high,
    .recommendation-box,
    .success-message,
    .warning-message,
    .achievement-badge,
    .info-card,
    .stat-box {
        border-radius: 18px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        background: rgba(255, 255, 255, 0.03);
        box-shadow: inset 0 0 0 1px rgba(255,255,255,0.02);
    }

    .recommendation-box {
        padding: 1rem 1.25rem;
        line-height: 1.6;
    }

    .warning-message,
    .success-message,
    .result-shell .risk-low,
    .result-shell .risk-mid,
    .result-shell .risk-high {
        padding: 1rem 1.25rem;
    }

    .result-shell > *:not(:last-child) {
        margin-bottom: 1rem;
    }

    .result-shell .stTabs {
        padding: 0.3rem 0.35rem 0.6rem;
        border-radius: 16px;
        background: rgba(255,255,255,0.02);
    }

    .result-shell .stTabs [data-baseweb="tab"] {
        margin: 0 0.15rem;
    }

    .risk-low { border-left: 4px solid #22c55e; }
    .risk-mid { border-left: 4px solid #facc15; }
    .risk-high { border-left: 4px solid #f87171; }

    .info-card {
        transition: transform 0.25s ease, border-color 0.25s ease;
    }

    .info-card:hover {
        transform: translateY(-4px);
        border-color: rgba(95, 244, 244, 0.4);
    }

    .fade-in {
        animation: fadeIn 0.6s ease forwards;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .floating {
        animation: floating 6s ease-in-out infinite;
    }

    @keyframes floating {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
    }
    
    [data-testid="stSidebar"] {
        min-width: 280px;
        max-width: 320px;
        padding: 0 8px;
    }

    .sidebar-brand {
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 28px 14px 10px;
    }

    .brand-icon {
        width: 52px;
        height: 52px;
        border-radius: 16px;
        background: linear-gradient(135deg, rgba(95,244,244,0.25), rgba(168,85,247,0.25));
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 26px;
    }

    .sidebar-brand h3 {
        margin: 0;
        color: var(--text);
        font-size: 1.4rem;
    }

    .sidebar-brand span,
    .sidebar-brand p {
        display: block;
        margin: 0;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.28rem;
        color: var(--muted);
    }

    .sidebar-divider {
        margin: 16px 14px;
        height: 1px;
        background: linear-gradient(90deg, rgba(95,244,244,0.4), transparent);
    }

    .sidebar-note {
        padding: 18px 16px 28px;
        color: var(--muted);
        font-size: 0.85rem;
    }

    .showcase-wrapper {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: 24px;
    }

    .model-card {
        position: relative;
        padding: 26px;
        border-radius: 28px;
        background: var(--card-grad);
        border: 1px solid rgba(255,255,255,0.1);
        overflow: hidden;
        min-height: 250px;
        box-shadow: 0 25px 50px rgba(5,7,15,0.45);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .model-card::after {
        content: "";
        position: absolute;
        inset: 0;
        background: radial-gradient(circle at top right, rgba(255,255,255,0.12), transparent 55%);
        opacity: 0;
        transition: opacity 0.4s ease;
    }

    .model-card:hover::after {
        opacity: 1;
    }

    .model-icon {
        width: 54px;
        height: 54px;
        border-radius: 18px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
        background: rgba(255,255,255,0.08);
        margin-bottom: 16px;
    }

    .model-card h3 {
        margin: 0;
        font-size: 1.35rem;
    }

    .model-card p {
        margin: 8px 0 18px;
        color: var(--muted);
        min-height: 60px;
    }

    .model-chip {
        display: inline-flex;
        padding: 0.35rem 0.9rem;
        border-radius: 999px;
        border: 1px solid rgba(255,255,255,0.2);
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    div[data-testid="stVerticalBlock"]:has(.overlay-sentinel) {
        position: fixed;
        inset: 0;
        z-index: 9999;
        background: rgba(3, 5, 14, 0.96);
        backdrop-filter: blur(18px);
        padding: clamp(18px, 3vw, 40px);
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        gap: 16px;
    }

    div[data-testid="stVerticalBlock"]:has(.overlay-sentinel) > div:not(:has(.overlay-sentinel)) {
        width: 100%;
        max-width: 1100px;
        margin: 0 auto;
        background: rgba(7,10,22,0.85);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 28px;
        padding: clamp(18px, 2vw, 32px);
        box-shadow: 0 35px 80px rgba(0,0,0,0.45);
    }

    .overlay-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 18px;
        margin-bottom: 18px;
    }

    .overlay-title {
        display: flex;
        gap: 18px;
        align-items: center;
    }

    .overlay-title h2 {
        margin: 0;
    }

    .overlay-title p {
        margin: 6px 0 0;
        color: var(--muted);
        max-width: 640px;
    }

    .overlay-icon {
        width: 64px;
        height: 64px;
        border-radius: 20px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 30px;
        background: rgba(255,255,255,0.08);
    }

    div[data-testid="stVerticalBlock"]:has(.overlay-sentinel) .stButton>button {
        width: 100%;
        border-radius: 18px;
        border: 1px solid rgba(255,255,255,0.2);
        padding: 0.65rem 1.4rem;
        background: rgba(255,255,255,0.08);
        color: var(--text);
        font-weight: 600;
    }

    div[data-testid="stVerticalBlock"]:has(.overlay-sentinel) .stButton>button:hover {
        border-color: rgba(95,244,244,0.5);
        color: var(--aqua);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

working_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = Path(working_dir)

NOTEBOOK_CONFIG = {
    "Diabetes": {
        "path": base_dir / "notebooks" / "Advance Project Diabetes Prediction Using ML.ipynb",
        "description": "Complete training pipeline, preprocessing steps and performance visualizations for the diabetes prediction model.",
        "tagline": "Glycemic insights & engineered feature tracking.",
        "accent": "#5ff4f4",
        "icon": "🩺"
    },
    "Heart Disease": {
        "path": base_dir / "notebooks" / "Advance Project Heart Disease Prediction Using ML.ipynb",
        "description": "End-to-end heart disease pipeline with distribution plots, correlation analysis and model evaluation charts.",
        "tagline": "Cardio diagnostics blended with lifestyle cues.",
        "accent": "#f472b6",
        "icon": "❤️"
    },
    "Kidney Disease": {
        "path": base_dir / "notebooks" / "Advance Project Kidney Disease Prediction Using ML.ipynb",
        "description": "Visual journey of data cleaning, feature engineering and performance diagrams for kidney disease prediction.",
        "tagline": "Renal panels layered with symptom awareness.",
        "accent": "#a855f7",
        "icon": "💧"
    },
}

# Load models
diabetes_model = pickle.load(open(f'{working_dir}/saved_models/diabetes.pkl','rb'))
heart_disease_model = pickle.load(open(f'{working_dir}/saved_models/heart.pkl','rb'))
# NOTE:
# The pickle file for kidney model is named 'kindey.pkl' in the saved_models folder.
# We load using that exact filename to avoid FileNotFoundError.
kidney_disease_model = pickle.load(open(f'{working_dir}/saved_models/kindey.pkl','rb'))

if 'user_predictions' not in st.session_state:
    st.session_state.user_predictions = []
if 'achievements' not in st.session_state:
    st.session_state.achievements = []
if 'health_streak' not in st.session_state:
    st.session_state.health_streak = 0
if 'points' not in st.session_state:
    st.session_state.points = 0
if 'viewer_open' not in st.session_state:
    st.session_state.viewer_open = False
if 'viewer_model' not in st.session_state:
    st.session_state.viewer_model = None


@st.cache_data(show_spinner=False)
def load_notebook_html(nb_path: Path) -> Tuple[bool, str]:
    """Convert notebook content to embeddable HTML."""
    try:
        if not nb_path.exists():
            return False, f"Notebook not found: {nb_path.name}"
        with nb_path.open("r", encoding="utf-8") as source:
            notebook = nbformat.read(source, as_version=4)
        exporter = HTMLExporter()
        exporter.exclude_input_prompt = True
        exporter.exclude_output_prompt = True
        html_body, _ = exporter.from_notebook_node(notebook)
        return True, html_body
    except Exception as exc:
        return False, str(exc)


def open_model_viewer(model_key: str):
    """Store which notebook should be visualized in fullscreen overlay."""
    st.session_state.viewer_model = model_key
    st.session_state.viewer_open = True


def close_model_viewer():
    """Close the fullscreen notebook viewer."""
    st.session_state.viewer_model = None
    st.session_state.viewer_open = False

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
    st.markdown(
        """
        <div class='sidebar-brand'>
            <div class='brand-icon'>🏥</div>
            <div>
                <span>Virtual health assistant</span>
                <h3>VHA</h3>
                <p>AI-powered predictions</p>
            </div>
        </div>
        <div class='sidebar-divider'></div>
        """,
        unsafe_allow_html=True,
    )

    # Navigation only (main app pages)
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

    st.markdown(
        """
        <div class='sidebar-note'>
            Calibrated risk models, cinematic visuals, and instant wellness playbooks — all in one secure console.
        </div>
        """,
        unsafe_allow_html=True,
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


if st.session_state.viewer_open and st.session_state.viewer_model:
    model_key = st.session_state.viewer_model
    config = NOTEBOOK_CONFIG.get(model_key)
    st.markdown(
        """
        <style>
        body { overflow: hidden !important; }
        [data-testid="stSidebar"] { display: none !important; }
        [data-testid="stAppViewContainer"] > .main {
            margin-left: 0 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    overlay_block = st.container()
    with overlay_block:
        st.markdown("<div class='overlay-sentinel'></div>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class='overlay-header'>
                <div class='overlay-title'>
                    <span class='overlay-icon'>{config['icon']}</span>
                    <div>
                        <h2>{model_key} Visual Studio</h2>
                        <p>{config['description']}</p>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        close_col = st.columns([0.82, 0.18])[1]
        with close_col:
            if st.button("Close viewer ✕", key="close_viewer"):
                close_model_viewer()
                st.rerun()
        success, payload = load_notebook_html(config["path"])
        if success and payload.strip():
            components.html(payload, height=900, scrolling=True)
        elif success:
            st.info("Notebook is empty or has no visible content to render.")
        else:
            st.error(f"Unable to load notebook: {payload}")
    st.stop()


if selected == 'Dashboard':
    st.markdown(
        """
        <div class='hero fade-in'>
            <span class='neon-pill'>Next-gen digital clinic</span>
            <h1>Real-time disease intelligence powered by responsible AI.</h1>
            <p>
                Run hyper-personalized risk assessments for diabetes, heart disease, and kidney disease
                with cinematic visuals, adaptive recommendations, and smooth micro-interactions.
            </p>
            <div class='hero-actions'>
                <span class='metric-chip'>3 advanced predictive models</span>
                <span class='metric-chip'>Precision recommendations</span>
                <span class='metric-chip'>Continuous progress tracking</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cta_col1, cta_col2 = st.columns([1.3, 1])
    with cta_col1:
        if st.button("Launch Model Insights 🚀", use_container_width=True, key="cta_model"):
            open_model_viewer("Diabetes")
            st.rerun()
    with cta_col2:
        st.markdown(
            """
            <div class='glass-panel floating'>
                <h4 style="margin-bottom:0.4rem;">Today's signal</h4>
                <p style="margin:0;color:var(--muted);">Stay proactive - run a prediction to refresh your insights.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    stats = [
        ("Total Predictions", len(st.session_state.user_predictions), "Live volume"),
        ("Health Points", st.session_state.points, "Gamified wellness"),
        ("Achievements", len(st.session_state.achievements), "Milestones unlocked"),
        ("Health Streak", f"{st.session_state.health_streak} days", "Consistency record"),
    ]

    stat_cols = st.columns(4)
    for col, data in zip(stat_cols, stats):
        title, value, subtitle = data
        col.markdown(
            f"""
            <div class='neo-card fade-in'>
                <p class='metric-chip'>{subtitle}</p>
                <h2 style="margin:0.4rem 0;">{value}</h2>
                <p style="color:var(--muted);">{title}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with st.container():
        st.markdown("<div class='section-shell fade-in'>", unsafe_allow_html=True)
        st.markdown("<div class='section-header'>Intelligence Control Center</div>", unsafe_allow_html=True)
        intelligence_cols = st.columns([1.7, 1])

        with intelligence_cols[0]:
            st.markdown(
                """
                <div class='glass-panel fade-in'>
                    <h3 style="margin-top:0;">Operational pulse</h3>
                    <div class='timeline' style="margin-top:20px;">
                        <div class='timeline-step'>
                            <strong>Ingest metrics</strong>
                            <p style="color:var(--muted); margin-bottom:0;">Stream clinical-grade inputs with validations to reduce noise.</p>
                        </div>
                        <div class='timeline-step'>
                            <strong>Predict & contextualize</strong>
                            <p style="color:var(--muted); margin-bottom:0;">Hybrid ML models output calibrated probabilities and severity tiers.</p>
                        </div>
                        <div class='timeline-step'>
                            <strong>Prescribe action</strong>
                            <p style="color:var(--muted); margin-bottom:0;">Generate diet, habit, and monitoring playbooks instantly.</p>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with intelligence_cols[1]:
            st.markdown(
                """
                <div class='glass-panel fade-in'>
                    <h3 style="margin-top:0;">Model lineup</h3>
                    <div style="display:flex;flex-direction:column;gap:12px;margin-top:16px;">
                        <div class='info-card' style="margin:0;">
                            <strong>🩺 Diabetes</strong>
                            <p style="margin:4px 0 0;color:var(--muted);">Balanced accuracy tuned with engineered BMI and glucose bands.</p>
                        </div>
                        <div class='info-card' style="margin:0;">
                            <strong>❤️ Heart</strong>
                            <p style="margin:4px 0 0;color:var(--muted);">ECG-informed scoring with lifestyle-ready explanations.</p>
                        </div>
                        <div class='info-card' style="margin:0;">
                            <strong>💧 Kidney</strong>
                            <p style="margin:4px 0 0;color:var(--muted);">Holistic renal panel fusion plus symptom-aware cues.</p>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='section-shell fade-in'>", unsafe_allow_html=True)
        st.markdown("<div class='section-header'>Navigator</div>", unsafe_allow_html=True)
        guide_col1, guide_col2 = st.columns(2)

        with guide_col1:
            st.markdown(
                """
                <div class='info-card'>
                    <h4>Workflow playbook</h4>
                    <ul style="color:var(--muted);line-height:1.8;padding-left:20px;margin-bottom:0;">
                        <li>Pick a prediction journey from the sidebar.</li>
                        <li>Provide accurate biomarker inputs with confidence.</li>
                        <li>Review the risk badge, probability, and insight tabs.</li>
                        <li>Apply diet, habit, and monitoring strategies immediately.</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with guide_col2:
            st.markdown(
                """
                <div class='info-card'>
                    <h4>Experience promise</h4>
                    <ul style="color:var(--muted);line-height:1.8;padding-left:20px;margin-bottom:0;">
                        <li>All content is 100% English for global teams.</li>
                        <li>Smooth micro-animations keep context stable.</li>
                        <li>Notebook visualizations launch in fullscreen overlays.</li>
                        <li>Achievements and streaks gamify healthy behaviors.</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='section-shell fade-in'>", unsafe_allow_html=True)
        st.markdown("<div class='section-header'>Model Visual Showcase</div>", unsafe_allow_html=True)
        st.markdown("<p class='section-subtitle'>Launch immersive notebooks for each model without leaving the dashboard. Visual pipelines, charts, and diagnostics load inside a cinematic fullscreen stage.</p>", unsafe_allow_html=True)
        showcase_cols = st.columns(3)
        for col, (model_name, config) in zip(showcase_cols, NOTEBOOK_CONFIG.items()):
            with col:
                st.markdown(
                    f"""
                    <div class='model-card'>
                        <div class='model-icon'>{config['icon']}</div>
                        <h3>{model_name}</h3>
                        <p>{config['tagline']}</p>
                        <span class='model-chip'>Full notebook & diagrams</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if st.button(f"View {model_name}", use_container_width=True, key=f"view_{model_name.lower().replace(' ', '_')}"):
                    open_model_viewer(model_name)
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


if selected == 'Diabetes Prediction':
    with st.container():
        st.markdown("<div class='section-shell fade-in'>", unsafe_allow_html=True)
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
        
        trigger = st.button("🔍 Assess Diabetes Risk", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    if trigger:
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
                message_block = "<div class='warning-message'><b>⚠️ Alert:</b> You have a higher risk of diabetes. Please consult with a healthcare provider.</div>"
            else:
                message_block = "<div class='success-message'><b>✅ Good News:</b> Your diabetes risk is low. Continue maintaining healthy habits!</div>"

            with st.container():
                st.markdown("<div class='result-shell'>", unsafe_allow_html=True)
                st.markdown(message_block, unsafe_allow_html=True)
                render_recommendations("diabetes", p1)
                st.markdown("</div>", unsafe_allow_html=True)
            
            if achievements:
                st.markdown("<div class='section-header'>🏆 New Achievements Unlocked!</div>", unsafe_allow_html=True)
                for achievement in achievements:
                    st.markdown(f"<div class='achievement-badge'>{achievement}</div>", unsafe_allow_html=True)
        
        except ValueError:
            st.error("❌ Please enter valid numeric values for all fields")


if selected == 'Heart Disease Prediction':
    with st.container():
        st.markdown("<div class='section-shell fade-in'>", unsafe_allow_html=True)
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
        
        heart_trigger = st.button("🔍 Assess Heart Disease Risk", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    if heart_trigger:
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
                message_block = "<div class='warning-message'><b>⚠️ Alert:</b> You have a higher risk of heart disease. Seek medical consultation immediately.</div>"
            else:
                message_block = "<div class='success-message'><b>✅ Good News:</b> Your heart disease risk is low. Keep up your healthy lifestyle!</div>"
            
            with st.container():
                st.markdown("<div class='result-shell'>", unsafe_allow_html=True)
                st.markdown(message_block, unsafe_allow_html=True)
                render_recommendations("heart", p1)
                st.markdown("</div>", unsafe_allow_html=True)
            
            if achievements:
                st.markdown("<div class='section-header'>🏆 New Achievements Unlocked!</div>", unsafe_allow_html=True)
                for achievement in achievements:
                    st.markdown(f"<div class='achievement-badge'>{achievement}</div>", unsafe_allow_html=True)
        
        except ValueError:
            st.error("❌ Please enter valid values for all fields")


if selected == 'Kidney Disease Prediction':
    with st.container():
        st.markdown("<div class='section-shell fade-in'>", unsafe_allow_html=True)
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
        
        kidney_trigger = st.button("🔍 Assess Kidney Disease Risk", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    if kidney_trigger:
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
                message_block = "<div class='warning-message'><b>⚠️ Alert:</b> You have a higher risk of kidney disease. Consult a nephrologist.</div>"
            else:
                message_block = "<div class='success-message'><b>✅ Good News:</b> Your kidney disease risk is low. Maintain your healthy habits!</div>"
            
            with st.container():
                st.markdown("<div class='result-shell'>", unsafe_allow_html=True)
                st.markdown(message_block, unsafe_allow_html=True)
                render_recommendations("kidney", p1)
                st.markdown("</div>", unsafe_allow_html=True)
            
            if achievements:
                st.markdown("<div class='section-header'>🏆 New Achievements Unlocked!</div>", unsafe_allow_html=True)
                for achievement in achievements:
                    st.markdown(f"<div class='achievement-badge'>{achievement}</div>", unsafe_allow_html=True)
        
        except ValueError:
            st.error("❌ Please enter valid values for all fields")


if selected == 'Health Tips':
    tips = get_health_tips()
    
    with st.container():
        st.markdown("<div class='section-shell fade-in'>", unsafe_allow_html=True)
        st.markdown("<div class='section-header'>💡 Daily Health Tips & Education</div>", unsafe_allow_html=True)
        st.markdown("Learn evidence-based health tips to improve your wellbeing.")
        tips_markup = "".join(f"<div class='tip-card'>{tip}</div>" for tip in tips)
        st.markdown(f"<div class='tip-grid'>{tips_markup}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    disease_info = {
        "Diabetes": "Diabetes is a chronic condition affecting how your body processes blood glucose. Type 2 diabetes is the most common form, often preventable through lifestyle changes.",
        "Heart Disease": "Heart disease encompasses various conditions affecting the heart and blood vessels. Risk factors include high blood pressure, high cholesterol, smoking, and obesity.",
        "Kidney Disease": "Chronic kidney disease develops gradually and may not show symptoms until advanced stages. Early detection and management can slow progression significantly.",
    }
    
    with st.container():
        st.markdown("<div class='section-shell fade-in'>", unsafe_allow_html=True)
        st.markdown("<div class='section-header'>📚 Disease Information</div>", unsafe_allow_html=True)
        selected_disease = st.selectbox("Select a Disease to Learn More", list(disease_info.keys()))
        st.markdown(f"<div class='info-panel'><h4>{selected_disease}</h4><p>{disease_info[selected_disease]}</p></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


if selected == 'My Progress':
    with st.container():
        st.markdown("<div class='section-shell fade-in'>", unsafe_allow_html=True)
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
        st.markdown("</div>", unsafe_allow_html=True)
