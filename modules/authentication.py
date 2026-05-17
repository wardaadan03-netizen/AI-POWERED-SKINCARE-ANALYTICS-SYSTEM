import hashlib
import secrets
import json
import os
from datetime import datetime, timedelta
from functools import wraps
from flask import session, request, jsonify

class UserAuthentication:
    def __init__(self, user_db_path='data/users.json'):
        self.user_db_path = user_db_path
        self.users = self.load_users()
        
    def load_users(self):
        """Load users from JSON file"""
        if os.path.exists(self.user_db_path):
            with open(self.user_db_path, 'r') as f:
                return json.load(f)
        return {}
    
    def save_users(self):
        """Save users to JSON file"""
        os.makedirs(os.path.dirname(self.user_db_path), exist_ok=True)
        with open(self.user_db_path, 'w') as f:
            json.dump(self.users, f, indent=2)
    
    def hash_password(self, password):
        """Hash password using SHA-256 with salt"""
        salt = secrets.token_hex(16)
        hash_obj = hashlib.sha256((password + salt).encode())
        return f"{salt}:{hash_obj.hexdigest()}"
    
    def verify_password(self, password, stored_hash):
        """Verify password against stored hash"""
        try:
            salt, hash_value = stored_hash.split(':')
            hash_obj = hashlib.sha256((password + salt).encode())
            return hash_obj.hexdigest() == hash_value
        except:
            return False
    
    def register_user(self, email, password, user_data=None):
        """Register a new user"""
        email = email.lower().strip()
        
        if email in self.users:
            return False, "Email already registered"
        
        if len(password) < 6:
            return False, "Password must be at least 6 characters"
        
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return False, "Invalid email format"
        
        user_id = f"USER_{secrets.token_hex(4).upper()}"
        
        self.users[email] = {
            'user_id': user_id,
            'email': email,
            'password_hash': self.hash_password(password),
            'created_at': datetime.now().isoformat(),
            'last_login': None,
            'user_data': user_data or {},
            'preferences': {},
            'history': []
        }
        
        self.save_users()
        return True, user_id
    
    def login_user(self, email, password):
        """Login existing user"""
        email = email.lower().strip()
        
        if email not in self.users:
            return False, "Email not found"
        
        if not self.verify_password(password, self.users[email]['password_hash']):
            return False, "Invalid password"
        
        # Update last login
        self.users[email]['last_login'] = datetime.now().isoformat()
        self.save_users()
        
        return True, self.users[email]['user_id']
    
    def get_user_data(self, email):
        """Get user data by email"""
        email = email.lower().strip()
        return self.users.get(email, None)
    
    def update_user_preferences(self, email, preferences):
        """Update user preferences"""
        email = email.lower().strip()
        if email in self.users:
            self.users[email]['preferences'].update(preferences)
            self.save_users()
            return True
        return False
    
    def add_to_history(self, email, action, data):
        """Add action to user history"""
        email = email.lower().strip()
        if email in self.users:
            self.users[email]['history'].append({
                'timestamp': datetime.now().isoformat(),
                'action': action,
                'data': data
            })
            # Keep only last 100 actions
            self.users[email]['history'] = self.users[email]['history'][-100:]
            self.save_users()
            return True
        return False
    
    def get_user_stats(self, email):
        """Get user statistics"""
        email = email.lower().strip()
        if email not in self.users:
            return {}
        
        user = self.users[email]
        return {
            'member_since': user['created_at'],
            'last_login': user['last_login'],
            'total_actions': len(user['history']),
            'preferences_set': len(user['preferences']) > 0,
            'user_id': user['user_id']
        }
    
    def delete_user(self, email):
        """Delete user account"""
        email = email.lower().strip()
        if email in self.users:
            del self.users[email]
            self.save_users()
            return True
        return False
    
    def get_all_users(self):
        """Get all users (admin function)"""
        return {email: {'user_id': data['user_id'], 
                       'created_at': data['created_at'],
                       'last_login': data['last_login']} 
                for email, data in self.users.items()}

# Import re for email validation
import re

# Decorator for login required routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_email' not in session:
            if request.is_json:
                return jsonify({'error': 'Login required'}), 401
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Import for redirect
from flask import redirect, url_for
from functools import wraps