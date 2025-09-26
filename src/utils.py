import json
import os
from datetime import datetime

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv("../.env")

API_KEY_FOR_CURRENT_EXCHANGE_RATE = os.getenv("API_KEY_FOR_CURRENT_EXCHANGE_RATE")
API_KEY_ALPHA_VANTAGE = os.getenv("API_KEY_ALPHA_VANTAGE")


def get_greeting() -> str:
    """
    Возвращает приветсвие в зависимости от текущего времени
    """
    message = ""

    now_hour = datetime.now().hour

    if 0 <= now_hour < 6:
        message = "Доброй ночи"
    elif 6 <= now_hour < 12:
        message = "Доброе утро"
    elif 12 <= now_hour < 18:
        message = "Добрый день"
    elif 18 <= now_hour < 24:
        message = "Добрый вечер"

    return message


def read_transactions_xlsx(file_path: str) -> list[dict]:
    """
    Функция для считывания финансовых операций из Excel
    """
    xlsx_data = pd.read_excel(file_path)
    return xlsx_data.to_dict(orient="records")


def get_last_four(input_string: str) -> str:
    """
    Функция для возвращения последний четырёх символов
    """
    if input_string:
        return input_string[-4:]
    return "None"


def get_cashback(total_spent: float) -> float:
    """
    Функция для расчёта кешбека
    """
    return round((total_spent / 100), 2)


def filter_by_state(data: list[dict], state: str = "OK") -> list[dict]:
    """
    Фильтрует список словарей по значению ключа 'state'.
    """
    if not data:
        raise ValueError("Пустой список")

    new_data = list()

    for item in data:
        if item.get("Статус") == state:
            new_data.append(item)

    return new_data


def get_card_infos(transactions: list[dict]) -> list[dict]:
    """
    Возвращает инфомацию о картах
    """
    df = pd.DataFrame(transactions)

    cards = []

    negative_df = df[df["Сумма платежа"] < 0]
    data = negative_df.groupby("Номер карты")["Сумма платежа"].sum()

    for card_number, total_amount in data.items():

        card_number = get_last_four(str(card_number))
        total_spent = abs(round(total_amount, 2))
        cashback = get_cashback(total_spent)
        card_info = dict(last_digits=card_number, total_spent=total_spent, cashback=cashback)
        cards.append(card_info)

    return cards


def get_top_transactions(transactions: list[dict]) -> list[dict]:
    """
    Выводит топ топ-5 транзакций по сумме платежа.
    """
    data = sorted(transactions, key=lambda x: abs(x["Сумма платежа"]), reverse=True)[:5]
    result = []
    for i, transaction in enumerate(data, 1):
        transaction_info = dict(
            date=transaction["Дата платежа"],
            amount=transaction["Сумма платежа"],
            category=transaction["Категория"],
            description=transaction["Описание"],
        )
        result.append(transaction_info)
    return result


def get_current_exchange_rate(currency_codes: list) -> list:
    """
    Функция возврата текущего курса
    """

    url = "https://api.apilayer.com/exchangerates_data/latest"

    headers = {"apikey": API_KEY_FOR_CURRENT_EXCHANGE_RATE}
    result = []
    for code in currency_codes:
        params = {"symbols": "RUB", "base": code}
        response = requests.get(url, headers=headers, params=params)
        response_to_float = float(response.json()["rates"]["RUB"])

        currency_code_info = dict(currency=code, rate=round(response_to_float, 2))
        result.append(currency_code_info)

    return result


def get_stock(stocks: list) -> list:
    """
    Функция возврата текущего курса
    """
    url = "https://www.alphavantage.co/query"

    result = []
    for stock in stocks:
        params = {"function": "GLOBAL_QUOTE", "symbol": stock, "apikey": API_KEY_ALPHA_VANTAGE}
        response = requests.get(url, params=params)
        response_to_float = float(response.json()["Global Quote"]["05. price"])
        stocks_info = dict(stock=stock, price=round(response_to_float, 2))
        result.append(stocks_info)

    return result


def get_date(date: str) -> str:
    """
    Возвращает дату из формата ГГГГ-ММ-ДД в ДД.ММ.ГГГГ
    """

    year = date[:4]
    month = date[5:7]
    day = date[8:10]
    new_date = day + "." + month + "." + year

    try:
        datetime.strptime(new_date, "%d.%m.%Y")
        return new_date
    except ValueError:
        return date


def filter_by_date(data: list[dict], start_date: str, end_date: str) -> list[dict]:
    """
    Фильтрует список словарей в промежутке star_date и  end_date по значению Дата платежа
    """

    start_dt = datetime.strptime(start_date, "%d.%m.%Y")
    end_dt = datetime.strptime(end_date, "%d.%m.%Y")

    filter_date = []
    for item in data:
        date_value = str(item["Дата платежа"]).strip().lower()
        if date_value == "nan" or date_value == "":
            continue

        item_date = datetime.strptime(str(item["Дата платежа"]), "%d.%m.%Y")

        if start_dt <= item_date <= end_dt:
            filter_date.append(item)

    return filter_date


def load_json_data(file_path: str) -> dict:
    """
    Возвращает данные о финансовых транзакция из JSON
    """
    try:
        if not os.path.exists(file_path):
            return {}

        if os.path.getsize(file_path) == 0:
            return {}

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, dict):
            return data
        else:
            return {}

    except (json.JSONDecodeError, FileNotFoundError, PermissionError, OSError):
        return {}
