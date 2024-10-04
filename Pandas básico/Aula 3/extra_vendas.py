# %%
import pandas as pd
import requests
import re

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

def handle_names(df, original_column: str, new_columns: list):
    """Eliminate special characters and separate numeric values from non-numeric values."""
    # [^a-zA-Z0-9À-ÿ]: Matches every non alphanumeric characters and replace with whitespace
    df[original_column] = df[original_column].str.replace(r'[^a-zA-Z0-9À-ÿ]', ' ', regex=True).str.lower()
    # (.+?): Non-greedy match for any characters (captures the name, including spaces). The ? ensures it stops before the digits.
    # \s*: Matches any whitespace between the name and the digits.
    # (\d+)$: Captures one or more digits (assumed to be the ID) at the end of the string ($ ensures it’s at the end). 
    df[new_columns] = df[original_column].str.extract(r'(.+?)\s*(\d+)$')
    # Convert the second column values into numeric (int/float)
    df[new_columns[1]] = df[new_columns[1]].astype(int)
    # Drop the original column
    df.drop(columns=original_column, inplace=True)

    return df

def handle_currency(text):
    # If the value of the cell is 'str', applies the replacements
    if isinstance(text, str):
        # Replaces (,) into (.)
        text = re.sub(r',', '.', text)
        # Deletes every non-numerical characters besisdes (.)
        text = re.sub(r'[^.\d]', '', text)
    return text

# %%
url = 'https://cdn3.gnarususercontent.com.br/2928-transformacao-manipulacao-dados/dados_vendas_clientes.json'

# Fetch data from the URL
df = get_content(url)
df

# %%
# Specify the column to normalize (this can be generalized for any column)
column_to_normalize = 'dados_vendas'
df = normalize_column(df, column_to_normalize)
df
# %%
df = df.explode(['Cliente', 'Valor da compra'], ignore_index=True)
df

# %%
new_columns = ['Nome cliente', 'ID cliente']
df = handle_names(df, 'Cliente', new_columns)
df
# handle_names(df, 'Cliente')

# %%
df['Valor da compra'] = df['Valor da compra'].apply(handle_currency)
df
