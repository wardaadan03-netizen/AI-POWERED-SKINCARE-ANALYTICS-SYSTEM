from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime
import random
import numpy as np
import os
import secrets
import json

# Import modules
from modules.authentication import UserAuthentication
from modules.recommender import SkincareRecommender

app = Flask(__name__)

# ============================================
# CONFIG
# ============================================

app.secret_key = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
DEBUG = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}
MAX_CONTENT_LENGTH = 10 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('data', exist_ok=True)
os.makedirs('data/raw', exist_ok=True)
os.makedirs('data/processed', exist_ok=True)
os.makedirs('data/models', exist_ok=True)

auth = UserAuthentication()
recommender = SkincareRecommender()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def login_required(f):
    from functools import wraps
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_email' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapper

# ============================================
# PAGE ROUTES
# ============================================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        success, result = auth.login_user(email, password)
        if success:
            session['user_email'] = email
            session['user_id'] = result
            return jsonify({'success': True, 'redirect': '/dashboard'})
        return jsonify({'success': False, 'error': result}), 401
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        success, result = auth.register_user(email, password)
        if success:
            session['user_email'] = email
            session['user_id'] = result
            return jsonify({'success': True, 'redirect': '/profile-setup'})
        return jsonify({'success': False, 'error': result}), 400
    return render_template('register.html')

@app.route('/profile-setup', methods=['GET', 'POST'])
@login_required
def profile_setup():
    if request.method == 'POST':
        # Get form data
        skin_type = request.form.get('skin_type')
        skin_concerns = request.form.getlist('skin_concerns')
        age = request.form.get('age')
        gender = request.form.get('gender')
        monthly_budget = request.form.get('monthly_budget')
        
        # Debug
        print(f"📋 Skin Type: {skin_type}")
        print(f"📋 Skin Concerns: {skin_concerns}")
        print(f"📋 Age: {age}")
        print(f"📋 Gender: {gender}")
        print(f"📋 Budget: {monthly_budget}")
        
        # Validate
        if not skin_type or skin_type == '' or skin_type == 'Select your skin type...':
            return jsonify({'success': False, 'error': 'Please select your skin type'}), 400
        
        if not skin_concerns or len(skin_concerns) == 0:
            return jsonify({'success': False, 'error': 'Please select at least one skin concern'}), 400
        
        if not age or age == '':
            return jsonify({'success': False, 'error': 'Please enter your age'}), 400
        
        try:
            age_int = int(age)
            if age_int < 18:
                return jsonify({'success': False, 'error': 'You must be at least 18 years old'}), 400
        except ValueError:
            return jsonify({'success': False, 'error': 'Please enter a valid age'}), 400
        
        # Build preferences
        preferences = {
            'skin_type': skin_type,
            'skin_concerns': skin_concerns,
            'age': age_int,
            'gender': gender or 'Prefer not say',
            'monthly_budget': float(monthly_budget) if monthly_budget else 50
        }
        
        # Save to auth
        success = auth.update_user_preferences(session['user_email'], preferences)
        
        if success:
            print(f"✅ Profile saved for {session['user_email']}: {preferences}")
            return jsonify({'success': True, 'redirect': '/dashboard'})
        else:
            return jsonify({'success': False, 'error': 'Failed to save preferences'}), 500
    
    return render_template('profile_setup.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/recommendations')
@login_required
def recommendations_page():
    return render_template('recommendations.html')

@app.route('/profile')
@login_required
def profile_page():
    return render_template('profile.html')

@app.route('/ingredients')
@login_required
def ingredients_page():
    return render_template('ingredients.html')

@app.route('/disclaimer')
def disclaimer():
    return render_template('disclaimer.html')

@app.route('/qr-code')
@login_required
def qr_code():
    return render_template('qr_code.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/favicon.ico')
def favicon():
    return '', 204

# ============================================
# API ROUTES
# ============================================

@app.route('/api/recommendations', methods=['GET', 'POST'])
def get_recommendations():
    user_email = session.get('user_email')
    
    if user_email:
        user_data = auth.get_user_data(user_email)
        preferences = user_data.get('preferences', {})
        print(f"📋 User preferences: {preferences}")
    else:
        preferences = {'skin_type': 'Normal', 'skin_concerns': [], 'monthly_budget': 50}
    
    products = recommender.get_recommendations(preferences, top_n=8)
    
    if not products:
        products = [
            {'name': 'CeraVe Hydrating Cleanser', 'brand': 'CeraVe', 'price': 12.99, 'rating': 4.7, 'match_percentage': 92, 'category': 'Cleanser', 'benefits': ['Hydrating', 'Gentle'], 'skin_types': ['Oily', 'Dry', 'Combination', 'Normal', 'Sensitive'], 'concerns': ['Dryness', 'Sensitive']},
            {'name': 'The Ordinary Niacinamide', 'brand': 'The Ordinary', 'price': 5.90, 'rating': 4.4, 'match_percentage': 88, 'category': 'Serum', 'benefits': ['Pore reduction', 'Oil control'], 'skin_types': ['Oily', 'Combination'], 'concerns': ['Acne', 'Large Pores']},
            {'name': "Paula's Choice Vitamin C", 'brand': "Paula's Choice", 'price': 49.00, 'rating': 4.6, 'match_percentage': 85, 'category': 'Serum', 'benefits': ['Brightening', 'Antioxidant'], 'skin_types': ['Oily', 'Dry', 'Combination', 'Normal'], 'concerns': ['Pigmentation', 'Wrinkles']},
            {'name': 'La Roche-Posay Anthelios', 'brand': 'La Roche-Posay', 'price': 29.99, 'rating': 4.7, 'match_percentage': 90, 'category': 'Sunscreen', 'benefits': ['Sun protection', 'Gentle'], 'skin_types': ['All'], 'concerns': ['Sun Protection']},
            {'name': "Kiehl's Ultra Facial Cream", 'brand': "Kiehl's", 'price': 38.00, 'rating': 4.5, 'match_percentage': 82, 'category': 'Moisturizer', 'benefits': ['24hr hydration', 'Smoothing'], 'skin_types': ['All'], 'concerns': ['Dryness']},
            {'name': 'CeraVe Moisturizing Cream', 'brand': 'CeraVe', 'price': 14.99, 'rating': 4.8, 'match_percentage': 78, 'category': 'Moisturizer', 'benefits': ['Barrier repair', 'Deep hydration'], 'skin_types': ['All'], 'concerns': ['Dryness', 'Sensitive']}
        ]
    
    return jsonify({'success': True, 'products': products})

@app.route('/api/personalized-recommendations', methods=['GET'])
@login_required
def get_personalized_recommendations():
    user_email = session.get('user_email')
    user_data = auth.get_user_data(user_email)
    preferences = user_data.get('preferences', {})
    
    print(f"📋 Personalized recommendations for: {user_email}")
    print(f"📋 Preferences: {preferences}")
    
    if not preferences or not preferences.get('skin_type'):
        return jsonify({'success': True, 'products': []})
    
    recommendations = recommender.get_recommendations_by_preferences(preferences, top_n=8)
    return jsonify({'success': True, 'products': recommendations})

@app.route('/api/analytics')
@login_required
def get_analytics():
    user_email = session.get('user_email')
    user_data = auth.get_user_data(user_email)
    preferences = user_data.get('preferences', {})
    
    scatter_data = {
        'data': [{
            'x': [25, 30, 35, 40, 45, 50, 55, 60],
            'y': [50, 100, 150, 200, 250, 300, 350, 400],
            'z': [85, 83, 81, 79, 76, 73, 71, 68],
            'mode': 'markers',
            'type': 'scatter3d',
            'marker': {'size': 10, 'color': [85, 83, 81, 79, 76, 73, 71, 68], 'colorscale': 'Viridis'}
        }],
        'layout': {'title': '3D Analysis', 'height': 400, 'paper_bgcolor': 'rgba(0,0,0,0)', 'plot_bgcolor': 'rgba(0,0,0,0)'}
    }

    z_data = [[70 + np.sin(i / 2) * 10 + np.cos(j / 2) * 10 for j in range(10)] for i in range(10)]
    surface_data = {
        'data': [{'z': z_data, 'type': 'surface', 'colorscale': 'Viridis'}],
        'layout': {'title': 'Surface Analysis', 'height': 400, 'paper_bgcolor': 'rgba(0,0,0,0)', 'plot_bgcolor': 'rgba(0,0,0,0)'}
    }

    return jsonify({
        'ingredient_network': scatter_data,
        'budget_analysis': surface_data,
        'skin_distribution': scatter_data,
        'user_stats': {
            'skin_health_score': random.randint(75, 95),
            'routine_consistency': random.randint(70, 95),
            'product_match_score': random.randint(70, 90),
            'total_recommendations': random.randint(5, 12)
        }
    })

@app.route('/api/ingredients')
def get_ingredients():
    return jsonify({
        'success': True,
        'ingredients': recommender.get_ingredient_insights()
    })

@app.route('/api/submit-feedback', methods=['POST'])
def submit_feedback():
    data = request.json or {}
    user_email = session.get('user_email', 'anonymous')
    success = recommender.save_feedback(
        user_email,
        data.get('product_name', 'Platform Experience'),
        data.get('rating', 5),
        data.get('feedback', '')
    )
    return jsonify({'success': success})

@app.route('/api/predict-rating', methods=['POST'])
def predict_rating():
    data = request.json or {}
    product_name = data.get('product_name', '')
    user_email = session.get('user_email')
    
    if user_email:
        user_data = auth.get_user_data(user_email)
        preferences = user_data.get('preferences', {})
    else:
        preferences = {}
    
    predicted_rating = recommender.predict_product_rating(preferences, product_name)
    return jsonify({
        'success': True,
        'predicted_rating': predicted_rating,
        'confidence': random.randint(75, 95),
        'product': product_name
    })

@app.route('/api/user/profile', methods=['GET'])
def get_user_profile():
    user_email = session.get('user_email')
    if not user_email:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401

    user_data = auth.get_user_data(user_email)
    if user_data:
        return jsonify({
            'success': True,
            'user': {
                'email': user_email,
                'user_id': user_data.get('user_id'),
                'member_since': user_data.get('created_at'),
                'last_login': user_data.get('last_login'),
                'preferences': user_data.get('preferences', {}),
                'total_recommendations': len(recommender.get_user_feedback(user_email)),
                'login_count': len(user_data.get('history', []))
            }
        })
    return jsonify({'success': False, 'error': 'User not found'}), 404

@app.route('/api/user/preferences', methods=['POST'])
def update_user_preferences():
    user_email = session.get('user_email')
    if not user_email:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401

    preferences = request.json or {}
    success = auth.update_user_preferences(user_email, preferences)
    return jsonify({'success': success})

@app.route('/api/user/activity', methods=['GET'])
def get_user_activity():
    user_email = session.get('user_email')
    if not user_email:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401

    user_data = auth.get_user_data(user_email)
    activities = user_data.get('history', [])
    return jsonify({'success': True, 'activities': activities[-20:]})

@app.route('/api/user/delete', methods=['DELETE'])
def delete_user_account():
    user_email = session.get('user_email')
    if not user_email:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401

    success = auth.delete_user(user_email)
    if success:
        session.clear()
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Could not delete account'}), 500

# ============================================
# ERROR HANDLING
# ============================================

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error='Page not found'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('error.html', error='Server error occurred'), 500

@app.errorhandler(Exception)
def handle_exception(error):
    app.logger.error(f"Unhandled exception: {str(error)}")
    return render_template('error.html', error=str(error)), 500

# ============================================
# RUN THE APP
# ============================================

if __name__ == '__main__':
    print("=" * 60)
    print("✨ Inzaghi's Bliss Skincare Platform")
    print("=" * 60)
    print(f"Server running at: http://localhost:5000")
    print(f"Debug mode: {DEBUG}")
    print("Press CTRL+C to quit")
    print("=" * 60)
    app.run(debug=DEBUG, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))