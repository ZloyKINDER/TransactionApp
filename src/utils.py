import datetime


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




