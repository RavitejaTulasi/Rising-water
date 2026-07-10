# 🌊 Flood Prediction Using Machine Learning

A Machine Learning-based web application that predicts the likelihood of flooding using weather and rainfall parameters. The application is built using **Python**, **Flask**, and **Scikit-learn**, providing users with a simple and interactive interface to predict flood occurrence based on historical rainfall and weather conditions.

---

## 🚀 Live Demo

🌐 **Live Application**

https://rising-water-l3ro.onrender.com

📂 **GitHub Repository**

https://github.com/RavitejaTulasi/Rising-water

---

# 📖 Project Overview

Floods are among the most devastating natural disasters, causing severe damage to life, property, agriculture, and infrastructure. Accurate flood prediction enables authorities and communities to take preventive actions and minimize losses.

This project uses historical rainfall and weather data to train a Machine Learning model capable of predicting the likelihood of flood occurrence. The trained model is integrated into a Flask web application that allows users to enter weather parameters and receive instant predictions.

---

# ✨ Features

- 🌧 Predict flood occurrence using Machine Learning
- 🌡 Analyze weather and rainfall parameters
- 💻 Interactive and user-friendly web interface
- 📱 Responsive web design
- ⚡ Real-time flood prediction
- 🤖 Machine Learning model integration
- 🔄 Predict Again functionality
- ☁️ Deployed on Render

---

# 🛠 Technologies Used

## Programming Language

- Python 3

## Frontend

- HTML5
- CSS3
- JavaScript

## Backend

- Flask

## Machine Learning

- Scikit-learn
- Random Forest Classifier
- Logistic Regression
- Decision Tree
- XGBoost

## Python Libraries

- Pandas
- NumPy
- Joblib
- Matplotlib
- Seaborn
- OpenPyXL

## Deployment

- Render
- GitHub

---

# 📂 Project Structure

```text
FLOODPREDICTION/
│
├── app.py                      # Flask application
├── README.md                   # Project documentation
├── requirements.txt            # Project dependencies
├── Procfile                    # Render deployment configuration
├── Flood_Prediction.ipynb       # ML model training notebook
│
├── data/
│   ├── flood_prediction.xlsx
│   └── rainfall in india 1901-2015.xlsx
│
├── models/
│   ├── floods.save             # Trained Random Forest model
│   └── transform.save          # Saved StandardScaler
│
├── notebooks/
│   ├── Rainfall_analysis.ipynb
│   └── models/
│       ├── floods.save
│       └── transform.save
│
├── static/
│   ├── flood.jpg               # Banner image
│   ├── style.css               # CSS styles
│   └── script.js               # JavaScript
│
└── templates/
    ├── home.html               # Home page
    ├── index.html              # Prediction page
    ├── chance.html             # Flood prediction result
    └── no_chance.html          # No flood prediction result
```

> **Note:** The `notebooks/models/` folder contains duplicate model files created during development. For a cleaner repository, you can remove it and keep only the root-level `models/` folder.

---

# 📊 Dataset

The project uses historical rainfall and weather data for training and prediction.

## Input Features

- Temperature
- Humidity
- Cloud Cover
- Annual Rainfall
- January-February Rainfall
- March-May Rainfall
- June-September Rainfall
- October-December Rainfall
- Average June Rainfall
- Sub Rainfall

## Target Variable

| Value | Prediction |
|--------|------------|
| 0 | No Flood |
| 1 | Flood |

---

# 🤖 Machine Learning Models

The following Machine Learning algorithms were trained and evaluated:

- Logistic Regression
- Decision Tree
- Random Forest
- XGBoost

## Model Performance

| Model | Accuracy |
|---------|----------|
| Logistic Regression | **91.30%** |
| Decision Tree | **95.65%** |
| Random Forest | **95.65%** |
| XGBoost | **86.96%** |

After evaluating all models, the **Random Forest Classifier** was selected for deployment due to its high accuracy and robust performance.

---

# 🔄 Project Workflow

```text
Historical Dataset
        │
        ▼
Data Collection
        │
        ▼
Data Cleaning & Preprocessing
        │
        ▼
Exploratory Data Analysis
        │
        ▼
Feature Selection
        │
        ▼
Train-Test Split
        │
        ▼
Feature Scaling
        │
        ▼
Model Training
        │
        ▼
Model Evaluation
        │
        ▼
Model Serialization
        │
        ▼
Flask Web Application
        │
        ▼
Flood Prediction
```

---

# ⚙️ Installation

## Clone the Repository

```bash
git clone https://github.com/RavitejaTulasi/Rising-water.git
```

## Navigate to the Project

```bash
cd Rising-water
```

## Create a Virtual Environment

### Windows

```bash
python -m venv .venv
```

Activate the environment:

```bash
.venv\Scripts\activate
```

### Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run the Application

```bash
python app.py
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

---

# 🌐 Deployment

The application is successfully deployed on **Render**.

### Live Website

https://rising-water-l3ro.onrender.com

---

# 📸 Application Screens

### 🏠 Home Page

- Navigation Bar
- Flood Banner
- Project Introduction
- Predict Floods Button

### 📋 Prediction Page

- Weather Parameter Form
- Rainfall Input Form
- Predict Button

### 📊 Result Pages

- Flood Prediction Result
- No Flood Prediction Result

---

# 🔮 Future Enhancements

- 🌦 Live Weather API Integration
- 📍 Location-Based Flood Prediction
- 🗺 Interactive Flood Risk Maps
- 📧 Email Notifications
- 📱 Mobile Application
- 🤖 Deep Learning Models
- ☁ Cloud Database Integration
- 📊 Real-Time Weather Dashboard

---

# 👨‍💻 Author

**Raviteja Tulasi**

**B.Tech – Computer Science and Engineering (Artificial Intelligence)**

KKR & KSR Institute of Technology and Sciences

GitHub: https://github.com/RavitejaTulasi

---

# 🙏 Acknowledgements

This project was developed with the support of:

- SkillWallet
- Flask
- Scikit-learn
- Pandas
- NumPy
- XGBoost
- Render
- GitHub
- Open Source Community

---

# 📜 License

This project is developed for educational and learning purposes.

---

# ⭐ Support

If you found this project helpful, please consider giving it a ⭐ on GitHub.

Your support motivates future improvements and helps others discover the project.

---

## 📬 Contact

For any questions or suggestions, feel free to connect through GitHub:

🔗 https://github.com/RavitejaTulasi