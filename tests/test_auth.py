"""
Unit tests for authentication module
"""

import unittest
import sys
import os
import json
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.authentication import UserAuthentication

class TestAuthentication(unittest.TestCase):
    
    def setUp(self):
        """Set up test authentication with temporary file"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.auth = UserAuthentication(user_db_path=self.temp_db.name)
        self.test_email = "test@example.com"
        self.test_password = "Test123!"
    
    def tearDown(self):
        """Clean up temporary file"""
        os.unlink(self.temp_db.name)
    
    def test_user_registration(self):
        """Test user registration"""
        success, user_id = self.auth.register_user(self.test_email, self.test_password)
        
        self.assertTrue(success)
        self.assertIsNotNone(user_id)
        self.assertIn(self.test_email, self.auth.users)
    
    def test_duplicate_registration(self):
        """Test duplicate registration prevention"""
        self.auth.register_user(self.test_email, self.test_password)
        success, message = self.auth.register_user(self.test_email, "Different123!")
        
        self.assertFalse(success)
        self.assertEqual(message, "Email already registered")
    
    def test_login_success(self):
        """Test successful login"""
        self.auth.register_user(self.test_email, self.test_password)
        success, user_id = self.auth.login_user(self.test_email, self.test_password)
        
        self.assertTrue(success)
        self.assertIsNotNone(user_id)
    
    def test_login_wrong_password(self):
        """Test login with wrong password"""
        self.auth.register_user(self.test_email, self.test_password)
        success, message = self.auth.login_user(self.test_email, "WrongPassword")
        
        self.assertFalse(success)
        self.assertEqual(message, "Invalid password")
    
    def test_login_nonexistent_user(self):
        """Test login with non-existent user"""
        success, message = self.auth.login_user("nonexistent@example.com", "password")
        
        self.assertFalse(success)
        self.assertEqual(message, "Email not found")
    
    def test_password_hashing(self):
        """Test password hashing"""
        hash1 = self.auth.hash_password("password123")
        hash2 = self.auth.hash_password("password123")
        
        # Different salts should produce different hashes
        self.assertNotEqual(hash1, hash2)
        
        # But both should verify correctly
        self.assertTrue(self.auth.verify_password("password123", hash1))
        self.assertTrue(self.auth.verify_password("password123", hash2))
    
    def test_update_preferences(self):
        """Test updating user preferences"""
        self.auth.register_user(self.test_email, self.test_password)
        
        preferences = {
            'skin_type': 'Oily',
            'monthly_budget': 100,
            'skin_concerns': ['Acne']
        }
        
        success = self.auth.update_user_preferences(self.test_email, preferences)
        self.assertTrue(success)
        
        user_data = self.auth.get_user_data(self.test_email)
        self.assertEqual(user_data['preferences']['skin_type'], 'Oily')
        self.assertEqual(user_data['preferences']['monthly_budget'], 100)
    
    def test_add_to_history(self):
        """Test adding to user history"""
        self.auth.register_user(self.test_email, self.test_password)
        
        success = self.auth.add_to_history(self.test_email, 'login', {'ip': '127.0.0.1'})
        self.assertTrue(success)
        
        user_data = self.auth.get_user_data(self.test_email)
        self.assertEqual(len(user_data['history']), 1)
        self.assertEqual(user_data['history'][0]['action'], 'login')
    
    def test_get_user_stats(self):
        """Test getting user statistics"""
        self.auth.register_user(self.test_email, self.test_password)
        
        # Add some actions
        self.auth.add_to_history(self.test_email, 'action1', {})
        self.auth.add_to_history(self.test_email, 'action2', {})
        
        stats = self.auth.get_user_stats(self.test_email)
        
        self.assertEqual(stats['total_actions'], 2)
        self.assertIsNotNone(stats['member_since'])
        self.assertIsNotNone(stats['user_id'])
    
    def test_delete_user(self):
        """Test user deletion"""
        self.auth.register_user(self.test_email, self.test_password)
        self.assertIn(self.test_email, self.auth.users)
        
        success = self.auth.delete_user(self.test_email)
        self.assertTrue(success)
        self.assertNotIn(self.test_email, self.auth.users)

class TestPasswordStrength(unittest.TestCase):
    
    def test_weak_password(self):
        """Test weak password detection"""
        from utils.helpers import validate_password
        
        # Too short
        valid, msg = validate_password("12345")
        self.assertFalse(valid)
        
        # Just minimum length
        valid, msg = validate_password("123456")
        self.assertTrue(valid)
    
    def test_strong_password(self):
        """Test strong password validation"""
        from utils.helpers import validate_password
        
        valid, msg = validate_password("StrongP@ss123!")
        self.assertTrue(valid)

if __name__ == '__main__':
    unittest.main()