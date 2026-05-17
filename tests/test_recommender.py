"""
Unit tests for recommender module
"""

import unittest
import pandas as pd
import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.recommender import SkincareRecommender

class TestRecommender(unittest.TestCase):
    
    def setUp(self):
        """Set up test data"""
        self.recommender = SkincareRecommender()
        
        # Sample user data
        self.test_user = {
            'skin_type': 'Oily',
            'skin_concerns': ['Acne', 'Large Pores'],
            'monthly_budget': 50,
            'age': 28,
            'gender': 'Female',
            'uses_retinol': False,
            'uses_vitamin_c': True,
            'uses_niacinamide': True
        }
    
    def test_calculate_product_score(self):
        """Test product score calculation"""
        product = {
            'name': 'Test Product',
            'brand': 'Test Brand',
            'price': 15.99,
            'tier': 'affordable',
            'rating': 4.5,
            'skin_types': ['Oily', 'Combination'],
            'concerns': ['Acne'],
            'ingredients': ['Niacinamide']
        }
        
        score = self.recommender.calculate_product_score(
            product, 
            self.test_user['skin_type'],
            self.test_user['skin_concerns'],
            self.test_user['monthly_budget'],
            self.test_user['age'],
            self.test_user['gender'],
            self.test_user['uses_retinol'],
            self.test_user['uses_vitamin_c'],
            self.test_user['uses_niacinamide']
        )
        
        # Score should be between 0 and 1
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 1)
    
    def test_get_recommendations(self):
        """Test getting recommendations"""
        recommendations = self.recommender.get_recommendations(self.test_user, top_n=5)
        
        # Should return 5 recommendations
        self.assertEqual(len(recommendations), 5)
        
        # Each recommendation should have required fields
        for rec in recommendations:
            self.assertIn('name', rec)
            self.assertIn('brand', rec)
            self.assertIn('price', rec)
            self.assertIn('rating', rec)
            self.assertIn('match_percentage', rec)
    
    def test_get_ingredient_recommendations(self):
        """Test ingredient recommendations"""
        concerns = ['Acne', 'Wrinkles']
        ingredients = self.recommender.get_ingredient_recommendations(concerns)
        
        # Should return list of ingredients
        self.assertIsInstance(ingredients, list)
        self.assertGreater(len(ingredients), 0)
    
    def test_predict_product_rating(self):
        """Test product rating prediction"""
        product_name = 'CeraVe Hydrating Cleanser'
        rating = self.recommender.predict_product_rating(self.test_user, product_name)
        
        # Rating should be between 1 and 5
        self.assertGreaterEqual(rating, 1)
        self.assertLessEqual(rating, 5)

class TestRecommendationQuality(unittest.TestCase):
    
    def setUp(self):
        self.recommender = SkincareRecommender()
        
        # Different user profiles
        self.profiles = [
            {'skin_type': 'Oily', 'skin_concerns': ['Acne'], 'monthly_budget': 30},
            {'skin_type': 'Dry', 'skin_concerns': ['Dryness', 'Wrinkles'], 'monthly_budget': 150},
            {'skin_type': 'Sensitive', 'skin_concerns': ['Redness'], 'monthly_budget': 80}
        ]
    
    def test_recommendations_are_relevant(self):
        """Test that recommendations are relevant to user profile"""
        for profile in self.profiles:
            recs = self.recommender.get_recommendations(profile, top_n=3)
            
            # All recommendations should have at least 50% match
            for rec in recs:
                self.assertGreaterEqual(rec['match_percentage'], 50)
    
    def test_budget_constraints(self):
        """Test that recommendations respect budget"""
        low_budget_user = {'skin_type': 'Normal', 'skin_concerns': [], 'monthly_budget': 20}
        recs = self.recommender.get_recommendations(low_budget_user, top_n=5)
        
        # Some recommendations should be affordable
        affordable_count = sum(1 for r in recs if r['price'] <= 25)
        self.assertGreater(affordable_count, 0)

if __name__ == '__main__':
    unittest.main()