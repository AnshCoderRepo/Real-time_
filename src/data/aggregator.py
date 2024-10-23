import logging
from datetime import datetime, date, timezone, timedelta
from src.config.config import Config
from collections import Counter
import sqlite3
import random  # Add this import

class WeatherDataAggregator:
    def __init__(self, db_path='weather_data.db'):
        self.data = {}
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS daily_summary
                     (date TEXT, city TEXT, avg_temp REAL, max_temp REAL, min_temp REAL, dominant_condition TEXT)''')
        conn.commit()
        conn.close()

    def add_weather_data(self, city, timestamp, temperature, condition):
        """
        Add weather data for a city.

        Args:
            city (str): The name of the city.
            timestamp (datetime): The timestamp of the weather data.
            temperature (float): The temperature in Celsius.
            condition (str): The weather condition.

        Raises:
            ValueError: If invalid input is provided.
        """
        if not isinstance(city, str) or not city:
            raise ValueError("City must be a non-empty string")
        if not isinstance(timestamp, datetime):
            raise ValueError("Timestamp must be a datetime object")
        if not isinstance(temperature, (int, float)):
            raise ValueError("Temperature must be a number")
        if not isinstance(condition, str) or not condition:
            raise ValueError("Condition must be a non-empty string")

        if city not in self.data:
            self.data[city] = []
        # Simulate variation in temperature
        min_temp = temperature - random.uniform(0, 5)
        max_temp = temperature + random.uniform(0, 5)
        self.data[city].append((timestamp, min_temp, temperature, max_temp, condition))

    def get_daily_summary(self):
        today = date.today()
        daily_summary = {}
        for city, data_points in self.data.items():
            today_data = [d for d in data_points if d[0].date() == today]
            if today_data:
                min_temps = [temp[1] for temp in today_data]
                avg_temps = [temp[2] for temp in today_data]
                max_temps = [temp[3] for temp in today_data]
                conditions = [cond[4] for cond in today_data]
                avg_temp = sum(avg_temps) / len(avg_temps)
                max_temp = max(max_temps)
                min_temp = min(min_temps)
                dominant_condition = max(set(conditions), key=conditions.count)
                daily_summary[city] = {
                    'temp': avg_temp,
                    'max_temp': max_temp,
                    'min_temp': min_temp,
                    'dominant_condition': dominant_condition
                }
                self._store_daily_summary(today, city, avg_temp, max_temp, min_temp, dominant_condition)
        return today, daily_summary

    def _store_daily_summary(self, date, city, avg_temp, max_temp, min_temp, dominant_condition):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''INSERT OR REPLACE INTO daily_summary
                     (date, city, avg_temp, max_temp, min_temp, dominant_condition)
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (str(date), city, avg_temp, max_temp, min_temp, dominant_condition))
        conn.commit()
        conn.close()
        logging.info(f"Stored daily summary for {city} on {date} in database")

    def get_historical_data(self, days=7):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        end_date = date.today()
        start_date = end_date - timedelta(days=days-1)
        
        c.execute('''SELECT date, city, avg_temp FROM daily_summary
                     WHERE date >= ? AND date <= ?
                     ORDER BY date, city''', (start_date.isoformat(), end_date.isoformat()))
        data = c.fetchall()
        conn.close()

        # Fill in missing dates with None values
        all_cities = set(city for _, city, _ in data)
        filled_data = []
        for d in (start_date + timedelta(n) for n in range(days)):
            for city in all_cities:
                matching = [temp for date, c, temp in data if date == d.isoformat() and c == city]
                temp = matching[0] if matching else None
                filled_data.append((d.isoformat(), city, temp))

        return filled_data
