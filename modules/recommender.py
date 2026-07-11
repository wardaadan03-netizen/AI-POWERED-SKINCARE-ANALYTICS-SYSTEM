"""
Skincare Recommendation Module
Provides product recommendations based on user preferences
"""

import random
import json
import os
from datetime import datetime

class SkincareRecommender:
    """Handles product recommendations for skincare"""
    
    def __init__(self, data_path=None):
        self.data_path = data_path or 'data/raw/skincare_dataset.csv'
        self.feedback_path = 'data/feedback.json'
        self.products = self.load_products()
        self.feedback = self.load_feedback()
    
    def load_products(self):
        """Load products from dataset or use defaults"""
        return [
            {'name': 'CeraVe Hydrating Cleanser', 'brand': 'CeraVe', 'price': 12.99, 'rating': 4.7, 'category': 'Cleanser', 'skin_types': ['Oily', 'Dry', 'Combination', 'Normal', 'Sensitive'], 'concerns': ['Dryness', 'Sensitive'], 'ingredients': ['Ceramides', 'Hyaluronic Acid', 'Glycerin']},
            {'name': 'La Roche-Posay Effaclar', 'brand': 'La Roche-Posay', 'price': 16.99, 'rating': 4.6, 'category': 'Cleanser', 'skin_types': ['Oily', 'Combination'], 'concerns': ['Acne', 'Large Pores'], 'ingredients': ['Salicylic Acid', 'Zinc PCA', 'Glycerin']},
            {'name': 'The Ordinary Niacinamide 10%', 'brand': 'The Ordinary', 'price': 5.90, 'rating': 4.4, 'category': 'Serum', 'skin_types': ['Oily', 'Combination', 'Sensitive'], 'concerns': ['Acne', 'Large Pores', 'Redness'], 'ingredients': ['Niacinamide', 'Zinc PCA']},
            {'name': "Paula's Choice Vitamin C", 'brand': "Paula's Choice", 'price': 49.00, 'rating': 4.6, 'category': 'Serum', 'skin_types': ['Oily', 'Dry', 'Combination', 'Normal'], 'concerns': ['Pigmentation', 'Wrinkles', 'Dullness'], 'ingredients': ['Vitamin C', 'Vitamin E', 'Ferulic Acid']},
            {'name': 'La Roche-Posay Anthelios', 'brand': 'La Roche-Posay', 'price': 29.99, 'rating': 4.7, 'category': 'Sunscreen', 'skin_types': ['Oily', 'Dry', 'Combination', 'Normal', 'Sensitive'], 'concerns': ['Sun Protection'], 'ingredients': ['Mexoryl XL', 'Titanium Dioxide']},
            {'name': "Kiehl's Ultra Facial Cream", 'brand': "Kiehl's", 'price': 38.00, 'rating': 4.5, 'category': 'Moisturizer', 'skin_types': ['Oily', 'Dry', 'Combination', 'Normal'], 'concerns': ['Dryness', 'Wrinkles'], 'ingredients': ['Squalane', 'Glycerin']},
            {'name': 'CeraVe Moisturizing Cream', 'brand': 'CeraVe', 'price': 14.99, 'rating': 4.8, 'category': 'Moisturizer', 'skin_types': ['Oily', 'Dry', 'Combination', 'Normal', 'Sensitive'], 'concerns': ['Dryness', 'Sensitive'], 'ingredients': ['Ceramides', 'Hyaluronic Acid', 'Petrolatum']},
            {'name': 'Supergoop! Unseen Sunscreen', 'brand': 'Supergoop!', 'price': 38.00, 'rating': 4.6, 'category': 'Sunscreen', 'skin_types': ['Oily', 'Dry', 'Combination', 'Normal', 'Sensitive'], 'concerns': ['Sun Protection'], 'ingredients': ['Avobenzone', 'Homosalate', 'Octisalate']},
            {'name': 'Fresh Soy Face Cleanser', 'brand': 'Fresh', 'price': 38.00, 'rating': 4.5, 'category': 'Cleanser', 'skin_types': ['Oily', 'Dry', 'Combination', 'Normal', 'Sensitive'], 'concerns': ['Dullness', 'Sensitive'], 'ingredients': ['Soy Proteins', 'Rosewater', 'Cucumber Extract']},
            {'name': 'SkinCeuticals C E Ferulic', 'brand': 'SkinCeuticals', 'price': 182.00, 'rating': 4.9, 'category': 'Serum', 'skin_types': ['Oily', 'Dry', 'Combination', 'Normal'], 'concerns': ['Pigmentation', 'Wrinkles', 'Dullness'], 'ingredients': ['Vitamin C', 'Vitamin E', 'Ferulic Acid']},
            {'name': 'La Mer Crème de la Mer', 'brand': 'La Mer', 'price': 380.00, 'rating': 4.7, 'category': 'Moisturizer', 'skin_types': ['Oily', 'Dry', 'Combination', 'Normal', 'Sensitive'], 'concerns': ['Wrinkles', 'Dryness', 'Sensitive'], 'ingredients': ['Miracle Broth', 'Lime Extract', 'Seaweed']},
            {'name': 'Shiseido Ultimate Sun Protector', 'brand': 'Shiseido', 'price': 52.00, 'rating': 4.8, 'category': 'Sunscreen', 'skin_types': ['Oily', 'Dry', 'Combination', 'Normal'], 'concerns': ['Sun Protection'], 'ingredients': ['WetForce Technology', 'Hyaluronic Acid', 'Green Tea']},
        ]
    
    def load_feedback(self):
        """Load user feedback from file"""
        os.makedirs(os.path.dirname(self.feedback_path), exist_ok=True)
        
        if os.path.exists(self.feedback_path):
            try:
                with open(self.feedback_path, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_feedback(self, user_email, product_name, rating, feedback_text=""):
        """Save user feedback"""
        if user_email not in self.feedback:
            self.feedback[user_email] = []
        
        self.feedback[user_email].append({
            'product': product_name,
            'rating': rating,
            'feedback': feedback_text,
            'timestamp': datetime.now().isoformat(),
            'liked': rating >= 4
        })
        
        # Save to file
        os.makedirs(os.path.dirname(self.feedback_path), exist_ok=True)
        with open(self.feedback_path, 'w') as f:
            json.dump(self.feedback, f, indent=2, default=str)
        
        return True
    
    def get_user_feedback(self, user_email):
        """Get user feedback history"""
        return self.feedback.get(user_email, [])
    
    def calculate_product_score(self, product, skin_type=None, concerns=None, budget=None, age=None, gender=None, uses_retinol=False, uses_vitamin_c=False, uses_niacinamide=False):
        """Calculate match score for a product"""
        score = 0
        
        # Skin type match (30 points)
        if skin_type and product.get('skin_types'):
            if skin_type in product['skin_types']:
                score += 30
            elif any(st in product['skin_types'] for st in ['Combination', 'Normal']):
                score += 15
        
        # Concern match (25 points)
        if concerns and product.get('concerns'):
            matched = sum(1 for c in concerns if c in product['concerns'])
            if matched > 0:
                score += min(25, matched * 8)
        
        # Budget match (20 points)
        if budget and product.get('price'):
            if product['price'] <= budget:
                score += 20
            elif product['price'] <= budget * 1.5:
                score += 10
        
        # Rating bonus (15 points)
        if product.get('rating'):
            score += (product['rating'] - 3) * 8
        
        # Ingredient match (10 points)
        if product.get('ingredients'):
            ingredients_str = str(product['ingredients'])
            if uses_retinol and 'Retinol' in ingredients_str:
                score += 3
            if uses_vitamin_c and 'Vitamin C' in ingredients_str:
                score += 3
            if uses_niacinamide and 'Niacinamide' in ingredients_str:
                score += 4
        
        return min(100, score)
    
    def get_recommendations(self, user_preferences, top_n=8):
        """Get product recommendations based on user preferences"""
        skin_type = user_preferences.get('skin_type')
        concerns = user_preferences.get('skin_concerns', [])
        budget = user_preferences.get('monthly_budget', 50)
        age = user_preferences.get('age')
        gender = user_preferences.get('gender')
        
        scored_products = []
        for product in self.products:
            score = self.calculate_product_score(
                product, skin_type, concerns, budget, age, gender
            )
            scored_products.append({
                **product,
                'match_percentage': score,
                'benefits': product.get('concerns', ['Skin care'])[:3]
            })
        
        # Sort by match score
        scored_products.sort(key=lambda x: x['match_percentage'], reverse=True)
        
        # Add some randomness for variety
        random.seed(42)
        random.shuffle(scored_products[:top_n * 2])
        
        return scored_products[:top_n]
    
    def get_recommendations_by_preferences(self, preferences, top_n=8):
        """Alias for get_recommendations"""
        return self.get_recommendations(preferences, top_n)
    
    def get_ingredient_insights(self):
        """Get ingredient insights for the ingredients page"""
        return {
            'Niacinamide': {
                'rating': 4.8,
                'benefits': ['Reduces inflammation', 'Minimizes pores', 'Brightens skin'],
                'best_for': ['Oily skin', 'Acne-prone skin', 'Hyperpigmentation'],
                'science': 'Niacinamide (Vitamin B3) is a water-soluble vitamin that works by strengthening the skin barrier and reducing water loss.'
            },
            'Vitamin C': {
                'rating': 4.7,
                'benefits': ['Antioxidant protection', 'Brightening', 'Collagen support'],
                'best_for': ['Dull skin', 'Hyperpigmentation', 'Aging skin'],
                'science': 'L-Ascorbic Acid (Vitamin C) is a potent antioxidant that neutralizes free radicals and stimulates collagen synthesis.'
            },
            'Hyaluronic Acid': {
                'rating': 4.9,
                'benefits': ['Deep hydration', 'Plumping', 'Barrier support'],
                'best_for': ['Dry skin', 'Dehydrated skin', 'All skin types'],
                'science': 'Hyaluronic Acid is a naturally occurring humectant that can hold up to 1000 times its weight in water.'
            },
            'Retinol': {
                'rating': 4.6,
                'benefits': ['Cell turnover', 'Collagen stimulation', 'Fine line reduction'],
                'best_for': ['Aging skin', 'Acne-prone skin', 'Textured skin'],
                'science': 'Retinol (Vitamin A derivative) works by increasing cell turnover and stimulating collagen production.'
            },
            'Salicylic Acid': {
                'rating': 4.4,
                'benefits': ['Exfoliation', 'Pore clearing', 'Acne treatment'],
                'best_for': ['Oily skin', 'Acne-prone skin', 'Blackheads'],
                'science': 'Salicylic acid is a BHA (beta hydroxy acid) that penetrates into pores to dissolve dead skin cells and excess oil.'
            }
        }
    
    def predict_product_rating(self, user_preferences, product_name):
        """Predict rating for a specific product"""
        # Find the product
        product = next((p for p in self.products if p['name'].lower() == product_name.lower()), None)
        
        if not product:
            return 4.0
        
        # Base rating from product
        base_rating = product.get('rating', 4.0)
        
        # Adjust based on user preferences
        adjustment = 0
        skin_type = user_preferences.get('skin_type')
        if skin_type and skin_type in product.get('skin_types', []):
            adjustment += 0.3
        
        concerns = user_preferences.get('skin_concerns', [])
        if concerns and product.get('concerns'):
            matched = sum(1 for c in concerns if c in product['concerns'])
            adjustment += min(0.5, matched * 0.15)
        
        predicted = min(5.0, max(1.0, base_rating + adjustment))
        return round(predicted, 1)