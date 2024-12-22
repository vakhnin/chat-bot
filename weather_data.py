import os

import requests


def get_weather_data(api_key: str, city: str) -> dict:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Ошибка при получении данных от API")


if __name__ == '__main__':
    api_weather_key = os.getenv("API_WEATHER_KEY")
    if not api_weather_key:
        raise ValueError("Переменная окружения API_WEATHER_KEY не установлена!")
    city = "Moscow"
    weather_data = get_weather_data(api_weather_key, city)
    print(weather_data)
