from typing import Optional
from fastapi import APIRouter, HTTPException
import numpy as np
import pandas as pd
from api.services import TourismDataService, clean_records, get_monument_image

router = APIRouter(prefix="/api/destinations", tags=["Destinations"])


@router.get("")
def list_destinations(
    state: Optional[str] = None,
    typology: Optional[str] = None,
    unesco_only: Optional[bool] = None,
    search: Optional[str] = None,
    sort_by: Optional[str] = "Total_Tourist_Visits",
    ascending: bool = False,
    limit: Optional[int] = None
):
    service = TourismDataService.get_instance()
    df = service.df_dest.copy()
    
    if isinstance(state, str) and state not in ("All States", "All", ""):
        df = df[df['State'] == state]
    if isinstance(typology, str) and typology not in ("All Typologies", "All", ""):
        df = df[df['Destination_Type'] == typology]
    if isinstance(unesco_only, bool):
        df = df[df['Is_UNESCO_Site'] == (1 if unesco_only else 0)]
    if isinstance(search, str) and search.strip():
        s = search.strip().lower()
        df = df[df['Monument_Name'].str.lower().str.contains(s) | df['State'].str.lower().str.contains(s)]
        
    if isinstance(sort_by, str) and sort_by in df.columns:
        df = df.sort_values(by=sort_by, ascending=ascending)
        
    if isinstance(limit, int) and limit > 0:
        df = df.head(limit)
        
    return {
        "total_count": len(df),
        "destinations": clean_records(df)
    }


@router.get("/spotlight/{name}")
def get_destination_spotlight(name: str):
    service = TourismDataService.get_instance()
    df = service.df_dest
    
    matches = df[df['Monument_Name'].str.lower() == name.lower()]
    if matches.empty:
        matches = df[df['Monument_Name'].str.lower().str.contains(name.lower())]
        
    if matches.empty:
        raise HTTPException(status_code=404, detail=f"Destination '{name}' not found")
        
    row = matches.iloc[0].to_dict()
    clean_row = {k: (None if pd.isna(v) else v) for k, v in row.items()}
    clean_row['Image_URL'] = get_monument_image(clean_row['Monument_Name'], clean_row.get('Circle', ''))
    return clean_row


@router.get("/rankings")
def get_top_rankings(top_n: int = 15):
    service = TourismDataService.get_instance()
    top_df = service.df_dest.sort_values(by='Total_Tourist_Visits', ascending=False).head(top_n)
    return {
        "top_n": top_n,
        "rankings": clean_records(top_df)
    }


@router.get("/map")
def get_map_markers(
    state: Optional[str] = None,
    typology: Optional[str] = None,
    unesco_only: Optional[bool] = None
):
    service = TourismDataService.get_instance()
    df = service.df_dest.copy()
    
    if isinstance(state, str) and state not in ("All States", "All", ""):
        df = df[df['State'] == state]
    if isinstance(typology, str) and typology not in ("All Typologies", "All", ""):
        df = df[df['Destination_Type'] == typology]
    if isinstance(unesco_only, bool):
        df = df[df['Is_UNESCO_Site'] == (1 if unesco_only else 0)]
        
    markers = []
    for _, row in df.iterrows():
        lat = row.get('Latitude')
        lon = row.get('Longitude')
        if pd.notnull(lat) and pd.notnull(lon):
            markers.append({
                "name": row['Monument_Name'],
                "circle": row['Circle'],
                "state": row['State'],
                "lat": float(lat),
                "lon": float(lon),
                "total_visits": int(row['Total_Tourist_Visits']),
                "foreign_share_pct": float(round(row['Foreign_Tourist_Share'], 1)),
                "domestic_share_pct": float(round(row['Domestic_Tourist_Share'], 1)),
                "is_unesco": bool(row['Is_UNESCO_Site'] == 1),
                "footfall_tier": str(row.get('Footfall_Tier', 'Tier-3 (40k-125k)')),
                "destination_type": str(row.get('Destination_Type', 'Monument')),
                "avg_temp_c": float(round(row['Annual_Avg_Temp_C'], 1)),
                "annual_rainfall_mm": float(round(row['Annual_Total_Rainfall_mm'], 0)),
                "cluster_name": str(row.get('Cluster_Name', 'Cluster')),
                "image_url": get_monument_image(row['Monument_Name'], row.get('Circle', ''))
            })
            
    return {
        "count": len(markers),
        "markers": markers
    }


@router.get("/typology-impact")
def get_typology_and_unesco_impact():
    service = TourismDataService.get_instance()
    df = service.df_dest
    
    unesco_summary = df.groupby('Is_UNESCO_Site').agg(
        Count=('Monument_Name', 'count'),
        Mean_Footfall=('Total_Tourist_Visits', 'mean'),
        Median_Footfall=('Total_Tourist_Visits', 'median'),
        Avg_Foreign_Share=('Foreign_Tourist_Share', 'mean')
    ).reset_index()
    
    unesco_summary['Status'] = unesco_summary['Is_UNESCO_Site'].map({
        1: 'UNESCO World Heritage',
        0: 'Non-UNESCO Monument'
    })
    
    typology_summary = df.groupby('Destination_Type').agg(
        Count=('Monument_Name', 'count'),
        Mean_Footfall=('Total_Tourist_Visits', 'mean'),
        Median_Footfall=('Total_Tourist_Visits', 'median'),
        Avg_Foreign_Share=('Foreign_Tourist_Share', 'mean'),
        Mean_Log_Visits=('Log_Total_Visits', 'mean')
    ).reset_index().sort_values(by='Median_Footfall', ascending=False)
    
    typology_distribution = []
    for _, row in df.iterrows():
        typology_distribution.append({
            "type": row['Destination_Type'],
            "name": row['Monument_Name'],
            "log_visits": float(round(row['Log_Total_Visits'], 3)),
            "visits": int(row['Total_Tourist_Visits'])
        })
        
    return {
        "unesco_comparison": clean_records(unesco_summary),
        "typology_summary": clean_records(typology_summary),
        "typology_distribution": typology_distribution
    }
