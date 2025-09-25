import datetime
import os
from pprint import pprint
from typing import Dict, List

import requests
from dotenv import load_dotenv

import pandas as pd


load_dotenv("../.env")

API_KEY_FOR_CURRENT_EXCHANGE_RATE = os.getenv("API_KEY_FOR_CURRENT_EXCHANGE_RATE")
API_KEY_ALPHA_VANTAGE = os.getenv("API_KEY_ALPHA_VANTAGE")



def get_greeting() -> str:
    """
    Возвращает приветсвие в зависимости от текущего времени
    """
    massage = ""

    now_hour = datetime.datetime.now().hour

    if 6 <= now_hour < 12:
        massage = "Доброе утро"
    elif 12 <= now_hour < 18:
        massage = "Добрый день"
    elif 18 <= now_hour < 24:
        massage = "Добрый вечер"

    return massage

def read_transactions_xlsx(file_path: str) -> list[dict]:
    """
    Функция для считывания финансовых операций из Excel
    """
    xlsx_data = pd.read_excel(file_path)
    return xlsx_data.to_dict(orient="records")


def get_last_four(input_string:str) -> str:
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


def get_top_transactions(transactions: list[dict]) -> list[dict]:
    """
    Выводит топ топ-5 транзакций по сумме платежа.
    """
    data = sorted(transactions, key=lambda x: abs(x['Сумма платежа']), reverse=True)[:5]
    result = []
    for i, transaction  in enumerate(data, 1):
        transaction_info = dict(
            date=transaction['Дата платежа'],
            amount= transaction['Сумма платежа'],
            category=transaction['Категория'],
            description=transaction['Описание'],
        )
        result.append(transaction_info)
    return result


def get_current_exchange_rate(currency_code: str) -> float:
    """
    Функция возврата текущего курса
    """

    url = "https://api.apilayer.com/exchangerates_data/latest"

    headers = {"apikey": API_KEY_FOR_CURRENT_EXCHANGE_RATE}
    params = {"symbols": "RUB", "base": currency_code}

    response = requests.get(url, headers=headers, params=params)

    response_to_float = float(response.json()["rates"]["RUB"])
    return round(response_to_float, 2)


def get_stock(stock:str) -> float:
    """
     Функция возврата текущего курса
     """
    url = "https://www.alphavantage.co/query"

    params = {"function": "GLOBAL_QUOTE", "symbol": stock, "apikey": API_KEY_ALPHA_VANTAGE}
    response = requests.get(url,params=params)

    response_to_float = float(response.json()["Global Quote"]["05. price"])
    return round(response_to_float, 2)







