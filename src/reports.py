from datetime import datetime
from pprint import pprint
from typing import Optional

from src.utils import get_date, filter_by_date

import pandas as pd
from dateutil.relativedelta import relativedelta


def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> pd.DataFrame:
    end_date = datetime.now()
    if date is not None:
        end_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").date()


    start_date = end_date - relativedelta(months=3)

    start_date_formated = datetime.strftime(start_date, "%Y-%m-%d %H:%M:%S")
    end_date_formated = datetime.strftime(end_date, "%Y-%m-%d %H:%M:%S")

    start_date_str = get_date(start_date_formated)
    end_date_str = get_date(end_date_formated)

    transactions_list = transactions.to_dict(orient="records")
    data_filtered = filter_by_date(transactions_list, start_date_str, end_date_str)

    data = pd.DataFrame(data_filtered)

    category_data = data[data["Категория"] == category]
    data = category_data.groupby("Категория")["Сумма платежа"].sum()
    result = pd.DataFrame(data)
    return result

