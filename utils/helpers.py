"""
Helper Functions for Skincare Analytics Platform
Contains utility functions for data processing, validation, and formatting
"""

import re
import hashlib
import secrets
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from functools import wraps
from flask import session, redirect, url_for, request, jsonify

# ============================================
# DATA VALIDATION FUNCTIONS
# ============================================

def validate_email(email):
    """
    Validate email format
    
    Args:
        email: Email string to validate
    
    Returns:
        Boolean indicating if email is valid
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_password(password):
    """
    Validate password strength
    
    Args:
        password: Password string to validate
    
    Returns:
        Tuple (is_valid, message)
    """
    if len(password) < 6:
        return False, "Password must be at least 6 characters"
    
    if len(password) > 100:
        return False, "Password is too long"
    
    return True, "Password is valid"

def validate_age(age):
    """
    Validate age value
    
    Args:
        age: Age value to validate
    
    Returns:
        Boolean indicating if age is valid
    """
    try:
        age = int(age)
        return 18 <= age <= 120
    except (ValueError, TypeError):
        return False

def validate_budget(budget):
    """
    Validate budget amount
    
    Args:
        budget: Budget value to validate
    
    Returns:
        Boolean indicating if budget is valid
    """
    try:
        budget = float(budget)
        return 0 <= budget <= 100000
    except (ValueError, TypeError):
        return False

# ============================================
# DATA PROCESSING FUNCTIONS
# ============================================

def clean_text(text):
    """
    Clean and normalize text
    
    Args:
        text: Input text string
    
    Returns:
        Cleaned text string
    """
    if pd.isna(text):
        return ""
    
    text = str(text)
    text = text.strip()
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'\s+', ' ', text)
    
    return text

def standardize_skin_type(skin_type):
    """
    Standardize skin type values
    
    Args:
        skin_type: Input skin type string
    
    Returns:
        Standardized skin type
    """
    skin_type = str(skin_type).lower().strip()
    
    mapping = {
        'oily': 'Oily',
        'dry': 'Dry',
        'combination': 'Combination',
        'combo': 'Combination',
        'normal': 'Normal',
        'sensitive': 'Sensitive'
    }
    
    return mapping.get(skin_type, 'Normal')

def standardize_gender(gender):
    """
    Standardize gender values
    
    Args:
        gender: Input gender string
    
    Returns:
        Standardized gender
    """
    gender = str(gender).lower().strip()
    
    mapping = {
        'female': 'Female',
        'f': 'Female',
        'male': 'Male',
        'm': 'Male',
        'non-binary': 'Non-binary',
        'nonbinary': 'Non-binary',
        'nb': 'Non-binary'
    }
    
    return mapping.get(gender, 'Prefer not say')

# ============================================
# HASHING AND SECURITY FUNCTIONS
# ============================================

def hash_password(password):
    """
    Hash password using SHA-256 with salt
    
    Args:
        password: Plain text password
    
    Returns:
        Hashed password string with salt
    """
    salt = secrets.token_hex(16)
    hash_obj = hashlib.sha256((password + salt).encode())
    return f"{salt}:{hash_obj.hexdigest()}"

def verify_password(password, hashed_password):
    """
    Verify password against hash
    
    Args:
        password: Plain text password
        hashed_password: Stored hash string
    
    Returns:
        Boolean indicating if password matches
    """
    try:
        salt, hash_value = hashed_password.split(':')
        hash_obj = hashlib.sha256((password + salt).encode())
        return hash_obj.hexdigest() == hash_value
    except:
        return False

def generate_token():
    """
    Generate secure random token
    
    Returns:
        Random token string
    """
    return secrets.token_urlsafe(32)

# ============================================
# FORMATTING FUNCTIONS
# ============================================

def format_currency(amount):
    """
    Format number as currency
    
    Args:
        amount: Number to format
    
    Returns:
        Formatted currency string
    """
    try:
        return f"${float(amount):,.2f}"
    except:
        return "$0.00"

def format_percentage(value, decimals=1):
    """
    Format number as percentage
    
    Args:
        value: Number to format
        decimals: Number of decimal places
    
    Returns:
        Formatted percentage string
    """
    try:
        return f"{float(value):.{decimals}f}%"
    except:
        return "0%"

def format_number(num):
    """
    Format number with commas
    
    Args:
        num: Number to format
    
    Returns:
        Formatted number string
    """
    try:
        return f"{int(num):,}"
    except:
        return "0"

def format_date(date, format_str='%Y-%m-%d %H:%M'):
    """
    Format datetime object
    
    Args:
        date: Datetime object or string
        format_str: Desired output format
    
    Returns:
        Formatted date string
    """
    if date is None:
        return "N/A"
    
    if isinstance(date, str):
        try:
            date = pd.to_datetime(date)
        except:
            return date
    
    if isinstance(date, (datetime, pd.Timestamp)):
        return date.strftime(format_str)
    
    return str(date)

# ============================================
# DATA AGGREGATION FUNCTIONS
# ============================================

def aggregate_by_category(df, category_col, value_col, agg_func='mean'):
    """
    Aggregate data by category
    
    Args:
        df: DataFrame
        category_col: Column to group by
        value_col: Column to aggregate
        agg_func: Aggregation function
    
    Returns:
        Aggregated DataFrame
    """
    if agg_func == 'mean':
        return df.groupby(category_col)[value_col].mean().sort_values(ascending=False)
    elif agg_func == 'sum':
        return df.groupby(category_col)[value_col].sum().sort_values(ascending=False)
    elif agg_func == 'count':
        return df.groupby(category_col)[value_col].count().sort_values(ascending=False)
    else:
        return df.groupby(category_col)[value_col].agg(agg_func)

def create_age_groups(df, age_col='Age', bins=None):
    """
    Create age groups from age column
    
    Args:
        df: DataFrame
        age_col: Name of age column
        bins: Custom bin edges
    
    Returns:
        DataFrame with age group column
    """
    if bins is None:
        bins = [0, 18, 25, 35, 45, 55, 65, 100]
        labels = ['<18', '18-24', '25-34', '35-44', '45-54', '55-64', '65+']
    else:
        labels = [f"{bins[i]}-{bins[i+1]-1}" for i in range(len(bins)-1)]
    
    df_copy = df.copy()
    df_copy['AgeGroup'] = pd.cut(df_copy[age_col], bins=bins, labels=labels, right=False)
    
    return df_copy

def create_budget_tiers(df, budget_col='MonthlyBudget_USD', tiers=None):
    """
    Create budget tiers from budget column
    
    Args:
        df: DataFrame
        budget_col: Name of budget column
        tiers: Custom tier boundaries
    
    Returns:
        DataFrame with budget tier column
    """
    if tiers is None:
        tiers = [0, 25, 50, 100, 200, 500, 10000]
        labels = ['Budget', 'Economy', 'Moderate', 'Mid-Range', 'Premium', 'Luxury']
    else:
        labels = [f"Tier {i+1}" for i in range(len(tiers)-1)]
    
    df_copy = df.copy()
    df_copy['BudgetTier'] = pd.cut(df_copy[budget_col], bins=tiers, labels=labels, right=False)
    
    return df_copy

# ============================================
# STATISTICAL FUNCTIONS
# ============================================

def calculate_confidence_interval(data, confidence=0.95):
    """
    Calculate confidence interval for data
    
    Args:
        data: List or array of values
        confidence: Confidence level (0.95 = 95%)
    
    Returns:
        Tuple (lower_bound, upper_bound, mean)
    """
    import scipy.stats as stats
    
    data = np.array(data)
    mean = np.mean(data)
    std_err = stats.sem(data)
    margin = std_err * stats.t.ppf((1 + confidence) / 2., len(data)-1)
    
    return mean - margin, mean + margin, mean

def calculate_outliers(data, method='iqr'):
    """
    Detect outliers in data
    
    Args:
        data: List or array of values
        method: Detection method ('iqr' or 'zscore')
    
    Returns:
        Boolean array indicating outliers
    """
    data = np.array(data)
    
    if method == 'iqr':
        Q1 = np.percentile(data, 25)
        Q3 = np.percentile(data, 75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        return (data < lower_bound) | (data > upper_bound)
    
    elif method == 'zscore':
        z_scores = np.abs((data - np.mean(data)) / np.std(data))
        return z_scores > 3
    
    else:
        raise ValueError("Method must be 'iqr' or 'zscore'")

# ============================================
# DECORATORS
# ============================================

def login_required(f):
    """
    Decorator to require login for routes
    
    Args:
        f: Function to decorate
    
    Returns:
        Decorated function
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_email' not in session:
            if request.is_json:
                return jsonify({'error': 'Login required'}), 401
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """
    Decorator to require admin privileges
    
    Args:
        f: Function to decorate
    
    Returns:
        Decorated function
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_email' not in session:
            if request.is_json:
                return jsonify({'error': 'Login required'}), 401
            return redirect(url_for('login'))
        
        # Check if user is admin (customize as needed)
        if session.get('user_email') != 'admin@skincareai.com':
            if request.is_json:
                return jsonify({'error': 'Admin privileges required'}), 403
            return redirect(url_for('dashboard'))
        
        return f(*args, **kwargs)
    return decorated_function

def handle_errors(f):
    """
    Decorator to handle exceptions in routes
    
    Args:
        f: Function to decorate
    
    Returns:
        Decorated function
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            print(f"Error in {f.__name__}: {str(e)}")
            if request.is_json:
                return jsonify({'error': str(e)}), 500
            return render_template('error.html', error=str(e)), 500
    return decorated_function

# ============================================
# FILE HANDLING FUNCTIONS
# ============================================

def allowed_file(filename, allowed_extensions=None):
    """
    Check if file has allowed extension
    
    Args:
        filename: Name of file
        allowed_extensions: Set of allowed extensions
    
    Returns:
        Boolean indicating if file is allowed
    """
    if allowed_extensions is None:
        allowed_extensions = {'csv', 'xlsx', 'xls'}
    
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def get_file_extension(filename):
    """
    Get file extension from filename
    
    Args:
        filename: Name of file
    
    Returns:
        File extension string
    """
    if '.' not in filename:
        return ''
    return filename.rsplit('.', 1)[1].lower()

def generate_unique_filename(original_filename):
    """
    Generate unique filename with timestamp
    
    Args:
        original_filename: Original file name
    
    Returns:
        Unique filename string
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    name, ext = original_filename.rsplit('.', 1) if '.' in original_filename else (original_filename, '')
    return f"{name}_{timestamp}.{ext}"

# ============================================
# EXPORT FUNCTIONS
# ============================================

__all__ = [
    # Validation
    'validate_email', 'validate_password', 'validate_age', 'validate_budget',
    
    # Processing
    'clean_text', 'standardize_skin_type', 'standardize_gender',
    
    # Security
    'hash_password', 'verify_password', 'generate_token',
    
    # Formatting
    'format_currency', 'format_percentage', 'format_number', 'format_date',
    
    # Aggregation
    'aggregate_by_category', 'create_age_groups', 'create_budget_tiers',
    
    # Statistics
    'calculate_confidence_interval', 'calculate_outliers',
    
    # Decorators
    'login_required', 'admin_required', 'handle_errors',
    
    # File handling
    'allowed_file', 'get_file_extension', 'generate_unique_filename'
]