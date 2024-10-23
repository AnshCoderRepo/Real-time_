import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')
    API_BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'
    UPDATE_INTERVAL = 300  # 5 minutes in seconds
    CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
    TEMPERATURE_UNIT = 'fahrenheit'  # or 'fahrenheit'
    
    # Alerting thresholds
    MAX_TEMPERATURE_THRESHOLD = 35  # in Celsius
    CONSECUTIVE_ALERTS = 2

    # Database configuration (you can modify this based on your database choice)
    DATABASE_URL = 'mongodb+srv://anshk1126:g7NAsQWxj9vpbd8o@cluster0.e2d9k.mongodb.net/'

# Add a print statement to check if the API key is loaded correctly
print(f"API Key: {Config.API_KEY}")