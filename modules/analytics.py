"""
Analytics Module for Skincare Platform
Handles data analytics, metrics calculation, and insights generation
"""

import pandas as pd
import numpy as np
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List, Union
from sklearn.metrics import mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logger = logging.getLogger(__name__)

# Optional imports with fallback
try:
    import plotly.graph_objs as go
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    logger.warning("Plotly not installed. Dashboard functions will be disabled.")

class SkincareAnalytics:
    """Skincare analytics engine for data insights and metrics"""
    
    # Required columns for each analysis
    REQUIRED_COLUMNS = {
        'user_metrics': ['UserID', 'Age', 'MonthlyBudget_USD', 'ProductEffectiveness_Score', 
                        'CustomerSatisfaction_pct', 'WillRepurchase', 'SkinType', 
                        'Gender', 'SkinConcerns'],
        'ingredient_impact': [],  # Dynamic based on 'Uses*' columns
        'trends': ['RegistrationDate']
    }
    
    # Budget thresholds
    BUDGET_THRESHOLDS = {
        'low': 50,
        'mid': 150,
        'high': 300
    }
    
    # Ingredient mapping for concerns
    INGREDIENT_MAP = {
        'Acne': ['Salicylic Acid', 'Niacinamide', 'Benzoyl Peroxide'],
        'Wrinkles': ['Retinol', 'Peptides', 'Vitamin C'],
        'Pigmentation': ['Vitamin C', 'Kojic Acid', 'Alpha Arbutin'],
        'Dryness': ['Hyaluronic Acid', 'Ceramides', 'Squalane'],
        'Redness': ['Niacinamide', 'Centella Asiatica', 'Aloe Vera']
    }
    
    def __init__(self, df: Optional[pd.DataFrame] = None, 
                 config: Optional[Dict[str, Any]] = None):
        """
        Initialize analytics engine
        
        Args:
            df: DataFrame containing skincare data
            config: Configuration dictionary for thresholds, caching, etc.
        """
        self.df = df
        self.config = config or {}
        self.insights_cache = {}
        self.cache_ttl = self.config.get('cache_ttl', 3600)  # 1 hour default
        self.max_data_size = self.config.get('max_data_size', 1000000)  # 1M rows
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        
        # Validate data on initialization
        if self.df is not None:
            self._validate_data()
    
    def _validate_data(self) -> bool:
        """Validate dataframe has required structure"""
        if self.df is None or self.df.empty:
            self.logger.warning("DataFrame is empty or None")
            return False
        
        # Check for required columns (at minimum)
        required_min = ['UserID', 'CustomerSatisfaction_pct']
        missing = [col for col in required_min if col not in self.df.columns]
        
        if missing:
            self.logger.error(f"Missing required columns: {missing}")
            return False
        
        # Check data size
        if len(self.df) > self.max_data_size:
            self.logger.warning(f"Data size ({len(self.df)}) exceeds max ({self.max_data_size})")
        
        return True
    
    def set_data(self, df: pd.DataFrame) -> None:
        """Set or update dataframe with validation"""
        self.df = df
        self.insights_cache = {}
        self._validate_data()
        self.logger.info(f"Data updated with {len(df)} rows")
    
    def _check_columns(self, columns: List[str]) -> bool:
        """Check if required columns exist"""
        if self.df is None:
            return False
        missing = [col for col in columns if col not in self.df.columns]
        if missing:
            self.logger.warning(f"Missing columns: {missing}")
            return False
        return True
    
    def _get_cached_or_compute(self, key: str, compute_func, *args, **kwargs):
        """Get from cache or compute and cache"""
        if key in self.insights_cache:
            return self.insights_cache[key]
        
        result = compute_func(*args, **kwargs)
        self.insights_cache[key] = result
        return result
    
    def calculate_user_metrics(self, user_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Calculate personalized user metrics
        
        Args:
            user_id: Specific user ID (optional)
        
        Returns:
            Dictionary of user metrics
        """
        if self.df is None or self.df.empty:
            return {}
        
        # Check required columns
        required_cols = ['UserID', 'Age', 'MonthlyBudget_USD', 'ProductEffectiveness_Score', 
                        'CustomerSatisfaction_pct', 'WillRepurchase', 'SkinType', 
                        'Gender', 'SkinConcerns']
        
        if not self._check_columns(required_cols):
            return {}
        
        try:
            if user_id:
                user_data = self.df[self.df['UserID'] == user_id]
                if user_data.empty:
                    self.logger.warning(f"User {user_id} not found")
                    return {}
            else:
                user_data = self.df
            
            metrics = {
                'total_users': int(len(self.df['UserID'].unique())),
                'avg_age': float(user_data['Age'].mean()) if not user_data.empty else 0,
                'avg_budget': float(user_data['MonthlyBudget_USD'].mean()) if not user_data.empty else 0,
                'avg_effectiveness': float(user_data['ProductEffectiveness_Score'].mean()) if not user_data.empty else 0,
                'avg_satisfaction': float(user_data['CustomerSatisfaction_pct'].mean()) if not user_data.empty else 0,
                'repurchase_rate': float(user_data['WillRepurchase'].mean() * 100) if not user_data.empty else 0,
                'skin_type_distribution': user_data['SkinType'].value_counts().to_dict() if not user_data.empty else {},
                'gender_distribution': user_data['Gender'].value_counts().to_dict() if not user_data.empty else {},
                'top_concerns': user_data['SkinConcerns'].value_counts().head(5).to_dict() if not user_data.empty else {}
            }
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Error calculating user metrics: {e}")
            return {}
    
    def calculate_ingredient_impact(self, use_cache: bool = True) -> pd.DataFrame:
        """
        Calculate impact of each active ingredient on satisfaction
        
        Args:
            use_cache: Whether to use cached results
        
        Returns:
            DataFrame with ingredient impact scores
        """
        if use_cache and 'ingredient_impact' in self.insights_cache:
            return self.insights_cache['ingredient_impact']
        
        if self.df is None or self.df.empty:
            return pd.DataFrame()
        
        try:
            ingredient_cols = [col for col in self.df.columns if col.startswith('Uses')]
            if not ingredient_cols:
                self.logger.warning("No ingredient columns found")
                return pd.DataFrame()
            
            ingredient_names = [col.replace('Uses', '') for col in ingredient_cols]
            
            impact_scores = []
            for col, name in zip(ingredient_cols, ingredient_names):
                with_ing = self.df[self.df[col] == 1]['CustomerSatisfaction_pct'].mean()
                without_ing = self.df[self.df[col] == 0]['CustomerSatisfaction_pct'].mean()
                impact = with_ing - without_ing
                
                impact_scores.append({
                    'ingredient': name,
                    'usage_rate': float(self.df[col].mean() * 100),
                    'satisfaction_with': float(with_ing) if not pd.isna(with_ing) else 0,
                    'satisfaction_without': float(without_ing) if not pd.isna(without_ing) else 0,
                    'impact_score': float(impact) if not pd.isna(impact) else 0,
                    'effectiveness_boost': float(with_ing - self.df['CustomerSatisfaction_pct'].mean()) if not pd.isna(with_ing) else 0
                })
            
            result_df = pd.DataFrame(impact_scores).sort_values('impact_score', ascending=False)
            self.insights_cache['ingredient_impact'] = result_df
            return result_df
            
        except Exception as e:
            self.logger.error(f"Error calculating ingredient impact: {e}")
            return pd.DataFrame()
    
    def calculate_budget_analysis(self) -> Dict[str, Any]:
        """Analyze budget segments and their impact"""
        if self.df is None or self.df.empty:
            return {}
        
        required_cols = ['MonthlyBudget_USD', 'CustomerSatisfaction_pct', 
                        'ProductEffectiveness_Score', 'WillRepurchase']
        if not self._check_columns(required_cols):
            return {}
        
        try:
            # Create budget segments
            budget_segments = pd.cut(self.df['MonthlyBudget_USD'], 
                                     bins=[0, 30, 75, 150, 300, 10000],
                                     labels=['Budget (<$30)', 'Economy ($30-75)', 
                                            'Mid-Range ($75-150)', 'Premium ($150-300)', 
                                            'Luxury ($300+)'])
            
            analysis = {
                'segment_distribution': self.df.groupby(budget_segments, observed=True).size().to_dict(),
                'segment_satisfaction': self.df.groupby(budget_segments, observed=True)['CustomerSatisfaction_pct'].mean().to_dict(),
                'segment_effectiveness': self.df.groupby(budget_segments, observed=True)['ProductEffectiveness_Score'].mean().to_dict(),
                'segment_repurchase': self.df.groupby(budget_segments, observed=True)['WillRepurchase'].mean().to_dict(),
                'correlation_budget_satisfaction': float(self.df['MonthlyBudget_USD'].corr(self.df['CustomerSatisfaction_pct']) or 0)
            }
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error calculating budget analysis: {e}")
            return {}
    
    def calculate_skin_type_insights(self) -> pd.DataFrame:
        """Generate insights by skin type"""
        if self.df is None or self.df.empty:
            return pd.DataFrame()
        
        required_cols = ['SkinType', 'Age', 'MonthlyBudget_USD', 
                        'CustomerSatisfaction_pct', 'ProductEffectiveness_Score', 
                        'WillRepurchase', 'SkinConcerns']
        
        if not self._check_columns(required_cols):
            return pd.DataFrame()
        
        try:
            insights = []
            for skin_type in self.df['SkinType'].unique():
                subset = self.df[self.df['SkinType'] == skin_type]
                
                insights.append({
                    'skin_type': skin_type,
                    'count': int(len(subset)),
                    'avg_age': float(subset['Age'].mean()) if not subset.empty else 0,
                    'avg_budget': float(subset['MonthlyBudget_USD'].mean()) if not subset.empty else 0,
                    'avg_satisfaction': float(subset['CustomerSatisfaction_pct'].mean()) if not subset.empty else 0,
                    'avg_effectiveness': float(subset['ProductEffectiveness_Score'].mean()) if not subset.empty else 0,
                    'repurchase_rate': float(subset['WillRepurchase'].mean() * 100) if not subset.empty else 0,
                    'top_concern': subset['SkinConcerns'].mode()[0] if not subset.empty else 'N/A',
                    'avg_ingredients': float(subset[[col for col in subset.columns if col.startswith('Uses')]].sum(axis=1).mean()) if not subset.empty else 0
                })
            
            return pd.DataFrame(insights)
            
        except Exception as e:
            self.logger.error(f"Error calculating skin type insights: {e}")
            return pd.DataFrame()
    
    def calculate_trends(self, days: int = 30) -> Dict[str, Any]:
        """Calculate trends over time"""
        if self.df is None or self.df.empty:
            return {}
        
        if 'RegistrationDate' not in self.df.columns:
            self.logger.warning("RegistrationDate column not found")
            return {}
        
        try:
            # Convert to datetime safely
            self.df['RegistrationDate'] = pd.to_datetime(self.df['RegistrationDate'], errors='coerce')
            self.df = self.df.dropna(subset=['RegistrationDate'])
            
            if self.df.empty:
                return {}
            
            cutoff_date = datetime.now() - timedelta(days=days)
            
            recent_users = self.df[self.df['RegistrationDate'] >= cutoff_date]
            old_users = self.df[self.df['RegistrationDate'] < cutoff_date]
            
            trends = {
                'user_growth_rate': float((len(recent_users) / len(old_users)) * 100) if len(old_users) > 0 else 0,
                'recent_avg_age': float(recent_users['Age'].mean()) if not recent_users.empty else 0,
                'recent_avg_budget': float(recent_users['MonthlyBudget_USD'].mean()) if not recent_users.empty else 0,
                'recent_satisfaction': float(recent_users['CustomerSatisfaction_pct'].mean()) if not recent_users.empty else 0,
                'satisfaction_trend': float(recent_users['CustomerSatisfaction_pct'].mean() - old_users['CustomerSatisfaction_pct'].mean()) if not old_users.empty else 0,
                'budget_trend': float(recent_users['MonthlyBudget_USD'].mean() - old_users['MonthlyBudget_USD'].mean()) if not old_users.empty else 0,
                'popular_ingredients': self.get_trending_ingredients(recent_users) if not recent_users.empty else []
            }
            
            return trends
            
        except Exception as e:
            self.logger.error(f"Error calculating trends: {e}")
            return {}
    
    def get_trending_ingredients(self, recent_df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Identify trending ingredients"""
        try:
            if recent_df.empty or self.df is None:
                return []
            
            ingredient_cols = [col for col in self.df.columns if col.startswith('Uses')]
            if not ingredient_cols:
                return []
            
            ingredient_names = [col.replace('Uses', '') for col in ingredient_cols]
            
            recent_usage = recent_df[ingredient_cols].mean()
            overall_usage = self.df[ingredient_cols].mean()
            
            trending = []
            for col, name in zip(ingredient_cols, ingredient_names):
                if overall_usage[col] > 0:
                    growth = ((recent_usage[col] - overall_usage[col]) / overall_usage[col]) * 100
                else:
                    growth = 0
                    
                trending.append({
                    'ingredient': name,
                    'growth_percentage': float(growth),
                    'current_usage': float(recent_usage[col] * 100)
                })
            
            return sorted(trending, key=lambda x: x['growth_percentage'], reverse=True)[:5]
            
        except Exception as e:
            self.logger.error(f"Error getting trending ingredients: {e}")
            return []
    
    def generate_recommendation_insights(self, user_preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Generate personalized insights based on user preferences"""
        insights = {
            'skin_type_match': {},
            'budget_recommendation': '',
            'ingredient_recommendations': [],
            'product_categories': []
        }
        
        try:
            # Skin type analysis
            skin_type = user_preferences.get('skin_type', 'Normal')
            skin_analysis = self.calculate_skin_type_insights()
            
            if not skin_analysis.empty:
                skin_data = skin_analysis[skin_analysis['skin_type'] == skin_type]
                if not skin_data.empty:
                    insights['skin_type_match'] = {
                        'avg_satisfaction': float(skin_data['avg_satisfaction'].values[0]),
                        'common_concern': skin_data['top_concern'].values[0],
                        'avg_ingredients': float(skin_data['avg_ingredients'].values[0])
                    }
            
            # Budget recommendation
            budget = user_preferences.get('monthly_budget', 50)
            if budget < self.BUDGET_THRESHOLDS['low']:
                insights['budget_recommendation'] = 'Focus on affordable drugstore brands with high effectiveness ratings'
            elif budget < self.BUDGET_THRESHOLDS['mid']:
                insights['budget_recommendation'] = 'Mix of drugstore staples and mid-range specialty products'
            elif budget < self.BUDGET_THRESHOLDS['high']:
                insights['budget_recommendation'] = 'Consider premium brands with clinical-grade ingredients'
            else:
                insights['budget_recommendation'] = 'Explore luxury brands with innovative formulations'
            
            # Ingredient recommendations based on concerns
            concerns = user_preferences.get('skin_concerns', [])
            recommended_ingredients = set()
            for concern in concerns:
                if concern in self.INGREDIENT_MAP:
                    recommended_ingredients.update(self.INGREDIENT_MAP[concern])
            
            insights['ingredient_recommendations'] = list(recommended_ingredients)[:5]
            
            # Product categories
            if skin_type in ['Oily', 'Combination']:
                insights['product_categories'] = ['Oil-free cleansers', 'Lightweight moisturizers', 'Niacinamide serums']
            elif skin_type == 'Dry':
                insights['product_categories'] = ['Hydrating cleansers', 'Rich moisturizers', 'Hyaluronic acid serums']
            elif skin_type == 'Sensitive':
                insights['product_categories'] = ['Gentle cleansers', 'Fragrance-free products', 'Soothing ingredients']
            else:
                insights['product_categories'] = ['Balanced routine', 'Antioxidant serums', 'Sunscreen']
            
        except Exception as e:
            self.logger.error(f"Error generating recommendation insights: {e}")
        
        return insights
    
    def get_performance_metrics(self, predictions: np.ndarray, actuals: np.ndarray) -> Dict[str, float]:
        """Calculate model performance metrics"""
        try:
            if len(predictions) == 0 or len(actuals) == 0:
                return {}
            
            predictions = np.array(predictions)
            actuals = np.array(actuals)
            
            rmse = float(np.sqrt(mean_squared_error(actuals, predictions)))
            r2 = float(r2_score(actuals, predictions))
            mae = float(np.mean(np.abs(predictions - actuals)))
            
            # Handle MAPE safely
            mask = actuals != 0
            if np.any(mask):
                mape = float(np.mean(np.abs((actuals[mask] - predictions[mask]) / actuals[mask])) * 100)
            else:
                mape = 0
            
            return {
                'RMSE': rmse,
                'R2_Score': r2,
                'MAE': mae,
                'MAPE': mape,
                'accuracy_percentage': float(max(0, (1 - mape/100) * 100))
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating performance metrics: {e}")
            return {}
    
    def generate_summary_report(self) -> Dict[str, Any]:
        """Generate complete summary report"""
        if self.df is None or self.df.empty:
            return {'error': 'No data available'}
        
        try:
            report = {
                'overview': self.calculate_user_metrics(),
                'ingredient_impact': self.calculate_ingredient_impact().to_dict('records'),
                'budget_analysis': self.calculate_budget_analysis(),
                'skin_type_insights': self.calculate_skin_type_insights().to_dict('records'),
                'trends': self.calculate_trends(),
                'key_insights': self.extract_key_insights(),
                'generated_at': datetime.now().isoformat()
            }
            
            return report
            
        except Exception as e:
            self.logger.error(f"Error generating summary report: {e}")
            return {'error': str(e)}
    
    def extract_key_insights(self) -> List[str]:
        """Extract key business insights"""
        insights = []
        
        try:
            if self.df is None or self.df.empty:
                return ["No data available for insights"]
            
            # Overall metrics
            avg_satisfaction = self.df['CustomerSatisfaction_pct'].mean()
            insights.append(f"Average customer satisfaction is {avg_satisfaction:.1f}%")
            
            # Best performing skin type
            skin_analysis = self.calculate_skin_type_insights()
            if not skin_analysis.empty:
                best_skin = skin_analysis.loc[skin_analysis['avg_satisfaction'].idxmax()]
                insights.append(f"{best_skin['skin_type']} skin users have the highest satisfaction at {best_skin['avg_satisfaction']:.1f}%")
            
            # Ingredient impact
            ingredient_impact = self.calculate_ingredient_impact()
            if not ingredient_impact.empty:
                top_ingredient = ingredient_impact.iloc[0]
                insights.append(f"{top_ingredient['ingredient']} provides the biggest satisfaction boost (+{top_ingredient['impact_score']:.1f}%)")
            
            # Budget insight
            if 'MonthlyBudget_USD' in self.df.columns and 'CustomerSatisfaction_pct' in self.df.columns:
                budget_corr = self.df['MonthlyBudget_USD'].corr(self.df['CustomerSatisfaction_pct'])
                if budget_corr > 0.3:
                    insights.append(f"Higher budget correlates with higher satisfaction (correlation: {budget_corr:.2f})")
                else:
                    insights.append("Budget doesn't strongly correlate with satisfaction - effectiveness matters more!")
            
            # Repurchase insight
            if 'WillRepurchase' in self.df.columns:
                repurchase_rate = self.df['WillRepurchase'].mean() * 100
                insights.append(f"Overall repurchase rate is {repurchase_rate:.1f}%")
            
            # Top concern
            if 'SkinConcerns' in self.df.columns:
                top_concern = self.df['SkinConcerns'].mode()[0]
                insights.append(f"{top_concern} is the most common skin concern")
            
        except Exception as e:
            self.logger.error(f"Error extracting key insights: {e}")
            insights.append("Error generating insights")
        
        return insights


def create_analytics_dashboard(df: pd.DataFrame) -> Any:
    """
    Create comprehensive analytics dashboard
    
    Args:
        df: DataFrame with skincare data
    
    Returns:
        Plotly figure object or None if Plotly not available
    """
    if not PLOTLY_AVAILABLE:
        logger.warning("Plotly not available. Install with: pip install plotly")
        return None
    
    if df is None or df.empty:
        logger.warning("No data for dashboard")
        return None
    
    try:
        analytics = SkincareAnalytics(df)
        
        # Get metrics
        ingredient_impact = analytics.calculate_ingredient_impact()
        
        # Create subplot dashboard
        fig = make_subplots(
            rows=2, cols=3,
            subplot_titles=('Satisfaction Distribution', 'Budget Analysis', 
                           'Ingredient Impact', 'Skin Type Satisfaction',
                           'Repurchase by Skin Type', 'Top Concerns'),
            specs=[[{'type': 'histogram'}, {'type': 'box'}, {'type': 'bar'}],
                   [{'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}]]
        )
        
        # 1. Satisfaction distribution
        fig.add_trace(go.Histogram(x=df['CustomerSatisfaction_pct'], 
                                   nbinsx=20, name='Satisfaction',
                                   marker_color='steelblue'), row=1, col=1)
        
        # 2. Budget distribution
        fig.add_trace(go.Box(y=df['MonthlyBudget_USD'], name='Budget',
                            marker_color='coral'), row=1, col=2)
        
        # 3. Ingredient impact
        if not ingredient_impact.empty:
            fig.add_trace(go.Bar(x=ingredient_impact.head(8)['ingredient'],
                                y=ingredient_impact.head(8)['impact_score'],
                                name='Impact', marker_color='lightgreen'), row=1, col=3)
        
        # 4. Skin type satisfaction
        skin_sat = df.groupby('SkinType')['CustomerSatisfaction_pct'].mean().sort_values()
        fig.add_trace(go.Bar(x=skin_sat.values, y=skin_sat.index, orientation='h',
                            name='Satisfaction', marker_color='lightcoral'), row=2, col=1)
        
        # 5. Repurchase by skin type
        repurchase_by_skin = df.groupby('SkinType')['WillRepurchase'].mean() * 100
        fig.add_trace(go.Bar(x=repurchase_by_skin.index, y=repurchase_by_skin.values,
                            name='Repurchase Rate', marker_color='lightblue'), row=2, col=2)
        
        # 6. Top concerns
        top_concerns = df['SkinConcerns'].value_counts().head(5)
        fig.add_trace(go.Bar(x=top_concerns.values, y=top_concerns.index, orientation='h',
                            name='Concerns', marker_color='gold'), row=2, col=3)
        
        fig.update_layout(title='Skincare Analytics Dashboard',
                          height=800,
                          showlegend=False,
                          title_x=0.5)
        
        return fig
        
    except Exception as e:
        logger.error(f"Error creating dashboard: {e}")
        return None