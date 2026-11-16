from fastapi import APIRouter
from api.services import TourismDataService, DESTINATION_IMAGES

router = APIRouter(prefix="/api/overview", tags=["Overview"])


@router.get("")
def get_overview_data():
    service = TourismDataService.get_instance()
    df_dest = service.df_dest
    
    total_visits = int(df_dest['Total_Tourist_Visits'].sum())
    top_dest_row = df_dest.sort_values(by='Total_Tourist_Visits', ascending=False).iloc[0]
    avg_dom_share = float(round(df_dest['Domestic_Tourist_Share'].mean(), 2))
    unesco_count = int(df_dest['Is_UNESCO_Site'].sum())
    avg_temp = float(round(df_dest['Annual_Avg_Temp_C'].mean(), 2))
    
    kpis = {
        "total_monuments_footfall": total_visits,
        "total_monuments_footfall_m": round(total_visits / 1e6, 2),
        "total_destinations_monitored": len(df_dest),
        "top_destination": {
            "name": top_dest_row['Monument_Name'],
            "state": top_dest_row['State'],
            "annual_visits": int(top_dest_row['Total_Tourist_Visits']),
            "annual_visits_m": round(top_dest_row['Total_Tourist_Visits'] / 1e6, 2)
        },
        "average_domestic_share_pct": avg_dom_share,
        "unesco_sites_count": unesco_count,
        "average_annual_temperature_c": avg_temp
    }
    
    showcase_items = [
        {
            "name": "Taj Mahal",
            "location": "Agra, Uttar Pradesh",
            "volume_str": "5.07M Visits",
            "image": DESTINATION_IMAGES['taj mahal'],
            "is_unesco": True
        },
        {
            "name": "Qutub Minar",
            "location": "Mehrauli, New Delhi",
            "volume_str": "2.30M Visits",
            "image": DESTINATION_IMAGES['qutub minar'],
            "is_unesco": True
        },
        {
            "name": "Hampi Ruins",
            "location": "Ballari, Karnataka",
            "volume_str": "610K Visits",
            "image": DESTINATION_IMAGES['hampi'],
            "is_unesco": True
        },
        {
            "name": "Goa Heritage",
            "location": "Old Goa, Goa",
            "volume_str": "425K Visits",
            "image": DESTINATION_IMAGES['goa'],
            "is_unesco": True
        }
    ]
    
    analytical_scope = {
        "title": "Problem Definition & Analytical Scope",
        "description": "Tourism across India exhibits pronounced spatial over-concentration (top 5 monuments capture ~30% of total footfall) and temporal volatility (Post-Monsoon and Winter capture ~60% of annual international visits).",
        "key_pillars": [
            "Longitudinal & Seasonal Demand: Tracking 40 years of international tourism growth and 19 years of quarterly arrival patterns.",
            "Climate Sensitivity Analysis: Examining empirical influence of temperature deviations and monsoon precipitation on tourist visits.",
            "Supervised Demand Forecasting: Multiple Linear Regression to estimate tourist demand based on structural and climatic attributes.",
            "Unsupervised Destination Clustering: Segmenting destinations via K-Means (k=4) into distinct behavioral archetypes.",
            "Data-Driven Interventions: Evidence-grounded recommendations for circuit decongestion, carrying capacity management, and weather adaptation."
        ]
    }
    
    data_sources = {
        "title": "Data Sources & Quality Verification",
        "points": [
            "Ministry of Tourism India: Centrally Protected Ticketed Monuments Footfall & State/UT Tourism Compendium.",
            "Open-Meteo ERA5 Reanalysis: Authentic meteorological observations across all 33 Indian destination administrative circles.",
            "Data Cleaning Protocol: Filtered 34 circle subtotals and national totals to prevent double-counting.",
            "Principled Outlier Treatment: Identified 14 statistical upper outliers using IQR (>787k visits). Retained raw numbers for KPI reporting while using log transformations ln(1 + Visits) for regression models."
        ]
    }
    
    return {
        "kpis": kpis,
        "showcase": showcase_items,
        "analytical_scope": analytical_scope,
        "data_sources": data_sources
    }
