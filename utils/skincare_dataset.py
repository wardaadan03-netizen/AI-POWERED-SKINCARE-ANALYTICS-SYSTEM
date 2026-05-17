
import subprocess
import sys


# ============================================
# AUTO-INSTALL MISSING PACKAGES
# ============================================
def install_packages():
    packages = ['pandas', 'numpy', 'openpyxl', 'matplotlib', 'seaborn']
    for package in packages:
        try:
            __import__(package)
            print(f"{package} already installed")
        except ImportError:
            print(f"     Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install_packages()

# ============================================
# IMPORTS
# ============================================
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

print("\n" + "="*80)
print("GENERATING SKINCARE DATASET WITH REALISTIC DISTRIBUTIONS")
print("="*80)

n = 100000
np.random.seed(42)
random.seed(42)

# ============================================
# REALISTIC DISTRIBUTIONS (Not Uniform!)
# ============================================

# 1. Gender distribution (realistic for skincare market)
# Female dominant (65%), Male (25%), Others (10%)
gender_options = ['Female', 'Male', 'Non-binary', 'Prefer not say']
gender_weights = [0.65, 0.25, 0.05, 0.05]  # Realistic weights

# 2. Skin type distribution (realistic)
# Combination most common, then Oily, Dry, Normal, Sensitive
skin_types = ['Combination', 'Oily', 'Dry', 'Normal', 'Sensitive']
skin_weights = [0.40, 0.25, 0.18, 0.10, 0.07]

# 3. Skin concerns distribution
concerns = ['Acne', 'Pigmentation', 'Wrinkles', 'Dryness', 'Large Pores', 'Redness', 'Dullness']
concern_weights = [0.30, 0.20, 0.18, 0.12, 0.08, 0.07, 0.05]

# 4. Age distribution (normal/bell curve)
age_mean, age_std = 34, 12
age_values = np.random.normal(age_mean, age_std, n).astype(int)
age_values = np.clip(age_values, 18, 70)

# 5. Budget distribution (right-skewed - more lower budgets)
budget_options = [20, 30, 50, 75, 100, 150, 200, 300, 500]
budget_weights = [0.25, 0.20, 0.18, 0.12, 0.10, 0.07, 0.04, 0.03, 0.01]

# 6. Product effectiveness (normal around 4.0)
effectiveness_mean, effectiveness_std = 4.0, 0.6

# 7. Satisfaction (normal around 80%)
satisfaction_mean, satisfaction_std = 80, 10

# 8. Repurchase rate (~75% will repurchase)
repurchase_rate = 0.75

# 9. Active ingredients usage (realistic percentages)
ingredient_rates = {
    'Retinol': 0.35,      # 35% use retinol
    'VitaminC': 0.45,     # 45% use vitamin C
    'Niacinamide': 0.40,  # 40% use niacinamide
    'HyaluronicAcid': 0.55, # 55% use hyaluronic acid
    'SalicylicAcid': 0.30,
    'GlycolicAcid': 0.25,
    'Peptides': 0.20,
    'Ceramides': 0.35
}

# ============================================
# BRANDS DATABASE
# ============================================
brands = {
    'affordable': ['CeraVe', 'The Ordinary', 'Neutrogena', 'Cetaphil', 'Simple', 'Inkey List', 'e.l.f.', 'Cosrx', 'Bioderma', 'La Roche-Posay'],
    'mid_range': ['Kiehl\'s', 'Clinique', 'Estee Lauder', 'Lancôme', 'Paula\'s Choice', 'Drunk Elephant', 'Glow Recipe', 'Fresh', 'Sunday Riley', 'Tatcha'],
    'luxury': ['La Mer', 'SK-II', 'Chanel', 'Dior', 'Guerlain', 'La Prairie', 'Clé de Peau', 'Sisley', 'Valmont', 'Augustinus Bader']
}

# ============================================
# PRODUCTS DATABASE
# ============================================
products = {
    'Cleanser': [
        {'name': 'CeraVe Hydrating Cleanser', 'brand': 'CeraVe', 'price': 12.99, 'tier': 'affordable', 'ingredients': ['Ceramides', 'Hyaluronic Acid', 'Glycerin'], 'rating': 4.7, 'reviews': 15234},
        {'name': 'La Roche-Posay Effaclar', 'brand': 'La Roche-Posay', 'price': 16.99, 'tier': 'affordable', 'ingredients': ['Salicylic Acid', 'Zinc PCA', 'Glycerin'], 'rating': 4.6, 'reviews': 8921},
        {'name': 'Fresh Soy Face Cleanser', 'brand': 'Fresh', 'price': 38.00, 'tier': 'mid_range', 'ingredients': ['Soy Proteins', 'Rosewater', 'Cucumber Extract'], 'rating': 4.5, 'reviews': 3456},
        {'name': 'SK-II Facial Treatment Cleanser', 'brand': 'SK-II', 'price': 75.00, 'tier': 'luxury', 'ingredients': ['Pitera', 'Hydrolyzed Silk', 'Meadowfoam Oil'], 'rating': 4.8, 'reviews': 1234},
    ],
    'Serum': [
        {'name': 'The Ordinary Niacinamide 10%', 'brand': 'The Ordinary', 'price': 5.90, 'tier': 'affordable', 'ingredients': ['Niacinamide', 'Zinc PCA'], 'rating': 4.4, 'reviews': 45678},
        {'name': 'Paula\'s Choice Vitamin C', 'brand': 'Paula\'s Choice', 'price': 49.00, 'tier': 'mid_range', 'ingredients': ['15% Vitamin C', 'Vitamin E', 'Ferulic Acid'], 'rating': 4.6, 'reviews': 8923},
        {'name': 'SkinCeuticals C E Ferulic', 'brand': 'SkinCeuticals', 'price': 182.00, 'tier': 'luxury', 'ingredients': ['15% Vitamin C', '1% Vitamin E', '0.5% Ferulic Acid'], 'rating': 4.9, 'reviews': 5678},
        {'name': 'La Mer The Concentrate', 'brand': 'La Mer', 'price': 395.00, 'tier': 'luxury', 'ingredients': ['Miracle Broth', 'Lime Tea Extract', 'Sea Kelp'], 'rating': 4.8, 'reviews': 2345},
    ],
    'Moisturizer': [
        {'name': 'CeraVe Moisturizing Cream', 'brand': 'CeraVe', 'price': 14.99, 'tier': 'affordable', 'ingredients': ['Ceramides', 'Hyaluronic Acid', 'Petrolatum'], 'rating': 4.8, 'reviews': 67890},
        {'name': 'Kiehl\'s Ultra Facial Cream', 'brand': 'Kiehl\'s', 'price': 38.00, 'tier': 'mid_range', 'ingredients': ['Squalane', 'Glycerin', 'Imperata Cylindrica'], 'rating': 4.5, 'reviews': 23456},
        {'name': 'La Mer Crème de la Mer', 'brand': 'La Mer', 'price': 380.00, 'tier': 'luxury', 'ingredients': ['Miracle Broth', 'Lime Extract', 'Seaweed'], 'rating': 4.7, 'reviews': 12345},
    ],
    'Sunscreen': [
        {'name': 'Supergoop! Unseen Sunscreen', 'brand': 'Supergoop!', 'price': 38.00, 'tier': 'mid_range', 'ingredients': ['Avobenzone', 'Homosalate', 'Octisalate'], 'rating': 4.6, 'reviews': 34567},
        {'name': 'La Roche-Posay Anthelios', 'brand': 'La Roche-Posay', 'price': 29.99, 'tier': 'affordable', 'ingredients': ['Mexoryl XL', 'Titanium Dioxide', 'Glycerin'], 'rating': 4.7, 'reviews': 45678},
        {'name': 'Shiseido Ultimate Sun Protector', 'brand': 'Shiseido', 'price': 52.00, 'tier': 'mid_range', 'ingredients': ['WetForce Technology', 'Hyaluronic Acid', 'Green Tea'], 'rating': 4.8, 'reviews': 12345},
    ]
}

# ============================================
# HELPER FUNCTIONS
# ============================================
def weighted_choice(options, weights):
    """Select option based on weights"""
    return np.random.choice(options, p=weights)

def mess_text(text, prob=0.05):  # Reduced probability for cleaner data
    if pd.isna(text) or random.random() > prob:
        return text
    text = str(text)
    if len(text) > 3 and random.random() < 0.3:
        pos = random.randint(0, len(text)-1)
        text = text[:pos] + random.choice('abcdefghijklmnopqrstuvwxyz') + text[pos+1:]
    return text

# ============================================
# GENERATE DATASET WITH REALISTIC DISTRIBUTIONS
# ============================================
print("\nGenerating dataset with realistic distributions...\n")

# Generate data with weighted distributions
data = {
    # ===== A. USER IDENTITY =====
    'UserID': [f'DERMAI_{i:06d}' for i in range(n)],
    'Email': [f"user{random.randint(1,9999)}@{random.choice(['gmail.com','yahoo.com','hotmail.com'])}" for _ in range(n)],
    'RegistrationDate': [datetime.now() - timedelta(days=random.randint(0, 730)) for _ in range(n)],
    'LastActive': [datetime.now() - timedelta(days=random.randint(0, 30)) for _ in range(n)],
    'Age': age_values,
    'Gender': np.random.choice(gender_options, n, p=gender_weights),
    'SkinType': np.random.choice(skin_types, n, p=skin_weights),
    'SkinConcerns': np.random.choice(concerns, n, p=concern_weights),
    'FitzpatrickScale': np.random.choice([1,2,3,4,5,6], n, p=[0.05,0.10,0.20,0.30,0.25,0.10]),
    'Allergies': np.random.choice(['Fragrance', 'Niacinamide', 'Retinol', 'Vitamin C', 'Essential Oils', 'None'], 
                                   n, p=[0.08, 0.05, 0.05, 0.05, 0.07, 0.70]),
    
    # ===== B. LOCATION & CLIMATE =====
    'Country': np.random.choice(['USA', 'Canada', 'UK', 'India', 'Australia', 'Germany', 'France', 'Brazil', 'UAE', 'Singapore'],
                                n, p=[0.30, 0.10, 0.10, 0.15, 0.05, 0.08, 0.08, 0.05, 0.05, 0.04]),
    'City': np.random.choice(['New York', 'London', 'Mumbai', 'Sydney', 'Paris', 'Berlin', 'Toronto', 'Dubai', 'Singapore', 'São Paulo'], n),
    'Climate': np.random.choice(['Tropical', 'Dry', 'Temperate', 'Continental', 'Cold', 'Mediterranean'],
                                n, p=[0.20, 0.15, 0.25, 0.15, 0.10, 0.15]),
    'Humidity_pct': np.random.normal(60, 20, n).clip(20, 95).astype(int),
    'AvgTemperature_C': np.round(np.random.normal(18, 15, n).clip(-10, 45), 1),
    'UV_Index': np.round(np.random.normal(6, 3, n).clip(0, 12), 1),
    'Pollution_AQI': np.random.exponential(100, n).clip(20, 500).astype(int),
    'WaterHardness': np.random.choice(['Soft', 'Moderate', 'Hard', 'Very Hard'], n, p=[0.20, 0.40, 0.30, 0.10]),
    
    # ===== C. LIFESTYLE =====
    'SleepHours': np.round(np.random.normal(7, 1.5, n).clip(4, 11), 1),
    'StressLevel_1to10': np.random.normal(5, 2, n).clip(1, 10).astype(int),
    'WaterIntake_Liters': np.round(np.random.exponential(2, n).clip(0.5, 5), 1),
    'Exercise_Weekly': np.random.poisson(3, n).clip(0, 14),
    'Diet_Sugar': np.random.choice(['Low', 'Medium', 'High', 'Very High'], n, p=[0.15, 0.45, 0.30, 0.10]),
    'Smoking': np.random.choice(['Never', 'Former', 'Current', 'Occasional'], n, p=[0.65, 0.15, 0.10, 0.10]),
    'Alcohol': np.random.choice(['Never', 'Monthly', 'Weekly', 'Daily'], n, p=[0.20, 0.30, 0.35, 0.15]),
    'MakeupWear': np.random.choice(['Never', 'Rarely', 'Weekly', 'Daily'], n, p=[0.15, 0.20, 0.25, 0.40]),
    
    # ===== D. PRODUCT USAGE & BRANDS =====
    'CurrentCleanser': [random.choice(products['Cleanser'])['name'] for _ in range(n)],
    'CleanserBrand': [random.choice(products['Cleanser'])['brand'] for _ in range(n)],
    'CleanserPrice': [random.choice(products['Cleanser'])['price'] for _ in range(n)],
    'CleanserRating': [random.choice(products['Cleanser'])['rating'] for _ in range(n)],
    'CleanserReviews': [random.choice(products['Cleanser'])['reviews'] for _ in range(n)],
    'CleanserIngredients': [', '.join(random.choice(products['Cleanser'])['ingredients']) for _ in range(n)],
    
    'CurrentSerum': [random.choice(products['Serum'])['name'] for _ in range(n)],
    'SerumBrand': [random.choice(products['Serum'])['brand'] for _ in range(n)],
    'SerumPrice': [random.choice(products['Serum'])['price'] for _ in range(n)],
    'SerumRating': [random.choice(products['Serum'])['rating'] for _ in range(n)],
    'SerumReviews': [random.choice(products['Serum'])['reviews'] for _ in range(n)],
    'SerumIngredients': [', '.join(random.choice(products['Serum'])['ingredients']) for _ in range(n)],
    
    'CurrentMoisturizer': [random.choice(products['Moisturizer'])['name'] for _ in range(n)],
    'MoisturizerBrand': [random.choice(products['Moisturizer'])['brand'] for _ in range(n)],
    'MoisturizerPrice': [random.choice(products['Moisturizer'])['price'] for _ in range(n)],
    'MoisturizerRating': [random.choice(products['Moisturizer'])['rating'] for _ in range(n)],
    'MoisturizerReviews': [random.choice(products['Moisturizer'])['reviews'] for _ in range(n)],
    'MoisturizerIngredients': [', '.join(random.choice(products['Moisturizer'])['ingredients']) for _ in range(n)],
    
    'CurrentSunscreen': [random.choice(products['Sunscreen'])['name'] for _ in range(n)],
    'SunscreenSPF': np.random.choice([15, 30, 50, 70, 100], n, p=[0.05, 0.30, 0.45, 0.15, 0.05]),
    
    # ===== E. ACTIVE INGREDIENTS (with realistic rates) =====
    'UsesRetinol': np.random.choice([0, 1], n, p=[1-ingredient_rates['Retinol'], ingredient_rates['Retinol']]),
    'UsesVitaminC': np.random.choice([0, 1], n, p=[1-ingredient_rates['VitaminC'], ingredient_rates['VitaminC']]),
    'UsesNiacinamide': np.random.choice([0, 1], n, p=[1-ingredient_rates['Niacinamide'], ingredient_rates['Niacinamide']]),
    'UsesHyaluronicAcid': np.random.choice([0, 1], n, p=[1-ingredient_rates['HyaluronicAcid'], ingredient_rates['HyaluronicAcid']]),
    'UsesSalicylicAcid': np.random.choice([0, 1], n, p=[1-ingredient_rates['SalicylicAcid'], ingredient_rates['SalicylicAcid']]),
    'UsesGlycolicAcid': np.random.choice([0, 1], n, p=[1-ingredient_rates['GlycolicAcid'], ingredient_rates['GlycolicAcid']]),
    'UsesPeptides': np.random.choice([0, 1], n, p=[1-ingredient_rates['Peptides'], ingredient_rates['Peptides']]),
    'UsesCeramides': np.random.choice([0, 1], n, p=[1-ingredient_rates['Ceramides'], ingredient_rates['Ceramides']]),
    
    # ===== F. PRODUCT EFFECTIVENESS & REVIEWS =====
    'ProductEffectiveness_Score': np.round(np.random.normal(effectiveness_mean, effectiveness_std, n).clip(2, 5), 1),
    'CustomerSatisfaction_pct': np.random.normal(satisfaction_mean, satisfaction_std, n).clip(50, 98).astype(int),
    'WillRepurchase': np.random.choice([0, 1], n, p=[1-repurchase_rate, repurchase_rate]),
    'Recommendation_Score': np.random.normal(7, 2, n).clip(1, 10).astype(int),
    'ValueForMoney_Rating': np.round(np.random.normal(4.0, 0.7, n).clip(2, 5), 1),
    'SideEffects_Reported': np.random.choice(['None', 'Mild', 'Moderate', 'Severe'], n, p=[0.70, 0.20, 0.08, 0.02]),
    'VisibleResults_Weeks': np.random.choice([1, 2, 4, 6, 8, 12], n, p=[0.05, 0.15, 0.30, 0.25, 0.15, 0.10]),
    
    # ===== G. BUDGET =====
    'MonthlyBudget_USD': np.random.choice(budget_options, n, p=budget_weights),
    'PreferredTier': np.random.choice(['Affordable', 'Mid-Range', 'Luxury', 'Mix'], n, p=[0.40, 0.35, 0.10, 0.15]),
    'IngredientSavviness_1to10': np.random.normal(5, 2.5, n).clip(1, 10).astype(int),
    'WillingToPayPremium': np.random.choice([0, 1], n, p=[0.60, 0.40]),
    'LooksForSales': np.random.choice([0, 1], n, p=[0.35, 0.65]),
    
    # ===== H. ADVANCED SCORES =====
    'SkinBarrier_Score': np.random.normal(6, 2, n).clip(1, 10).astype(int),
    'Microbiome_Health_Score': np.random.normal(6.5, 1.8, n).clip(1, 10).astype(int),
    'SunDamage_Risk': np.random.choice(['Low', 'Medium', 'High'], n, p=[0.30, 0.50, 0.20]),
    'Aging_Signs_Score': np.random.normal(5, 2.5, n).clip(1, 10).astype(int),
    'Hydration_Level_pct': np.random.normal(65, 15, n).clip(20, 100).astype(int),
    'Oiliness_Level': np.random.choice(['Low', 'Medium', 'High', 'Very High'], n, p=[0.25, 0.40, 0.25, 0.10]),
    
    # ===== I. SAFETY =====
    'PrescriptionRetinoid': np.random.choice([0, 1], n, p=[0.92, 0.08]),
    'AccutaneHistory': np.random.choice([0, 1], n, p=[0.95, 0.05]),
    'PregnancyBreastfeeding': np.random.choice([0, 1], n, p=[0.95, 0.05]),
    'ChemoHistory': np.random.choice([0, 1], n, p=[0.98, 0.02]),
    'DrugAllergies': np.random.choice(['Sulfa', 'Penicillin', 'Aspirin', 'Codeine', 'None', 'Unknown'], 
                                       n, p=[0.03, 0.04, 0.03, 0.02, 0.80, 0.08]),
}

# ============================================
# CREATE DATAFRAME
# ============================================
df = pd.DataFrame(data)

print("Base dataset created with realistic distributions")

# ============================================
# ADD MINIMAL MESSINESS (Reduced for cleaner data)
# ============================================
print("\n Adding minimal data imperfections...")

# Add 5% duplicate rows (reduced from 20%)
duplicates = df.sample(n=int(n * 0.05), replace=True)
df = pd.concat([df, duplicates], ignore_index=True)
print(f"   Added {len(duplicates)} duplicate rows (5%)")

# Add random nulls (reduced frequency)
for col in df.columns:
    if df[col].dtype == 'object':
        null_count = int(len(df) * random.uniform(0.01, 0.03))  # Reduced from 3-7% to 1-3%
        null_idx = random.sample(range(len(df)), min(null_count, len(df)))
        df.loc[null_idx, col] = np.nan

# Add minimal typos
text_cols = ['SkinType', 'SkinConcerns', 'Gender', 'Country', 'City']
for col in text_cols:
    typo_idx = random.sample(range(len(df)), int(len(df) * 0.02))  # Reduced from 5% to 2%
    df.loc[typo_idx, col] = df.loc[typo_idx, col].apply(lambda x: mess_text(x, 0.5) if pd.notna(x) else x)

# Add few outliers
df.loc[random.sample(range(len(df)), 50), 'Age'] = np.random.choice([8, 9, 10, 85, 90, 95], 50)
df.loc[random.sample(range(len(df)), 30), 'MonthlyBudget_USD'] = np.random.choice([2000, 5000, 10000], 30)

# ============================================
# SAVE TO CSV
# ============================================
output_file = 'skincare_dataset.csv'
df.to_csv(output_file, index=False)

print("\n" + "="*80)
print("DATASET GENERATED SUCCESSFULLY!")
print("="*80)
print(f"   Rows: {df.shape[0]:,}")
print(f"   Columns: {df.shape[1]}")
print(f"   File: {output_file}")
print(f"   Location: {__import__('os').getcwd()}")
print("="*80)

# ============================================
# STATISTICS
# ============================================
print("\nDATASET STATISTICS:")
print(f"   • Unique Users: {df['UserID'].nunique():,}")
print(f"   • Avg Age: {df['Age'].mean():.1f} years")
print(f"\n   • Gender Distribution:")
for g in df['Gender'].value_counts().index:
    count = df['Gender'].value_counts()[g]
    pct = (count/len(df))*100
    print(f"      - {g}: {count:,} ({pct:.1f}%)")

print(f"\n   • Skin Types:")
for s in df['SkinType'].value_counts().index:
    count = df['SkinType'].value_counts()[s]
    pct = (count/len(df))*100
    print(f"      - {s}: {count:,} ({pct:.1f}%)")

print(f"\n   • Top Skin Concerns:")
for c in df['SkinConcerns'].value_counts().head(3).index:
    count = df['SkinConcerns'].value_counts()[c]
    pct = (count/len(df))*100
    print(f"      - {c}: {count:,} ({pct:.1f}%)")

print("\n   • Budget Statistics:")
print(f"      - Mean: ${df['MonthlyBudget_USD'].mean():.2f}")
print(f"      - Median: ${df['MonthlyBudget_USD'].median():.2f}")

print("\n   • Product Ratings:")
print(f"      - Avg Effectiveness: {df['ProductEffectiveness_Score'].mean():.2f}/5")
print(f"      - Avg Satisfaction: {df['CustomerSatisfaction_pct'].mean():.1f}%")
print(f"      - Repurchase Rate: {df['WillRepurchase'].mean()*100:.1f}%")

print("\n   • Active Ingredients Usage:")
for ing, rate in ingredient_rates.items():
    col = f'Uses{ing}'
    if col in df.columns:
        usage = df[col].mean() * 100
        print(f"      - {ing}: {usage:.1f}% (target: {rate*100:.0f}%)")

print("\n" + "="*80)
print(" COMPLETE! Your dataset with realistic distributions is ready.")
print("="*80)