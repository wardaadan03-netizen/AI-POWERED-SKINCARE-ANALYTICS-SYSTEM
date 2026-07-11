# 🧴 Inzaghi's Bliss - AI-Powered Skincare Platform

## 📌 Overview

**Inzaghi's Bliss** is an AI-powered skincare intelligence platform that provides personalized skincare recommendations based on user profiles. The system uses machine learning algorithms to analyze skin types, concerns, and preferences to suggest suitable skincare products.

---

## 🎯 Problem Statement

People often struggle to choose the right skincare products due to lack of personalized guidance. This platform solves this by using AI to analyze skin attributes and recommend appropriate skincare solutions based on data-driven insights.

---

## ✨ Key Features

### 🔐 Authentication & Profiles
- User registration and login system
- Secure password hashing with salt
- Session management
- Personalized user profiles

### 🧴 Skincare Analysis
- Skin type detection
- Skin concern identification
- Product match scoring
- Ingredient analysis

### 🎯 Smart Recommendations
- AI-powered product recommendations
- Match percentage scores
- Category filtering (Cleansers, Serums, Moisturizers, Sunscreens)
- Budget-based filtering

### 📊 Interactive Dashboard
- Real-time skin health metrics
- Product comparison tool
- Ingredient usage analysis
- 3D visualizations using Plotly

### 📱 User Features
- QR code for mobile app download
- Medical disclaimer popup
- Product feedback system
- Profile management

### 🎨 Modern UI/UX
- Glass-morphism design
- Responsive layout
- Smooth animations
- Dark theme optimized for skincare

---

## 🚀 Live Demo

**URL:** http://localhost:5000

---

## 🧠 Technologies Used

### Backend
- **Python 3.8+** - Core programming language
- **Flask 3.1.3** - Web framework
- **Pandas 3.0.3** - Data manipulation
- **NumPy 2.4.5** - Numerical operations
- **Scikit-learn 1.8.0** - Machine learning
- **Joblib 1.5.3** - Model serialization
- **bcrypt 5.0.0** - Password hashing

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling (Glass-morphism, animations)
- **JavaScript** - Interactivity
- **jQuery 3.7.1** - DOM manipulation
- **Plotly 6.7.0** - 3D visualizations
- **Font Awesome 6.4.0** - Icons

### Data & Models
- **Dataset:** 100,000+ synthetic skincare records
- **Algorithms:** Logistic Regression, Decision Tree, Random Forest
- **Features:** Age, Skin Type, Concerns, Budget, Ingredients

---

## 📂 Project Structure

```
AI-POWERED-SKINCARE-APP/
│
├── data/
│   ├── users.json              # User database
│   ├── feedback.json           # User feedback
│   └── raw/
│       └── skincare_dataset.csv # Generated dataset
│
├── modules/
│   ├── __init__.py
│   ├── authentication.py       # User auth logic
│   ├── recommender.py          # Recommendation engine
│   ├── preprocessing.py        # Data preprocessing
│   └── analytics.py            # Analytics engine
│
├── utils/
│   ├── __init__.py
│   └── helpers.py              # Helper functions
│
├── static/
│   ├── css/
│   │   └── style.css           # Main styles
│   └── js/
│       ├── base.js             # Shared JS
│       ├── dashboard.js        # Dashboard JS
│       ├── main.js             # UI interactions
│       └── 3d_visualization.js # 3D charts
│
├── templates/
│   ├── base.html               # Base template
│   ├── index.html              # Landing page
│   ├── login.html              # Login page
│   ├── register.html           # Registration page
│   ├── dashboard.html          # User dashboard
│   ├── profile.html            # User profile
│   ├── profile_setup.html      # Profile setup
│   ├── recommendations.html    # Recommendations
│   ├── ingredients.html        # Ingredient science
│   ├── disclaimer.html         # Disclaimer page
│   └── qr_code.html            # QR code page
│
├── tests/
│   ├── test_auth.py
│   ├── test_preprocessing.py
│   └── test_recommender.py
│
├── uploads/                    # User uploads
│
├── .env                        # Environment variables
├── .gitignore                  # Git ignore
├── app.py                      # Main Flask app
├── config.py                   # Configuration
├── run.py                      # Entry point
├── setup.py                    # Setup script
├── skincare_dataset.py         # Dataset generator
├── requirements.txt            # Dependencies
├── README.md                   # Documentation
└── LICENSE                     # License
```

---

## ⚙️ How to Run This Project

### 1. Prerequisites

- Python 3.8 or higher installed
- pip package manager

### 2. Clone the Repository

```bash
git clone https://github.com/your-username/AI-POWERED-SKINCARE-APP.git
cd AI-POWERED-SKINCARE-APP
```

### 3. Create Virtual Environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Mac/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Generate Dataset

```bash
python skincare_dataset.py
```

### 6. Set Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your-secret-key-here
FLASK_DEBUG=true
PORT=5000
```

### 7. Run the Application

```bash
python run.py
# OR
python app.py
```

### 8. Open in Browser

```
http://localhost:5000
```

---

## 🧪 Test Accounts

### Demo Account
- **Email:** demo@inzaghis-bliss.com
- **Password:** demo123

### Create Your Own Account
- Register with your email and password
- Complete your profile
- Get personalized recommendations!

---

## 🔒 Security Features

- **Password Hashing:** SHA-256 with salt
- **Session Management:** Secure cookie-based sessions
- **Secret Key:** Environment variable based
- **File Upload:** Limited to CSV files (10MB max)
- **Login Required:** Protected routes

---

## 📊 Machine Learning Models

### Algorithms Used
- **Logistic Regression** - Binary classification
- **Decision Tree Classifier** - Multi-class classification  
- **Random Forest Classifier** - Ensemble learning

### Features
- Age, Gender, Skin Type, Skin Concerns
- Monthly Budget, Product Preferences
- Active Ingredients Usage

### Evaluation Metrics
- Accuracy Score: ~85%
- Precision & Recall
- Confusion Matrix

---

## 🔄 API Endpoints

### Authentication
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/login` | POST | User login |
| `/register` | POST | User registration |
| `/logout` | GET | User logout |

### User Profile
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/user/profile` | GET | Get user profile |
| `/api/user/preferences` | POST | Update preferences |
| `/api/user/activity` | GET | Get activity history |

### Recommendations
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/recommendations` | POST | Get recommendations |
| `/api/personalized-recommendations` | GET | Get personalized recommendations |
| `/api/predict-rating` | POST | Predict product rating |

### Analytics
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/analytics` | GET | Get analytics data |
| `/api/ingredients` | GET | Get ingredient insights |
| `/api/submit-feedback` | POST | Submit user feedback |

---

## 🎨 UI/UX Features

- **Glass-morphism Design:** Modern, translucent cards with backdrop blur
- **Responsive Layout:** Works on desktop, tablet, and mobile
- **Dark Theme:** Optimized for skincare with dark background
- **3D Visualizations:** Interactive Plotly charts
- **Animated Elements:** Smooth transitions and hover effects
- **Toast Notifications:** Real-time feedback
- **Disclaimer Popup:** Automatic on login/register

---

## 📱 QR Code & Mobile

- **QR Code:** Scan to open the web app on mobile
- **Download Buttons:** App Store and Google Play (coming soon)
- **Mobile Responsive:** Fully optimized for mobile devices

---

## 🛡️ Medical Disclaimer

⚠️ **Important:** This application is only a recommendation system. Always:
- Perform a patch test before using new products
- Consult a dermatologist for serious skin conditions
- Review product ingredients carefully
- Understand that results may vary

---

## 🚀 Future Improvements

- [ ] Image-based skin analysis using CNN
- [ ] Real-time chat support
- [ ] Email notifications
- [ ] Social sharing features
- [ ] Mobile app (iOS & Android)
- [ ] Integration with e-commerce platforms
- [ ] Advanced recommendation algorithms
- [ ] Multi-language support

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 👨‍💻 Author

**Warda Adan**

- GitHub: [wardaadan03-netizen](https://github.com/wardaadan03-netizen)
- Project Link: [https://github.com/wardaadan03-netizen/AI-POWERED-SKINCARE-APP](https://github.com/wardaadan03-netizen/AI-POWERED-SKINCARE-APP)

---

## ⭐ Acknowledgements

- Scikit-learn documentation
- Plotly for 3D visualizations
- Font Awesome for icons
- Flask community
- Open-source datasets
- Machine Learning community

---

## 📞 Support

For support, email support@inzaghis-bliss.com or open an issue on GitHub.

---

**Made with ❤️ by Team Inzaghi's Bliss**
```

---

## 📋 **What Was Updated:**

| Section | Changes |
|---------|---------|
| **Project Structure** | Added full folder structure with all new files |
| **Features** | Added all new features (QR code, disclaimer, 3D visuals, etc.) |
| **Technologies** | Added all modern technologies (Flask 3.1.3, Plotly 6.7.0, etc.) |
| **API Endpoints** | Complete list of all API routes |
| **Security** | Added security features section |
| **Disclaimer** | Added medical disclaimer information |
| **Future Improvements** | Added all planned features |
| **UI/UX** | Added design features section |

---

