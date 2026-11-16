"""
Feature Extraction and Feature Engineering Module
DS2004: Fundamentals of Data Science
Project: Tourist Demand Pattern Analysis Across Indian Destinations

Creates domain-specific tourism demand and meteorological features:
- Tourist volume aggregates and shares (Domestic Share, Foreign Share)
- Tourist growth rates and domestic-to-foreign ratios
- Thermal comfort deviation from ideal human comfort (22°C)
- Climate and rainfall classification indices
- UNESCO World Heritage site identification
- Destination architectural & cultural typology classification
- Logarithmic transforms and feature scaling for linear models
"""

import os
import numpy as np
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

PROCESSED_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "processed")

# Canonical list of UNESCO World Heritage Cultural/Natural sites in India present in ASI ticketed list
UNESCO_KEYWORDS = [
    'taj mahal', 'agra fort', 'fatehpur sikri', 'qutub minar', 'red fort', 'humayun',
    'konark', 'mamallapuram', 'ellora', 'ajanta', 'elephanta', 'khajuraho', 'sanchi',
    'hampi', 'pattadakal', 'mahabodhi', 'brihadisvara', 'brihadeeswarar', 'chittorgarh',
    'kumbhalgarh', 'ran-ki-vav', 'champaner', 'dholavira', 'nalanda'
]


def classify_destination_type(name: str) -> str:
    """Classifies monument into structural/cultural typologies."""
    n = str(name).lower()
    if any(k in n for k in ['fort', 'palace', 'garhi', 'kotla', 'red fort', 'agra fort', 'kumbhalgarh', 'chittor']):
        return 'Fort & Palace'
    elif any(k in n for k in ['temple', 'mandir', 'sun temple', 'shore temple', 'brihad', 'devalaya']):
        return 'Temple & Religious'
    elif any(k in n for k in ['cave', 'caves', 'rock-cut', 'ajanta', 'ellora', 'elephanta', 'kanheri', 'karla']):
        return 'Caves & Rock-Cut'
    elif any(k in n for k in ['tomb', 'mausoleum', 'taj mahal', 'sikandra', 'itimad', 'humayun', 'safdarjung']):
        return 'Mausoleum & Tomb'
    elif any(k in n for k in ['stupa', 'ruins', 'excavated', 'site', 'hampi', 'nalanda', 'sarnath', 'lothal']):
        return 'Archaeological Ruins'
    else:
        return 'Heritage & Memorial'


def classify_thermal_comfort(temp: float) -> str:
    """Classifies annual average temperature into tourism comfort tiers."""
    if temp < 15.0:
        return 'Cool / Alpine (<15°C)'
    elif temp <= 25.0:
        return 'Comfortable / Optimal (15-25°C)'
    elif temp <= 27.5:
        return 'Warm / Subtropical (25-27.5°C)'
    else:
        return 'Hot / Tropical (>27.5°C)'


def classify_rainfall_severity(rain: float) -> str:
    """Classifies annual precipitation into tourism rainfall exposure zones."""
    if rain < 800.0:
        return 'Arid / Low Rainfall (<800 mm)'
    elif rain <= 1500.0:
        return 'Moderate Rainfall (800-1500 mm)'
    elif rain <= 2500.0:
        return 'Heavy Rainfall (1500-2500 mm)'
    else:
        return 'Very Heavy / Coastal Monsoon (>2500 mm)'


def engineer_destination_features(df_dest: pd.DataFrame, df_state: pd.DataFrame = None) -> pd.DataFrame:
    """
    Computes all advanced domain features on the cleaned destination dataset.
    """
    df = df_dest.copy()
    
    # 1. Total Tourist Visits
    df['Total_Tourist_Visits'] = df['Domestic_2019_20'] + df['Foreign_2019_20']
    
    # 2. Tourist Shares (%)
    df['Domestic_Tourist_Share'] = (
        (df['Domestic_2019_20'] / (df['Total_Tourist_Visits'] + 1e-9)) * 100.0
    ).round(2)
    df['Foreign_Tourist_Share'] = (
        (df['Foreign_2019_20'] / (df['Total_Tourist_Visits'] + 1e-9)) * 100.0
    ).round(2)
    
    # 3. Domestic to Foreign Ratio
    df['Domestic_to_Foreign_Ratio'] = (
        df['Domestic_2019_20'] / (df['Foreign_2019_20'] + 1.0)
    ).round(2)
    
    # 4. Growth Rates
    df['Tourist_Growth_Rate_Domestic'] = df['Growth_Domestic_Pct']
    df['Tourist_Growth_Rate_Foreign'] = df['Growth_Foreign_Pct']
    
    # Overall 2019 to 2020 growth rate
    total_2020 = df['Domestic_2020_21'] + df['Foreign_2020_21']
    df['Overall_Growth_Rate'] = (
        ((total_2020 - df['Total_Tourist_Visits']) / (df['Total_Tourist_Visits'] + 1e-9)) * 100.0
    ).round(2)
    
    # 5. Meteorological & Climate Comfort Features
    # Ideal human thermal comfort benchmark for outdoor tourism is ~22°C (ASHRAE / Tourism Climate Index standard)
    df['Temp_Ideal_Deviation'] = (df['Annual_Avg_Temp_C'] - 22.0).abs().round(2)
    df['Annual_Temp_Range'] = (df['Max_Temp_C'] - df['Min_Temp_C']).round(2)
    df['Monsoon_Rainfall_Share'] = (
        (df['Monsoon_Rainfall_mm'] / (df['Annual_Total_Rainfall_mm'] + 1e-5)) * 100.0
    ).round(2)
    
    df['Thermal_Comfort_Category'] = df['Annual_Avg_Temp_C'].apply(classify_thermal_comfort)
    df['Rainfall_Severity_Category'] = df['Annual_Total_Rainfall_mm'].apply(classify_rainfall_severity)
    
    # 6. UNESCO World Heritage Site Flag
    df['Is_UNESCO_Site'] = df['Monument_Name'].apply(
        lambda name: int(any(kw in str(name).lower() for kw in UNESCO_KEYWORDS))
    )
    
    # 7. Destination Cultural/Structural Typology
    df['Destination_Type'] = df['Monument_Name'].apply(classify_destination_type)
    
    # 8. State Macro Volume Integration (if state data provided)
    if df_state is not None:
        state_vol_map = dict(zip(df_state['State'], df_state['Total_Visits_2019']))
        df['State_Tourism_Volume'] = df['State'].map(state_vol_map).fillna(df_state['Total_Visits_2019'].median())
        df['Log_State_Tourism_Volume'] = np.log1p(df['State_Tourism_Volume'])
        
    # 9. Logarithmic transformations for ML regression
    df['Log_Total_Visits'] = np.log1p(df['Total_Tourist_Visits'])
    df['Log_Domestic_Visits'] = np.log1p(df['Domestic_2019_20'])
    df['Log_Foreign_Visits'] = np.log1p(df['Foreign_2019_20'])
    
    # 10. Footfall Volume Tier
    df['Footfall_Tier'] = pd.qcut(
        df['Total_Tourist_Visits'],
        q=4,
        labels=['Tier-4 (<40k)', 'Tier-3 (40k-125k)', 'Tier-2 (125k-340k)', 'Tier-1 (>340k)']
    )
    
    logger.info(f"Engineered features for {len(df)} destinations. Total features: {df.shape[1]}")
    return df


def engineer_all_and_save():
    """
    Loads cleaned datasets, executes feature engineering, and saves enriched data.
    """
    dest_path = os.path.join(PROCESSED_DIR, "destinations_cleaned.csv")
    state_path = os.path.join(PROCESSED_DIR, "statewise_tourism_cleaned.csv")
    
    if not os.path.exists(dest_path):
        from src.cleaner import clean_all_and_save
        clean_all_and_save()
        
    df_dest = pd.read_csv(dest_path)
    df_state = pd.read_csv(state_path) if os.path.exists(state_path) else None
    
    df_featured = engineer_destination_features(df_dest, df_state)
    
    out_path = os.path.join(PROCESSED_DIR, "destinations_featured.csv")
    df_featured.to_csv(out_path, index=False)
    logger.info(f"Saved featured destination dataset to {out_path} ({df_featured.shape})")
    return df_featured


if __name__ == "__main__":
    engineer_all_and_save()
