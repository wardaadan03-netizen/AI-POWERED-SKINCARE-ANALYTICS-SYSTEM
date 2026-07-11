"""
Modules package for Skincare Analytics Platform
"""
from .authentication import UserAuthentication
from .recommender import SkincareRecommender
from .preprocessing import SkincareDataPreprocessor
from .analytics import SkincareAnalytics, create_analytics_dashboard

__all__ = [
    'UserAuthentication', 
    'SkincareRecommender', 
    'SkincareDataPreprocessor',
    'SkincareAnalytics',
    'create_analytics_dashboard'
]