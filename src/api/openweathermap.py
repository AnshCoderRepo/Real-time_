import aiohttp
import asyncio
import logging
from datetime import datetime
from src.config.config import Config

class OpenWeatherMapAPI:
    """Handles API interactions with OpenWeatherMap."""

    def __init__(self):
        """Initialize the API client with configuration settings."""
        self.base_url = Config.BASE_URL
        self.api_key = Config.API_KEY
        logging.info(f"OpenWeatherMapAPI initialized with base URL: {self.base_url}")
        logging.info(f"API Key (first 5 characters): {self.api_key[:5]}...")

    @staticmethod
    def kelvin_to_celsius(kelvin):
        """Convert temperature from Kelvin to Celsius."""
        return kelvin - 273.15

    @staticmethod
    def kelvin_to_fahrenheit(kelvin):
        return (kelvin - 273.15) * 9/5 + 32

    async def get_weather_data(self, city, max_retries=3):
        """
        Retrieve weather data for a specific city.

        Args:
            city (str): The name of the city.
            max_retries (int): Maximum number of retry attempts.

        Returns:
            dict: Weather data for the city, or None if retrieval failed.
        """
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric'  # Request data in Celsius
        }
        for attempt in range(max_retries):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(self.base_url, params=params) as response:
                        if response.status == 200:
                            data = await response.json()
                            # No need to convert temperature as it's already in Celsius
                            return data
                        elif response.status == 401:
                            logging.error(f"API Key is invalid. Please check your OpenWeatherMap API key.")
                            return None
                        else:
                            logging.error(f"Failed to fetch data for {city}. Status code: {response.status}")
                            return None
            except aiohttp.ClientConnectorError as e:
                logging.warning(f"Connection error for {city} (attempt {attempt + 1}/{max_retries}): {str(e)}")
                if attempt == max_retries - 1:
                    logging.error(f"Failed to fetch data for {city} after {max_retries} attempts")
                    return None
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
            except Exception as e:
                logging.error(f"Unexpected error for {city}: {str(e)}")
                return None

    async def get_weather_for_cities(self, cities):
        tasks = [self.get_weather_data(city) for city in cities]
        results = await asyncio.gather(*tasks)
        return {city: result for city, result in zip(cities, results) if result is not None}

    async def get_weather_data_for_cities(self, cities):
        logging.info(f"Fetching weather data for cities: {cities}")
        tasks = [self.get_weather_data(city) for city in cities]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        valid_results = [r for r in results if r is not None and not isinstance(r, Exception)]
        logging.info(f"Received valid results for {len(valid_results)} out of {len(cities)} cities")
        return valid_results
