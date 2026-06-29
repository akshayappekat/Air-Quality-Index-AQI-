# 🌍 Air Quality Index (AQI) Web App

A live web application that calculates the **Air Quality Index (AQI)** in real-time based on pollutant concentrations — built with Flask and deployed on Render.

🔗 **Live Demo:** https://air-quality-index-aqi.onrender.com

---

## 🚀 Features

- 🔢 Enter pollutant values (PM2.5, PM10, NO₂, SO₂, CO)
- 📊 Instant AQI calculation using **US EPA standard breakpoints**
- 🎨 Color-coded AQI categories (Good → Hazardous)
- 💡 Health advice based on AQI level
- 📌 Dominant pollutant identification
- 📉 Sub-index breakdown per pollutant
- 📱 Fully responsive UI

---

## 🎯 AQI Categories

| AQI Range | Category | Color |
|-----------|----------|-------|
| 0 – 50 | Good | 🟢 Green |
| 51 – 100 | Moderate | 🟡 Yellow |
| 101 – 150 | Unhealthy for Sensitive Groups | 🟠 Orange |
| 151 – 200 | Unhealthy | 🔴 Red |
| 201 – 300 | Very Unhealthy | 🟣 Purple |
| 301 – 500 | Hazardous | 🟤 Maroon |

---

## 🧠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask |
| Frontend | HTML, CSS, JavaScript |
| AQI Logic | US EPA Linear Interpolation |
| Deployment | Render (free tier) |
| Server | Gunicorn |

---

## 📁 Project Structure

```
├── app.py                  # Flask backend + AQI calculation logic
├── templates/
│   └── index.html          # Frontend UI
├── requirements.txt        # Python dependencies
├── Procfile                # Render/Heroku start command
├── render.yaml             # Render deployment config
├── 038_ADS_LAB6.ipynb      # Original data analysis notebook
└── README.md
```

---

## ⚙️ Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/akshayappekat/Air-Quality-Index-AQI-.git
cd Air-Quality-Index-AQI-

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python app.py

# 4. Open in browser
http://127.0.0.1:5000
```

---

## 📊 Original Notebook

The `038_ADS_LAB6.ipynb` notebook contains:
- Data cleaning and preprocessing of air quality dataset (AP001.csv)
- Z-score normalization
- K-Means clustering to group pollution levels
- Elbow method for optimal cluster selection
- PCA dimensionality reduction
- Correlation heatmap visualization

---

## 👤 Author

**Akshay Appekat**  
GitHub: [@akshayappekat](https://github.com/akshayappekat)
