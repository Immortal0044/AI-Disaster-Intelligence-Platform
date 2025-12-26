# 🌍 AI Disaster Intelligence Platform

An end-to-end AI-powered disaster intelligence system that detects, stores, and visualizes disaster risks in near real-time by combining weather signals, social indicators, backend APIs, and geospatial visualization.

---

## 🚀 Overview

The AI Disaster Intelligence Platform is a full-stack system designed to:
- Predict disaster type and severity using an ML-ready inference layer
- Store disaster events in a relational database
- Serve predictions through REST APIs
- Visualize disaster locations and risk levels on an interactive map

The project follows industry-style separation of concerns between **ML**, **backend**, and **frontend** layers.

---

## 🧠 Key Features

- 📊 **ML Inference Layer**
  - Modular inference system (rule-based baseline, ML-ready)
  - Easily replaceable with trained ML models

- ⚙ **Backend (FastAPI)**
  - REST APIs for disaster prediction and retrieval
  - PostgreSQL database integration
  - Clean schema design and persistence

- 🌍 **Frontend (React + Leaflet)**
  - Interactive map visualization
  - Multiple disaster markers
  - Risk-level color coding (LOW / MEDIUM / HIGH)

- 🗄 **Database**
  - PostgreSQL storage for disaster events
  - Supports historical disaster visualization

---

## 🏗 Architecture

AI-Disaster-Intelligence-Platform/
├── ml/
│ └── inference/
│ └── predict.py # ML inference logic
├── backend/
│ └── app/
│ ├── main.py # FastAPI app
│ ├── db.py # Database config
│ └── models/ # SQLAlchemy models
├── frontend/
│ └── src/
│ ├── DisasterMap.js # Map & markers
│ └── App.js
└── README.md


---

## 🔌 API Endpoints

### ✅ Health Check


GET /health


### 🔮 Predict Disaster


POST /predict/disaster


**Sample Input**
```json
{
  "latitude": 19.076,
  "longitude": 72.8777,
  "timestamp": "2025-12-26T18:00:00",
  "weather_rainfall": 180,
  "weather_wind_speed": 20,
  "social_signal_score": 0.9
}

🌍 Get All Disasters
GET /disasters


Returns all stored disaster events for map visualization.

🗺 Frontend Visualization

Interactive Leaflet map

Multiple markers from backend data

Color-coded risk levels:

🔴 HIGH

🟠 MEDIUM

🟢 LOW

🧪 Tech Stack

Machine Learning

Python (ML-ready inference layer)

Backend

FastAPI

SQLAlchemy

PostgreSQL

Frontend

React

Leaflet / React-Leaflet

Axios

Tools

Git & GitHub

REST APIs

📌 Project Status

✅ Fully completed end-to-end system
✅ ML-ready architecture
✅ Backend + Frontend integrated
✅ Resume & interview ready

👤 Author

Developed as a full-stack AI project demonstrating applied machine learning, backend engineering, and geospatial visualization.

📄 License

This project is for educational and demonstration purposes.