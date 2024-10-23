import logging
from .app import WeatherMonitoringApp

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    app = WeatherMonitoringApp()
    app.start()
