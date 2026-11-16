from fastapi import APIRouter
from api.services import TourismDataService

router = APIRouter(prefix="/api/meta", tags=["Metadata"])


@router.get("/health")
def health_check():
    try:
        service = TourismDataService.get_instance()
        return {
            "status": "online",
            "version": "2.0.0",
            "platform": "Tourist Demand Pattern Analysis Across Indian Destinations",
            "destinations_count": len(service.df_dest),
            "states_count": len(service.df_state),
            "models_loaded": {
                "regression": service.regressor.is_fitted,
                "clustering": service.clusterer.is_fitted
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "detail": str(e)
        }


@router.get("/filters")
def get_filter_options():
    service = TourismDataService.get_instance()
    df_dest = service.df_dest
    
    states = sorted([str(s) for s in df_dest['State'].dropna().unique()])
    typologies = sorted([str(t) for t in df_dest['Destination_Type'].dropna().unique()])
    clusters = sorted([str(c) for c in df_dest['Cluster_Name'].dropna().unique()]) if 'Cluster_Name' in df_dest.columns else []
    
    return {
        "states": ["All States"] + states,
        "typologies": ["All Typologies"] + typologies,
        "clusters": ["All Clusters"] + clusters,
        "tourist_types": ["All Tourists (Total)", "Domestic Only", "Foreign Only"],
        "heritage_classifications": ["All Sites", "UNESCO Sites Only", "Non-UNESCO Only"]
    }
