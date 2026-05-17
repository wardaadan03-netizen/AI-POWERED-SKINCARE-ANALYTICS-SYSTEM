import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
import joblib
import re
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class SkincareDataPreprocessor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_columns = None
        self.imputer = SimpleImputer(strategy='median')
        
    def process_dataset(self, df, is_training=True):
        """Main preprocessing pipeline"""
        df = df.copy()
        
        # Handle datetime columns
        date_cols = ['RegistrationDate', 'LastActive']
        for col in date_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
                if is_training:
                    df[col + '_days_ago'] = (datetime.now() - df[col]).dt.days
                    df[col + '_days_ago'].fillna(df[col + '_days_ago'].median(), inplace=True)
        
        # Age preprocessing
        if 'Age' in df.columns:
            df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
            df['Age'].clip(18, 100, inplace=True)
            df['Age'].fillna(df['Age'].median(), inplace=True)
            df['AgeGroup'] = pd.cut(df['Age'], bins=[0, 25, 35, 45, 55, 100], 
                                   labels=['18-25', '26-35', '36-45', '46-55', '55+'])
        
        # Budget preprocessing
        if 'MonthlyBudget_USD' in df.columns:
            df['MonthlyBudget_USD'] = pd.to_numeric(df['MonthlyBudget_USD'], errors='coerce')
            df['MonthlyBudget_USD'].clip(0, 10000, inplace=True)
            df['MonthlyBudget_USD'].fillna(df['MonthlyBudget_USD'].median(), inplace=True)
            df['BudgetTier'] = pd.cut(df['MonthlyBudget_USD'], 
                                     bins=[0, 30, 75, 150, 300, 100000],
                                     labels=['Low', 'Medium', 'High', 'Premium', 'Luxury'])
        
        # Categorical encoding
        categorical_cols = ['SkinType', 'Gender', 'Climate', 'SkinConcerns', 'PreferredTier']
        for col in categorical_cols:
            if col in df.columns:
                df[col] = df[col].astype(str).fillna('Unknown')
                if is_training:
                    self.label_encoders[col] = LabelEncoder()
                    df[col + '_encoded'] = self.label_encoders[col].fit_transform(df[col])
                else:
                    if col in self.label_encoders:
                        # Handle unseen categories
                        df[col + '_encoded'] = df[col].map(
                            lambda x: self.label_encoders[col].transform([x])[0] 
                            if x in self.label_encoders[col].classes_ 
                            else -1
                        )
        
        # Handle missing values in numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            df[col].fillna(df[col].median(), inplace=True)
        
        # Create composite scores
        if all(col in df.columns for col in ['ProductEffectiveness_Score', 'CustomerSatisfaction_pct']):
            df['OverallScore'] = (df['ProductEffectiveness_Score'] * 20 + 
                                 df['CustomerSatisfaction_pct']) / 2
        
        # Active ingredients usage score
        ingredient_cols = [col for col in df.columns if col.startswith('Uses')]
        if ingredient_cols:
            df['ActiveIngredientsCount'] = df[ingredient_cols].sum(axis=1)
            df['IngredientDiversityScore'] = (df['ActiveIngredientsCount'] / len(ingredient_cols)) * 100
        
        # Lifestyle score
        if 'SleepHours' in df.columns and 'StressLevel_1to10' in df.columns:
            df['LifestyleScore'] = (df['SleepHours'] / 10 * 100 - df['StressLevel_1to10'] * 10 + 100).clip(0, 100)
        
        # Hydration score
        if 'Hydration_Level_pct' in df.columns:
            df['HydrationScore'] = df['Hydration_Level_pct']
        
        # Feature selection for model
        if is_training:
            self.feature_columns = [col for col in df.columns if col.endswith('_encoded') or 
                                   col in ['Age', 'MonthlyBudget_USD', 'ActiveIngredientsCount',
                                          'OverallScore', 'LifestyleScore', 'HydrationScore',
                                          'ProductEffectiveness_Score', 'CustomerSatisfaction_pct',
                                          'Recommendation_Score', 'ValueForMoney_Rating']]
            self.feature_columns = [col for col in self.feature_columns if col in df.columns]
        
        return df
    
    def scale_features(self, df, is_training=True):
        """Scale numerical features"""
        if not self.feature_columns:
            return df
        
        features = df[self.feature_columns].copy()
        
        # Handle missing values
        features = features.fillna(0)
        
        if is_training:
            scaled_features = self.scaler.fit_transform(features)
            joblib.dump(self.scaler, 'data/models/scaler.pkl')
        else:
            scaled_features = self.scaler.transform(features)
        
        # Add scaled features back
        for i, col in enumerate(self.feature_columns):
            df[col + '_scaled'] = scaled_features[:, i]
        
        return df
    
    def save_models(self):
        """Save preprocessor models"""
        os.makedirs('data/models', exist_ok=True)
        joblib.dump(self.label_encoders, 'data/models/label_encoders.pkl')
        joblib.dump(self.feature_columns, 'data/models/feature_columns.pkl')
        
    def load_models(self):
        """Load preprocessor models"""
        self.label_encoders = joblib.load('data/models/label_encoders.pkl')
        self.feature_columns = joblib.load('data/models/feature_columns.pkl')
        self.scaler = joblib.load('data/models/scaler.pkl')