import os

import requests

currencies = ["USD", "EUR", "GBP"]


def get_currency_rates(api_key: str) -> dict:
    url = f"https://openexchangerates.org/api/latest.json?app_id={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Ошибка при получении данных от API")


def process_currency_data(data: dict) -> float:
    usd_to_rub = data['rates']['RUB']
    return usd_to_rub


def format_currency_data(currency_name: str, rate: float) -> str:
    return f"Курс {currency_name}: {rate:.2f}"


def process_multiple_currencies(data: dict, currencies: list) -> dict:
    rates = {}
    for currency in currencies:
        if currency in data['rates']:
            rates[currency] = data['rates'][currency]
    return rates


if __name__ == '__main__':
    currency_name = "USD/RUB"
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("Переменная окружения API_KEY не установлена!")
    currency_data = get_currency_rates(api_key)
    usd_to_rub = process_currency_data(currency_data)
    formatted_data = format_currency_data(currency_name, usd_to_rub)
    print(formatted_data)
    rates = process_multiple_currencies(currency_data, currencies)
    for currency, rate in rates.items():
        print(f"Курс {currency}: {rate}")
