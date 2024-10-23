import sys
import os
import logging

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

from src.app import WeatherMonitoringApp

if __name__ == "__main__":
    app = WeatherMonitoringApp()
    app.start()
