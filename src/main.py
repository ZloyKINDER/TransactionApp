import pandas as pd

from src.utils import read_transactions_xlsx
from src.reports import spending_by_category

data = read_transactions_xlsx("../data/operations.xlsx")
df = pd.DataFrame(data)

print(spending_by_category(df, "Супермаркеты", "2021-09-12 16:15:15"))
