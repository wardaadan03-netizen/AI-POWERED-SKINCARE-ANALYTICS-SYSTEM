"""
Data Preprocessing Module
Handles data cleaning and feature engineering
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

class SkincareDataPreprocessor:
    """Handles data preprocessing for skincare data"""
    
    def __init__(self):
        self.label_encoders = {}
        self.scaler = None
        self.feature_columns = None
    
    def handle_missing_values(self, df):
        """Handle missing values in the dataset"""
        df = df.copy()
        
        # Numeric columns - fill with median
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            df[col].fillna(df[col].median(), inplace=True)
        
        # Categorical columns - fill with mode
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else 'Unknown', inplace=True)
        
        return df
    
    def handle_outliers(self, df, columns=None, method='iqr'):
        """Handle outliers in the dataset"""
        df = df.copy()
        
        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns
        
        for col in columns:
            if method == 'iqr':
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower = Q1 - 1.5 * IQR
                upper = Q3 + 1.5 * IQR
                df[col] = df[col].clip(lower, upper)
            
            elif method == 'zscore':
                z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
                df.loc[z_scores > 3, col] = df[col].median()
        
        return df
    
    def feature_engineering(self, df):
        """Create new features from existing ones"""
        df = df.copy()
        
        # Age groups
        df['AgeGroup'] = pd.cut(df['Age'], 
                               bins=[0, 18, 25, 35, 45, 55, 65, 100],
                               labels=['<18', '18-24', '25-34', '35-44', '45-54', '55-64', '65+'])
        
        # Budget tiers
        df['BudgetTier'] = pd.cut(df['MonthlyBudget_USD'],
                                 bins=[0, 25, 50, 100, 200, 500, 10000],
                                 labels=['Budget', 'Economy', 'Moderate', 'Mid-Range', 'Premium', 'Luxury'])
        
        # Skin health composite score
        df['SkinHealthScore'] = (
            df['ProductEffectiveness_Score'] * 0.4 +
            df['CustomerSatisfaction_pct'] / 100 * 0.3 +
            df['SkinBarrier_Score'] / 10 * 0.3
        )
        
        return df
    
    def fix_data_types(self, df):
        """Fix data types in the dataset"""
        df = df.copy()
        
        # Convert date columns
        date_cols = [col for col in df.columns if 'Date' in col or 'date' in col]
        for col in date_cols:
            try:
                df[col] = pd.to_datetime(df[col], errors='coerce')
            except:
                pass
        
        # Convert numeric columns
        numeric_cols = ['Age', 'MonthlyBudget_USD', 'ProductEffectiveness_Score', 
                       'CustomerSatisfaction_pct', 'SkinBarrier_Score']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df
    
    def encode_categorical(self, df, columns=None):
        """Encode categorical variables"""
        df = df.copy()
        
        if columns is None:
            columns = df.select_dtypes(include=['object']).columns
        
        for col in columns:
            if col in df.columns:
                if col not in self.label_encoders:
                    self.label_encoders[col] = LabelEncoder()
                    df[col] = self.label_encoders[col].fit_transform(df[col].astype(str))
                else:
                    df[col] = self.label_encoders[col].transform(df[col].astype(str))
        
        return df
    
    def prepare_features(self, df, target_col=None):
        """Prepare features for model training"""
        df = self.fix_data_types(df)
        df = self.handle_missing_values(df)
        df = self.handle_outliers(df)
        df = self.feature_engineering(df)
        
        # Store feature columns
        self.feature_columns = [col for col in df.columns if col != target_col]
        
        return df
    
    def create_sample_data(self):
        """Create sample data for testing"""
        np.random.seed(42)
        n = 1000
        
        return pd.DataFrame({
            'UserID': [f'USER_{i}' for i in range(n)],
            'Age': np.random.randint(18, 70, n),
            'Gender': np.random.choice(['Female', 'Male', 'Non-binary'], n),
            'SkinType': np.random.choice(['Oily', 'Dry', 'Combination', 'Normal', 'Sensitive'], n),
            'MonthlyBudget_USD': np.random.choice([20, 30, 50, 75, 100, 150, 200], n),
            'ProductEffectiveness_Score': np.random.normal(4.0, 0.6, n).clip(2, 5),
            'CustomerSatisfaction_pct': np.random.normal(80, 10, n).clip(50, 98),
            'SkinBarrier_Score': np.random.randint(1, 10, n)
        })