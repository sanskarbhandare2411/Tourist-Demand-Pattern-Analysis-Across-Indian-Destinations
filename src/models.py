"""
Machine Learning - Tourist Demand Prediction Module
DS2004: Fundamentals of Data Science
Project: Tourist Demand Pattern Analysis Across Indian Destinations

Implements syllabus-level supervised learning:
- Multiple Linear Regression for tourist demand prediction
- Log-scale formulation with inverse exponential transformation
- Comprehensive evaluation: MAE, RMSE, R², 5-Fold Cross Validation
- Model persistence using Joblib
- Real-time prediction interface with user feature controls
"""

import os
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models")
PROCESSED_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "processed")
TABLES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "outputs", "tables")


class TouristDemandRegression:
    """
    Syllabus-standard Multiple Linear Regression model for destination-level tourist demand.
    """
    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        self.scaler = StandardScaler()
        self.model = LinearRegression()
        self.ridge_model = Ridge(alpha=1.0)
        self.feature_names = []
        self.metrics = {}
        self.coefficients_df = pd.DataFrame()
        self.is_fitted = False

    def prepare_features(self, df: pd.DataFrame, is_training: bool = True):
        """Prepares numerical features and destination type dummies."""
        df_work = df.copy()
        
        # Base numerical features
        num_cols = [
            'Is_UNESCO_Site',
            'Foreign_Tourist_Share',
            'Domestic_Tourist_Share',
            'Annual_Avg_Temp_C',
            'Annual_Total_Rainfall_mm',
            'Temp_Ideal_Deviation',
            'Monsoon_Rainfall_mm'
        ]
        
        # Typology dummies
        if 'Destination_Type' in df_work.columns:
            type_dummies = pd.get_dummies(df_work['Destination_Type'], prefix='Type', drop_first=True)
            X = pd.concat([df_work[num_cols], type_dummies], axis=1)
        else:
            X = df_work[num_cols].copy()
            
        if is_training:
            self.feature_names = list(X.columns)
        else:
            # Align with training features
            for col in self.feature_names:
                if col not in X.columns:
                    X[col] = 0
            X = X[self.feature_names]
            
        return X

    def train(self, df: pd.DataFrame, test_size: float = 0.2):
        """
        Trains Linear Regression model with 80/20 train/test split.
        Uses Log(1 + Visits) as the target variable to satisfy linearity assumptions,
        then computes evaluation metrics both on log scale and actual visit count scale.
        """
        logger.info(f"Training Linear Regression model on {len(df)} destinations...")
        X = self.prepare_features(df, is_training=True)
        y_log = df['Log_Total_Visits']
        y_actual = df['Total_Tourist_Visits']
        
        X_train, X_test, y_train, y_test, idx_train, idx_test = train_test_split(
            X, y_log, df.index, test_size=test_size, random_state=self.random_state
        )
        
        # Feature standardization
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Fit OLS Linear Regression
        self.model.fit(X_train_scaled, y_train)
        self.ridge_model.fit(X_train_scaled, y_train)
        
        # Predictions (log scale)
        y_pred_train_log = self.model.predict(X_train_scaled)
        y_pred_test_log = self.model.predict(X_test_scaled)
        
        # Inverse transform to actual visits: exp(y_log) - 1
        y_test_actual = y_actual.loc[idx_test]
        y_pred_test_actual = np.expm1(y_pred_test_log)
        y_pred_test_actual = np.clip(y_pred_test_actual, a_min=0, a_max=None)
        
        # Log-scale metrics
        mae_log = mean_absolute_error(y_test, y_pred_test_log)
        rmse_log = np.sqrt(mean_squared_error(y_test, y_pred_test_log))
        r2_log = r2_score(y_test, y_pred_test_log)
        
        # Actual visit metrics
        mae_actual = mean_absolute_error(y_test_actual, y_pred_test_actual)
        rmse_actual = np.sqrt(mean_squared_error(y_test_actual, y_pred_test_actual))
        r2_actual = r2_score(y_test_actual, y_pred_test_actual)
        
        # 5-Fold Cross Validation
        kf = KFold(n_splits=5, shuffle=True, random_state=self.random_state)
        X_all_scaled = self.scaler.transform(X)
        cv_r2_scores = cross_val_score(self.model, X_all_scaled, y_log, cv=kf, scoring='r2')
        cv_mae_scores = -cross_val_score(self.model, X_all_scaled, y_log, cv=kf, scoring='neg_mean_absolute_error')
        
        self.metrics = {
            'mae_log': float(round(mae_log, 4)),
            'rmse_log': float(round(rmse_log, 4)),
            'r2_log': float(round(r2_log, 4)),
            'mae_actual': float(round(mae_actual, 2)),
            'rmse_actual': float(round(rmse_actual, 2)),
            'r2_actual': float(round(r2_actual, 4)),
            'cv_r2_mean': float(round(cv_r2_scores.mean(), 4)),
            'cv_r2_std': float(round(cv_r2_scores.std(), 4)),
            'cv_mae_mean': float(round(cv_mae_scores.mean(), 4)),
            'n_train': int(len(X_train)),
            'n_test': int(len(X_test)),
            'intercept': float(round(self.model.intercept_, 4))
        }
        
        # Coefficients table
        coefs = pd.DataFrame({
            'Feature': self.feature_names,
            'Standardized_Coefficient': self.model.coef_,
            'Absolute_Impact': np.abs(self.model.coef_)
        }).sort_values(by='Absolute_Impact', ascending=False).reset_index(drop=True)
        
        coefs['Direction'] = np.where(coefs['Standardized_Coefficient'] >= 0, 'Positive (+)', 'Negative (-)')
        coefs['Standardized_Coefficient'] = coefs['Standardized_Coefficient'].round(4)
        coefs['Absolute_Impact'] = coefs['Absolute_Impact'].round(4)
        self.coefficients_df = coefs
        self.is_fitted = True
        
        logger.info(f"Model Training Complete. Test Log-R²: {r2_log:.3f}, Test MAE (log): {mae_log:.3f}, CV R²: {cv_r2_scores.mean():.3f}")
        return self.metrics

    def predict_visits(self, input_dict: dict) -> dict:
        """
        Takes raw user input dictionary and returns predicted tourist footfall.
        """
        if not self.is_fitted:
            raise ValueError("Model has not been trained or loaded yet.")
            
        df_input = pd.DataFrame([input_dict])
        
        # Derive complementary share if missing
        if 'Domestic_Tourist_Share' not in df_input.columns and 'Foreign_Tourist_Share' in df_input.columns:
            df_input['Domestic_Tourist_Share'] = max(0.0, 100.0 - df_input['Foreign_Tourist_Share'].iloc[0])
        elif 'Foreign_Tourist_Share' not in df_input.columns and 'Domestic_Tourist_Share' in df_input.columns:
            df_input['Foreign_Tourist_Share'] = max(0.0, 100.0 - df_input['Domestic_Tourist_Share'].iloc[0])
            
        if 'Temp_Ideal_Deviation' not in df_input.columns and 'Annual_Avg_Temp_C' in df_input.columns:
            df_input['Temp_Ideal_Deviation'] = abs(df_input['Annual_Avg_Temp_C'].iloc[0] - 22.0)
            
        if 'Monsoon_Rainfall_mm' not in df_input.columns and 'Annual_Total_Rainfall_mm' in df_input.columns:
            df_input['Monsoon_Rainfall_mm'] = df_input['Annual_Total_Rainfall_mm'].iloc[0] * 0.70
            
        X = self.prepare_features(df_input, is_training=False)
        X_scaled = self.scaler.transform(X)
        pred_log = self.model.predict(X_scaled)[0]
        pred_visits = int(max(0, np.expm1(pred_log)))
        
        # Prediction interval estimate (+/- 1 RMSE)
        lower_visits = int(max(0, np.expm1(pred_log - self.metrics.get('rmse_log', 1.5))))
        upper_visits = int(max(0, np.expm1(pred_log + self.metrics.get('rmse_log', 1.5))))
        
        return {
            'predicted_log_visits': round(pred_log, 3),
            'predicted_total_visits': pred_visits,
            'prediction_interval_lower': lower_visits,
            'prediction_interval_upper': upper_visits
        }

    def save(self, filepath: str = None):
        """Saves model artifacts to disk."""
        if filepath is None:
            os.makedirs(MODELS_DIR, exist_ok=True)
            filepath = os.path.join(MODELS_DIR, "linear_regression_model.joblib")
        joblib.dump({
            'model': self.model,
            'scaler': self.scaler,
            'feature_names': self.feature_names,
            'metrics': self.metrics,
            'coefficients_df': self.coefficients_df,
            'is_fitted': self.is_fitted
        }, filepath)
        logger.info(f"Model artifacts saved to {filepath}")

    @classmethod
    def load(cls, filepath: str = None):
        """Loads saved model artifacts from disk."""
        if filepath is None:
            filepath = os.path.join(MODELS_DIR, "linear_regression_model.joblib")
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Model file not found at: {filepath}")
        data = joblib.load(filepath)
        obj = cls()
        obj.model = data['model']
        obj.scaler = data['scaler']
        obj.feature_names = data['feature_names']
        obj.metrics = data['metrics']
        obj.coefficients_df = data['coefficients_df']
        obj.is_fitted = data['is_fitted']
        return obj


def train_and_save_model():
    """Trains regression model on featured dataset and saves results."""
    feat_path = os.path.join(PROCESSED_DIR, "destinations_featured.csv")
    if not os.path.exists(feat_path):
        from src.feature_engineering import engineer_all_and_save
        engineer_all_and_save()
        
    df = pd.read_csv(feat_path)
    regressor = TouristDemandRegression(random_state=42)
    metrics = regressor.train(df)
    regressor.save()
    
    # Save coefficients to tables
    os.makedirs(TABLES_DIR, exist_ok=True)
    regressor.coefficients_df.to_csv(os.path.join(TABLES_DIR, "regression_coefficients.csv"), index=False)
    
    # Save metrics table
    metrics_df = pd.DataFrame([metrics])
    metrics_df.to_csv(os.path.join(TABLES_DIR, "regression_evaluation_metrics.csv"), index=False)
    
    return regressor, metrics


if __name__ == "__main__":
    regressor, metrics = train_and_save_model()
    print("=== MODEL EVALUATION METRICS ===")
    for k, v in metrics.items():
        print(f"{k}: {v}")
    print("\n=== TOP FEATURE COEFFICIENTS ===")
    print(regressor.coefficients_df.head(10))
