import asyncio
import logging
from datetime import datetime, timezone
import sys
import os
import threading
import tkinter as tk
from src.api.openweathermap import OpenWeatherMapAPI
from src.data.aggregator import WeatherDataAggregator
from src.alerts.alert_system import AlertSystem
from src.visualization.data_visualizer import DataVisualizer
from src.config.config import Config

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# At the top of the file, update the logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class WeatherMonitoringApp:
    def __init__(self):
        self.api_client = OpenWeatherMapAPI()
        self.aggregator = WeatherDataAggregator()
        self.alert_system = AlertSystem()
        self.visualizer = DataVisualizer(self.on_closing)
        self.running = True
        self.active_alerts = set()
        logging.info("WeatherMonitoringApp initialized")

    def on_closing(self):
        logging.info("Application closing...")
        self.running = False
        self.visualizer.root.quit()
        self.visualizer.root.destroy()

    async def update_weather_data(self):
        logging.info("Updating weather data...")
        logging.info(f"Fetching weather data for cities: {Config.CITIES}")
        weather_data = await self.api_client.get_weather_for_cities(Config.CITIES)
        logging.info(f"Received weather data for {len(weather_data)} out of {len(Config.CITIES)} cities")

        for city, data in weather_data.items():
            # Simulate multiple data points
            for _ in range(5):  # Add 5 data points per update
                timestamp = datetime.fromtimestamp(data['dt'], tz=timezone.utc)
                temperature = round(data['main']['temp'], 1)  # Round to 1 decimal place
                condition = data['weather'][0]['main']
                self.aggregator.add_weather_data(city, timestamp, temperature, condition)
                if self.alert_system.check_alerts(city, temperature):
                    self.active_alerts.add(city)
                else:
                    self.active_alerts.discard(city)
                logging.info(f"Added weather data for {city} at {timestamp}")
                logging.info(f"Updated weather data for {city}: {temperature}°C, {condition}")
                await asyncio.sleep(0.1)  # Small delay between simulated data points

        if len(weather_data) < len(Config.CITIES):
            missing_cities = set(Config.CITIES) - set(weather_data.keys())
            logging.warning(f"Failed to fetch data for cities: {', '.join(missing_cities)}")

    def generate_daily_summary(self):
        date, daily_summary = self.aggregator.get_daily_summary()
        if not daily_summary:
            logging.warning("No data available for daily summary. Skipping visualization.")
            return
        historical_data = self.aggregator.get_historical_data()
        self.visualizer.update(date, daily_summary, historical_data, self.active_alerts)
        logging.info(f"Generated daily summary for {date}")

    async def run(self):
        while self.running:
            await self.update_weather_data()
            self.generate_daily_summary()
            await asyncio.sleep(Config.UPDATE_INTERVAL)

    def start(self):
        asyncio.run(self.run())
        self.visualizer.run()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    app = WeatherMonitoringApp()
    app.start()
