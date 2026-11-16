from fastapi import APIRouter
from api.services import TourismDataService, clean_records, get_monument_image
from api.schemas import RecommendationFilterRequest

router = APIRouter(prefix="/api/recommendations", tags=["Insights & Recommendations"])


@router.get("/strategies")
def get_cluster_strategies():
    service = TourismDataService.get_instance()
    strategies = service.recommender.get_cluster_strategies()
    return {
        "strategies": strategies
    }


@router.get("/decongestion")
def get_decongestion_recommendations():
    service = TourismDataService.get_instance()
    decongestion = service.recommender.get_decongestion_recommendations()
    return {
        "recommendations": decongestion
    }


@router.get("/weather")
def get_weather_recommendations():
    service = TourismDataService.get_instance()
    weather_recs = service.recommender.get_weather_adaptive_recommendations()
    return {
        "recommendations": weather_recs
    }


@router.get("/seasonal")
def get_seasonal_recommendations():
    service = TourismDataService.get_instance()
    sec_rec = service.recommender.get_seasonal_recommendations()
    return {
        "recommendations": sec_rec.get('recommendations', [])
    }


@router.post("/filter")
def filter_recommendations(payload: RecommendationFilterRequest):
    service = TourismDataService.get_instance()
    recommender = service.recommender
    
    user_prefs = {
        'state': payload.state,
        'destination_type': payload.destination_type,
        'crowd_preference': payload.crowd_preference,
        'weather_preference': payload.weather_preference
    }
    
    matches = recommender.recommend_destinations(user_prefs, top_k=payload.top_k)
    
    results = []
    if not matches.empty:
        for _, r in matches.iterrows():
            results.append({
                "name": r['Monument_Name'],
                "circle": r['Circle'],
                "state": r['State'],
                "destination_type": r['Destination_Type'],
                "total_visits": int(r['Total_Tourist_Visits']),
                "foreign_share_pct": float(round(r['Foreign_Tourist_Share'], 1)),
                "annual_avg_temp_c": float(round(r['Annual_Avg_Temp_C'], 1)),
                "annual_rainfall_mm": float(round(r['Annual_Total_Rainfall_mm'], 0)),
                "is_unesco": bool(r['Is_UNESCO_Site'] == 1),
                "image_url": get_monument_image(r['Monument_Name'], r['Circle'])
            })
            
    return {
        "count": len(results),
        "destinations": results
    }
