
"""
Application Runner
Run this file to start the complete application
"""

import os
import sys
import subprocess
import webbrowser
import time

def check_dependencies():
    """Check and install required dependencies"""
    required_packages = [
        'flask', 'pandas', 'numpy', 'scikit-learn', 
        'plotly', 'joblib', 'bcrypt'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"Installing missing packages: {missing_packages}")
        for package in missing_packages:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print("All dependencies installed!")
    else:
        print("All dependencies satisfied!")

def check_data_files():
    """Check if data files exist, generate if not"""
    data_path = 'data/raw/skincare_dataset.csv'
    
    if not os.path.exists(data_path):
        print("Dataset not found. Generating dataset...")
        os.makedirs('data/raw', exist_ok=True)
        os.makedirs('data/processed', exist_ok=True)
        os.makedirs('data/models', exist_ok=True)
        
        # Run data generation notebook as script
        if os.path.exists('notebooks/01_data_generation.ipynb'):
            print("Please run the data generation notebook first:")
            print("  jupyter notebook notebooks/01_data_generation.ipynb")
            return False
    
    print(f"Data files found at {data_path}")
    return True

def create_directories():
    """Create necessary directories"""
    directories = [
        'data/raw',
        'data/processed', 
        'data/models',
        'static/css',
        'static/js',
        'static/assets/images',
        'templates',
        'uploads',
        'notebooks'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    print("Directory structure created!")

def run_app():
    """Start the Flask application"""
    print("\n" + "="*80)
    print("STARTING SKINCARE ANALYTICS PLATFORM")
    print("="*80)
    
    # Open browser after a short delay
    def open_browser():
        time.sleep(1.5)
        webbrowser.open('http://localhost:5000')
    
    import threading
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Import and run app
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except ImportError as e:
        print(f"Error importing app: {e}")
        print("Make sure app.py exists in the current directory")
        sys.exit(1)

def main():
    """Main execution function"""
    print("="*80)
    print("SKINCARE ANALYTICS PLATFORM SETUP")
    print("="*80)
    
    # Create directories
    create_directories()
    
    # Check dependencies
    check_dependencies()
    
    # Check data files
    if not check_data_files():
        print("\nPlease generate the dataset first using the notebook.")
        print("\nSteps to get started:")
        print("1. Run: jupyter notebook notebooks/01_EDA.ipynb")
        print("2. Run: jupyter notebook notebooks/02_data_preprocessing.ipynb")
        print("3. Run: jupyter notebook notebooks/05_model_training.ipynb")
        print("4. Then run: python run.py")
        sys.exit(1)
    
    # Run application
    run_application()

if __name__ == '__main__':
    main()