"""
Pydantic schemas for the Tourist Demand Pattern Analysis API.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    is_unesco_site: int = Field(default=1, description="1 if UNESCO World Heritage, 0 otherwise")
    destination_type: str = Field(default="Fort & Palace", description="Typology of destination")
    foreign_tourist_share: float = Field(default=8.5, ge=0.0, le=100.0, description="Expected foreign visitor share %")
    annual_avg_temp_c: float = Field(default=24.5, ge=-10.0, le=55.0, description="Annual average temperature in Celsius")
    annual_total_rainfall_mm: float = Field(default=1100.0, ge=0.0, le=12000.0, description="Annual total rainfall in mm")


class PredictionResponse(BaseModel):
    predicted_total_visits: int
    prediction_interval_lower: int
    prediction_interval_upper: int
    predicted_log_visits: float
    input_features: Dict[str, Any]


class RecommendationFilterRequest(BaseModel):
    state: str = Field(default="All", description="State name or 'All'")
    destination_type: str = Field(default="All", description="Typology or 'All'")
    crowd_preference: str = Field(default="Any", description="'Any', 'Low Crowds (<100k)', 'Moderate (100k-500k)', 'High / Iconic (>500k)'")
    weather_preference: str = Field(default="Any", description="'Any', 'Cool (<20°C)', 'Moderate (20-26°C)', 'Warm (>26°C)'")
    top_k: int = Field(default=6, ge=1, le=50)


class DestinationSummary(BaseModel):
    Monument_Name: str
    Circle: str
    State: str
    Destination_Type: str
    Total_Tourist_Visits: int
    Domestic_2019_20: int
    Foreign_2019_20: int
    Domestic_Tourist_Share: float
    Foreign_Tourist_Share: float
    Annual_Avg_Temp_C: float
    Annual_Total_Rainfall_mm: float
    Is_UNESCO_Site: int
    Footfall_Tier: Optional[str] = None
    Cluster_ID: Optional[int] = None
    Cluster_Name: Optional[str] = None
    Latitude: Optional[float] = None
    Longitude: Optional[float] = None
    Image_URL: str
