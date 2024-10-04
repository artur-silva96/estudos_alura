# %%
import pandas as pd
import numpy as np
import plotly.express as px
import requests
from feature_engine import encoding

# %%
def get_DataFrame(url):
    response = requests.get(url)
    if response.status_code == 200:
        return pd.json_normalize(response.json())
    else:
        response.raise_for_status()

def get_outliers(df, column):
    Q1 = df[column].quantile(.25) # First quartile (25%)
    Q3 = df[column].quantile(.75) # Third quartile (75%)
    IQR = Q3 - Q1 # Interquartile range
    LL = Q1 - 1.5*IQR # Lower limit
    UL = Q3 + 1.5*IQR # Upper limit
    return (df[column] < LL) | (df[column] > UL)


# %%
url = 'https://cdn3.gnarususercontent.com.br/2929-pandas/dataset-telecon.json'

df = get_DataFrame(url)
df

# %%
df.info()

# %%
df['conta.cobranca.Total'].unique()

# %%
# We can see that when 'cliente.tempo_servico' is '0.0', conta.cobranca.Total is a whitespaced string (' ')
idx = df[df['cliente.tempo_servico'] == 0][
    ['cliente.tempo_servico', 'conta.contrato', 'conta.cobranca.mensal', 'conta.cobranca.Total']
].index
idx

# %%
# Understanding that, by the end of the two-year contract, 'cliente.tempo_servico' will be 24 months
df.loc[df['cliente.tempo_servico'] == 0, 'cliente.tempo_servico']  = 24.0

df.loc[df['conta.cobranca.Total'] == ' ', 'conta.cobranca.Total']  = df.loc[df['conta.cobranca.Total'] == ' ', 'conta.cobranca.mensal']*df.loc[df['conta.cobranca.Total'] == ' ', 'cliente.tempo_servico']
df['conta.cobranca.Total'] = df['conta.cobranca.Total'].astype(float)
df.info()

# %%
df.loc[idx][
    ['cliente.tempo_servico', 'conta.contrato', 'conta.cobranca.mensal', 'conta.cobranca.Total']
]
# %%
# Visualizing the unique values and their occurences and check for inconsistency
for col in df.columns:
    print(df[col].value_counts())
    print('-'*15)

# %%
# Checking for empty strings in 'Churn' column
df.query('Churn == ""')

# %%
df = df[df['Churn'] != ''].reset_index(drop=True)
df

# %%
# Checking for duplicates
df.duplicated().sum()

# %%
# Deleting duplicated values
df.drop_duplicates(inplace=True)
# Checking again
df.duplicated().sum()

# %%
# Checking for NaN values
df.isna()

# %%
df.isna().sum()

# %%
df.isna().any(axis=1).sum()

# %%
idx_tempo_servico = df[df['cliente.tempo_servico'].isna()].index
idx_tempo_servico

# %%
df.iloc[idx_tempo_servico][['cliente.tempo_servico', 'conta.cobranca.mensal', 'conta.cobranca.Total']]

# %%
# Since 'conta.cobranca.Total' is 'conta.cobranca.mensal' * 'cliente.tempo_servico', we can fill NaN values
df.fillna(
    {'cliente.tempo_servico': np.ceil(df['conta.cobranca.Total']/df['conta.cobranca.mensal'])},
    inplace=True
)
df.iloc[idx_tempo_servico][['cliente.tempo_servico', 'conta.cobranca.mensal', 'conta.cobranca.Total']]

# %%
# Understanding the remaining NaN values
df.isna().sum()

# %%
df.isna().any(axis=1).sum()

# %%
column_conta = ['conta.contrato', 'conta.faturamente_eletronico', 'conta.metodo_pagamento']

# %%
for col in column_conta:
    print(df[col].value_counts())
    print('-'*30)

# %%
# As we can't figure a way to deal with the missing values effectively, we will delete them
df.dropna(subset=column_conta, ignore_index=True, inplace=True)
df

# %%
df.isna().sum()

# %%
df.describe()

# %%
px.box(df['cliente.tempo_servico'])

# %%
column = 'cliente.tempo_servico'
get_outliers(df, column)

# %%
df[get_outliers(df, column)][column]

# %%
df.loc[get_outliers(df, column), 'cliente.tempo_servico'] = np.ceil(
    df.loc[get_outliers(df, column), 'conta.cobranca.Total'] / df.loc[get_outliers(df, column), 'conta.cobranca.mensal']
)

# %%
px.box(df['cliente.tempo_servico'])

# %%
df[get_outliers(df, column)][['cliente.tempo_servico', 'conta.cobranca.Total', 'conta.cobranca.mensal']]

# %%
df[get_outliers(df,column)]

# %%
df = df[~get_outliers(df, column)].reset_index(drop=True)
df

# %%
px.box(df['cliente.tempo_servico'])

# %%
for col in df.columns:
    print(f'Coluna: {col}')
    print(df[col].unique())
    print('-'*30)

# %%
df.drop(columns='id_cliente', inplace=True)
df

# %%
category_cols = ['Churn', 'cliente.genero', 'cliente.parceiro',
                 'cliente.dependentes', 'telefone.servico_telefone',
                 'conta.faturamente_eletronico']

mapping = {
    'nao': '0',
    'sim': '1',
    'masculino': '0',
    'feminino': '1'
}

category_features = ['telefone.varias_linhas', 'internet.servico_internet',
                     'internet.seguranca_online', 'internet.backup_online',
                     'internet.protecao_dispositivo', 'internet.suporte_tecnico',
                     'internet.tv_streaming', 'internet.filmes_streaming',
                     'conta.contrato', 'conta.metodo_pagamento']

# %%
df[category_cols] = df[category_cols].replace(mapping).astype(int)
df[category_cols]

# %%
# Similar to pd.get_dummies()
onehot = encoding.OneHotEncoder()
onehot.fit(df)
onehot.transform(df)
