from unittest.mock import Mock, patch

from src.views import main_page


@patch("src.views.datetime")
@patch("src.views.get_date")
@patch("src.views.read_transactions_xlsx")
@patch("src.views.filter_by_date")
@patch("src.views.filter_by_state")
@patch("src.views.load_json_data")
@patch("src.views.get_greeting")
@patch("src.views.get_card_infos")
@patch("src.views.get_top_transactions")
@patch("src.views.get_current_exchange_rate")
@patch("src.views.get_stock")
def test_main_page_flow(
    mock_get_stock,
    mock_get_exchange_rate,
    mock_get_top_transactions,
    mock_get_card_infos,
    mock_get_greeting,
    mock_load_json_data,
    mock_filter_by_state,
    mock_filter_by_date,
    mock_read_transactions_xlsx,
    mock_get_date,
    mock_datetime,
):
    """Тест основного потока выполнения функции"""
    # Мокаем datetime
    mock_now = Mock()
    mock_now.hour = 14
    mock_datetime.now.return_value = mock_now

    mock_date_pars = Mock()
    mock_date_pars.year = 2023
    mock_date_pars.month = 1
    mock_datetime.strptime.return_value = mock_date_pars

    mock_start_of_month_pars = Mock()
    mock_datetime.return_value = mock_start_of_month_pars
    mock_datetime.strftime.return_value = "2023-01-01 00:00:00"

    # Мокаем остальные функции
    mock_get_date.side_effect = lambda x: {"2021-01-20 15:25:13": "20.01.2021", "2023-01-01 00:00:00": "01.01.2023"}[x]

    mock_read_transactions_xlsx.return_value = [{"Дата платежа": "01.01.2023", "Сумма": 100, "Статус": "OK"}]

    mock_filter_by_date.return_value = [{"Дата платежа": "01.01.2023", "Сумма": 100, "Статус": "OK"}]

    mock_filter_by_state.return_value = [{"Дата платежа": "01.01.2023", "Сумма": 100, "Статус": "OK"}]

    mock_load_json_data.return_value = {"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "GOOGL"]}

    mock_get_greeting.return_value = "Добрый день"
    mock_get_card_infos.return_value = [{"last_digits": "1234", "total_spent": 1000.0, "cashback": 10.0}]

    mock_get_top_transactions.return_value = [
        {"date": "01.01.2023", "amount": -100.0, "category": "Еда", "description": "Обед"}
    ]

    mock_get_exchange_rate.return_value = [{"currency": "USD", "rate": 91.23}, {"currency": "EUR", "rate": 98.45}]

    mock_get_stock.return_value = [{"stock": "AAPL", "price": 255.46}, {"stock": "GOOGL", "price": 246.54}]

    # Вызываем функцию
    result = main_page("2021-01-20 15:25:13")

    # Проверяем структуру результата
    assert isinstance(result, dict)
    assert "greeting" in result
    assert "cards" in result
    assert "top_transactions" in result
    assert "currency_rates" in result
    assert "stock_prices" in result

    # Проверяем вызовы функций
    mock_get_date.assert_called()
    mock_read_transactions_xlsx.assert_called_once_with("../data/operations.xlsx")
    mock_filter_by_date.assert_called_once()
    mock_filter_by_state.assert_called_once()
    mock_load_json_data.assert_called_once_with("../user_settings.json")
    mock_get_greeting.assert_called_once_with(14)
