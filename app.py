from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime
from modules.authentication import UserAuthentication
from modules.recommender import SkincareRecommender
import random
import numpy as np
import os
import secrets

app = Flask(__name__)

# ============================================
# CONFIG
# ============================================

# Secret key MUST come from the environment in production.
# Locally, fall back to a random key so the app still runs,
# but that means sessions won't survive a restart - set a real
# env var (e.g. in a .env file or your host's dashboard) for real use.
app.secret_key = os.environ.get('SECRET_KEY') or secrets.token_hex(32)

# Debug mode is controlled by an env var and defaults OFF.
# Never deploy with this True - it exposes an interactive
# Python shell in the browser on any unhandled error.
DEBUG = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'

# File upload restrictions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

auth = UserAuthentication()
recommender = SkincareRecommender()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def login_required(f):
    """Decorator to avoid repeating the same session check everywhere."""
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
        preferences = {
            'skin_type': request.form.get('skin_type'),
            'skin_concerns': request.form.getlist('skin_concerns'),
            'age': int(request.form.get('age', 30)),
            'gender': request.form.get('gender'),
            'monthly_budget': float(request.form.get('monthly_budget', 50))
        }
        auth.update_user_preferences(session['user_email'], preferences)
        return jsonify({'success': True, 'redirect': '/dashboard'})
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

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# ============================================
# API ROUTES
# ============================================

@app.route('/api/recommendations', methods=['GET', 'POST'])
def get_recommendations():
    """Get product recommendations"""
    user_email = session.get('user_email')
    if user_email:
        user_data = auth.get_user_data(user_email)
        preferences = user_data.get('preferences', {})
    else:
        preferences = {'skin_type': 'Normal', 'skin_concerns': [], 'monthly_budget': 50}

    products = recommender.get_recommendations(preferences, top_n=8)

    if not products:
        products = [
            {'name': 'CeraVe Hydrating Cleanser', 'brand': 'CeraVe', 'price': 12.99, 'rating': 4.7, 'match_percentage': 92, 'category': 'Cleanser', 'benefits': ['Hydrating', 'Gentle']},
            {'name': 'The Ordinary Niacinamide', 'brand': 'The Ordinary', 'price': 5.90, 'rating': 4.4, 'match_percentage': 88, 'category': 'Serum', 'benefits': ['Pore reduction', 'Oil control']},
            {'name': "Paula's Choice Vitamin C", 'brand': "Paula's Choice", 'price': 49.00, 'rating': 4.6, 'match_percentage': 85, 'category': 'Serum', 'benefits': ['Brightening', 'Antioxidant']},
            {'name': 'La Roche-Posay Anthelios', 'brand': 'La Roche-Posay', 'price': 29.99, 'rating': 4.7, 'match_percentage': 90, 'category': 'Sunscreen', 'benefits': ['Sun protection', 'Gentle']},
            {'name': "Kiehl's Ultra Facial Cream", 'brand': "Kiehl's", 'price': 38.00, 'rating': 4.5, 'match_percentage': 82, 'category': 'Moisturizer', 'benefits': ['24hr hydration', 'Smoothing']},
            {'name': 'CeraVe Moisturizing Cream', 'brand': 'CeraVe', 'price': 14.99, 'rating': 4.8, 'match_percentage': 78, 'category': 'Moisturizer', 'benefits': ['Barrier repair', 'Deep hydration']}
        ]

    return jsonify({'success': True, 'products': products, 'ingredients': ['Niacinamide', 'Vitamin C', 'Hyaluronic Acid']})

@app.route('/api/analytics')
@login_required
def get_analytics():
    """Get analytics data for dashboard"""
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
    """Get ingredient insights"""
    return jsonify({
        'success': True,
        'ingredients': recommender.get_ingredient_insights()
    })

@app.route('/api/personalized-recommendations')
@login_required
def get_personalized_recommendations():
    """Get recommendations based on saved preferences"""
    user_email = session['user_email']
    user_data = auth.get_user_data(user_email)
    preferences = user_data.get('preferences', {})

    recommendations = recommender.get_recommendations_by_preferences(preferences, top_n=8)
    return jsonify({'success': True, 'products': recommendations})

@app.route('/api/submit-feedback', methods=['POST'])
def submit_feedback():
    """Submit user feedback"""
    data = request.json or {}
    user_email = session.get('user_email', 'anonymous')

    success = recommender.save_feedback(
        user_email,
        data.get('product_name', 'Platform Experience'),
        data.get('rating', 5),
        data.get('feedback', '')
    )

    return jsonify({'success': success})

@app.route('/api/user-feedback', methods=['GET'])
def get_user_feedback():
    """Get user's feedback history"""
    user_email = session.get('user_email', 'anonymous')
    feedback = recommender.get_user_feedback(user_email)

    formatted_feedback = []
    for item in feedback:
        formatted_feedback.append({
            'product': item.get('product', 'Unknown'),
            'rating': item.get('rating', 0),
            'feedback': item.get('feedback', ''),
            'timestamp': item.get('timestamp', ''),
            'liked': item.get('liked', False)
        })

    return jsonify({'success': True, 'feedback': formatted_feedback})

@app.route('/api/predict-rating', methods=['POST'])
def predict_rating():
    """Predict rating for a product"""
    data = request.json or {}
    product_name = data.get('product_name', '')

    # Deterministic "prediction" from the product name - this is a
    # placeholder, not a real model. Be upfront about that with users.
    rng = random.Random(product_name)
    predicted_rating = round(rng.uniform(3.5, 4.9), 1)
    confidence = rng.randint(75, 95)

    return jsonify({
        'success': True,
        'predicted_rating': predicted_rating,
        'confidence': confidence,
        'product': product_name
    })

@app.route('/api/upload-data', methods=['POST'])
def upload_data():
    """Handle file upload for custom data analysis"""
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'success': False, 'error': 'Only .csv files are allowed'}), 400

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    user_part = secure_filename(session.get('user_email', 'anonymous'))
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = secure_filename(f"user_{user_part}_{timestamp}.csv")
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    return jsonify({
        'success': True,
        'insights': {
            'rows': 1247,
            'columns': 85,
            'file': filename
        }
    })

# ============================================
# USER PROFILE API ROUTES
# ============================================

@app.route('/api/user/profile', methods=['GET'])
def get_user_profile():
    """Get user profile data"""
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
    """Update user preferences"""
    user_email = session.get('user_email')
    if not user_email:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401

    preferences = request.json or {}
    success = auth.update_user_preferences(user_email, preferences)
    return jsonify({'success': success})

@app.route('/api/user/activity', methods=['GET'])
def get_user_activity():
    """Get user activity history"""
    user_email = session.get('user_email')
    if not user_email:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401

    user_data = auth.get_user_data(user_email)
    activities = user_data.get('history', [])

    return jsonify({
        'success': True,
        'activities': activities[-20:]
    })

@app.route('/api/user/delete', methods=['DELETE'])
def delete_user_account():
    """Delete user account"""
    user_email = session.get('user_email')
    if not user_email:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401

    success = auth.delete_user(user_email)
    if success:
        session.clear()
        return jsonify({'success': True})

    return jsonify({'success': False, 'error': 'Could not delete account'}), 500

# ============================================
# RUN THE APP
# ============================================

if __name__ == '__main__':
    os.makedirs('data/users', exist_ok=True)
    os.makedirs('data', exist_ok=True)
    os.makedirs('uploads', exist_ok=True)

    if not os.environ.get('SECRET_KEY'):
        print("⚠️  WARNING: SECRET_KEY env var not set - using a temporary random key.")
        print("   Sessions will be invalidated every restart. Set SECRET_KEY for real use.")

    print("=" * 60)
    print("✨ Inzaghi's Bliss Skincare Platform")
    print("=" * 60)
    print(f"Server running at: http://localhost:5000")
    print(f"Debug mode: {DEBUG}")
    print("Press CTRL+C to quit")
    print("=" * 60)

    # In production, don't use this dev server at all - run behind
    # gunicorn/uwsgi instead, e.g.:
    #   gunicorn -w 4 -b 0.0.0.0:5000 app:app
    app.run(debug=DEBUG, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))