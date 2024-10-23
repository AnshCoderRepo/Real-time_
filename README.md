## 🌤 Real-Time Weather Monitoring System
## 📌 Overview
-This project is a Python-based Real-Time Weather Monitoring System that leverages the OpenWeatherMap API to fetch, process, and visualize weather data for multiple cities. It provides real-time weather summaries, tracks historical trends, and issues configurable alerts for temperature thresholds. The system is designed to be modular, scalable, and user-friendly.

## 🚀 Features
**Real-time Weather Data: Retrieve up-to-the-minute weather data for multiple cities.**
**Daily Summaries: Aggregate and summarize daily weather data (e.g., max/min/avg temperature).**
**Weather Condition Analysis: Identify dominant weather conditions in each location.**
**Historical Trends Visualization: Visualize weather patterns and trends over time.**
**Configurable Alerts: Set custom temperature thresholds and receive real-time alerts via console or email.**
**Customizable Setup: Easily configure the system to monitor different cities or modify alert conditions.**

## 🔧 Design Choices
**Modular Architecture:**
The project is divided into distinct modules such as API, Data Aggregation, Alerts, and Visualization. This makes it easy to maintain, extend, or replace individual components without affecting the entire system.

**Asynchronous API Calls:**
To handle concurrent requests efficiently, Python's asyncio and aiohttp are utilized for fetching weather data asynchronously. This allows for quick data retrieval across multiple cities.

**In-Memory Processing with Database Backup:**
Recent data is processed in-memory for fast access, while SQLite serves as a persistent store for historical data, enabling long-term trend analysis.

**Configurable System:**
The system can be tailored to your needs through a configuration file, where you can adjust the list of cities, update intervals, and alert thresholds with ease.

**Visualization with Matplotlib:**
Leveraging Matplotlib, the system generates clear and insightful visualizations of weather trends and summaries, which are perfect for quick understanding of data patterns.

**Flexible Alerting System:**
Alerts can be triggered based on user-defined temperature thresholds. The system can be extended to support various notification channels, such as SMS or third-party APIs.

## 🖥 Prerequisites
Python 3.7 or newer
pip (Python package installer)
OpenWeatherMap API Key

## ⚙️ Installation and Setup
**1. Clone the Repository**
```
git clone https://github.com/Vaibhavbasidoni/Real-Time-Data-Processing-System-for-Weather-Monitoring-with-Rollups-and-Aggregates.git
cd Real-Time Data Processing System 
```

**2. Set Up a Virtual Environment (Recommended)**

```
python -m venv venv
source venv/bin/activate   # On Windows, use: venv\Scripts\activate
```

**3. Install Dependencies**
```
pip install -r requirements.txt
```

**4. Configure the System**

Navigate to `src/config/config.py`and update the following:
Replace "your_api_key_here" with your OpenWeatherMap API key.
Modify the CITIES list to include the cities you want to monitor.
Set UPDATE_INTERVAL and ALERT_THRESHOLDS as per your preferences.

**5. Run the System**
```
python run.py
```

## 📂 Project Structure
**Real-Time Data Processing System/**
```
├── src/
│   ├── api/
│   │   └── openweathermap.py            # Handles API requests to OpenWeatherMap
│   ├── data/
│   │   └── aggregator.py                # Aggregates weather data for cities
│   ├── alerts/
│   │   └── alert_system.py              # Triggers alerts based on weather conditions
│   ├── visualization/
│   │   └── data_visualizer.py           # Generates graphs and charts
│   └── config/
│       └── config.py                    # Configuration settings (API key, cities, thresholds)
├── tests/
│   └── test_weather_system.py           # Test cases for the weather monitoring system
├── run.py                               # Main entry point to run the system
├── README.md                            # Project documentation
└── requirements.txt                     # Python dependencies
```

## ⚙️ Configuration Options
You can easily customize the system by modifying the following parameters in src/config/config.py:

API_KEY: Your OpenWeatherMap API key.
CITIES: List of cities to monitor.
UPDATE_INTERVAL: Time interval (in seconds) between weather data updates.
ALERT_THRESHOLDS: Define temperature thresholds to trigger alerts.

## 🧪 Running Tests
To ensure the system functions as expected, run the test suite using:
```
python -m unittest discover tests
```
## 🛠 Extending the System

The system is designed to be extensible. Here are a few ways you can enhance it:
**Add New Cities:**
Simply modify the CITIES list in `src/config/config.py`.
**Update Alert Thresholds:**
Customize temperature limits in ALERT_THRESHOLDS within the configuration file.
**Add New Data Visualizations:**

Extend the DataVisualizer class in src/visualization/data_visualizer.py to create additional plots or enhance existing ones.

## 🔍 Troubleshooting
API Key Issues: Ensure you’ve set a valid API key in the configuration file.
Connection Errors: Check your internet connection if data retrieval is failing.
Visualization Errors: Verify that Matplotlib is installed and correctly configured if you encounter issues generating charts.

## 📧 Support
For any questions or issues, feel free to open an issue on GitHub or reach out via email.