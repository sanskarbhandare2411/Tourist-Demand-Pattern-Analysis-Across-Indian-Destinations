"""
Machine Learning - Destination Clustering Module (K-Means)
DS2004: Fundamentals of Data Science
Project: Tourist Demand Pattern Analysis Across Indian Destinations

Implements syllabus-level unsupervised learning:
- K-Means Clustering on destination tourism demand behaviors
- Feature scaling with StandardScaler
- Model evaluation: Inertia (Elbow Method) and Silhouette Analysis (k=2..8)
- Domain-grounded Cluster Profiling and Archetype naming
- 2D PCA dimensionality reduction and visualization
- Model persistence with Joblib
"""

import os
import joblib
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, silhouette_samples
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models")
PROCESSED_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "processed")
TABLES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "outputs", "tables")
FIGURES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "outputs", "figures")


CLUSTER_ARCHETYPES = {
    0: {
        'name': 'Tier-1 Iconic Global Mega-Hubs',
        'badge': 'Global Icons',
        'color': '#ef4444',
        'desc': 'High-volume international icons with substantial foreign tourist share, UNESCO status, and national prominence (e.g., Taj Mahal, Agra Fort, Qutub Minar, Red Fort).'
    },
    1: {
        'name': 'Domestic Cultural Heritage Powerhouses',
        'badge': 'Domestic Hubs',
        'color': '#3b82f6',
        'desc': 'Massive domestic footfall with overwhelmingly domestic travelers (>95%), moderate foreign presence, and high cultural/historical significance (e.g., Sun Temple Konark, Golconda, Charminar).'
    },
    2: {
        'name': 'High-Precipitation & Monsoon-Sensitive Enclaves',
        'badge': 'Coastal / Monsoon Enclaves',
        'color': '#10b981',
        'desc': 'Destinations located in coastal or heavy-rainfall zones (>2000 mm rain), exhibiting strong seasonal variations and climate-dependent visitation patterns (e.g., Goa, Kerala, Mumbai heritage).'
    },
    3: {
        'name': 'Emerging & Niche Archaeological Sites',
        'badge': 'Emerging Heritage',
        'color': '#f59e0b',
        'desc': 'Moderate-to-low volume heritage destinations with high latent potential, seeking infrastructure, connectivity, and promotional upgrades (e.g., regional stupas, lesser-known rock-cut temples).'
    }
}


class DestinationKMeansClustering:
    """
    K-Means clustering pipeline for grouping Indian destinations based on
    tourist demand volume, domestic/foreign mix, growth momentum, and climate parameters.
    """
    def __init__(self, n_clusters: int = 4, random_state: int = 42):
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=2, random_state=random_state)
        self.model = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=15)
        self.feature_cols = [
            'Log_Total_Visits',
            'Foreign_Tourist_Share',
            'Tourist_Growth_Rate_Domestic',
            'Annual_Avg_Temp_C',
            'Annual_Total_Rainfall_mm',
            'Temp_Ideal_Deviation'
        ]
        self.k_evaluation_df = pd.DataFrame()
        self.cluster_summary_df = pd.DataFrame()
        self.is_fitted = False

    def evaluate_k_range(self, df: pd.DataFrame, k_range=range(2, 9)) -> pd.DataFrame:
        """Evaluates clustering quality across candidate k values using Inertia and Silhouette scores."""
        X = df[self.feature_cols].copy()
        X_scaled = self.scaler.fit_transform(X)
        
        results = []
        for k in k_range:
            km = KMeans(n_clusters=k, random_state=self.random_state, n_init=10)
            labels = km.fit_predict(X_scaled)
            sil = silhouette_score(X_scaled, labels)
            results.append({
                'k': k,
                'Inertia': round(km.inertia_, 2),
                'Silhouette_Score': round(sil, 4)
            })
            
        self.k_evaluation_df = pd.DataFrame(results)
        return self.k_evaluation_df

    def fit_predict(self, df: pd.DataFrame) -> pd.DataFrame:
        """Fits KMeans on the chosen k and assigns cluster labels and archetypes."""
        df_work = df.copy()
        X = df_work[self.feature_cols].copy()
        X_scaled = self.scaler.fit_transform(X)
        
        self.model.fit(X_scaled)
        labels = self.model.labels_
        df_work['Cluster_ID'] = labels
        
        # 2D PCA coordinates for plotting
        pca_coords = self.pca.fit_transform(X_scaled)
        df_work['PCA_Dim1'] = pca_coords[:, 0].round(3)
        df_work['PCA_Dim2'] = pca_coords[:, 1].round(3)
        
        # Silhouette score for fitted model
        sil_score = silhouette_score(X_scaled, labels)
        logger.info(f"K-Means fitted with k={self.n_clusters}. Silhouette Score: {sil_score:.4f}, Inertia: {self.model.inertia_:.2f}")
        
        # Determine archetype mappings by sorting clusters by Log_Total_Visits and Foreign Share
        cluster_means = df_work.groupby('Cluster_ID')[self.feature_cols].mean()
        
        # Map cluster labels to archetypes consistently
        # High foreign share & high volume -> Global Icons (0)
        # High rainfall -> Monsoon Enclaves (2)
        # High volume but low foreign share -> Domestic Hubs (1)
        # Lower volume -> Emerging Heritage (3)
        
        assigned_archetypes = {}
        # Identify high rainfall cluster
        rain_cluster = cluster_means['Annual_Total_Rainfall_mm'].idxmax()
        assigned_archetypes[rain_cluster] = 2
        
        # Remaining clusters
        remaining = [c for c in range(self.n_clusters) if c != rain_cluster]
        remaining_means = cluster_means.loc[remaining]
        
        # Highest foreign share among remaining
        foreign_cluster = remaining_means['Foreign_Tourist_Share'].idxmax()
        assigned_archetypes[foreign_cluster] = 0
        
        # Remaining 2
        rem2 = [c for c in remaining if c != foreign_cluster]
        if len(rem2) >= 2:
            vol_cluster = cluster_means.loc[rem2, 'Log_Total_Visits'].idxmax()
            emerging_cluster = cluster_means.loc[rem2, 'Log_Total_Visits'].idxmin()
            assigned_archetypes[vol_cluster] = 1
            assigned_archetypes[emerging_cluster] = 3
        else:
            for r in rem2:
                assigned_archetypes[r] = 1
                
        # Remap dataframe cluster IDs to normalized archetype IDs
        df_work['Cluster_Archetype_ID'] = df_work['Cluster_ID'].map(assigned_archetypes).fillna(df_work['Cluster_ID'])
        df_work['Cluster_Name'] = df_work['Cluster_Archetype_ID'].map(lambda x: CLUSTER_ARCHETYPES.get(x, {}).get('name', f'Cluster {x}'))
        df_work['Cluster_Badge'] = df_work['Cluster_Archetype_ID'].map(lambda x: CLUSTER_ARCHETYPES.get(x, {}).get('badge', f'C{x}'))
        
        # Build profile summary table
        profile = df_work.groupby(['Cluster_Archetype_ID', 'Cluster_Name']).agg(
            Destination_Count=('Monument_Name', 'count'),
            Avg_Total_Visits=('Total_Tourist_Visits', 'mean'),
            Median_Total_Visits=('Total_Tourist_Visits', 'median'),
            Avg_Foreign_Share=('Foreign_Tourist_Share', 'mean'),
            Avg_Domestic_Share=('Domestic_Tourist_Share', 'mean'),
            Avg_Annual_Temp=('Annual_Avg_Temp_C', 'mean'),
            Avg_Annual_Rainfall=('Annual_Total_Rainfall_mm', 'mean'),
            Avg_Domestic_Growth=('Tourist_Growth_Rate_Domestic', 'mean'),
            UNESCO_Sites_Count=('Is_UNESCO_Site', 'sum')
        ).reset_index().round(2)
        
        self.cluster_summary_df = profile
        self.is_fitted = True
        return df_work

    def save(self, filepath: str = None):
        """Saves clustering pipeline artifacts."""
        if filepath is None:
            os.makedirs(MODELS_DIR, exist_ok=True)
            filepath = os.path.join(MODELS_DIR, "kmeans_clustering_model.joblib")
        joblib.dump({
            'model': self.model,
            'scaler': self.scaler,
            'pca': self.pca,
            'feature_cols': self.feature_cols,
            'n_clusters': self.n_clusters,
            'cluster_summary_df': self.cluster_summary_df,
            'k_evaluation_df': self.k_evaluation_df,
            'is_fitted': self.is_fitted
        }, filepath)
        logger.info(f"Clustering model saved to {filepath}")

    @classmethod
    def load(cls, filepath: str = None):
        """Loads saved clustering model from disk."""
        if filepath is None:
            filepath = os.path.join(MODELS_DIR, "kmeans_clustering_model.joblib")
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Clustering model file not found at: {filepath}")
        data = joblib.load(filepath)
        obj = cls(n_clusters=data['n_clusters'])
        obj.model = data['model']
        obj.scaler = data['scaler']
        obj.pca = data['pca']
        obj.feature_cols = data['feature_cols']
        obj.cluster_summary_df = data['cluster_summary_df']
        obj.k_evaluation_df = data['k_evaluation_df']
        obj.is_fitted = data['is_fitted']
        return obj


def train_and_save_clustering():
    """Executes clustering pipeline, evaluates k, assigns clusters, and saves outputs."""
    feat_path = os.path.join(PROCESSED_DIR, "destinations_featured.csv")
    if not os.path.exists(feat_path):
        from src.feature_engineering import engineer_all_and_save
        engineer_all_and_save()
        
    df = pd.read_csv(feat_path)
    clusterer = DestinationKMeansClustering(n_clusters=4, random_state=42)
    
    # 1. Evaluate k range
    k_eval = clusterer.evaluate_k_range(df, k_range=range(2, 8))
    
    # 2. Fit and assign clusters
    df_clustered = clusterer.fit_predict(df)
    
    # 3. Save model
    clusterer.save()
    
    # 4. Save tables
    os.makedirs(TABLES_DIR, exist_ok=True)
    k_eval.to_csv(os.path.join(TABLES_DIR, "clustering_evaluation_k.csv"), index=False)
    clusterer.cluster_summary_df.to_csv(os.path.join(TABLES_DIR, "cluster_profiles_summary.csv"), index=False)
    
    # 5. Save clustered destination data
    out_clustered_path = os.path.join(PROCESSED_DIR, "destinations_clustered.csv")
    df_clustered.to_csv(out_clustered_path, index=False)
    logger.info(f"Clustered destinations saved to {out_clustered_path}")
    
    return clusterer, df_clustered


if __name__ == "__main__":
    clusterer, df_clustered = train_and_save_clustering()
    print("=== K-MEANS EVALUATION ACROSS K ===")
    print(clusterer.k_evaluation_df)
    print("\n=== CLUSTER PROFILES SUMMARY ===")
    print(clusterer.cluster_summary_df)
