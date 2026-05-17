"""
Enhanced Recommender with Sub-Products and Intelligent Matching
"""

import pandas as pd
import numpy as np
import random
import json
import os
from datetime import datetime

class SkincareRecommender:
    def __init__(self):
        self.products_db = self.load_enhanced_products()
        self.feedback_file = 'data/feedback.json'
        self.user_feedback = self.load_feedback()
        
    def load_enhanced_products(self):
        """Load products with sub-categories and detailed attributes"""
        return {
            'Cleanser': {
                'sub_categories': {
                    'Gel Cleanser': [
                        {'name': 'Purifying Gel Cleanser', 'brand': 'CeraVe', 'price': 14.99, 'tier': 'affordable',
                         'rating': 4.7, 'skin_types': ['Oily', 'Combination'], 'concerns': ['Acne', 'Large Pores'],
                         'ingredients': ['Salicylic Acid', 'Niacinamide', 'Glycerin'], 'reviews': 15234,
                         'benefits': ['Oil control', 'Pore minimization', 'Acne prevention']},
                        {'name': 'Fresh Soy Face Cleanser', 'brand': 'Fresh', 'price': 38.00, 'tier': 'mid_range',
                         'rating': 4.6, 'skin_types': ['Normal', 'Combination'], 'concerns': ['Dullness'],
                         'ingredients': ['Soy Proteins', 'Rosewater', 'Cucumber Extract'], 'reviews': 3456,
                         'benefits': ['Gentle cleansing', 'Brightening', 'Hydrating']}
                    ],
                    'Cream Cleanser': [
                        {'name': 'Hydrating Cream Cleanser', 'brand': 'CeraVe', 'price': 12.99, 'tier': 'affordable',
                         'rating': 4.8, 'skin_types': ['Dry', 'Normal', 'Sensitive'], 'concerns': ['Dryness'],
                         'ingredients': ['Ceramides', 'Hyaluronic Acid', 'Glycerin'], 'reviews': 45678,
                         'benefits': ['Deep hydration', 'Barrier repair', 'Gentle cleansing']},
                        {'name': 'La Roche-Posay Toleriane', 'brand': 'La Roche-Posay', 'price': 16.99, 'tier': 'affordable',
                         'rating': 4.7, 'skin_types': ['Sensitive', 'Dry'], 'concerns': ['Redness', 'Dryness'],
                         'ingredients': ['Ceramide-3', 'Niacinamide', 'Shea Butter'], 'reviews': 23456,
                         'benefits': ['Calms irritation', 'Restores moisture', 'Soothing']}
                    ],
                    'Foaming Cleanser': [
                        {'name': 'Foaming Facial Cleanser', 'brand': 'Cetaphil', 'price': 11.99, 'tier': 'affordable',
                         'rating': 4.5, 'skin_types': ['Oily', 'Combination'], 'concerns': ['Acne'],
                         'ingredients': ['Glycerin', 'Niacinamide'], 'reviews': 34567,
                         'benefits': ['Deep pore cleansing', 'Oil removal', 'Non-stripping']}
                    ]
                }
            },
            'Serum': {
                'sub_categories': {
                    'Vitamin C Serum': [
                        {'name': '15% Vitamin C Serum', 'brand': "Paula's Choice", 'price': 49.00, 'tier': 'mid_range',
                         'rating': 4.7, 'skin_types': ['Aging', 'Dull', 'Normal'], 'concerns': ['Pigmentation', 'Wrinkles'],
                         'ingredients': ['15% Vitamin C', 'Vitamin E', 'Ferulic Acid'], 'reviews': 8923,
                         'benefits': ['Brightening', 'Antioxidant protection', 'Collagen boost']}
                    ],
                    'Niacinamide Serum': [
                        {'name': 'Niacinamide 10% + Zinc 1%', 'brand': 'The Ordinary', 'price': 5.90, 'tier': 'affordable',
                         'rating': 4.6, 'skin_types': ['Oily', 'Combination'], 'concerns': ['Acne', 'Large Pores', 'Redness'],
                         'ingredients': ['Niacinamide', 'Zinc PCA'], 'reviews': 45678,
                         'benefits': ['Pore reduction', 'Oil control', 'Redness calming']}
                    ],
                    'Hyaluronic Acid Serum': [
                        {'name': 'Hyaluronic Acid 2% + B5', 'brand': 'The Ordinary', 'price': 6.80, 'tier': 'affordable',
                         'rating': 4.5, 'skin_types': ['All'], 'concerns': ['Dryness', 'Dehydration'],
                         'ingredients': ['Hyaluronic Acid', 'Vitamin B5'], 'reviews': 34567,
                         'benefits': ['Intense hydration', 'Plumping', 'Skin smoothing']}
                    ],
                    'Retinol Serum': [
                        {'name': 'Retinol 0.5% in Squalane', 'brand': 'The Ordinary', 'price': 7.90, 'tier': 'affordable',
                         'rating': 4.4, 'skin_types': ['Aging'], 'concerns': ['Wrinkles', 'Texture'],
                         'ingredients': ['Retinol', 'Squalane'], 'reviews': 23456,
                         'benefits': ['Anti-aging', 'Fine line reduction', 'Skin renewal']}
                    ]
                }
            },
            'Moisturizer': {
                'sub_categories': {
                    'Gel Moisturizer': [
                        {'name': 'Hydro Boost Water Gel', 'brand': 'Neutrogena', 'price': 19.99, 'tier': 'affordable',
                         'rating': 4.6, 'skin_types': ['Oily', 'Combination'], 'concerns': ['Dehydration'],
                         'ingredients': ['Hyaluronic Acid', 'Glycerin'], 'reviews': 56789,
                         'benefits': ['Lightweight hydration', 'Non-greasy', 'Fresh finish']}
                    ],
                    'Cream Moisturizer': [
                        {'name': 'Moisturizing Cream', 'brand': 'CeraVe', 'price': 14.99, 'tier': 'affordable',
                         'rating': 4.8, 'skin_types': ['Dry', 'Normal', 'Sensitive'], 'concerns': ['Dryness'],
                         'ingredients': ['Ceramides', 'Hyaluronic Acid'], 'reviews': 67890,
                         'benefits': ['24-hour hydration', 'Barrier restoration', 'Non-comedogenic']}
                    ]
                }
            },
            'Sunscreen': {
                'sub_categories': {
                    'Mineral Sunscreen': [
                        {'name': 'Mineral Sunscreen SPF 50', 'brand': 'Supergoop', 'price': 38.00, 'tier': 'mid_range',
                         'rating': 4.7, 'skin_types': ['Sensitive', 'Normal'], 'concerns': ['Sun Protection'],
                         'ingredients': ['Zinc Oxide', 'Titanium Dioxide'], 'reviews': 34567,
                         'benefits': ['Broad spectrum protection', 'Gentle on skin', 'Non-irritating']}
                    ],
                    'Chemical Sunscreen': [
                        {'name': 'Anthelios SPF 60', 'brand': 'La Roche-Posay', 'price': 29.99, 'tier': 'affordable',
                         'rating': 4.8, 'skin_types': ['All'], 'concerns': ['Sun Protection'],
                         'ingredients': ['Mexoryl XL', 'Avobenzone'], 'reviews': 45678,
                         'benefits': ['High protection', 'Invisible finish', 'Water resistant']}
                    ]
                }
            },
            'Treatment': {
                'sub_categories': {
                    'Exfoliant': [
                        {'name': '2% BHA Liquid Exfoliant', 'brand': "Paula's Choice", 'price': 32.00, 'tier': 'mid_range',
                         'rating': 4.8, 'skin_types': ['Oily', 'Combination'], 'concerns': ['Acne', 'Large Pores', 'Texture'],
                         'ingredients': ['Salicylic Acid', 'Green Tea'], 'reviews': 78901,
                         'benefits': ['Unclogs pores', 'Smooths texture', 'Reduces breakouts']}
                    ],
                    'Mask': [
                        {'name': 'Advanced Night Repair Mask', 'brand': 'Estee Lauder', 'price': 85.00, 'tier': 'luxury',
                         'rating': 4.7, 'skin_types': ['Aging', 'Dry'], 'concerns': ['Wrinkles', 'Dullness'],
                         'ingredients': ['ChronoluxCB', 'Hyaluronic Acid'], 'reviews': 12345,
                         'benefits': ['Overnight repair', 'Morning radiance', 'Deep nourishment']}
                    ]
                }
            }
        }
    
    def load_feedback(self):
        """Load user feedback from JSON file"""
        if os.path.exists(self.feedback_file):
            try:
                with open(self.feedback_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_feedback(self, email, product_name, rating, feedback_text):
        """Save user feedback"""
        if email not in self.user_feedback:
            self.user_feedback[email] = []
        
        self.user_feedback[email].append({
            'product': product_name,
            'rating': rating,
            'feedback': feedback_text,
            'timestamp': datetime.now().isoformat(),
            'liked': rating >= 4
        })
        
        os.makedirs('data', exist_ok=True)
        with open(self.feedback_file, 'w') as f:
            json.dump(self.user_feedback, f, indent=2)
        
        return True
    
    def get_user_feedback(self, email):
        """Get user's feedback history"""
        return self.user_feedback.get(email, [])
    
    def get_recommendations_by_preferences(self, user_preferences, top_n=8):
        """Get recommendations based on user's saved preferences"""
        recommendations = []
        
        skin_type = user_preferences.get('skin_type', 'Normal')
        concerns = user_preferences.get('skin_concerns', [])
        budget = user_preferences.get('monthly_budget', 50)
        
        for category, category_data in self.products_db.items():
            for sub_cat, products in category_data['sub_categories'].items():
                for product in products:
                    score = self.calculate_enhanced_score(product, skin_type, concerns, budget)
                    
                    if score > 0.3:
                        recommendations.append({
                            'name': product['name'],
                            'brand': product['brand'],
                            'price': product['price'],
                            'rating': product['rating'],
                            'match_percentage': round(score * 100, 1),
                            'category': category,
                            'sub_category': sub_cat,
                            'benefits': product['benefits'],
                            'ingredients': product['ingredients'],
                            'reviews': product.get('reviews', 0)
                        })
        
        recommendations.sort(key=lambda x: x['match_percentage'], reverse=True)
        return recommendations[:top_n]
    
    def calculate_enhanced_score(self, product, skin_type, concerns, budget):
        """Enhanced scoring with more factors"""
        score = 0
        
        # Skin type match (35%)
        if skin_type in product.get('skin_types', []):
            score += 0.35
        elif 'All' in product.get('skin_types', []):
            score += 0.20
        elif any(st in product.get('skin_types', []) for st in ['Normal', 'Combination']):
            score += 0.15
            
        # Concern match (30%)
        product_concerns = product.get('concerns', [])
        matched = sum(1 for c in concerns if c in product_concerns)
        if matched > 0 and concerns:
            score += 0.30 * min(matched / len(concerns), 1)
            
        # Budget match (20%)
        tier = product.get('tier', 'mid_range')
        if tier == 'affordable' and budget <= 50:
            score += 0.20
        elif tier == 'mid_range' and 30 <= budget <= 120:
            score += 0.20
        elif tier == 'luxury' and budget > 100:
            score += 0.15
            
        # Rating boost (15%)
        score += (product['rating'] - 4) * 0.15
        
        return min(score, 1.0)
    
    def get_ingredient_insights(self):
        """Get detailed ingredient information"""
        return {
            'Niacinamide': {
                'benefits': ['Reduces inflammation', 'Minimizes pores', 'Controls oil', 'Brightens skin'],
                'best_for': ['Acne', 'Large pores', 'Redness', 'Dullness'],
                'rating': 4.8,
                'science': 'Vitamin B3 that helps build keratin and improve skin barrier function'
            },
            'Vitamin C': {
                'benefits': ['Antioxidant protection', 'Brightens skin', 'Reduces pigmentation', 'Boosts collagen'],
                'best_for': ['Pigmentation', 'Dullness', 'Aging', 'Sun damage'],
                'rating': 4.9,
                'science': 'Powerful antioxidant that neutralizes free radicals and supports collagen production'
            },
            'Hyaluronic Acid': {
                'benefits': ['Deep hydration', 'Plumps skin', 'Reduces fine lines', 'Improves elasticity'],
                'best_for': ['Dryness', 'Dehydration', 'Fine lines', 'Loss of firmness'],
                'rating': 4.7,
                'science': 'Holds 1000x its weight in water, providing intense moisture retention'
            },
            'Retinol': {
                'benefits': ['Anti-aging', 'Cell turnover', 'Reduces wrinkles', 'Improves texture'],
                'best_for': ['Wrinkles', 'Fine lines', 'Uneven texture', 'Aging concerns'],
                'rating': 4.6,
                'science': 'Vitamin A derivative that accelerates cell renewal and collagen production'
            },
            'Salicylic Acid': {
                'benefits': ['Exfoliates pores', 'Reduces acne', 'Controls oil', 'Prevents breakouts'],
                'best_for': ['Acne', 'Blackheads', 'Whiteheads', 'Oily skin'],
                'rating': 4.5,
                'science': 'Beta hydroxy acid that penetrates deep into pores to clear congestion'
            },
            'Ceramides': {
                'benefits': ['Restores barrier', 'Locks in moisture', 'Protects skin', 'Reduces sensitivity'],
                'best_for': ['Dryness', 'Sensitive skin', 'Barrier damage', 'Eczema'],
                'rating': 4.8,
                'science': 'Lipids that form the skin barrier and retain moisture'
            }
        }
    
    def get_recommendations(self, user_preferences=None, top_n=6):
        """Get general recommendations (for backward compatibility)"""
        if user_preferences is None:
            user_preferences = {'skin_type': 'Normal', 'skin_concerns': [], 'monthly_budget': 50}
        return self.get_recommendations_by_preferences(user_preferences, top_n)