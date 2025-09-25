import datetime
import os
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





