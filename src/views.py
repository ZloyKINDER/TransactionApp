from datetime import datetime
from pprint import pprint

from src.utils import get_greeting, read_transactions_xlsx, get_date, filter_by_date, get_top_transactions, \
    get_card_infos, filter_by_state, load_json_data, get_current_exchange_rate, get_stock


def main_page(date_string: str) -> dict:
    date_end_of_month = get_date(date_string)

    date_pars = datetime.strptime(date_end_of_month, "%d.%m.%Y")
    start_of_month_pars = datetime(date_pars.year, date_pars.month, 1)
    start_of_month_str = datetime.strftime(start_of_month_pars, "%Y-%m-%d %H:%M:%S")
    date_start_of_month = get_date(start_of_month_str)

    result = {}
    result.update(greeting = get_greeting())

    transaction = read_transactions_xlsx('../data/operations.xlsx')

    filtered_transactions = filter_by_date(transaction, date_start_of_month, date_end_of_month)
    filtered_transactions = filter_by_state(filtered_transactions)

    result.update(cards = get_card_infos(filtered_transactions))
    result.update(top_transactions = get_top_transactions(filtered_transactions))

    user_settings = load_json_data('../user_settings.json')
    user_currencies = user_settings.get("user_currencies")
    user_stocks = user_settings.get("user_stocks")

    result.update(currency_rates=get_current_exchange_rate(user_currencies))

    result.update(stock_prices=get_stock(user_stocks))


    return result

pprint(main_page("2021-12-31 16:44:00"))
