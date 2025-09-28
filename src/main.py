import pandas as pd

from src.utils import read_transactions_xlsx

data = read_transactions_xlsx("../data/operations.xlsx")
df = pd.DataFrame(data)
