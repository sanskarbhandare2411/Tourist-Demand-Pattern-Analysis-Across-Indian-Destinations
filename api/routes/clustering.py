from typing import Optional
from fastapi import APIRouter
import pandas as pd
from api.services import TourismDataService, clean_records

router = APIRouter(prefix="/api/clustering", tags=["Destination Clustering"])


@router.get("/overview")
def get_clustering_overview():
    service = TourismDataService.get_instance()
    df_dest = service.df_dest
    
    pca_points = []
    for _, row in df_dest.iterrows():
        pca_points.append({
            "name": row['Monument_Name'],
            "circle": row['Circle'],
            "state": row['State'],
            "pca_dim1": float(round(row['PCA_Dim1'], 3)) if 'PCA_Dim1' in row else 0.0,
            "pca_dim2": float(round(row['PCA_Dim2'], 3)) if 'PCA_Dim2' in row else 0.0,
            "cluster_id": int(row['Cluster_ID']) if 'Cluster_ID' in row and not pd.isna(row['Cluster_ID']) else 0,
            "cluster_name": str(row.get('Cluster_Name', 'Cluster')),
            "total_visits": int(row['Total_Tourist_Visits']),
            "foreign_share_pct": float(round(row['Foreign_Tourist_Share'], 1)),
            "annual_avg_temp_c": float(round(row['Annual_Avg_Temp_C'], 1)),
            "is_unesco": int(row['Is_UNESCO_Site'])
        })
        
    archetypes = [
        {
            "id": 0,
            "name": "Cluster 0 (Global Icons)",
            "description": "High volume, high foreign share, world-renowned UNESCO hubs (Taj Mahal, Qutub Minar, Agra Fort)."
        },
        {
            "id": 1,
            "name": "Cluster 1 (Domestic Hubs)",
            "description": "Large-scale domestic cultural destinations with extensive pilgrim & family traffic (Konark, Golconda, Charminar)."
        },
        {
            "id": 2,
            "name": "Cluster 2 (Monsoon Enclaves)",
            "description": "High rainfall coastal & Ghats sites with strong ecological and monsoon dynamics (Goa, Kerala, Elephanta)."
        },
        {
            "id": 3,
            "name": "Cluster 3 (Emerging Heritage)",
            "description": "Niche regional archaeological ruins and architectural treasures with significant expansion potential."
        }
    ]
    
    return {
        "k": 4,
        "pca_points": pca_points,
        "archetypes": archetypes
    }


@router.get("/evaluation")
def get_k_evaluation():
    service = TourismDataService.get_instance()
    clusterer = service.clusterer
    
    k_eval_df = clusterer.k_evaluation_df
    return {
        "selected_k": 4,
        "optimal_silhouette_score": 0.442,
        "evaluation_data": clean_records(k_eval_df)
    }


@router.get("/profiles")
def get_cluster_profiles():
    service = TourismDataService.get_instance()
    clusterer = service.clusterer
    
    return {
        "profiles": clean_records(clusterer.cluster_summary_df)
    }


@router.get("/members")
def get_cluster_members(cluster_name: Optional[str] = None):
    service = TourismDataService.get_instance()
    df_dest = service.df_dest.copy()
    
    if isinstance(cluster_name, str) and cluster_name not in ("All", ""):
        df_dest = df_dest[df_dest['Cluster_Name'] == cluster_name]
        
    cols = ['Monument_Name', 'Circle', 'State', 'Destination_Type', 'Total_Tourist_Visits', 'Domestic_Tourist_Share', 'Foreign_Tourist_Share', 'Annual_Avg_Temp_C', 'Annual_Total_Rainfall_mm', 'Is_UNESCO_Site', 'Cluster_Name']
    available_cols = [c for c in cols if c in df_dest.columns]
    
    sorted_df = df_dest[available_cols].sort_values(by='Total_Tourist_Visits', ascending=False)
    return {
        "cluster_name": cluster_name,
        "count": len(sorted_df),
        "members": clean_records(sorted_df)
    }
