"""
Data Cleaning, Integration, and Outlier Treatment Module
DS2004: Fundamentals of Data Science
Project: Tourist Demand Pattern Analysis Across Indian Destinations

Handles:
- Missing values and datatype parsing
- Elimination of aggregate subtotal and grand total records
- State and destination name standardization
- Integration of tourism and meteorological datasets
- Outlier detection (IQR, Z-score) and principled treatment (Log transform & Capping)
"""

import os
import re
import numpy as np
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

PROCESSED_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "processed")
OUTPUTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "outputs", "tables")


def clean_monuments_data(df_monuments: pd.DataFrame, df_weather: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans ASI monument dataset and merges with authentic weather data.
    Filters out circle 'Total' and national 'Grand Total' aggregate rows.
    """
    df = df_monuments.copy()
    
    # 1. Filter out aggregate rows (Total and Grand Total)
    is_aggregate = df['Name of the Monument'].astype(str).str.strip().str.lower().isin(['total', 'grand total'])
    num_aggregates = is_aggregate.sum()
    df = df[~is_aggregate].copy()
    logger.info(f"Filtered out {num_aggregates} aggregate subtotal/total rows. Retained {len(df)} monuments.")
    
    # 2. Standardize column names
    col_mapping = {
        'Circle': 'Circle',
        'Name of the Monument': 'Monument_Name',
        'Domestic-2019-20': 'Domestic_2019_20',
        'Foreign-2019-20': 'Foreign_2019_20',
        'Domestic-2020-21': 'Domestic_2020_21',
        'Foreign-2020-21': 'Foreign_2020_21',
        '% Growth 2021-21/2019-20-Domestic': 'Growth_Domestic_Pct',
        '% Growth 2021-21/2019-20-Foreign': 'Growth_Foreign_Pct'
    }
    df.rename(columns=col_mapping, inplace=True)
    
    # 3. Clean string names
    df['Circle'] = df['Circle'].astype(str).str.strip()
    df['Monument_Name'] = df['Monument_Name'].astype(str).str.strip()
    
    # 4. Clean numeric columns and growth rates
    for col in ['Domestic_2019_20', 'Foreign_2019_20', 'Domestic_2020_21', 'Foreign_2020_21']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(np.int64)
        
    for col in ['Growth_Domestic_Pct', 'Growth_Foreign_Pct']:
        df[col] = (
            df[col].astype(str)
            .str.replace('%', '', regex=False)
            .str.replace(',', '', regex=False)
            .str.strip()
        )
        df[col] = pd.to_numeric(df[col], errors='coerce')
        # Impute missing growth rates with median
        median_val = df[col].median()
        df[col] = df[col].fillna(median_val)
        
    # 5. Merge with authentic weather dataset on 'Circle'
    weather_clean = df_weather.copy()
    weather_clean['Circle'] = weather_clean['Circle'].astype(str).str.strip()
    
    merged = pd.merge(df, weather_clean, on='Circle', how='left')
    logger.info(f"Merged monuments with weather data: {merged.shape[0]} rows, {merged.shape[1]} columns")
    
    # 6. Basic visit calculations
    merged['Total_Visits_2019'] = merged['Domestic_2019_20'] + merged['Foreign_2019_20']
    merged['Total_Visits_2020'] = merged['Domestic_2020_21'] + merged['Foreign_2020_21']
    
    # 7. Outlier Detection using IQR Method
    q1 = merged['Total_Visits_2019'].quantile(0.25)
    q3 = merged['Total_Visits_2019'].quantile(0.75)
    iqr = q3 - q1
    upper_whisker = q3 + 1.5 * iqr
    lower_whisker = max(0, q1 - 1.5 * iqr)
    
    # Z-score outlier detection
    mean_val = merged['Total_Visits_2019'].mean()
    std_val = merged['Total_Visits_2019'].std()
    merged['Z_Score_Visits'] = (merged['Total_Visits_2019'] - mean_val) / std_val
    
    merged['Is_Outlier_IQR'] = merged['Total_Visits_2019'] > upper_whisker
    merged['Is_Outlier_Zscore'] = merged['Z_Score_Visits'].abs() > 3.0
    
    outlier_count = merged['Is_Outlier_IQR'].sum()
    logger.info(f"Outlier detection: {outlier_count} monuments detected as statistical upper outliers (IQR > {upper_whisker:.0f}).")
    
    # 8. Principled Outlier Treatment
    # We do NOT drop real heritage wonders like the Taj Mahal.
    # Instead, we create mathematically sound representations:
    # a. Logarithmic transform (reduces positive skewness, stabilizes variance)
    merged['Log_Total_Visits'] = np.log1p(merged['Total_Visits_2019'])
    merged['Log_Domestic_Visits'] = np.log1p(merged['Domestic_2019_20'])
    merged['Log_Foreign_Visits'] = np.log1p(merged['Foreign_2019_20'])
    
    # b. Winsorized / Capped version at 95th percentile
    p95 = merged['Total_Visits_2019'].quantile(0.95)
    merged['Total_Visits_Capped'] = merged['Total_Visits_2019'].clip(upper=p95)
    
    return merged


def clean_statewise_data(df_statewise: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans State/UT-wise domestic and foreign tourist visits dataset.
    Standardizes state naming conventions and assigns geographical zones.
    """
    df = df_statewise.copy()
    
    # 1. Filter out Grand Total row
    df = df[~df['States/UTs'].astype(str).str.strip().str.lower().isin(['grand total'])].copy()
    
    # 2. Standardize column names
    col_mapping = {
        'States/UTs': 'State',
        'Domestic -2019': 'Domestic_2019',
        'Foreign - 2019': 'Foreign_2019',
        'Domestic -2020': 'Domestic_2020',
        'Foreign - 2020': 'Foreign_2020',
        'Growth rate - DTV  2020/19': 'Growth_DTV_Pct',
        'Growth rate - FTV 2020/19': 'Growth_FTV_Pct'
    }
    df.rename(columns=col_mapping, inplace=True)
    if 'S. No.' in df.columns:
        df.drop(columns=['S. No.'], inplace=True)
        
    # 3. Clean and map state names
    state_cleanup = {
        'A&N Island': 'Andaman & Nicobar Islands',
        'Telengana': 'Telangana',
        'J&K': 'Jammu & Kashmir',
        'Lakshdweep': 'Lakshadweep'
    }
    df['State'] = df['State'].astype(str).str.strip().replace(state_cleanup)
    
    # 4. Clean numeric columns and growth rates
    for col in ['Domestic_2019', 'Foreign_2019', 'Domestic_2020', 'Foreign_2020']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(np.int64)
        
    for col in ['Growth_DTV_Pct', 'Growth_FTV_Pct']:
        df[col] = (
            df[col].astype(str)
            .str.replace('%', '', regex=False)
            .str.replace(',', '', regex=False)
            .str.strip()
        )
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
    # 5. Feature columns for state totals and shares
    df['Total_Visits_2019'] = df['Domestic_2019'] + df['Foreign_2019']
    df['Total_Visits_2020'] = df['Domestic_2020'] + df['Foreign_2020']
    df['Domestic_Share_2019'] = (df['Domestic_2019'] / df['Total_Visits_2019'] * 100).round(2)
    df['Foreign_Share_2019'] = (df['Foreign_2019'] / df['Total_Visits_2019'] * 100).round(2)
    df['Overall_Growth_Pct'] = (
        (df['Total_Visits_2020'] - df['Total_Visits_2019']) / df['Total_Visits_2019'] * 100
    ).round(2)
    
    # 6. Assign Indian Geographical Regions
    region_map = {
        'Delhi': 'Northern', 'Haryana': 'Northern', 'Himachal Pradesh': 'Northern',
        'Jammu & Kashmir': 'Northern', 'Ladakh': 'Northern', 'Punjab': 'Northern',
        'Rajasthan': 'Northern', 'Uttar Pradesh': 'Northern', 'Uttarakhand': 'Northern',
        'Chandigarh': 'Northern',
        'Andhra Pradesh': 'Southern', 'Karnataka': 'Southern', 'Kerala': 'Southern',
        'Tamil Nadu': 'Southern', 'Telangana': 'Southern', 'Puducherry': 'Southern',
        'Lakshadweep': 'Southern',
        'Goa': 'Western', 'Gujarat': 'Western', 'Maharashtra': 'Western',
        'Dadra & Nagar Haveli': 'Western', 'Daman & Diu': 'Western',
        'Bihar': 'Eastern', 'Jharkhand': 'Eastern', 'Odisha': 'Eastern', 'West Bengal': 'Eastern',
        'Chhattisgarh': 'Central', 'Madhya Pradesh': 'Central',
        'Arunachal Pradesh': 'North-Eastern', 'Assam': 'North-Eastern', 'Manipur': 'North-Eastern',
        'Meghalaya': 'North-Eastern', 'Mizoram': 'North-Eastern', 'Nagaland': 'North-Eastern',
        'Sikkim': 'North-Eastern', 'Tripura': 'North-Eastern',
        'Andaman & Nicobar Islands': 'Islands'
    }
    df['Region'] = df['State'].map(region_map).fillna('Other')
    
    return df


def clean_quarterly_data(df_quarterly: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans and melts quarterly foreign tourist arrivals dataset into a tidy time-series format.
    """
    df = df_quarterly.copy()
    
    # Clean column names
    col_mapping = {
        'Year': 'Year',
        'Arrivals': 'Total_Annual_Arrivals',
        '% Distribution by Quarter - 1st Quarter (Jan-Mar)': 'Q1_Jan_Mar_Pct',
        '% Distribution by Quarter - 2nd Quarter(Apr-June)': 'Q2_Apr_Jun_Pct',
        '% Distribution by Quarter - 3rd Quarter (July-Sep)': 'Q3_Jul_Sep_Pct',
        '% Distribution by Quarter - 4th Quarter (Oct-Dec)': 'Q4_Oct_Dec_Pct'
    }
    df.rename(columns=col_mapping, inplace=True)
    
    # Reshape from wide to long format for seasonal analysis
    melted = []
    season_info = [
        ('Q1', 'Jan-Mar', 'Winter', 'Q1_Jan_Mar_Pct'),
        ('Q2', 'Apr-Jun', 'Summer', 'Q2_Apr_Jun_Pct'),
        ('Q3', 'Jul-Sep', 'Monsoon', 'Q3_Jul_Sep_Pct'),
        ('Q4', 'Oct-Dec', 'Post-Monsoon', 'Q4_Oct_Dec_Pct')
    ]
    
    for idx, row in df.iterrows():
        year = int(row['Year'])
        total_arr = float(row['Total_Annual_Arrivals'])
        for q_code, q_months, season, pct_col in season_info:
            pct_val = float(row[pct_col])
            est_arrivals = (total_arr * pct_val) / 100.0
            melted.append({
                'Year': year,
                'Quarter': q_code,
                'Quarter_Months': q_months,
                'Season': season,
                'Arrival_Share_Pct': pct_val,
                'Estimated_Arrivals': round(est_arrivals)
            })
            
    df_tidy = pd.DataFrame(melted)
    return df_tidy


def clean_fta_longitudinal_data(df_fta: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans 40-year longitudinal FTA data (1981-2020).
    """
    df = df_fta.copy()
    col_mapping = {
        'Year': 'Year',
        'FTAs in India (in million)': 'FTAs_Million',
        '%- change over previous year': 'FTA_Growth_Pct',
        'NRIs arrivals in India (in million)': 'NRIs_Million',
        'ITAs in India  (in million)': 'ITAs_Million'
    }
    df.rename(columns=col_mapping, inplace=True)
    df = df[['Year', 'FTAs_Million', 'FTA_Growth_Pct', 'NRIs_Million', 'ITAs_Million']].copy()
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce').astype(np.int64)
    df['FTAs_Million'] = pd.to_numeric(df['FTAs_Million'], errors='coerce')
    df['FTA_Growth_Pct'] = pd.to_numeric(df['FTA_Growth_Pct'], errors='coerce')
    return df


def clean_all_and_save():
    """
    Executes full data cleaning pipeline and writes processed datasets.
    """
    from src.data_loader import (
        load_monuments_data,
        load_statewise_data,
        load_quarterly_data,
        load_fta_longitudinal_data,
        load_weather_data
    )
    
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    
    df_raw_m = load_monuments_data()
    df_raw_w = load_weather_data()
    df_raw_s = load_statewise_data()
    df_raw_q = load_quarterly_data()
    df_raw_fta = load_fta_longitudinal_data()
    
    # Clean datasets
    df_clean_destinations = clean_monuments_data(df_raw_m, df_raw_w)
    df_clean_statewise = clean_statewise_data(df_raw_s)
    df_clean_quarterly = clean_quarterly_data(df_raw_q)
    df_clean_fta = clean_fta_longitudinal_data(df_raw_fta)
    
    # Save cleaned files
    dest_path = os.path.join(PROCESSED_DIR, "destinations_cleaned.csv")
    state_path = os.path.join(PROCESSED_DIR, "statewise_tourism_cleaned.csv")
    qtr_path = os.path.join(PROCESSED_DIR, "seasonal_quarterly_cleaned.csv")
    fta_path = os.path.join(PROCESSED_DIR, "longitudinal_fta_cleaned.csv")
    
    df_clean_destinations.to_csv(dest_path, index=False)
    df_clean_statewise.to_csv(state_path, index=False)
    df_clean_quarterly.to_csv(qtr_path, index=False)
    df_clean_fta.to_csv(fta_path, index=False)
    
    # Save outlier documentation table
    outliers_df = df_clean_destinations[df_clean_destinations['Is_Outlier_IQR']].sort_values(
        by='Total_Visits_2019', ascending=False
    )[[
        'Monument_Name', 'Circle', 'State', 'Domestic_2019_20',
        'Foreign_2019_20', 'Total_Visits_2019', 'Z_Score_Visits'
    ]]
    outliers_path = os.path.join(OUTPUTS_DIR, "outliers_documentation.csv")
    outliers_df.to_csv(outliers_path, index=False)
    
    logger.info(f"Cleaned datasets saved to {PROCESSED_DIR}")
    logger.info(f"Outlier documentation table saved to {outliers_path}")
    
    return {
        "destinations": df_clean_destinations,
        "statewise": df_clean_statewise,
        "quarterly": df_clean_quarterly,
        "fta": df_clean_fta
    }


if __name__ == "__main__":
    clean_all_and_save()
