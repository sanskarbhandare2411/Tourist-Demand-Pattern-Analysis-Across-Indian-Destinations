"""
Data Acquisition and Ingestion Module
DS2004: Fundamentals of Data Science
Project: Tourist Demand Pattern Analysis Across Indian Destinations

Loads authentic datasets from official sources:
1. Ministry of Tourism India - ASI Ticketed Monuments Footfall (2019-2021)
2. Ministry of Tourism India - State/UT-wise Domestic and Foreign Tourist Visits (2019-2020)
3. Ministry of Tourism India - Quarterly Foreign Tourist Arrivals (2001-2019)
4. Ministry of Tourism India - Longitudinal FTAs, NRIs, and ITAs (1981-2020)
5. Open-Meteo Historical Meteorological Archive - Temperature & Precipitation for Indian Destination Circles
6. Ministry of Tourism India - International Arrivals by Region and Purpose of Travel
7. Ministry of Tourism India - Age Group Demographic Distribution
"""

import os
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

RAW_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "raw")


def load_monuments_data(filepath: str = None) -> pd.DataFrame:
    """Load ASI centrally protected ticketed monuments footfall dataset."""
    if filepath is None:
        filepath = os.path.join(RAW_DIR, "India-Tourism-Statistics-2021-monuments.csv")
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Monuments data file not found at: {filepath}")
    df = pd.read_csv(filepath)
    logger.info(f"Loaded monuments data: {df.shape[0]} rows, {df.shape[1]} columns")
    return df


def load_statewise_data(filepath: str = None) -> pd.DataFrame:
    """Load State/UT-wise domestic and foreign tourist visits dataset."""
    if filepath is None:
        filepath = os.path.join(RAW_DIR, "India-Tourism-Statistics-statewise_2019-2020_domestic_foreign.csv")
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"State-wise data file not found at: {filepath}")
    df = pd.read_csv(filepath)
    logger.info(f"Loaded state-wise data: {df.shape[0]} rows, {df.shape[1]} columns")
    return df


def load_quarterly_data(filepath: str = None) -> pd.DataFrame:
    """Load 19-year quarterly seasonal tourist arrival distribution dataset."""
    if filepath is None:
        filepath = os.path.join(RAW_DIR, "India-Tourism-Statistics-2001-2019-quaterly.csv")
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Quarterly seasonal data file not found at: {filepath}")
    df = pd.read_csv(filepath)
    logger.info(f"Loaded quarterly data: {df.shape[0]} rows, {df.shape[1]} columns")
    return df


def load_fta_longitudinal_data(filepath: str = None) -> pd.DataFrame:
    """Load 40-year longitudinal foreign tourist arrival time series (1981-2020)."""
    if filepath is None:
        filepath = os.path.join(RAW_DIR, "India-Tourism-Statistics-1981-2020-fta_nri_ita.csv")
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"FTA longitudinal data file not found at: {filepath}")
    df = pd.read_csv(filepath)
    logger.info(f"Loaded longitudinal FTA data: {df.shape[0]} rows, {df.shape[1]} columns")
    return df


def load_weather_data(filepath: str = None) -> pd.DataFrame:
    """Load authentic historical weather data fetched from Open-Meteo Archive API."""
    if filepath is None:
        filepath = os.path.join(RAW_DIR, "india_weather_historical.csv")
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Weather data file not found at: {filepath}")
    df = pd.read_csv(filepath)
    logger.info(f"Loaded historical weather data: {df.shape[0]} circles, {df.shape[1]} columns")
    return df


def load_purpose_data(filepath: str = None) -> pd.DataFrame:
    """Load international arrivals by region and purpose of visit."""
    if filepath is None:
        filepath = os.path.join(RAW_DIR, "India-Tourism-Statistics-2019_region-and-reason.csv")
    if os.path.exists(filepath):
        df = pd.read_csv(filepath)
        logger.info(f"Loaded purpose data: {df.shape[0]} rows, {df.shape[1]} columns")
        return df
    return pd.DataFrame()


def load_agegroup_data(filepath: str = None) -> pd.DataFrame:
    """Load international tourist age demographics data."""
    if filepath is None:
        filepath = os.path.join(RAW_DIR, "India-Tourism-Statistics-2001-2019-agegroup.csv")
    if os.path.exists(filepath):
        df = pd.read_csv(filepath)
        logger.info(f"Loaded age group data: {df.shape[0]} rows, {df.shape[1]} columns")
        return df
    return pd.DataFrame()


def load_all_raw_data() -> dict:
    """Convenience function to load all raw datasets into a dictionary."""
    return {
        "monuments": load_monuments_data(),
        "statewise": load_statewise_data(),
        "quarterly": load_quarterly_data(),
        "fta_longitudinal": load_fta_longitudinal_data(),
        "weather": load_weather_data(),
        "purpose": load_purpose_data(),
        "agegroup": load_agegroup_data()
    }


if __name__ == "__main__":
    datasets = load_all_raw_data()
    for name, df in datasets.items():
        print(f"Dataset '{name}': shape {df.shape}")
