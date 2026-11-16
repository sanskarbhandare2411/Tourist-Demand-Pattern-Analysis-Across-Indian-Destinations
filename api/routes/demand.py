from typing import Optional
from fastapi import APIRouter
from api.services import TourismDataService, clean_records

router = APIRouter(prefix="/api/demand", tags=["Tourism Demand"])


@router.get("/longitudinal")
def get_longitudinal_demand():
    service = TourismDataService.get_instance()
    df_fta = service.df_fta.copy().sort_values(by="Year")
    
    valid_fta = df_fta.dropna(subset=['FTAs_Million'])
    
    peak_2019 = float(df_fta[df_fta['Year'] == 2019]['FTAs_Million'].values[0]) if 2019 in df_fta['Year'].values else 10.93
    cagr_str = "~6.2% Annual Growth"
    covid_drop = float(df_fta[df_fta['Year'] == 2020]['FTA_Growth_Pct'].values[0]) if 2020 in df_fta['Year'].values else -74.9
    
    return {
        "metrics": {
            "pre_pandemic_peak_2019_million": peak_2019,
            "historical_cagr_1991_2019": cagr_str,
            "pandemic_impact_2020_pct": covid_drop
        },
        "time_series": clean_records(valid_fta),
        "insight": "International arrivals in India expanded from 1.28M in 1981 to 10.93M in 2019, followed by a sharp contraction during 2020 due to global pandemic border closures."
    }


@router.get("/statewise")
def get_statewise_demand(
    top_n: int = 12,
    sort_by: str = "Total Visits"
):
    service = TourismDataService.get_instance()
    df_state = service.df_state.copy()
    
    if sort_by == "Domestic Visits":
        df_sorted = df_state.sort_values(by='Domestic_2019', ascending=False)
    elif sort_by == "Foreign Visits":
        df_sorted = df_state.sort_values(by='Foreign_2019', ascending=False)
    else:
        df_sorted = df_state.sort_values(by='Total_Visits_2019', ascending=False)
        
    top_states = df_sorted.head(top_n)
    
    return {
        "top_n": top_n,
        "sort_by": sort_by,
        "states": clean_records(top_states),
        "all_states_summary": clean_records(df_state[['State', 'Region', 'Domestic_2019', 'Foreign_2019', 'Total_Visits_2019', 'Domestic_Share_2019', 'Foreign_Share_2019']].sort_values(by='Total_Visits_2019', ascending=False))
    }


@router.get("/composition")
def get_visitor_composition():
    service = TourismDataService.get_instance()
    df_dest = service.df_dest
    
    total_dom = int(df_dest['Domestic_2019_20'].sum())
    total_for = int(df_dest['Foreign_2019_20'].sum())
    total_all = total_dom + total_for
    
    pie_data = [
        {"name": "Domestic Visitors", "value": total_dom, "share_pct": round(total_dom / total_all * 100, 2)},
        {"name": "Foreign Visitors", "value": total_for, "share_pct": round(total_for / total_all * 100, 2)}
    ]
    
    scatter_points = []
    for _, row in df_dest.iterrows():
        scatter_points.append({
            "name": row['Monument_Name'],
            "circle": row['Circle'],
            "state": row['State'],
            "total_visits": int(row['Total_Tourist_Visits']),
            "foreign_share_pct": float(round(row['Foreign_Tourist_Share'], 2)),
            "domestic_visits": int(row['Domestic_2019_20']),
            "destination_type": row['Destination_Type'],
            "is_unesco": int(row['Is_UNESCO_Site'])
        })
        
    return {
        "overall_pie": pie_data,
        "scatter_points": scatter_points
    }
