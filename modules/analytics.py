"""
Analytics Module for Skincare Platform
Handles data analytics, metrics calculation, and insights generation
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.metrics import mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

class SkincareAnalytics:
    def __init__(self, df=None):
        """
        Initialize analytics engine
        
        Args:
            df: DataFrame containing skincare data
        """
        self.df = df
        self.insights_cache = {}
        
    def set_data(self, df):
        """Set or update dataframe"""
        self.df = df
        self.insights_cache = {}
        
    def calculate_user_metrics(self, user_id=None):
        """
        Calculate personalized user metrics
        
        Args:
            user_id: Specific user ID (optional)
        
        Returns:
            Dictionary of user metrics
        """
        if self.df is None:
            return {}
        
        if user_id:
            user_data = self.df[self.df['UserID'] == user_id]
        else:
            user_data = self.df
            
        metrics = {
            'total_users': len(self.df['UserID'].unique()),
            'avg_age': user_data['Age'].mean(),
            'avg_budget': user_data['MonthlyBudget_USD'].mean(),
            'avg_effectiveness': user_data['ProductEffectiveness_Score'].mean(),
            'avg_satisfaction': user_data['CustomerSatisfaction_pct'].mean(),
            'repurchase_rate': user_data['WillRepurchase'].mean() * 100,
            'skin_type_distribution': user_data['SkinType'].value_counts().to_dict(),
            'gender_distribution': user_data['Gender'].value_counts().to_dict(),
            'top_concerns': user_data['SkinConcerns'].value_counts().head(5).to_dict()
        }
        
        return metrics
    
    def calculate_ingredient_impact(self):
        """
        Calculate impact of each active ingredient on satisfaction
        
        Returns:
            DataFrame with ingredient impact scores
        """
        if self.df is None:
            return pd.DataFrame()
        
        ingredient_cols = [col for col in self.df.columns if col.startswith('Uses')]
        ingredient_names = [col.replace('Uses', '') for col in ingredient_cols]
        
        impact_scores = []
        for col, name in zip(ingredient_cols, ingredient_names):
            with_ing = self.df[self.df[col] == 1]['CustomerSatisfaction_pct'].mean()
            without_ing = self.df[self.df[col] == 0]['CustomerSatisfaction_pct'].mean()
            impact = with_ing - without_ing
            
            impact_scores.append({
                'ingredient': name,
                'usage_rate': self.df[col].mean() * 100,
                'satisfaction_with': with_ing,
                'satisfaction_without': without_ing,
                'impact_score': impact,
                'effectiveness_boost': with_ing - self.df['CustomerSatisfaction_pct'].mean()
            })
        
        return pd.DataFrame(impact_scores).sort_values('impact_score', ascending=False)
    
    def calculate_budget_analysis(self):
        """
        Analyze budget segments and their impact
        
        Returns:
            Dictionary with budget analysis results
        """
        if self.df is None:
            return {}
        
        # Create budget segments
        budget_segments = pd.cut(self.df['MonthlyBudget_USD'], 
                                 bins=[0, 30, 75, 150, 300, 10000],
                                 labels=['Budget (<$30)', 'Economy ($30-75)', 
                                        'Mid-Range ($75-150)', 'Premium ($150-300)', 
                                        'Luxury ($300+)'])
        
        analysis = {
            'segment_distribution': self.df.groupby(budget_segments).size().to_dict(),
            'segment_satisfaction': self.df.groupby(budget_segments)['CustomerSatisfaction_pct'].mean().to_dict(),
            'segment_effectiveness': self.df.groupby(budget_segments)['ProductEffectiveness_Score'].mean().to_dict(),
            'segment_repurchase': self.df.groupby(budget_segments)['WillRepurchase'].mean().to_dict(),
            'correlation_budget_satisfaction': self.df['MonthlyBudget_USD'].corr(self.df['CustomerSatisfaction_pct'])
        }
        
        return analysis
    
    def calculate_skin_type_insights(self):
        """
        Generate insights by skin type
        
        Returns:
            DataFrame with skin type analysis
        """
        if self.df is None:
            return pd.DataFrame()
        
        insights = []
        for skin_type in self.df['SkinType'].unique():
            subset = self.df[self.df['SkinType'] == skin_type]
            
            insights.append({
                'skin_type': skin_type,
                'count': len(subset),
                'avg_age': subset['Age'].mean(),
                'avg_budget': subset['MonthlyBudget_USD'].mean(),
                'avg_satisfaction': subset['CustomerSatisfaction_pct'].mean(),
                'avg_effectiveness': subset['ProductEffectiveness_Score'].mean(),
                'repurchase_rate': subset['WillRepurchase'].mean() * 100,
                'top_concern': subset['SkinConcerns'].mode()[0] if not subset.empty else 'N/A',
                'avg_ingredients': subset[[col for col in subset.columns if col.startswith('Uses')]].sum(axis=1).mean()
            })
        
        return pd.DataFrame(insights)
    
    def calculate_trends(self, days=30):
        """
        Calculate trends over time
        
        Args:
            days: Number of days to look back
        
        Returns:
            Dictionary with trend analysis
        """
        if self.df is None or 'RegistrationDate' not in self.df.columns:
            return {}
        
        # Convert to datetime
        self.df['RegistrationDate'] = pd.to_datetime(self.df['RegistrationDate'])
        cutoff_date = datetime.now() - timedelta(days=days)
        
        recent_users = self.df[self.df['RegistrationDate'] >= cutoff_date]
        old_users = self.df[self.df['RegistrationDate'] < cutoff_date]
        
        trends = {
            'user_growth_rate': (len(recent_users) / len(old_users)) * 100 if len(old_users) > 0 else 0,
            'recent_avg_age': recent_users['Age'].mean(),
            'recent_avg_budget': recent_users['MonthlyBudget_USD'].mean(),
            'recent_satisfaction': recent_users['CustomerSatisfaction_pct'].mean(),
            'satisfaction_trend': recent_users['CustomerSatisfaction_pct'].mean() - old_users['CustomerSatisfaction_pct'].mean(),
            'budget_trend': recent_users['MonthlyBudget_USD'].mean() - old_users['MonthlyBudget_USD'].mean(),
            'popular_ingredients': self.get_trending_ingredients(recent_users)
        }
        
        return trends
    
    def get_trending_ingredients(self, recent_df):
        """
        Identify trending ingredients
        
        Args:
            recent_df: DataFrame with recent users
        
        Returns:
            List of trending ingredients
        """
        ingredient_cols = [col for col in self.df.columns if col.startswith('Uses')]
        ingredient_names = [col.replace('Uses', '') for col in ingredient_cols]
        
        recent_usage = recent_df[ingredient_cols].mean()
        overall_usage = self.df[ingredient_cols].mean()
        
        trending = []
        for col, name in zip(ingredient_cols, ingredient_names):
            growth = ((recent_usage[col] - overall_usage[col]) / overall_usage[col]) * 100
            trending.append({
                'ingredient': name,
                'growth_percentage': growth,
                'current_usage': recent_usage[col] * 100
            })
        
        return sorted(trending, key=lambda x: x['growth_percentage'], reverse=True)[:5]
    
    def generate_recommendation_insights(self, user_preferences):
        """
        Generate personalized insights based on user preferences
        
        Args:
            user_preferences: Dictionary with user preferences
        
        Returns:
            Dictionary with personalized insights
        """
        insights = {
            'skin_type_match': [],
            'budget_recommendation': '',
            'ingredient_recommendations': [],
            'product_categories': []
        }
        
        # Skin type analysis
        skin_type = user_preferences.get('skin_type', 'Normal')
        skin_analysis = self.calculate_skin_type_insights()
        
        if not skin_analysis.empty:
            skin_data = skin_analysis[skin_analysis['skin_type'] == skin_type]
            if not skin_data.empty:
                insights['skin_type_match'] = {
                    'avg_satisfaction': skin_data['avg_satisfaction'].values[0],
                    'common_concern': skin_data['top_concern'].values[0],
                    'avg_ingredients': skin_data['avg_ingredients'].values[0]
                }
        
        # Budget recommendation
        budget = user_preferences.get('monthly_budget', 50)
        if budget < 50:
            insights['budget_recommendation'] = 'Focus on affordable drugstore brands with high effectiveness ratings'
        elif budget < 150:
            insights['budget_recommendation'] = 'Mix of drugstore staples and mid-range specialty products'
        else:
            insights['budget_recommendation'] = 'Consider premium brands with clinical-grade ingredients'
        
        # Ingredient recommendations based on concerns
        concerns = user_preferences.get('skin_concerns', [])
        ingredient_map = {
            'Acne': ['Salicylic Acid', 'Niacinamide', 'Benzoyl Peroxide'],
            'Wrinkles': ['Retinol', 'Peptides', 'Vitamin C'],
            'Pigmentation': ['Vitamin C', 'Kojic Acid', 'Alpha Arbutin'],
            'Dryness': ['Hyaluronic Acid', 'Ceramides', 'Squalane'],
            'Redness': ['Niacinamide', 'Centella Asiatica', 'Aloe Vera']
        }
        
        recommended_ingredients = set()
        for concern in concerns:
            if concern in ingredient_map:
                recommended_ingredients.update(ingredient_map[concern])
        
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
        
        return insights
    
    def get_performance_metrics(self, predictions, actuals):
        """
        Calculate model performance metrics
        
        Args:
            predictions: Array of predicted values
            actuals: Array of actual values
        
        Returns:
            Dictionary with performance metrics
        """
        rmse = np.sqrt(mean_squared_error(actuals, predictions))
        r2 = r2_score(actuals, predictions)
        mae = np.mean(np.abs(predictions - actuals))
        mape = np.mean(np.abs((actuals - predictions) / actuals)) * 100
        
        return {
            'RMSE': rmse,
            'R2_Score': r2,
            'MAE': mae,
            'MAPE': mape,
            'accuracy_percentage': (1 - mape/100) * 100
        }
    
    def generate_summary_report(self):
        """
        Generate complete summary report
        
        Returns:
            Dictionary with comprehensive analytics
        """
        if self.df is None:
            return {}
        
        report = {
            'overview': self.calculate_user_metrics(),
            'ingredient_impact': self.calculate_ingredient_impact().to_dict('records'),
            'budget_analysis': self.calculate_budget_analysis(),
            'skin_type_insights': self.calculate_skin_type_insights().to_dict('records'),
            'trends': self.calculate_trends(),
            'key_insights': self.extract_key_insights()
        }
        
        return report
    
    def extract_key_insights(self):
        """
        Extract key business insights
        
        Returns:
            List of key insights
        """
        insights = []
        
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
        budget_corr = self.df['MonthlyBudget_USD'].corr(self.df['CustomerSatisfaction_pct'])
        if budget_corr > 0.3:
            insights.append(f"Higher budget correlates with higher satisfaction (correlation: {budget_corr:.2f})")
        else:
            insights.append("Budget doesn't strongly correlate with satisfaction - effectiveness matters more!")
        
        # Repurchase insight
        repurchase_rate = self.df['WillRepurchase'].mean() * 100
        insights.append(f"Overall repurchase rate is {repurchase_rate:.1f}%")
        
        # Top concern
        top_concern = self.df['SkinConcerns'].mode()[0]
        insights.append(f"{top_concern} is the most common skin concern")
        
        return insights


# Analytics Visualization Functions
def create_analytics_dashboard(df):
    """
    Create comprehensive analytics dashboard
    
    Args:
        df: DataFrame with skincare data
    
    Returns:
        Plotly figure object
    """
    import plotly.graph_objs as go
    from plotly.subplots import make_subplots
    
    analytics = SkincareAnalytics(df)
    
    # Get metrics
    metrics = analytics.calculate_user_metrics()
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