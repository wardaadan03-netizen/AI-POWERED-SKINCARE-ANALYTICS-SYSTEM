"""
User Authentication Module
Handles user registration, login, and profile management
"""

import json
import os
import hashlib
import secrets
from datetime import datetime
import uuid

class UserAuthentication:
    """Handles user authentication with JSON storage"""

    def __init__(self, user_db_path='data/users.json'):
        self.user_db_path = user_db_path
        self.users = {}
        self.load_users()

    def load_users(self):
        """Load users from JSON file"""
        os.makedirs(os.path.dirname(self.user_db_path), exist_ok=True)

        if os.path.exists(self.user_db_path):
            try:
                with open(self.user_db_path, 'r') as f:
                    self.users = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                self.users = {}
        else:
            self.users = {}
            self.save_users()

    def save_users(self):
        """Save users to JSON file"""
        os.makedirs(os.path.dirname(self.user_db_path), exist_ok=True)
        with open(self.user_db_path, 'w') as f:
            json.dump(self.users, f, indent=2, default=str)

    def _reload(self):
        """Reload users from disk so all gunicorn workers stay in sync.
        Each worker process has its own in-memory copy of self.users, but
        they all share the same JSON file on disk. Without this reload,
        a user created on one worker is invisible to the others until
        that worker happens to restart."""
        if os.path.exists(self.user_db_path):
            try:
                with open(self.user_db_path, 'r') as f:
                    self.users = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass

    def hash_password(self, password):
        """Hash password with salt"""
        salt = secrets.token_hex(16)
        hash_obj = hashlib.sha256((password + salt).encode())
        return f"{salt}:{hash_obj.hexdigest()}"

    def verify_password(self, password, hashed_password):
        """Verify password against hash"""
        try:
            salt, hash_value = hashed_password.split(':')
            hash_obj = hashlib.sha256((password + salt).encode())
            return hash_obj.hexdigest() == hash_value
        except (ValueError, AttributeError):
            return False

    def register_user(self, email, password):
        """Register a new user"""
        email = email.lower().strip()
        self._reload()

        # Debug
        print(f"🔐 Registering user: {email}")

        if email in self.users:
            return False, "Email already registered"

        if len(password) < 6:
            return False, "Password must be at least 6 characters"

        user_id = str(uuid.uuid4())
        self.users[email] = {
            'user_id': user_id,
            'email': email,
            'password': self.hash_password(password),
            'created_at': datetime.now().isoformat(),
            'last_login': None,
            'preferences': {
                'skin_type': '',
                'skin_concerns': [],
                'age': None,
                'gender': '',
                'monthly_budget': 50
            },
            'history': []
        }

        self.save_users()
        print(f"✅ User saved: {email}")
        return True, user_id

    def login_user(self, email, password):
        """Login user"""
        email = email.lower().strip()
        self._reload()

        if email not in self.users:
            return False, "Email not found"

        if not self.verify_password(password, self.users[email]['password']):
            return False, "Invalid password"

        # Update last login
        self.users[email]['last_login'] = datetime.now().isoformat()
        self.add_to_history(email, 'login', {'ip': '127.0.0.1'})
        self.save_users()

        return True, self.users[email]['user_id']

    def get_user(self, email):
        """Check if a user exists by email (used by app.py registration check)"""
        email = email.lower().strip()
        self._reload()
        return self.users.get(email)

    def get_user_data(self, email):
        """Get user data by email"""
        email = email.lower().strip()
        self._reload()
        return self.users.get(email)

    def update_user_preferences(self, email, preferences):
        """Update user preferences"""
        email = email.lower().strip()
        self._reload()

        if email not in self.users:
            return False

        # Merge preferences
        self.users[email]['preferences'].update(preferences)
        self.add_to_history(email, 'preferences_updated', {'preferences': preferences})
        self.save_users()
        return True

    def add_to_history(self, email, action, metadata=None):
        """Add action to user history

        NOTE: deliberately does NOT call self._reload(). This method is only
        ever called from within another method of this class (login_user,
        update_user_preferences, delete_user, etc.) that has already reloaded
        fresh data from disk and made its own in-memory change to
        self.users (e.g. setting last_login or merging preferences).
        Reloading again here would overwrite that pending in-memory change
        with the stale on-disk version before save_users() ever runs -
        which was the root cause of last_login and preferences never
        persisting.
        """
        email = email.lower().strip()

        if email not in self.users:
            return False

        if metadata is None:
            metadata = {}

        self.users[email]['history'].append({
            'action': action,
            'timestamp': datetime.now().isoformat(),
            'metadata': metadata
        })

        self.save_users()
        return True

    def get_user_stats(self, email):
        """Get user statistics"""
        email = email.lower().strip()
        self._reload()

        if email not in self.users:
            return None

        user = self.users[email]
        return {
            'user_id': user['user_id'],
            'member_since': user['created_at'],
            'last_login': user['last_login'],
            'total_actions': len(user['history']),
            'preferences': user['preferences']
        }

    def delete_user(self, email):
        """Delete user account"""
        email = email.lower().strip()
        self._reload()

        if email not in self.users:
            return False

        del self.users[email]
        self.save_users()
        return True
