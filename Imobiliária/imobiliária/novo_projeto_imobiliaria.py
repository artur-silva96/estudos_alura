# %%
# New handling of the original dataset
import pandas as pd
url = 'https://raw.githubusercontent.com/alura-cursos/pandas-conhecendo-a-biblioteca/main/base-de-dados/aluguel.csv'

df = pd.read_csv(url, sep=';')
df

# %%
### Creating new columns
df.fillna(0, inplace=True)
df['Valor_mensal'] = df[['Valor', 'Condominio']].sum(axis='columns')
df['Valor_anual'] = (df['Valor_mensal']*12) + df['IPTU']
df

# %%
df['Descricao'] = df['Tipo'] + ' em ' + df['Bairro'] + ' com ' +\
                  df['Quartos'].astype(str) + ' quartos(s) e ' +\
                  df['Vagas'].astype(str) + ' vagas de garagem.'
df

# %%
df['Possui_suite'] = df['Suites'].apply(lambda x: 'Sim' if x>0 else 'Nao')
df
# %%
### Exporting the data into the 'data' folder
df.to_csv('data/dados_atualizados.csv', index='False', sep=';')