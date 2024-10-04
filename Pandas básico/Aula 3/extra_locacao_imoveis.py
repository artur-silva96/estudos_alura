# %%
import pandas as pd
import requests

# %%
def get_content(url):
    """Fetches JSON data from a given URL and returns a DataFrame."""
    response = requests.get(url)
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        response.raise_for_status()

def normalize_column(df, column):
    """Generalizes the normalization of a specified column from a DataFrame."""
    if column in df.columns:
        return pd.json_normalize(df[column])
    else:
        raise ValueError(f"Column '{column}' not found in DataFrame")

# %%
url = 'https://cdn3.gnarususercontent.com.br/2928-transformacao-manipulacao-dados/dados_locacao_imoveis.json'

# Fetch data from the URL
df = get_content(url)
df

# %%
# Specify the column to normalize (this can be generalized for any column)
column_to_normalize = 'dados_locacao'
df = normalize_column(df, column_to_normalize)

# %%
df

# %%
df = df.explode(['datas_combinadas_pagamento', 'datas_de_pagamento', 'valor_aluguel'],
                 ignore_index=True)
df

# %%
df['valor_aluguel'] = df['valor_aluguel'].map(lambda x: x.replace('$', '')
                                                         .replace(',', '')
                                                         .replace('reais', '')
                                                         .strip()).astype(float)
df

# %%
## Using Series.str.extract to split the values between numeric and non-numeric
### (.+?): Non-greedy match for any characters (captures the name, including spaces). The ? ensures it stops before the digits.
### \s*: Matches any whitespace between the name and the digits.
### (\d+)$: Captures one or more digits (assumed to be the ID) at the end of the string ($ ensures it’s at the end).
df[['Cliente', 'ID Cliente']] = df['Cliente'].str.extract(r'(.+?)\s*(\d+)$')
df
