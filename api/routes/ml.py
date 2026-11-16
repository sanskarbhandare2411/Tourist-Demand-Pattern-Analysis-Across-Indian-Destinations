from fastapi import APIRouter
from api.services import TourismDataService, clean_records
from api.schemas import PredictionRequest, PredictionResponse

router = APIRouter(prefix="/api/ml", tags=["ML Demand Prediction"])


@router.get("/metrics")
def get_ml_metrics():
    service = TourismDataService.get_instance()
    regressor = service.regressor
    
    metrics = regressor.metrics
    coefs_df = regressor.coefficients_df
    
    return {
        "metrics": metrics,
        "coefficients": clean_records(coefs_df)
    }


@router.post("/predict", response_model=PredictionResponse)
def predict_tourist_demand(payload: PredictionRequest):
    service = TourismDataService.get_instance()
    regressor = service.regressor
    
    input_features = {
        'Is_UNESCO_Site': payload.is_unesco_site,
        'Destination_Type': payload.destination_type,
        'Foreign_Tourist_Share': payload.foreign_tourist_share,
        'Domestic_Tourist_Share': max(0.0, 100.0 - payload.foreign_tourist_share),
        'Annual_Avg_Temp_C': payload.annual_avg_temp_c,
        'Annual_Total_Rainfall_mm': payload.annual_total_rainfall_mm,
        'Temp_Ideal_Deviation': abs(payload.annual_avg_temp_c - 22.0),
        'Monsoon_Rainfall_mm': payload.annual_total_rainfall_mm * 0.70
    }
    
    pred_result = regressor.predict_visits(input_features)
    
    return {
        "predicted_total_visits": int(pred_result['predicted_total_visits']),
        "prediction_interval_lower": int(pred_result['prediction_interval_lower']),
        "prediction_interval_upper": int(pred_result['prediction_interval_upper']),
        "predicted_log_visits": float(round(pred_result['predicted_log_visits'], 3)),
        "input_features": input_features
    }
