from fastapi import APIRouter
import pandas as pd
from api.services import TourismDataService, clean_records

router = APIRouter(prefix="/api/seasonal", tags=["Seasonal Analysis"])


@router.get("/quarterly")
def get_quarterly_trends():
    service = TourismDataService.get_instance()
    df_qtr = service.df_qtr.sort_values(by=["Year", "Quarter"])
    return {
        "count": len(df_qtr),
        "data": clean_records(df_qtr)
    }


@router.get("/breakdown")
def get_seasonal_breakdown():
    service = TourismDataService.get_instance()
    df_qtr = service.df_qtr
    
    seasonal_avg = df_qtr.groupby('Season')['Arrival_Share_Pct'].mean().reset_index()
    seasonal_avg['Arrival_Share_Pct'] = seasonal_avg['Arrival_Share_Pct'].round(2)
    
    color_map = {
        'Winter': '#10b981',
        'Summer': '#f43f5e',
        'Monsoon': '#38bdf8',
        'Post-Monsoon': '#fbbf24'
    }
    records = []
    for _, row in seasonal_avg.iterrows():
        s = row['Season']
        records.append({
            "season": s,
            "share_pct": float(row['Arrival_Share_Pct']),
            "color": color_map.get(s, '#38bdf8')
        })
        
    return {
        "seasonal_averages": records
    }


@router.get("/summary")
def get_seasonal_summary():
    service = TourismDataService.get_instance()
    sec_rec = service.recommender.get_seasonal_recommendations()
    df_qtr = service.df_qtr
    
    # Pivot last 5 years
    qtr_pivot = df_qtr.pivot(index='Year', columns='Quarter', values='Arrival_Share_Pct').tail(5).reset_index()
    
    return {
        "peak_season": sec_rec.get('peak_season', 'Post-Monsoon'),
        "peak_period_description": "Post-Monsoon (Q4: Oct–Dec)",
        "peak_share_pct": sec_rec.get('peak_share_pct', 30.5),
        "secondary_peak_season": "Winter (Q1: Jan–Mar)",
        "secondary_peak_share_pct": sec_rec.get('quarterly_breakdown', {}).get('Q1', 28.8),
        "trough_season": "Summer (Q2: Apr–Jun)",
        "trough_share_pct": sec_rec.get('trough_share_pct', 19.1),
        "seasonality_ratio": sec_rec.get('seasonality_ratio', 1.60),
        "quarterly_breakdown": sec_rec.get('quarterly_breakdown', {}),
        "last_5_years_matrix": clean_records(qtr_pivot),
        "recommendations": sec_rec.get('recommendations', [])
    }
