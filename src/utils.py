import datetime
import os
from pprint import pprint
from typing import Dict, List

import pandas as pd


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


data_temp = read_transactions_xlsx("../data/operations.xlsx")

filter_date = filter_by_state(data_temp, "OK")
pprint(get_top_transactions(filter_date))






