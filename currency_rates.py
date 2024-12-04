import os

import requests


def get_currency_rates(api_key: str) -> dict:
    url = f"https://openexchangerates.org/api/latest.json?app_id={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Ошибка при получении данных от API")


if __name__ == '__main__':
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("Переменная окружения API_KEY не установлена!")
    rates = get_currency_rates(api_key)
    print(rates)
