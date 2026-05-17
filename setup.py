from setuptools import setup, find_packages

setup(
    name="skincare-analytics-platform",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="AI-powered skincare analytics platform with 3D visualizations",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/skincare-analytics-platform",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "flask>=2.3.3",
        "pandas>=2.0.3",
        "numpy>=1.24.3",
        "scikit-learn>=1.3.0",
        "plotly>=5.15.0",
        "matplotlib>=3.7.2",
        "seaborn>=0.12.2",
        "joblib>=1.3.1",
        "bcrypt>=4.0.1",
    ],
    entry_points={
        "console_scripts": [
            "skincare-app=app:main",
        ],
    },
)