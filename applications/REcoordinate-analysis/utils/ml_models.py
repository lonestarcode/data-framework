import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from xgboost import XGBRegressor
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout, LSTM
import joblib
import logging
from typing import Dict, List, Tuple, Any
from datetime import datetime

class PropertyValuePredictor:
    def __init__(self, model_path: str = None):
        self.model_path = model_path
        self.model = None
        self.scaler = StandardScaler()
        self.feature_columns = [
            'square_footage', 'bedrooms', 'bathrooms', 'lot_size',
            'year_built', 'last_sold_price', 'days_on_market',
            'median_income', 'population_density', 'crime_rate',
            'school_rating', 'walk_score', 'property_tax_rate'
        ]
        
        # Initialize models
        self._initialize_models()
        
    def _initialize_models(self):
        """Initialize different models for ensemble prediction"""
        self.models = {
            'rf': RandomForestRegressor(
                n_estimators=200,
                max_depth=20,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42
            ),
            'gb': GradientBoostingRegressor(
                n_estimators=200,
                learning_rate=0.1,
                max_depth=5,
                random_state=42
            ),
            'xgb': XGBRegressor(
                n_estimators=200,
                learning_rate=0.1,
                max_depth=5,
                random_state=42
            )
        }
        
    def prepare_data(self, data: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare and preprocess data for model training"""
        # Create preprocessing pipeline
        numeric_features = [col for col in data.columns if data[col].dtype in ['int64', 'float64']]
        categorical_features = [col for col in data.columns if data[col].dtype == 'object']
        
        numeric_transformer = Pipeline(steps=[
            ('scaler', StandardScaler())
        ])
        
        categorical_transformer = Pipeline(steps=[
            ('onehot', OneHotEncoder(drop='first', sparse=False))
        ])
        
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_features),
                ('cat', categorical_transformer, categorical_features)
            ])
        
        return preprocessor.fit_transform(data)

    def train_model(self, X: np.ndarray, y: np.ndarray):
        """Train multiple models and create an ensemble"""
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        model_scores = {}
        predictions = {}
        
        for name, model in self.models.items():
            # Train model
            model.fit(X_train, y_train)
            
            # Make predictions
            pred = model.predict(X_test)
            predictions[name] = pred
            
            # Calculate metrics
            mse = mean_squared_error(y_test, pred)
            r2 = r2_score(y_test, pred)
            
            model_scores[name] = {
                'mse': mse,
                'r2': r2
            }
            
            logging.info(f"Model {name} - MSE: {mse:.2f}, R2: {r2:.2f}")
        
        # Save models
        self._save_models()
        
        return model_scores

    def predict_property_value(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """Make ensemble prediction for property value"""
        try:
            # Prepare features
            X = self._prepare_features(features)
            
            # Make predictions with each model
            predictions = {}
            for name, model in self.models.items():
                pred = model.predict(X)
                predictions[name] = pred[0]
            
            # Calculate ensemble prediction (weighted average)
            weights = {'rf': 0.4, 'gb': 0.3, 'xgb': 0.3}
            ensemble_pred = sum(pred * weights[name] for name, pred in predictions.items())
            
            # Calculate confidence score
            confidence = self._calculate_prediction_confidence(predictions)
            
            return {
                'predicted_value': ensemble_pred,
                'confidence_score': confidence,
                'model_predictions': predictions
            }
            
        except Exception as e:
            logging.error(f"Error in property value prediction: {str(e)}")
            raise

    def _prepare_features(self, features: Dict[str, Any]) -> np.ndarray:
        """Prepare features for prediction"""
        # Convert dictionary to DataFrame
        df = pd.DataFrame([features])
        
        # Ensure all required features are present
        for col in self.feature_columns:
            if col not in df.columns:
                df[col] = 0
        
        return self.prepare_data(df)

    def _calculate_prediction_confidence(self, predictions: Dict[str, float]) -> float:
        """Calculate confidence score based on model agreement"""
        values = list(predictions.values())
        mean_pred = np.mean(values)
        std_pred = np.std(values)
        
        # Calculate coefficient of variation
        cv = std_pred / mean_pred
        
        # Convert to confidence score (0-100)
        confidence = max(0, min(100, 100 * (1 - cv)))
        
        return confidence

    def _save_models(self):
        """Save trained models to disk"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        for name, model in self.models.items():
            filename = f"models/{name}_model_{timestamp}.joblib"
            joblib.dump(model, filename)
            logging.info(f"Saved model {name} to {filename}")

class MarketTrendPredictor:
    def __init__(self):
        self.lstm_model = self._build_lstm_model()
        
    def _build_lstm_model(self) -> Sequential:
        """Build LSTM model for time series prediction"""
        model = Sequential([
            LSTM(50, return_sequences=True, input_shape=(30, 1)),
            Dropout(0.2),
            LSTM(50, return_sequences=False),
            Dropout(0.2),
            Dense(25),
            Dense(1)
        ])
        model.compile(optimizer='adam', loss='mse')
        return model

    def predict_market_trends(
        self,
        historical_data: pd.DataFrame,
        forecast_periods: int = 12
    ) -> Dict[str, Any]:
        """Predict future market trends using LSTM"""
        try:
            # Prepare time series data
            scaled_data = self.scaler.fit_transform(historical_data)
            X, y = self._prepare_sequences(scaled_data)
            
            # Train model
            self.lstm_model.fit(
                X, y,
                epochs=100,
                batch_size=32,
                validation_split=0.1,
                verbose=0
            )
            
            # Make predictions
            last_sequence = scaled_data[-30:]
            predictions = []
            
            for _ in range(forecast_periods):
                next_pred = self.lstm_model.predict(
                    last_sequence.reshape(1, 30, 1)
                )
                predictions.append(next_pred[0, 0])
                last_sequence = np.roll(last_sequence, -1)
                last_sequence[-1] = next_pred
            
            # Inverse transform predictions
            predictions = self.scaler.inverse_transform(
                np.array(predictions).reshape(-1, 1)
            )
            
            return {
                'predictions': predictions.flatten().tolist(),
                'confidence_intervals': self._calculate_confidence_intervals(predictions)
            }
            
        except Exception as e:
            logging.error(f"Error in market trend prediction: {str(e)}")
            raise

    def _prepare_sequences(
        self,
        data: np.ndarray,
        sequence_length: int = 30
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare sequences for LSTM model"""
        X, y = [], []
        for i in range(len(data) - sequence_length):
            X.append(data[i:(i + sequence_length)])
            y.append(data[i + sequence_length])
        return np.array(X), np.array(y)

    def _calculate_confidence_intervals(
        self,
        predictions: np.ndarray,
        confidence: float = 0.95
    ) -> Dict[str, List[float]]:
        """Calculate confidence intervals for predictions"""
        std = np.std(predictions)
        z_score = 1.96  # 95% confidence interval
        
        lower_bound = predictions - (z_score * std)
        upper_bound = predictions + (z_score * std)
        
        return {
            'lower_bound': lower_bound.flatten().tolist(),
            'upper_bound': upper_bound.flatten().tolist()
        }

# Usage example:
if __name__ == "__main__":
    # Initialize predictors
    value_predictor = PropertyValuePredictor()
    trend_predictor = MarketTrendPredictor()
    
    # Example property features
    sample_features = {
        'square_footage': 2000,
        'bedrooms': 3,
        'bathrooms': 2,
        'lot_size': 5000,
        'year_built': 1990,
        'last_sold_price': 400000,
        'days_on_market': 30,
        'median_income': 75000,
        'population_density': 5000,
        'crime_rate': 200,
        'school_rating': 8,
        'walk_score': 75,
        'property_tax_rate': 1.2
    }
    
    # Make predictions
    value_prediction = value_predictor.predict_property_value(sample_features)
    print("Property Value Prediction:", value_prediction)