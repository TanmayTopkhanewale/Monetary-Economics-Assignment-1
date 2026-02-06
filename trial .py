import pandas as pd
data = pd.read_csv(r'rbi_money_stock.csv')  # Adjust the path as needed
df = next(iter(data.values())) if isinstance(data, dict) else data
print(df.columns.tolist()[:30])
print(df.head(2))
