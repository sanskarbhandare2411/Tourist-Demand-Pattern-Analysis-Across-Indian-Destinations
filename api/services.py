"""
Service layer for data retrieval, caching, and model inference.
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd
import joblib

# Ensure project root is in sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.models import TouristDemandRegression
from src.clustering import DestinationKMeansClustering
from src.recommender import TourismRecommendationEngine

DATA_DIR = ROOT_DIR / "data" / "processed"
MODELS_DIR = ROOT_DIR / "models"

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


def get_monument_image(name: str, circle: str = "") -> str:
    """Returns curated high-resolution destination image URL."""
    n = str(name).lower()
    c = str(circle).lower()
    for key, url in DESTINATION_IMAGES.items():
        if key in n or key in c:
            return url
    return DESTINATION_IMAGES['default']


class TourismDataService:
    _instance = None

    def __init__(self):
        self._load_datasets()
        self._load_models()
        self.recommender = TourismRecommendationEngine(
            df_dest=self.df_dest,
            df_qtr=self.df_qtr,
            df_state=self.df_state
        )

    def _load_datasets(self):
        dest_file = DATA_DIR / "destinations_clustered.csv"
        if not dest_file.exists():
            dest_file = DATA_DIR / "destinations_featured.csv"
        
        self.df_dest = pd.read_csv(dest_file)
        # Ensure image urls
        if 'Image_URL' not in self.df_dest.columns:
            self.df_dest['Image_URL'] = self.df_dest.apply(
                lambda row: get_monument_image(row['Monument_Name'], row.get('Circle', '')),
                axis=1
            )
            
        self.df_state = pd.read_csv(DATA_DIR / "statewise_tourism_cleaned.csv")
        self.df_qtr = pd.read_csv(DATA_DIR / "seasonal_quarterly_cleaned.csv")
        self.df_fta = pd.read_csv(DATA_DIR / "longitudinal_fta_cleaned.csv")

    def _load_models(self):
        reg_path = MODELS_DIR / "linear_regression_model.joblib"
        cls_path = MODELS_DIR / "kmeans_clustering_model.joblib"
        
        if reg_path.exists():
            self.regressor = TouristDemandRegression.load(str(reg_path))
        else:
            from src.models import train_and_save_model
            self.regressor, _ = train_and_save_model()

        if cls_path.exists():
            self.clusterer = DestinationKMeansClustering.load(str(cls_path))
        else:
            from src.clustering import train_and_save_clustering
            self.clusterer, _ = train_and_save_clustering()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance


def clean_records(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Helper to convert DataFrame to json-friendly records, replacing NaNs with None."""
    cleaned = df.replace({np.nan: None, np.inf: None, -np.inf: None})
    return cleaned.to_dict(orient="records")
