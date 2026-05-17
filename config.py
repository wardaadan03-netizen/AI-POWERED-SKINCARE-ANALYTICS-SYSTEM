import os
from datetime import timedelta

class Config:
    """Application configuration"""
    
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Upload configuration
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload
    ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}
    
    # Data paths
    DATA_PATH = 'data/processed/processed_data.csv'
    RAW_DATA_PATH = 'data/raw/skincare_dataset.csv'
    TRAIN_DATA_PATH = 'data/processed/train_data.csv'
    TEST_DATA_PATH = 'data/processed/test_data.csv'
    
    # Model paths
    MODEL_PATH = 'data/models/recommender_model.pkl'
    SATISFACTION_MODEL_PATH = 'data/models/satisfaction_regressor.pkl'
    SCALER_PATH = 'data/models/scaler.pkl'
    LABEL_ENCODERS_PATH = 'data/models/label_encoders.pkl'
    FEATURE_COLUMNS_PATH = 'data/models/feature_columns.pkl'
    
    # Application settings
    APP_NAME = "Skincare AI Analytics Platform"
    APP_VERSION = "1.0.0"
    DEBUG = True
    
    # Recommendation settings
    DEFAULT_RECOMMENDATIONS = 6
    MAX_RECOMMENDATIONS = 20
    
    @staticmethod
    def init_app(app):
        """Initialize application"""
        # Create necessary directories
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs('data/raw', exist_ok=True)
        os.makedirs('data/processed', exist_ok=True)
        os.makedirs('data/models', exist_ok=True)