import pandas as pd

df = pd.read_csv(f'scrappeado/disco_resultados.csv',encoding='utf-8',converters={'tamaño':str}, index_col=0)

print(df[df.marca == 'Corona'])