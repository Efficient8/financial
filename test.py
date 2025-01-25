import pandas as pd

book = 'workbook.xlsx'

df = pd.read_excel(book)
print(df.head())