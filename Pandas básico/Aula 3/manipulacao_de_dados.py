# %%
import pandas as pd
import re

# %%
def allow_only_hyphen_apostrophe(text):
    # Replace hyphens that are NOT between two alphabetic characters or apostrophes
    text =  re.sub(r'(?<![a-zA-Z0-9])-(?![a-zA-Z0-9])', ' ', text).lower()
    # Replace all other special characters
    text = re.sub(r'[^a-zA-Z0-9\-\']', ' ', text)
    return text

# %%
# Reading data from 'dados_hospedagem.json'
df_hospedagem = pd.read_json('data/dados_hospedagem.json')
df_hospedagem

# %%
# Reading data from 'moveis_disponiveis.json'
df_moveis = pd.read_json('data/moveis_disponiveis.json')
df_moveis

# %%
# Normalizing json
df_hospedagem = pd.json_normalize(df_hospedagem['info_moveis'])
df_hospedagem

# %%
colunas = list(df_hospedagem.columns)
colunas

# %%
df_hospedagem = df_hospedagem.explode(colunas[3:], ignore_index=True)
df_hospedagem.head()

# %%
df_hospedagem.info()

# %%
# Handling numerical columns
colunas_numericas = ['max_hospedes', 'quantidade_banheiros', 'quantidade_quartos', 'quantidade_camas']
df_hospedagem[colunas_numericas] = df_hospedagem[colunas_numericas].astype(int)
df_hospedagem['avaliacao_geral'] = df_hospedagem['avaliacao_geral'].astype(float)
df_hospedagem

# %%
# Handling currency columns
colunas_moedas = ['taxa_deposito', 'taxa_limpeza', 'preco']
df_hospedagem[colunas_moedas] = df_hospedagem[colunas_moedas].map(lambda x: x.replace('$', '')
                                                             .replace(',', '')
                                                             .strip()).astype(float)

df_hospedagem.head()

# %%
# Handling text columns
colunas_texto = ['descricao_local', 'descricao_vizinhanca', 'comodidades']
df_hospedagem[colunas_texto] = df_hospedagem[colunas_texto].map(allow_only_hyphen_apostrophe)
df_hospedagem[colunas_texto]

# %%
# Transforming text columns into tokens
df_hospedagem[colunas_texto] = df_hospedagem[colunas_texto].map(lambda x: x.split())
df_hospedagem[colunas_texto]

# %%
df_moveis.head()

# %%
df_moveis.info()

# %%
# Converting to datetime type
df_moveis['data'] = pd.to_datetime(df_moveis['data'])

# %%
# Formating the date (Year-month)
df_moveis['data'].dt.strftime('%Y-%m')

# %%
# Sum of the 'True' values in column 'vaga_disponivel'
subset = df_moveis.groupby(df_moveis['data'].dt.strftime('%Y-%m'))['vaga_disponivel'].sum()
subset

# %%
df_moveis['preco'].fillna('0', inplace=True)
df_moveis['preco'] = df_moveis['preco'].map(lambda x: x.replace('$', '')
                                                       .replace(',', '')
                                                       .strip()).astype(float)
df_moveis