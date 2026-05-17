"""
Unit tests for preprocessing module
"""

import unittest
import pandas as pd
import numpy as np
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.preprocessing import SkincareDataPreprocessor

class TestPreprocessing(unittest.TestCase):
    
    def setUp(self):
        """Set up test data"""
        self.preprocessor = SkincareDataPreprocessor()
        
        # Create sample data
        self.sample_data = pd.DataFrame({
            'UserID': ['USER_001', 'USER_002', 'USER_003'],
            'Age': [25, 35, np.nan],
            'Gender': ['Female', 'Male', 'Female'],
            'SkinType': ['Oily', 'Dry', 'Combination'],
            'MonthlyBudget_USD': [50, 100, 75],
            'ProductEffectiveness_Score': [4.2, 3.8, 4.5],
            'CustomerSatisfaction_pct': [85, 78, 92]
        })
    
    def test_handle_missing_values(self):
        """Test missing value handling"""
        result = self.preprocessor.handle_missing_values(self.sample_data)
        
        # Check if missing values are filled
        self.assertEqual(result['Age'].isnull().sum(), 0)
        self.assertEqual(result['Age'].iloc[2], result['Age'].median())
    
    def test_handle_outliers(self):
        """Test outlier handling"""
        # Add outlier
        self.sample_data.loc[0, 'Age'] = 150
        
        result = self.preprocessor.handle_outliers(self.sample_data)
        
        # Check if outlier is capped
        self.assertLessEqual(result['Age'].max(), 100)
    
    def test_feature_engineering(self):
        """Test feature engineering"""
        result = self.preprocessor.feature_engineering(self.sample_data)
        
        # Check if new features are created
        self.assertIn('AgeGroup', result.columns)
        self.assertIn('BudgetTier', result.columns)
    
    def test_fix_data_types(self):
        """Test data type fixing"""
        # Add invalid data
        self.sample_data['RegistrationDate'] = ['2024-01-01', 'invalid', '2024-01-03']
        
        result = self.preprocessor.fix_data_types(self.sample_data)
        
        # Check if dates are converted properly
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(result['RegistrationDate']))

class TestDataValidation(unittest.TestCase):
    
    def test_age_validation(self):
        """Test age validation"""
        from utils.helpers import validate_age
        
        self.assertTrue(validate_age(25))
        self.assertTrue(validate_age(18))
        self.assertTrue(validate_age(100))
        self.assertFalse(validate_age(15))
        self.assertFalse(validate_age(150))
        self.assertFalse(validate_age('abc'))
    
    def test_email_validation(self):
        """Test email validation"""
        from utils.helpers import validate_email
        
        self.assertTrue(validate_email('test@example.com'))
        self.assertTrue(validate_email('user.name@domain.co.uk'))
        self.assertFalse(validate_email('invalid-email'))
        self.assertFalse(validate_email('missing@domain'))
        self.assertFalse(validate_email('@nodomain.com'))

if __name__ == '__main__':
    unittest.main()