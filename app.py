"""
Tourist Demand Pattern Analysis Across Indian Destinations
Professional Tourism Intelligence & Demand Modeling Platform
"""

import os
import sys
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from streamlit_folium import st_folium
import folium

# Set page config
st.set_page_config(
    page_title="Tourist Demand Pattern Analysis | Indian Destinations",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# High-Resolution Curated Real-World Destination Imagery
DESTINATION_IMAGES = {
    'taj mahal': 'https://images.unsplash.com/photo-1564507592333-c60657eea523?w=900&auto=format&fit=crop&q=80',
    'qutub minar': 'https://images.unsplash.com/photo-1587474260584-136574528ed5?w=900&auto=format&fit=crop&q=80',
    'red fort': 'https://images.unsplash.com/photo-1598324789736-4861f89564a0?w=900&auto=format&fit=crop&q=80',
    'agra fort': 'https://images.unsplash.com/photo-1548013146-72479768bada?w=900&auto=format&fit=crop&q=80',
    'amer fort': 'https://images.unsplash.com/photo-1599661046289-e31897846e41?w=900&auto=format&fit=crop&q=80',
    'jaipur': 'https://images.unsplash.com/photo-1599661046289-e31897846e41?w=900&auto=format&fit=crop&q=80',
    'hampi': 'https://images.unsplash.com/photo-1620766182966-c6eb5ed2b788?w=900&auto=format&fit=crop&q=80',
    'charminar': 'https://images.unsplash.com/photo-1572445271230-a78b5944a659?w=900&auto=format&fit=crop&q=80',
    'golconda': 'https://images.unsplash.com/photo-1572445271230-a78b5944a659?w=900&auto=format&fit=crop&q=80',
    'goa': 'https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=900&auto=format&fit=crop&q=80',
    'varanasi': 'https://images.unsplash.com/photo-1561361513-2d000a50f0dc?w=900&auto=format&fit=crop&q=80',
    'sarnath': 'https://images.unsplash.com/photo-1561361513-2d000a50f0dc?w=900&auto=format&fit=crop&q=80',
    'kolkata': 'https://images.unsplash.com/photo-1558431382-27e303142255?w=900&auto=format&fit=crop&q=80',
    'victoria': 'https://images.unsplash.com/photo-1558431382-27e303142255?w=900&auto=format&fit=crop&q=80',
    'mumbai': 'https://images.unsplash.com/photo-1570168007204-dfb528c6958f?w=900&auto=format&fit=crop&q=80',
    'elephanta': 'https://images.unsplash.com/photo-1570168007204-dfb528c6958f?w=900&auto=format&fit=crop&q=80',
    'delhi': 'https://images.unsplash.com/photo-1585135497273-1a86b09fe70e?w=900&auto=format&fit=crop&q=80',
    'humayun': 'https://images.unsplash.com/photo-1585135497273-1a86b09fe70e?w=900&auto=format&fit=crop&q=80',
    'ellora': 'https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?w=900&auto=format&fit=crop&q=80',
    'ajanta': 'https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?w=900&auto=format&fit=crop&q=80',
    'kerala': 'https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?w=900&auto=format&fit=crop&q=80',
    'thrissur': 'https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?w=900&auto=format&fit=crop&q=80',
    'mamallapuram': 'https://images.unsplash.com/photo-1582510003544-4d00b7f74220?w=900&auto=format&fit=crop&q=80',
    'shore temple': 'https://images.unsplash.com/photo-1582510003544-4d00b7f74220?w=900&auto=format&fit=crop&q=80',
    'konark': 'https://images.unsplash.com/photo-1524492412937-b28074a5d7da?w=900&auto=format&fit=crop&q=80',
    'sun temple': 'https://images.unsplash.com/photo-1524492412937-b28074a5d7da?w=900&auto=format&fit=crop&q=80',
    'default': 'https://images.unsplash.com/photo-1524492412937-b28074a5d7da?w=900&auto=format&fit=crop&q=80'
}

def get_monument_image(name, circle=""):
    """Returns curated high-resolution destination image URL."""
    n = str(name).lower()
    c = str(circle).lower()
    for key, url in DESTINATION_IMAGES.items():
        if key in n or key in c:
            return url
    return DESTINATION_IMAGES['default']


# ==========================================================
# LUXURY DARK ANALYTICS CSS WITH AMBIENT ANIMATIONS
# ==========================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700;800;900&family=Space+Grotesk:wght@500;600;700&display=swap');

    /* Global Dark Canvas with Subtle Grid & Ambient Gradient */
    .stApp {
        background-color: #080d1a;
        background-image: 
            radial-gradient(at 0% 0%, rgba(37, 99, 235, 0.14) 0px, transparent 50%),
            radial-gradient(at 100% 0%, rgba(13, 148, 136, 0.14) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(124, 58, 237, 0.12) 0px, transparent 50%),
            radial-gradient(at 0% 100%, rgba(245, 158, 11, 0.09) 0px, transparent 50%),
            linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
        background-size: 100% 100%, 100% 100%, 100% 100%, 100% 100%, 48px 48px, 48px 48px;
        background-attachment: fixed;
        color: #f1f5f9;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        overflow-x: hidden;
    }

    /* Ambient Animated Floating Orbs in Background */
    @keyframes floatOrb1 {
        0% { transform: translate(0, 0) scale(1); }
        50% { transform: translate(45px, -35px) scale(1.08); }
        100% { transform: translate(-25px, 30px) scale(0.95); }
    }

    @keyframes floatOrb2 {
        0% { transform: translate(0, 0) scale(1); }
        50% { transform: translate(-40px, 40px) scale(1.1); }
        100% { transform: translate(30px, -25px) scale(0.92); }
    }

    /* Typography Hierarchy */
    h1, h2, h3, h4 {
        font-family: 'Outfit', sans-serif !important;
        letter-spacing: -0.025em;
        color: #f8fafc;
    }

    /* Hero Section */
    .hero-container {
        padding: 24px 0 16px 0;
        animation: pageFadeSlide 0.7s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(56, 189, 248, 0.25);
        color: #38bdf8;
        padding: 5px 14px;
        border-radius: 30px;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        margin-bottom: 12px;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.15);
    }

    .pulse-dot {
        width: 8px;
        height: 8px;
        background-color: #38bdf8;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 8px #38bdf8;
        animation: pulseGlow 2s infinite ease-in-out;
    }

    @keyframes pulseGlow {
        0%, 100% { opacity: 0.5; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.3); }
    }

    .hero-title {
        font-family: 'Outfit', sans-serif !important;
        font-size: 3.2rem !important;
        font-weight: 900 !important;
        line-height: 1.08;
        margin: 0;
        color: #ffffff;
        text-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
    }

    .hero-gradient-text {
        background: linear-gradient(135deg, #60a5fa 0%, #38bdf8 35%, #a78bfa 70%, #f59e0b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        font-size: 1.25rem;
        font-weight: 500;
        color: #94a3b8;
        margin-top: 8px;
        margin-bottom: 24px;
        letter-spacing: -0.01em;
    }

    /* Premium Glassmorphic Cards */
    .glass-card {
        background: rgba(15, 23, 42, 0.65);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 24px;
        box-shadow: 0 12px 30px -5px rgba(0, 0, 0, 0.4), 0 0 1px 1px rgba(255, 255, 255, 0.05);
        transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
        position: relative;
        overflow: hidden;
        margin-bottom: 20px;
    }

    .glass-card:hover {
        transform: translateY(-4px);
        border-color: rgba(56, 189, 248, 0.35);
        box-shadow: 0 20px 35px -8px rgba(14, 165, 233, 0.25), 0 0 25px rgba(56, 189, 248, 0.12);
        background: rgba(20, 30, 50, 0.75);
    }

    /* KPI Statistic Cards */
    .kpi-card {
        background: rgba(15, 23, 42, 0.7);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 20px 16px;
        text-align: center;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.35);
        transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
        position: relative;
        overflow: hidden;
    }

    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #f59e0b);
        opacity: 0.85;
    }

    .kpi-card:hover {
        transform: translateY(-5px);
        border-color: rgba(56, 189, 248, 0.4);
        box-shadow: 0 18px 30px -8px rgba(56, 189, 248, 0.25), 0 0 20px rgba(56, 189, 248, 0.12);
        background: rgba(22, 34, 58, 0.8);
    }

    .kpi-title {
        font-size: 0.78rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 700;
    }

    .kpi-value {
        font-family: 'Space Grotesk', 'Outfit', sans-serif;
        font-size: 2.15rem;
        font-weight: 700;
        color: #ffffff;
        margin-top: 4px;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
    }

    .kpi-subtitle {
        font-size: 0.82rem;
        color: #34d399;
        font-weight: 600;
        margin-top: 4px;
    }

    /* Destination Showcase Cards */
    .showcase-card {
        position: relative;
        border-radius: 18px;
        overflow: hidden;
        background: rgba(15, 23, 42, 0.72);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.35);
        transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
        margin-bottom: 24px;
    }

    .showcase-card:hover {
        transform: translateY(-6px) scale(1.01);
        border-color: rgba(56, 189, 248, 0.45);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5), 0 0 25px rgba(56, 189, 248, 0.18);
    }

    .showcase-img {
        width: 100%;
        height: 210px;
        object-fit: cover;
        transition: transform 0.6s ease;
    }

    .showcase-card:hover .showcase-img {
        transform: scale(1.05);
    }

    .showcase-content {
        padding: 18px 20px;
    }

    .badge-unesco {
        background: linear-gradient(135deg, #10b981, #059669);
        color: #ffffff;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.4px;
        display: inline-block;
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
    }

    .badge-protected {
        background: rgba(148, 163, 184, 0.18);
        color: #cbd5e1;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .chip-stat {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.08);
        color: #e2e8f0;
        padding: 6px 12px;
        border-radius: 8px;
        font-size: 0.82rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    /* Sidebar Navigation Enhancement */
    [data-testid="stSidebar"] {
        background-color: rgba(9, 13, 24, 0.92) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }

    [data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.08) !important;
    }

    [data-testid="stRadio"] div[role="radiogroup"] {
        gap: 6px;
    }

    [data-testid="stRadio"] label {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 10px 14px;
        margin-bottom: 4px;
        transition: all 0.25s ease;
        cursor: pointer;
        color: #cbd5e1 !important;
    }

    [data-testid="stRadio"] label:hover {
        background: rgba(56, 189, 248, 0.08);
        border-color: rgba(56, 189, 248, 0.3);
        transform: translateX(4px);
        color: #ffffff !important;
    }

    [data-testid="stRadio"] label[data-checked="true"],
    [data-testid="stRadio"] label:has(input:checked) {
        background: linear-gradient(135deg, rgba(37, 99, 235, 0.28), rgba(124, 58, 237, 0.28)) !important;
        border: 1px solid rgba(56, 189, 248, 0.5) !important;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.25) !important;
        font-weight: 700;
        color: #ffffff !important;
    }

    /* Buttons */
    .stButton > button, div.stButton > button {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 50%, #7c3aed 100%) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 12px !important;
        padding: 11px 26px !important;
        font-weight: 700 !important;
        letter-spacing: 0.3px !important;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4) !important;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }

    .stButton > button:hover, div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(37, 99, 235, 0.55), 0 0 15px rgba(56, 189, 248, 0.3) !important;
        border-color: rgba(255, 255, 255, 0.4) !important;
    }

    .stButton > button:active, div.stButton > button:active {
        transform: translateY(0px) scale(0.98) !important;
    }

    /* Chart Containers */
    .stPlotlyChart {
        background: rgba(15, 23, 42, 0.65);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 10px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
        transition: border-color 0.3s ease;
    }

    .stPlotlyChart:hover {
        border-color: rgba(56, 189, 248, 0.3);
    }

    /* Dataframe Tables */
    [data-testid="stDataFrame"] {
        background: rgba(15, 23, 42, 0.65) !important;
        backdrop-filter: blur(14px) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
        overflow: hidden !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25) !important;
        padding: 4px;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(15, 23, 42, 0.6);
        padding: 6px;
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.07);
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        color: #94a3b8;
        font-weight: 600;
        padding: 8px 18px;
        border: none !important;
        transition: all 0.25s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: #f1f5f9;
        background: rgba(255, 255, 255, 0.05);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35);
    }

    /* Form Controls */
    [data-testid="stSelectbox"] > div > div, 
    div[data-baseweb="select"] > div {
        background: rgba(15, 23, 42, 0.75) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: #f1f5f9 !important;
    }

    [data-testid="stSelectbox"] > div > div:hover,
    div[data-baseweb="select"] > div:hover {
        border-color: rgba(56, 189, 248, 0.4) !important;
    }

    [data-testid="stExpander"] {
        background: rgba(15, 23, 42, 0.6) !important;
        backdrop-filter: blur(14px) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 14px !important;
        overflow: hidden;
    }

    .stAlert {
        background: rgba(15, 23, 42, 0.72) !important;
        backdrop-filter: blur(14px) !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        border-radius: 14px !important;
        color: #e2e8f0 !important;
    }

    /* Page Fade-In Entrance Animation */
    @keyframes pageFadeSlide {
        0% { opacity: 0; transform: translateY(12px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    /* Respect Reduced Motion */
    @media (prefers-reduced-motion: reduce) {
        .stApp, .hero-container, .showcase-card, .kpi-card, .stButton > button {
            animation: none !important;
            transition: none !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Add project root to sys.path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from src.data_loader import (
    load_monuments_data, load_statewise_data, load_quarterly_data,
    load_fta_longitudinal_data, load_weather_data
)
from src.cleaner import clean_monuments_data, clean_statewise_data, clean_quarterly_data, clean_fta_longitudinal_data
from src.feature_engineering import engineer_destination_features
from src.models import TouristDemandRegression
from src.clustering import DestinationKMeansClustering, CLUSTER_ARCHETYPES
from src.recommender import TourismRecommendationEngine
import src.eda as eda
import importlib
importlib.reload(eda)


@st.cache_data
def load_all_datasets():
    """Loads and caches processed datasets."""
    data_dir = os.path.join(PROJECT_ROOT, "data", "processed")
    dest_path = os.path.join(data_dir, "destinations_clustered.csv")
    if not os.path.exists(dest_path):
        dest_path = os.path.join(data_dir, "destinations_featured.csv")
        
    state_path = os.path.join(data_dir, "statewise_tourism_cleaned.csv")
    qtr_path = os.path.join(data_dir, "seasonal_quarterly_cleaned.csv")
    fta_path = os.path.join(data_dir, "longitudinal_fta_cleaned.csv")
    
    if os.path.exists(dest_path) and os.path.exists(state_path) and os.path.exists(qtr_path) and os.path.exists(fta_path):
        df_dest = pd.read_csv(dest_path)
        df_state = pd.read_csv(state_path)
        df_qtr = pd.read_csv(qtr_path)
        df_fta = pd.read_csv(fta_path)
    else:
        from src.cleaner import clean_all_and_save
        from src.feature_engineering import engineer_all_and_save
        from src.clustering import train_and_save_clustering
        from src.models import train_and_save_model
        
        clean_all_and_save()
        engineer_all_and_save()
        _, df_dest = train_and_save_clustering()
        train_and_save_model()
        
        df_state = pd.read_csv(state_path)
        df_qtr = pd.read_csv(qtr_path)
        df_fta = pd.read_csv(fta_path)
        
    return df_dest, df_state, df_qtr, df_fta


@st.cache_resource
def load_trained_models():
    """Loads trained regression and clustering models."""
    model_path = os.path.join(PROJECT_ROOT, "models", "linear_regression_model.joblib")
    cluster_path = os.path.join(PROJECT_ROOT, "models", "kmeans_clustering_model.joblib")
    
    if os.path.exists(model_path):
        regressor = TouristDemandRegression.load(model_path)
    else:
        from src.models import train_and_save_model
        regressor, _ = train_and_save_model()
        
    if os.path.exists(cluster_path):
        clusterer = DestinationKMeansClustering.load(cluster_path)
    else:
        from src.clustering import train_and_save_clustering
        clusterer, _ = train_and_save_clustering()
        
    return regressor, clusterer


# Load datasets & models
try:
    df_dest, df_state, df_qtr, df_fta = load_all_datasets()
    regressor, clusterer = load_trained_models()
    recommender = TourismRecommendationEngine(df_dest=df_dest, df_qtr=df_qtr, df_state=df_state)
except Exception as e:
    st.error(f"Error loading system pipeline: {e}")
    st.stop()


# ==========================================================
# SIDEBAR NAVIGATION & CONTROLS
# ==========================================================

st.sidebar.markdown("""
<div style="padding-bottom: 8px;">
    <div style="display:flex; align-items:center; gap:8px; margin-bottom:4px;">
        <span class="pulse-dot"></span>
        <span style="font-size:0.75rem; color:#38bdf8; font-weight:700; letter-spacing:0.8px;">LIVE PLATFORM</span>
    </div>
    <h2 style="font-family:'Outfit', sans-serif; font-size:1.4rem; font-weight:800; color:#ffffff; margin:0;">
        Tourist Demand
    </h2>
    <p style="font-size:0.82rem; color:#94a3b8; margin-top:2px; font-weight:500;">
        Pattern Analysis & Intelligence
    </p>
</div>
""", unsafe_allow_html=True)
st.sidebar.markdown("---")

PAGE_OPTIONS = [
    "1. Overview",
    "2. Tourism Demand Analysis",
    "3. Destination Analysis",
    "4. Seasonal Analysis",
    "5. Weather & Tourism",
    "6. ML Demand Prediction",
    "7. Destination Clustering",
    "8. Insights & Recommendations"
]

selected_page = st.sidebar.radio("Navigation Menu", PAGE_OPTIONS, index=0)
st.sidebar.markdown("---")

# Global Filter Options
st.sidebar.subheader("Destination Filters")

all_states = ['All States'] + sorted(list(df_dest['State'].dropna().unique()))
selected_state = st.sidebar.selectbox("Filter by State", all_states, index=0)

tourist_types = ["All Tourists (Total)", "Domestic Only", "Foreign Only"]
selected_tourist_type = st.sidebar.selectbox("Visitor Type", tourist_types, index=0)

all_types = ['All Typologies'] + sorted(list(df_dest['Destination_Type'].dropna().unique()))
selected_type = st.sidebar.selectbox("Heritage Typology", all_types, index=0)

unesco_filter = st.sidebar.radio("Heritage Classification", ["All Sites", "UNESCO Sites Only", "Non-UNESCO Only"], index=0)

# Filter Dataset based on sidebar
df_filtered = df_dest.copy()
if selected_state != 'All States':
    df_filtered = df_filtered[df_filtered['State'] == selected_state]
if selected_type != 'All Typologies':
    df_filtered = df_filtered[df_filtered['Destination_Type'] == selected_type]
if unesco_filter == "UNESCO Sites Only":
    df_filtered = df_filtered[df_filtered['Is_UNESCO_Site'] == 1]
elif unesco_filter == "Non-UNESCO Only":
    df_filtered = df_filtered[df_filtered['Is_UNESCO_Site'] == 0]

st.sidebar.markdown("---")
st.sidebar.caption(f"Active Filter: **{len(df_filtered)} / {len(df_dest)}** destinations")


# ==========================================================
# PAGE 1: OVERVIEW
# ==========================================================
if selected_page == "1. Overview":
    st.markdown("""
    <div class="hero-container">
        <div class="hero-badge">
            <span class="pulse-dot"></span> NATIONAL TOURISM INTELLIGENCE PLATFORM
        </div>
        <h1 class="hero-title">
            TOURIST DEMAND<br>
            <span class="hero-gradient-text">PATTERN ANALYSIS</span>
        </h1>
        <p class="hero-subtitle">Across Indian Destinations</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Modern Glassmorphic KPI Metrics
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        total_visits_m = df_dest['Total_Tourist_Visits'].sum() / 1e6
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Monuments Footfall</div>
            <div class="kpi-value">{total_visits_m:.1f}M</div>
            <div class="kpi-subtitle">144 Centrally-Protected Sites</div>
        </div>
        """, unsafe_allow_html=True)
        
    with k2:
        top_dest = df_dest.sort_values(by='Total_Tourist_Visits', ascending=False).iloc[0]
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Top Heritage Hub</div>
            <div class="kpi-value" style="font-size:1.35rem;">{top_dest['Monument_Name'][:14]}</div>
            <div class="kpi-subtitle">{top_dest['Total_Tourist_Visits']/1e6:.2f}M Annual Visitors</div>
        </div>
        """, unsafe_allow_html=True)
        
    with k3:
        avg_dom_share = df_dest['Domestic_Tourist_Share'].mean()
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Domestic Share</div>
            <div class="kpi-value">{avg_dom_share:.1f}%</div>
            <div class="kpi-subtitle">Predominant Visitor Base</div>
        </div>
        """, unsafe_allow_html=True)
        
    with k4:
        unesco_count = df_dest['Is_UNESCO_Site'].sum()
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">UNESCO Heritage</div>
            <div class="kpi-value">{unesco_count}</div>
            <div class="kpi-subtitle">World Heritage Sites</div>
        </div>
        """, unsafe_allow_html=True)
        
    with k5:
        avg_temp = df_dest['Annual_Avg_Temp_C'].mean()
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Average Climate</div>
            <div class="kpi-value">{avg_temp:.1f}°C</div>
            <div class="kpi-subtitle">Mean Destination Temp</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Real-World Destination Showcase Gallery
    st.subheader("🌟 Featured Destinations Showcase")
    st.caption("Visual highlights of prominent heritage hubs analyzed in the platform:")
    
    g1, g2, g3, g4 = st.columns(4)
    showcase_items = [
        {"name": "Taj Mahal", "loc": "Agra, Uttar Pradesh", "vol": "5.07M Visits", "img": DESTINATION_IMAGES['taj mahal']},
        {"name": "Qutub Minar", "loc": "Mehrauli, New Delhi", "vol": "2.30M Visits", "img": DESTINATION_IMAGES['qutub minar']},
        {"name": "Hampi Ruins", "loc": "Ballari, Karnataka", "vol": "610K Visits", "img": DESTINATION_IMAGES['hampi']},
        {"name": "Goa Heritage", "loc": "Old Goa, Goa", "vol": "425K Visits", "img": DESTINATION_IMAGES['goa']}
    ]
    
    for col, item in zip([g1, g2, g3, g4], showcase_items):
        with col:
            st.markdown(f"""
            <div class="showcase-card">
                <img src="{item['img']}" class="showcase-img" alt="{item['name']}">
                <div class="showcase-content">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                        <h4 style="margin:0; font-size:1.15rem; color:#ffffff;">{item['name']}</h4>
                        <span class="badge-unesco">UNESCO</span>
                    </div>
                    <p style="margin:2px 0 10px 0; font-size:0.85rem; color:#94a3b8;">📍 {item['loc']}</p>
                    <div class="chip-stat">👥 {item['vol']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Platform Architecture & Scope
    c_left, c_right = st.columns([3, 2])
    with c_left:
        st.markdown("""
        <div class="glass-card">
            <h3 style="margin-top:0; color:#38bdf8;">Problem Definition & Analytical Scope</h3>
            <p style="color:#cbd5e1; line-height:1.6;">
            Tourism across India exhibits pronounced <b>spatial over-concentration</b> (the top 5 monuments capture ~30% of total footfall) 
            and <b>temporal volatility</b> (Post-Monsoon and Winter capture ~60% of annual international visits).
            </p>
            <ul style="color:#cbd5e1; line-height:1.7;">
                <li><b>Longitudinal & Seasonal Demand:</b> Tracking 40 years of international tourism growth and 19 years of quarterly arrival patterns.</li>
                <li><b>Climate Sensitivity Analysis:</b> Examining the empirical influence of temperature deviations and monsoon precipitation on tourist visits.</li>
                <li><b>Supervised Demand Forecasting:</b> Multiple Linear Regression to estimate tourist demand based on structural and climatic attributes.</li>
                <li><b>Unsupervised Destination Clustering:</b> Segmenting destinations via K-Means (k=4) into distinct behavioral archetypes.</li>
                <li><b>Data-Driven Interventions:</b> Evidence-grounded recommendations for circuit decongestion, carrying capacity management, and weather adaptation.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with c_right:
        st.markdown("""
        <div class="glass-card">
            <h3 style="margin-top:0; color:#38bdf8;">Data Sources & Quality Verification</h3>
            <ul style="color:#cbd5e1; line-height:1.7;">
                <li><b>Ministry of Tourism India:</b> Centrally Protected Ticketed Monuments Footfall & State/UT Tourism Compendium.</li>
                <li><b>Open-Meteo ERA5 Reanalysis:</b> Authentic meteorological observations across all 33 Indian destination administrative circles.</li>
                <li><b>Data Cleaning Protocol:</b> Filtered 34 circle subtotals and national totals to prevent double-counting.</li>
                <li><b>Principled Outlier Treatment:</b> Identified 14 statistical upper outliers using IQR (>787k visits). Retained raw numbers for KPI reporting while using log transformations ln(1 + Visits) for regression models.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)


# ==========================================================
# PAGE 2: TOURISM DEMAND ANALYSIS
# ==========================================================
elif selected_page == "2. Tourism Demand Analysis":
    st.markdown('<div class="hero-container"><h1 class="hero-title">Tourism Demand <span class="hero-gradient-text">Analysis</span></h1><p class="hero-subtitle">Longitudinal Growth Trajectories & State-Wise Tourist Footfalls</p></div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📈 Longitudinal Growth (40 Years)", "🗺️ State-Wise Footfall", "👥 Domestic vs Foreign Dynamics"])
    
    with tab1:
        st.subheader("Foreign Tourist Arrivals (1981–2020)")
        fig_fta = eda.get_yearly_trends_plot(df_fta)
        st.plotly_chart(fig_fta, use_container_width=True)
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Pre-Pandemic Peak (2019)", f"{df_fta[df_fta['Year']==2019]['FTAs_Million'].values[0]:.2f} Million")
        c2.metric("Historical CAGR (1991–2019)", "~6.2% Annual Growth")
        c3.metric("Pandemic Impact (2020)", f"{df_fta[df_fta['Year']==2020]['FTA_Growth_Pct'].values[0]:.1f}% YoY")
        
        st.info("**Trend Insight:** International arrivals in India expanded from 1.28M in 1981 to 10.93M in 2019, followed by a sharp contraction during 2020 due to global border closures.")
        
    with tab2:
        st.subheader("State-Level Tourism Demand Comparison")
        col_ctrl, col_chart = st.columns([1, 3])
        with col_ctrl:
            top_n = st.slider("Display Top States", min_value=5, max_value=25, value=12)
            sort_by = st.selectbox("Rank By", ["Total Visits", "Domestic Visits", "Foreign Visits"])
        
        with col_chart:
            df_state_sorted = df_state.copy()
            if sort_by == "Domestic Visits":
                df_state_sorted = df_state_sorted.sort_values(by='Domestic_2019', ascending=False)
            elif sort_by == "Foreign Visits":
                df_state_sorted = df_state_sorted.sort_values(by='Foreign_2019', ascending=False)
            else:
                df_state_sorted = df_state_sorted.sort_values(by='Total_Visits_2019', ascending=False)
                
            fig_state = eda.get_statewise_demand_plot(df_state_sorted, top_n=top_n)
            st.plotly_chart(fig_state, use_container_width=True)
            
        st.markdown("**State-Level Statistics Table (Top 10 States)**")
        st.dataframe(
            df_state[['State', 'Region', 'Domestic_2019', 'Foreign_2019', 'Total_Visits_2019', 'Domestic_Share_2019', 'Foreign_Share_2019']]
            .sort_values(by='Total_Visits_2019', ascending=False).head(10)
            .style.format({'Domestic_2019': '{:,}', 'Foreign_2019': '{:,}', 'Total_Visits_2019': '{:,}', 'Domestic_Share_2019': '{:.2f}%', 'Foreign_Share_2019': '{:.2f}%'}),
            use_container_width=True, hide_index=True
        )

    with tab3:
        st.subheader("Domestic vs Foreign Visitor Composition")
        c1, c2 = st.columns(2)
        with c1:
            fig_pie = px.pie(
                values=[df_dest['Domestic_2019_20'].sum(), df_dest['Foreign_2019_20'].sum()],
                names=['Domestic Visitors', 'Foreign Visitors'],
                title='<b>Overall Monument Visitor Base</b>',
                color_discrete_sequence=['#38bdf8', '#f59e0b'],
                hole=0.4
            )
            fig_pie.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Plus Jakarta Sans, sans-serif', color='#e2e8f0')
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        with c2:
            fig_scatter_share = px.scatter(
                df_filtered, x='Total_Tourist_Visits', y='Foreign_Tourist_Share',
                color='Destination_Type', size='Domestic_2019_20',
                hover_name='Monument_Name', log_x=True,
                title='<b>Volume vs Foreign Visitor Share (%)</b>',
                labels={'Total_Tourist_Visits': 'Total Footfall (Log Scale)', 'Foreign_Tourist_Share': 'Foreign Share (%)'}
            )
            eda.apply_dark_theme(fig_scatter_share)
            st.plotly_chart(fig_scatter_share, use_container_width=True)


# ==========================================================
# PAGE 3: DESTINATION ANALYSIS
# ==========================================================
elif selected_page == "3. Destination Analysis":
    st.markdown('<div class="hero-container"><h1 class="hero-title">Destination <span class="hero-gradient-text">Analysis</span></h1><p class="hero-subtitle">Monuments Footfall, Heritage Visual Spotlight, and Geospatial Mapping</p></div>', unsafe_allow_html=True)
    
    t1, t2, t3, t4 = st.tabs(["📸 Destination Visual Spotlight", "🏆 Top Footfall Rankings", "🗺️ Geospatial Map", "🏛️ Typology & UNESCO Impact"])
    
    with t1:
        st.subheader("📸 Destination Spotlight & Visual Gallery")
        st.caption("Explore real-world destination imagery, architectural attributes, and climate profiles:")
        
        spot_names = sorted(list(df_dest['Monument_Name'].unique()))
        selected_spotlight = st.selectbox("Select Destination to Inspect", spot_names, index=spot_names.index('Taj Mahal') if 'Taj Mahal' in spot_names else 0)
        
        spot_row = df_dest[df_dest['Monument_Name'] == selected_spotlight].iloc[0]
        img_url = get_monument_image(spot_row['Monument_Name'], spot_row['Circle'])
        
        col_img, col_info = st.columns([1, 1])
        with col_img:
            unesco_tag = '<span class="badge-unesco">★ UNESCO World Heritage Site</span>' if spot_row['Is_UNESCO_Site'] == 1 else '<span class="badge-protected">Centrally Protected Monument</span>'
            st.markdown(f"""
            <div class="showcase-card">
                <img src="{img_url}" style="width:100%; height:320px; object-fit:cover;" alt="{spot_row['Monument_Name']}">
                <div style="padding:16px;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <h3 style="margin:0; color:#ffffff;">{spot_row['Monument_Name']}</h3>
                        {unesco_tag}
                    </div>
                    <p style="color:#94a3b8; margin:6px 0 0 0;">📍 {spot_row['Circle']} Circle | State: <b>{spot_row['State']}</b></p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with col_info:
            st.markdown("### Destination Performance Metrics")
            m1, m2 = st.columns(2)
            m1.metric("Annual Footfall", f"{spot_row['Total_Tourist_Visits']:,}")
            m2.metric("Domestic Share", f"{spot_row['Domestic_Tourist_Share']:.1f}%")
            
            m3, m4 = st.columns(2)
            m3.metric("Foreign Share", f"{spot_row['Foreign_Tourist_Share']:.1f}%")
            m4.metric("Annual Avg Temp", f"{spot_row['Annual_Avg_Temp_C']:.1f}°C")
            
            st.markdown("---")
            st.markdown(f"""
            - **Architectural Typology:** `{spot_row['Destination_Type']}`
            - **Footfall Tier:** `{spot_row.get('Footfall_Tier', 'N/A')}`
            - **Annual Precipitation:** `{spot_row['Annual_Total_Rainfall_mm']:.0f} mm`
            - **Assigned Demand Cluster:** `{spot_row.get('Cluster_Name', 'Cluster')}`
            """)
            
    with t2:
        st.subheader("Top Visited Monuments across India")
        top_k = st.slider("Select Top N Destinations", 5, 30, 15)
        fig_dest = eda.get_top_destinations_plot(df_filtered, top_n=top_k)
        st.plotly_chart(fig_dest, use_container_width=True)
        
        display_cols = ['Monument_Name', 'Circle', 'State', 'Destination_Type', 'Total_Tourist_Visits', 'Domestic_Tourist_Share', 'Foreign_Tourist_Share', 'Is_UNESCO_Site']
        st.dataframe(
            df_filtered[display_cols].sort_values(by='Total_Tourist_Visits', ascending=False).head(top_k)
            .style.format({'Total_Tourist_Visits': '{:,}', 'Domestic_Tourist_Share': '{:.2f}%', 'Foreign_Tourist_Share': '{:.2f}%'}),
            use_container_width=True, hide_index=True
        )
        
    with t3:
        st.subheader("Geospatial Map of Monitored Cultural Destinations")
        st.caption("Interactive Folium map of India color-coded by Volume Tier. Click any marker for statistics.")
        
        m = folium.Map(location=[22.0, 79.0], zoom_start=5, tiles="OpenStreetMap")
        color_map = {
            'Tier-1 (>340k)': '#ef4444',
            'Tier-2 (125k-340k)': '#f59e0b',
            'Tier-3 (40k-125k)': '#3b82f6',
            'Tier-4 (<40k)': '#10b981'
        }
        
        for idx, row in df_filtered.iterrows():
            lat = row['Latitude']
            lon = row['Longitude']
            if pd.notnull(lat) and pd.notnull(lon):
                name = row['Monument_Name']
                circle = row['Circle']
                state = row['State']
                visits = row['Total_Tourist_Visits']
                tier = row.get('Footfall_Tier', 'Tier-3 (40k-125k)')
                foreign_pct = row['Foreign_Tourist_Share']
                temp = row['Annual_Avg_Temp_C']
                rain = row['Annual_Total_Rainfall_mm']
                unesco_str = "UNESCO Site" if row['Is_UNESCO_Site'] == 1 else "Non-UNESCO"
                
                popup_html = f"""
                <div style="font-family:sans-serif; min-width:180px; color:#0f172a;">
                    <b>{name}</b><br>
                    <i>{circle} Circle, {state}</i><br>
                    <hr style="margin:4px 0;">
                    <b>Status:</b> {unesco_str}<br>
                    <b>Annual Visits:</b> {visits:,}<br>
                    <b>Foreign Share:</b> {foreign_pct:.1f}%<br>
                    <b>Climate:</b> {temp:.1f}°C, {rain:.0f} mm rain
                </div>
                """
                
                folium.CircleMarker(
                    location=[lat, lon],
                    radius=6 if row['Is_UNESCO_Site'] == 0 else 9,
                    color=color_map.get(tier, '#3b82f6'),
                    fill=True,
                    fill_opacity=0.8,
                    popup=folium.Popup(popup_html, max_width=250),
                    tooltip=f"{name} ({visits:,} visits)"
                ).add_to(m)
                
        st_folium(m, width=1100, height=520)
        
    with t4:
        st.subheader("Architectural Typology & UNESCO Impact")
        col_u1, col_u2 = st.columns(2)
        with col_u1:
            unesco_summary = df_dest.groupby('Is_UNESCO_Site').agg(
                Count=('Monument_Name', 'count'),
                Mean_Footfall=('Total_Tourist_Visits', 'mean'),
                Median_Footfall=('Total_Tourist_Visits', 'median'),
                Avg_Foreign_Share=('Foreign_Tourist_Share', 'mean')
            ).reset_index()
            unesco_summary['Status'] = unesco_summary['Is_UNESCO_Site'].map({1: 'UNESCO World Heritage', 0: 'Non-UNESCO Monument'})
            
            fig_unesco = px.bar(
                unesco_summary, x='Status', y='Mean_Footfall',
                color='Status', color_discrete_sequence=['#818cf8', '#10b981'],
                title='<b>Average Footfall: UNESCO vs Non-UNESCO Sites</b>',
                text_auto='.2s'
            )
            eda.apply_dark_theme(fig_unesco)
            st.plotly_chart(fig_unesco, use_container_width=True)
            
        with col_u2:
            fig_type = px.box(
                df_dest, x='Destination_Type', y='Log_Total_Visits',
                color='Destination_Type',
                title='<b>Footfall Distribution by Typology (Log Scale)</b>',
                labels={'Log_Total_Visits': 'Log(Visits)', 'Destination_Type': 'Typology'}
            )
            eda.apply_dark_theme(fig_type)
            st.plotly_chart(fig_type, use_container_width=True)


# ==========================================================
# PAGE 4: SEASONAL ANALYSIS
# ==========================================================
elif selected_page == "4. Seasonal Analysis":
    st.markdown('<div class="hero-container"><h1 class="hero-title">Seasonal Demand <span class="hero-gradient-text">Analysis</span></h1><p class="hero-subtitle">19 Years of Quarterly Visitor Influx & Peak Periods</p></div>', unsafe_allow_html=True)
    
    fig_qtr = eda.get_seasonal_trends_plot(df_qtr)
    st.plotly_chart(fig_qtr, use_container_width=True)
    
    c1, c2 = st.columns([1, 1])
    with c1:
        st.subheader("Seasonal Arrival Breakdown")
        seasonal_avg = df_qtr.groupby('Season')['Arrival_Share_Pct'].mean().reset_index()
        fig_donut = px.pie(
            seasonal_avg, names='Season', values='Arrival_Share_Pct',
            color='Season',
            color_discrete_map={'Winter': '#10b981', 'Summer': '#f43f5e', 'Monsoon': '#38bdf8', 'Post-Monsoon': '#fbbf24'},
            hole=0.4, title='<b>National Average Arrival Share by Season</b>'
        )
        fig_donut.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Plus Jakarta Sans, sans-serif', color='#e2e8f0')
        )
        st.plotly_chart(fig_donut, use_container_width=True)
        
    with c2:
        st.subheader("Peak vs Trough Findings")
        sec_rec = recommender.get_seasonal_recommendations()
        st.markdown(f"""
        - **Peak Demand Period:** **{sec_rec.get('peak_season', 'Post-Monsoon')} (Q4: Oct–Dec)** captures **{sec_rec.get('peak_share_pct', 30.5)}%** of annual tourist volume.
        - **Secondary Winter Peak:** **Winter (Q1: Jan–Mar)** accounts for **{sec_rec.get('quarterly_breakdown', {}).get('Q1', 28.8)}%** of annual volume.
        - **Summer Trough:** **Summer (Q2: Apr–Jun)** records the lowest visitor influx at **{sec_rec.get('trough_share_pct', 19.1)}%**.
        - **Seasonality Ratio:** Peak demand is **{sec_rec.get('seasonality_ratio', 1.60)}x** higher than the summer slump, highlighting the need for off-season incentives.
        """)
        
        st.markdown("---")
        st.markdown("**Historical Quarterly Share Table (Last 5 Years)**")
        qtr_pivot = df_qtr.pivot(index='Year', columns='Quarter', values='Arrival_Share_Pct').tail(5)
        st.dataframe(qtr_pivot.style.format('{:.1f}%'), use_container_width=True)


# ==========================================================
# PAGE 5: WEATHER & TOURISM
# ==========================================================
elif selected_page == "5. Weather & Tourism":
    st.markdown('<div class="hero-container"><h1 class="hero-title">Weather & Tourism <span class="hero-gradient-text">Demand</span></h1><p class="hero-subtitle">Empirical Relationships Between Climate Variables & Visitor Footfalls</p></div>', unsafe_allow_html=True)
    
    w_tab1, w_tab2, w_tab3 = st.tabs(["🌡️ Temperature vs Demand", "🌧️ Rainfall Impact", "📊 Correlation Matrix"])
    
    with w_tab1:
        st.subheader("Destination Average Temperature vs Footfall")
        fig_temp = eda.get_weather_temp_scatter(df_filtered)
        st.plotly_chart(fig_temp, use_container_width=True)
        
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.markdown("""
            **Thermal Comfort Insights:**
            - The ideal human thermal comfort benchmark for outdoor tourism is around **22.0°C**.
            - Tourist destinations with average annual temperatures between **20°C and 25°C** demonstrate higher baseline visitation and visitor dwell time.
            - Significant deviation from thermal comfort correlates negatively with baseline demand ($\beta = -0.299$).
            """)
        with col_t2:
            comfort_counts = df_dest['Thermal_Comfort_Category'].value_counts().reset_index()
            comfort_counts.columns = ['Thermal Comfort Tier', 'Destinations Count']
            st.dataframe(comfort_counts, use_container_width=True, hide_index=True)
            
    with w_tab2:
        st.subheader("Precipitation & Monsoon Exposure")
        fig_rain = eda.get_weather_rain_scatter(df_filtered)
        st.plotly_chart(fig_rain, use_container_width=True)
        
        st.info("**Precipitation Takeaway:** Moderate annual rainfall (800–1500 mm) supports pleasant green surroundings. In contrast, coastal monsoon regions with precipitation $>2500$ mm (Goa, Kerala) experience seasonal footfall drops during peak monsoon months (July–August).")
        
    with w_tab3:
        st.subheader("Statistical Correlation Matrix")
        fig_corr = eda.get_correlation_heatmap_plot(df_dest)
        st.plotly_chart(fig_corr, use_container_width=True)
        
        st.markdown("""
        **Key Correlations:**
        - **Log Visits vs UNESCO Site:** Positive correlation ($r = +0.52$), confirming international brand appeal.
        - **Log Visits vs Foreign Share:** Positive correlation ($r = +0.33$).
        - **Log Visits vs Thermal Deviation:** Negative correlation ($r = -0.19$).
        """)


# ==========================================================
# PAGE 6: ML DEMAND PREDICTION
# ==========================================================
elif selected_page == "6. ML Demand Prediction":
    st.markdown('<div class="hero-container"><h1 class="hero-title">ML Demand <span class="hero-gradient-text">Prediction</span></h1><p class="hero-subtitle">Multiple Linear Regression Model with Interactive Demand Simulator</p></div>', unsafe_allow_html=True)
    
    m_col1, m_col2 = st.columns([1, 1])
    
    with m_col1:
        st.subheader("Model Evaluation Benchmarks")
        m = regressor.metrics
        
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("Log MAE", f"{m['mae_log']:.3f}", help="Mean Absolute Error on ln(1 + Visits)")
        col_m2.metric("Log RMSE", f"{m['rmse_log']:.3f}", help="Root Mean Squared Error on ln scale")
        col_m3.metric("Log R² Score", f"{m['r2_log']:.3f}", help="Explained variance on log scale")
        
        st.markdown(f"""
        - **5-Fold Cross Validation R²:** `{m['cv_r2_mean']:.3f} ± {m['cv_r2_std']:.3f}`
        - **5-Fold Cross Validation MAE:** `{m['cv_mae_mean']:.3f}`
        - **Holdout Test Set Size:** `{m['n_test']}` destinations (20%)
        - **Actual Scale Test MAE:** `{m['mae_actual']:,.0f}` visits
        """)
        
        st.markdown("---")
        st.subheader("Standardized Feature Coefficients")
        fig_coef = px.bar(
            regressor.coefficients_df, x='Standardized_Coefficient', y='Feature',
            orientation='h', color='Direction',
            color_discrete_map={'Positive (+)': '#10b981', 'Negative (-)': '#f43f5e'},
            title='<b>Impact of Attributes on Tourist Demand</b>'
        )
        eda.apply_dark_theme(fig_coef)
        fig_coef.update_layout(yaxis=dict(autorange="reversed"), margin=dict(l=40, r=40, t=40, b=30))
        st.plotly_chart(fig_coef, use_container_width=True)
        
    with m_col2:
        st.subheader("Interactive Demand Simulator")
        st.caption("Adjust destination parameters to simulate annual visitor footfall:")
        
        with st.form("demand_prediction_form"):
            sim_unesco = st.selectbox("UNESCO World Heritage Site?", [1, 0], format_func=lambda x: "Yes (UNESCO Recognized)" if x == 1 else "No (Standard Monument)")
            sim_type = st.selectbox("Typology", ['Fort & Palace', 'Temple & Religious', 'Mausoleum & Tomb', 'Caves & Rock-Cut', 'Archaeological Ruins', 'Heritage & Memorial'])
            sim_foreign_share = st.slider("Expected Foreign Tourist Share (%)", 0.0, 50.0, 8.5, 0.5)
            sim_avg_temp = st.slider("Annual Average Temperature (°C)", 10.0, 32.0, 24.5, 0.5)
            sim_rainfall = st.slider("Annual Total Rainfall (mm)", 300, 4000, 1100, 50)
            
            submit_pred = st.form_submit_button("Predict Tourist Demand 🚀")
            
        if submit_pred:
            input_features = {
                'Is_UNESCO_Site': sim_unesco,
                'Destination_Type': sim_type,
                'Foreign_Tourist_Share': sim_foreign_share,
                'Domestic_Tourist_Share': 100.0 - sim_foreign_share,
                'Annual_Avg_Temp_C': sim_avg_temp,
                'Annual_Total_Rainfall_mm': sim_rainfall,
                'Temp_Ideal_Deviation': abs(sim_avg_temp - 22.0),
                'Monsoon_Rainfall_mm': sim_rainfall * 0.70
            }
            
            pred_result = regressor.predict_visits(input_features)
            p_val = pred_result['predicted_total_visits']
            p_low = pred_result['prediction_interval_lower']
            p_high = pred_result['prediction_interval_upper']
            
            st.success("### Prediction Calculated!")
            p1, p2, p3 = st.columns(3)
            p1.metric("Predicted Annual Visits", f"{p_val:,}")
            p2.metric("Lower Bound (-1 RMSE)", f"{p_low:,}")
            p3.metric("Upper Bound (+1 RMSE)", f"{p_high:,}")


# ==========================================================
# PAGE 7: DESTINATION CLUSTERING
# ==========================================================
elif selected_page == "7. Destination Clustering":
    st.markdown('<div class="hero-container"><h1 class="hero-title">Destination <span class="hero-gradient-text">Clustering</span></h1><p class="hero-subtitle">K-Means Segmentation of Indian Destinations Based on Demand Behaviors</p></div>', unsafe_allow_html=True)
    
    cl_t1, cl_t2, cl_t3 = st.tabs(["🎯 Cluster Map & PCA", "📈 Validation Curves", "📋 Cluster Profiles"])
    
    with cl_t1:
        st.subheader("Destination Clusters in PCA Space")
        fig_pca = px.scatter(
            df_dest, x='PCA_Dim1', y='PCA_Dim2',
            color='Cluster_Name',
            hover_name='Monument_Name',
            hover_data=['Circle', 'State', 'Total_Tourist_Visits', 'Foreign_Tourist_Share', 'Annual_Avg_Temp_C'],
            title='<b>2D PCA Projection of Destination Demand Clusters (k=4)</b>',
            labels={'PCA_Dim1': 'Principal Component 1 (Volume & Prominence)', 'PCA_Dim2': 'Principal Component 2 (Climate & Rainfall)'}
        )
        eda.apply_dark_theme(fig_pca)
        st.plotly_chart(fig_pca, use_container_width=True)
        
        st.markdown("""
        **Discovered Cluster Archetypes:**
        - **Cluster 0 (Global Icons):** High volume, high foreign share, UNESCO hubs (Taj Mahal, Qutub Minar, Agra Fort).
        - **Cluster 1 (Domestic Hubs):** Large-scale domestic cultural destinations (Konark, Golconda, Charminar).
        - **Cluster 2 (Monsoon Enclaves):** High rainfall coastal & Ghats sites (Goa, Kerala, Mumbai caves).
        - **Cluster 3 (Emerging Heritage):** Niche regional archaeological ruins with expansion potential.
        """)
        
    with cl_t2:
        st.subheader("Optimal Clusters Determination ($k$)")
        k_eval_df = clusterer.k_evaluation_df
        c1, c2 = st.columns(2)
        with c1:
            fig_elbow = px.line(k_eval_df, x='k', y='Inertia', markers=True, title='<b>Elbow Method (Inertia vs k)</b>')
            fig_elbow.add_vline(x=4, line_dash='dash', line_color='#f43f5e', annotation_text='Selected k=4')
            eda.apply_dark_theme(fig_elbow)
            st.plotly_chart(fig_elbow, use_container_width=True)
        with c2:
            fig_sil = px.line(k_eval_df, x='k', y='Silhouette_Score', markers=True, title='<b>Silhouette Analysis vs k</b>')
            fig_sil.add_vline(x=4, line_dash='dash', line_color='#f43f5e', annotation_text='Selected k=4 (0.442)')
            eda.apply_dark_theme(fig_sil)
            st.plotly_chart(fig_sil, use_container_width=True)
            
    with cl_t3:
        st.subheader("Cluster Profiles Summary")
        st.dataframe(clusterer.cluster_summary_df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        st.subheader("Inspect Destinations by Cluster")
        chosen_cluster = st.selectbox("Select Cluster Archetype", df_dest['Cluster_Name'].dropna().unique())
        cluster_members = df_dest[df_dest['Cluster_Name'] == chosen_cluster]
        st.dataframe(
            cluster_members[['Monument_Name', 'Circle', 'State', 'Destination_Type', 'Total_Tourist_Visits', 'Domestic_Tourist_Share', 'Foreign_Tourist_Share', 'Annual_Avg_Temp_C', 'Annual_Total_Rainfall_mm', 'Is_UNESCO_Site']]
            .sort_values(by='Total_Tourist_Visits', ascending=False)
            .style.format({'Total_Tourist_Visits': '{:,}', 'Domestic_Tourist_Share': '{:.2f}%', 'Foreign_Tourist_Share': '{:.2f}%'}),
            use_container_width=True, hide_index=True
        )


# ==========================================================
# PAGE 8: INSIGHTS & RECOMMENDATIONS
# ==========================================================
elif selected_page == "8. Insights & Recommendations":
    st.markdown('<div class="hero-container"><h1 class="hero-title">Insights & <span class="hero-gradient-text">Recommendations</span></h1><p class="hero-subtitle">Empirical Recommendations Calculated Directly from Analytical Findings</p></div>', unsafe_allow_html=True)
    
    r_tab1, r_tab2, r_tab3 = st.tabs(["🏛️ Strategic Interventions", "🚦 Decongestion & Weather", "🧭 Destination Recommender"])
    
    with r_tab1:
        st.subheader("Cluster-Specific Strategic Roadmaps")
        for s in recommender.get_cluster_strategies():
            with st.expander(f"📌 {s['archetype']} — Focus: {s['focus']}", expanded=True):
                for bullet in s['strategies']:
                    st.markdown(f"- {bullet}")
                    
    with r_tab2:
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Circuit Decongestion Strategy")
            for item in recommender.get_decongestion_recommendations():
                st.markdown(f"- {item}")
        with c2:
            st.subheader("Climate & Weather Adaptation")
            for item in recommender.get_weather_adaptive_recommendations():
                st.markdown(f"- {item}")
                
        st.markdown("---")
        st.subheader("Seasonal Scheduling Advice")
        sec_recs = recommender.get_seasonal_recommendations()
        for item in sec_recs.get('recommendations', []):
            st.markdown(f"- {item}")

    with r_tab3:
        st.subheader("🧭 Interactive Destination Recommender")
        st.caption("Find curated Indian destinations matching your travel preferences:")
        
        rc1, rc2, rc3, rc4 = st.columns(4)
        with rc1:
            pref_state = st.selectbox("State", ['All'] + sorted(list(df_dest['State'].unique())), key="rec_st")
        with rc2:
            pref_type = st.selectbox("Typology", ['All'] + sorted(list(df_dest['Destination_Type'].unique())), key="rec_typ")
        with rc3:
            pref_crowd = st.selectbox("Crowd Level", ['Any', 'Low Crowds (<100k)', 'Moderate (100k-500k)', 'High / Iconic (>500k)'], key="rec_crd")
        with rc4:
            pref_weather = st.selectbox("Climate Comfort", ['Any', 'Cool (<20°C)', 'Moderate (20-26°C)', 'Warm (>26°C)'], key="rec_wth")
            
        user_prefs = {
            'state': pref_state,
            'destination_type': pref_type,
            'crowd_preference': pref_crowd,
            'weather_preference': pref_weather
        }
        
        matches = recommender.recommend_destinations(user_prefs, top_k=6)
        if not matches.empty:
            st.markdown(f"**Found {len(matches)} recommended destinations:**")
            
            grid_cols = st.columns(3)
            for idx, (_, r) in enumerate(matches.iterrows()):
                target_col = grid_cols[idx % 3]
                img = get_monument_image(r['Monument_Name'], r['Circle'])
                badge_html = '<span class="badge-unesco">★ UNESCO</span>' if r['Is_UNESCO_Site'] == 1 else '<span class="badge-protected">Protected</span>'
                
                with target_col:
                    st.markdown(f"""
                    <div class="showcase-card">
                        <img src="{img}" class="showcase-img" style="height:170px;" alt="{r['Monument_Name']}">
                        <div class="showcase-content">
                            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                                <h4 style="margin:0; font-size:1.05rem; color:#ffffff;">{r['Monument_Name']}</h4>
                                {badge_html}
                            </div>
                            <p style="margin:2px 0 8px 0; font-size:0.8rem; color:#94a3b8;">📍 {r['Circle']} Circle, {r['State']}</p>
                            <div style="font-size:0.82rem; color:#cbd5e1; line-height:1.6;">
                                👥 <b>Visits:</b> {r['Total_Tourist_Visits']:,}<br>
                                🌡️ <b>Temp:</b> {r['Annual_Avg_Temp_C']:.1f}°C | 🌧️ {r['Annual_Total_Rainfall_mm']:.0f} mm
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("No destinations matched the strict filters. Try selecting 'Any' for some criteria.")
