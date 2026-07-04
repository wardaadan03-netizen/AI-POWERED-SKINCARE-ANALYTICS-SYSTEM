import subprocess
import sys

# ============================================
# AUTO-INSTALL MISSING PACKAGES
# ============================================
def install_packages():
    packages = ['pandas', 'numpy', 'openpyxl']
    for package in packages:
        try:
            __import__(package)
            print(f" {package} already installed")
        except ImportError:
            print(f" Installing {package}...")
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
print("GENERATING SKINCARE DATASET")
print("="*80)

n = 100000

# ============================================
# BRANDS DATABASE (Affordable to High-End)
# ============================================
brands = {
    'affordable': ['CeraVe', 'The Ordinary', 'Neutrogena', 'Cetaphil', 'Simple', 'Inkey List', 'e.l.f.', 'Cosrx', 'Bioderma', 'La Roche-Posay'],
    'mid_range': ['Kiehl\'s', 'Clinique', 'Estee Lauder', 'Lancôme', 'Paula\'s Choice', 'Drunk Elephant', 'Glow Recipe', 'Fresh', 'Sunday Riley', 'Tatcha'],
    'luxury': ['La Mer', 'SK-II', 'Chanel', 'Dior', 'Guerlain', 'La Prairie', 'Clé de Peau', 'Sisley', 'Valmont', 'Augustinus Bader']
}

# ============================================
# PRODUCTS WITH INGREDIENTS, PRICES, RATINGS
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
# HELPER FUNCTIONS FOR MESSINESS
# ============================================
def mess_text(text, prob=0.1):
    if pd.isna(text) or random.random() > prob:
        return text
    text = str(text)
    if len(text) > 3:
        pos = random.randint(0, len(text)-1)
        text = text[:pos] + random.choice('abcdefghijklmnopqrstuvwxyz') + text[pos+1:]
    if random.random() < 0.08:
        text = text.upper() if random.random() > 0.5 else text.lower()
    return text

def random_null(prob=0.05):
    return np.nan if random.random() < prob else None

# ============================================
# GENERATE DATASET
# ============================================
print("\n Generating 10,000+ rows...\n")

data = {
    # ===== A. USER IDENTITY =====
    'UserID': [f'DERMAI_{i:06d}' for i in range(n)],
    'Email': [f"user{random.randint(1,9999)}@{random.choice(['gmail.com','yahoo.com','hotmail.com'])}" for _ in range(n)],
    'RegistrationDate': [datetime.now() - timedelta(days=random.randint(0, 730)) for _ in range(n)],
    'LastActive': [datetime.now() - timedelta(days=random.randint(0, 30)) for _ in range(n)],
    'Age': [random.randint(18, 70) for _ in range(n)],
    'Gender': [random.choice(['Male', 'Female', 'Non-binary', 'Prefer not say']) for _ in range(n)],
    'SkinType': [random.choice(['Oily', 'Dry', 'Combination', 'Normal', 'Sensitive']) for _ in range(n)],
    'SkinConcerns': [random.choice(['Acne', 'Wrinkles', 'Pigmentation', 'Redness', 'Dryness', 'Large Pores', 'Dullness', 'Multiple']) for _ in range(n)],
    'FitzpatrickScale': [random.randint(1, 6) for _ in range(n)],
    'Allergies': [random.choice(['Fragrance', 'Niacinamide', 'Retinol', 'Vitamin C', 'Essential Oils', 'None', 'Unknown']) for _ in range(n)],
    
    # ===== B. LOCATION & CLIMATE =====
    'Country': [random.choice(['USA', 'Canada', 'UK', 'India', 'Australia', 'Germany', 'France', 'Brazil', 'UAE', 'Singapore']) for _ in range(n)],
    'City': [random.choice(['New York', 'London', 'Mumbai', 'Sydney', 'Paris', 'Berlin', 'Toronto', 'Dubai', 'Singapore', 'São Paulo']) for _ in range(n)],
    'Climate': [random.choice(['Tropical', 'Dry', 'Temperate', 'Continental', 'Cold', 'Mediterranean']) for _ in range(n)],
    'Humidity_pct': [random.randint(20, 95) for _ in range(n)],
    'AvgTemperature_C': [round(random.uniform(-10, 45), 1) for _ in range(n)],
    'UV_Index': [round(random.uniform(0, 12), 1) for _ in range(n)],
    'Pollution_AQI': [random.randint(20, 500) for _ in range(n)],
    'WaterHardness': [random.choice(['Soft', 'Moderate', 'Hard', 'Very Hard']) for _ in range(n)],
    
    # ===== C. LIFESTYLE =====
    'SleepHours': [round(random.uniform(4, 11), 1) for _ in range(n)],
    'StressLevel_1to10': [random.randint(1, 10) for _ in range(n)],
    'WaterIntake_Liters': [round(random.uniform(0.5, 5), 1) for _ in range(n)],
    'Exercise_Weekly': [random.randint(0, 14) for _ in range(n)],
    'Diet_Sugar': [random.choice(['Low', 'Medium', 'High', 'Very High']) for _ in range(n)],
    'Smoking': [random.choice(['Never', 'Former', 'Current', 'Occasional']) for _ in range(n)],
    'Alcohol': [random.choice(['Never', 'Monthly', 'Weekly', 'Daily']) for _ in range(n)],
    'MakeupWear': [random.choice(['Never', 'Rarely', 'Weekly', 'Daily']) for _ in range(n)],
    
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
    'SunscreenSPF': [random.choice([15, 30, 50, 70, 100]) for _ in range(n)],
    
    # ===== E. ACTIVE INGREDIENTS =====
    'UsesRetinol': [random.choice([0, 1]) for _ in range(n)],
    'UsesVitaminC': [random.choice([0, 1]) for _ in range(n)],
    'UsesNiacinamide': [random.choice([0, 1]) for _ in range(n)],
    'UsesHyaluronicAcid': [random.choice([0, 1]) for _ in range(n)],
    'UsesSalicylicAcid': [random.choice([0, 1]) for _ in range(n)],
    'UsesGlycolicAcid': [random.choice([0, 1]) for _ in range(n)],
    'UsesPeptides': [random.choice([0, 1]) for _ in range(n)],
    'UsesCeramides': [random.choice([0, 1]) for _ in range(n)],
    
    # ===== F. PRODUCT EFFECTIVENESS & REVIEWS =====
    'ProductEffectiveness_Score': [round(random.uniform(2, 5), 1) for _ in range(n)],
    'CustomerSatisfaction_pct': [random.randint(60, 98) for _ in range(n)],
    'WillRepurchase': [random.choice([0, 1]) for _ in range(n)],
    'Recommendation_Score': [random.randint(1, 10) for _ in range(n)],
    'ValueForMoney_Rating': [round(random.uniform(2, 5), 1) for _ in range(n)],
    'SideEffects_Reported': [random.choice(['None', 'Mild', 'Moderate', 'Severe']) for _ in range(n)],
    'VisibleResults_Weeks': [random.choice([1, 2, 4, 6, 8, 12]) for _ in range(n)],
    
    # ===== G. BUDGET =====
    'MonthlyBudget_USD': [random.choice([10, 20, 30, 50, 75, 100, 150, 200, 300, 500]) for _ in range(n)],
    'PreferredTier': [random.choice(['Affordable', 'Mid-Range', 'Luxury', 'Mix']) for _ in range(n)],
    'IngredientSavviness_1to10': [random.randint(1, 10) for _ in range(n)],
    'WillingToPayPremium': [random.choice([0, 1]) for _ in range(n)],
    'LooksForSales': [random.choice([0, 1]) for _ in range(n)],
    
    # ===== H. ADVANCED SCORES =====
    'SkinBarrier_Score': [random.randint(1, 10) for _ in range(n)],
    'Microbiome_Health_Score': [random.randint(1, 10) for _ in range(n)],
    'SunDamage_Risk': [random.choice(['Low', 'Medium', 'High']) for _ in range(n)],
    'Aging_Signs_Score': [random.randint(1, 10) for _ in range(n)],
    'Hydration_Level_pct': [random.randint(20, 100) for _ in range(n)],
    'Oiliness_Level': [random.choice(['Low', 'Medium', 'High', 'Very High']) for _ in range(n)],
    
    # ===== I. SAFETY =====
    'PrescriptionRetinoid': [random.choice([0, 1]) for _ in range(n)],
    'AccutaneHistory': [random.choice([0, 1]) for _ in range(n)],
    'PregnancyBreastfeeding': [random.choice([0, 1]) for _ in range(n)],
    'ChemoHistory': [random.choice([0, 1]) for _ in range(n)],
    'DrugAllergies': [random.choice(['Sulfa', 'Penicillin', 'Aspirin', 'Codeine', 'None', 'Unknown']) for _ in range(n)],
}

# ============================================
# CREATE DATAFRAME
# ============================================
df = pd.DataFrame(data)

print("Base dataset created")

# ============================================
# ADD MESSINESS (Duplicates, Nulls, Outliers)
# ============================================
print("Adding messiness...")

# Add 20% duplicate rows
duplicates = df.sample(n=int(n * 0.2), replace=True)
df = pd.concat([df, duplicates], ignore_index=True)
print(f"Added {len(duplicates)} duplicate rows")

# Add random nulls
for col in df.columns:
    if df[col].dtype == 'object':
        null_count = int(len(df) * random.uniform(0.03, 0.07))
        null_idx = random.sample(range(len(df)), min(null_count, len(df)))
        df.loc[null_idx, col] = np.nan

# Add typos to text columns
text_cols = ['SkinType', 'SkinConcerns', 'Gender', 'Country', 'City']
for col in text_cols:
    typo_idx = random.sample(range(len(df)), int(len(df) * 0.05))
    df.loc[typo_idx, col] = df.loc[typo_idx, col].apply(lambda x: mess_text(x, 0.8) if pd.notna(x) else x)

# Add outliers
df.loc[random.sample(range(len(df)), 100), 'Age'] = random.choice([8, 9, 10, 99, 105, 120])
df.loc[random.sample(range(len(df)), 80), 'MonthlyBudget_USD'] = random.choice([5000, 10000, 99999])

# Inconsistent date formats
df.loc[random.sample(range(len(df)), 200), 'RegistrationDate'] = '2020/01/15'
df.loc[random.sample(range(len(df)), 150), 'LastActive'] = 'jan-2022'

# ============================================
# SAVE TO EXCEL
# ============================================
output_file = 'skincare_dataset_complete.xlsx'
df.to_excel(output_file, index=False, engine='openpyxl')

print("\n" + "="*80)
print(" DATASET GENERATED SUCCESSFULLY!")
print("="*80)
print(f"Rows: {df.shape[0]:,}")
print(f"Columns: {df.shape[1]}")
print(f"File: {output_file}")
print(f"Location: {__import__('os').getcwd()}")
print("="*80)

# ============================================
# STATISTICS
# ============================================
print("\n Dataset Statistics:")
print(f"   • Unique Users: {df['UserID'].nunique():,}")
print(f"   • Avg Age: {df['Age'].mean():.1f}")
print(f"   • Gender Distribution:")
for g in df['Gender'].value_counts().head(5).index:
    print(f"      - {g}: {df['Gender'].value_counts()[g]:,}")
print(f"   • Skin Types:")
for s in df['SkinType'].value_counts().head(5).index:
    print(f"      - {s}: {df['SkinType'].value_counts()[s]:,}")

print("\n Brand Tiers Distribution:")
for tier in ['affordable', 'mid_range', 'luxury']:
    count = df[df['CleanserBrand'].isin(brands[tier])].shape[0]
    print(f"   • {tier.title()}: {count:,} users")

print("\n Product Ratings Summary:")
print(f"   • Cleanser Avg Rating: {df['CleanserRating'].mean():.2f}/5")
print(f"   • Serum Avg Rating: {df['SerumRating'].mean():.2f}/5")
print(f"   • Moisturizer Avg Rating: {df['MoisturizerRating'].mean():.2f}/5")

print("\n Price Summary:")
print(f"   • Avg Cleanser Price: ${df['CleanserPrice'].mean():.2f}")
print(f"   • Avg Serum Price: ${df['SerumPrice'].mean():.2f}")
print(f"   • Avg Moisturizer Price: ${df['MoisturizerPrice'].mean():.2f}")

print("\n Top Active Ingredients Used:")
ingredients = ['Retinol', 'VitaminC', 'Niacinamide', 'HyaluronicAcid', 'SalicylicAcid']
for ing in ingredients:
    col = f'Uses{ing}'
    if col in df.columns:
        usage = df[col].mean() * 100
        print(f"   • {ing}: {usage:.1f}%")

print("\n" + "="*80)
print("COMPLETE! Your dataset is ready to use.")
print("="*80)