# %%
# Importing data
import pandas as pd

url = 'https://raw.githubusercontent.com/alura-cursos/pandas-conhecendo-a-biblioteca/main/base-de-dados/aluguel.csv'

df = pd.DataFrame(pd.read_csv(url, sep = ';'))

def filtro_apartamento(df:pd.DataFrame, expr:str)-> pd.DataFrame:
    '''Returns a filtered DataFrame'''
    filtered_df = df.copy()
    return filtered_df.query(expr)

# %%
# Exploratory data analysis
### Analysing monthly renting costs grouped by types of property
df.groupby('Tipo')[['Valor']].mean().sort_values('Valor')

# %%
### Horizontal bar graph representing the previous command
grafico_valor_tipo = df.groupby('Tipo')[['Valor']].mean().sort_values('Valor')
grafico_valor_tipo.plot(kind='barh')

# %%
### Verifying all unique types
df['Tipo'].unique()

# %%
### Removing the types that won't be useful
imoveis_comerciais = ['Conjunto Comercial/Sala', 'Prédio Inteiro', 'Loja/Salão', 'Galpão/Depósito/Armazém',
                      'Casa Comercial', 'Terreno Padrão', 'Box/Garagem','Loja Shopping/ Ct Comercial',
                      'Chácara', 'Loteamento/Condomínio', 'Sítio', 'Pousada/Chalé', 'Studio', 'Hotel', 'Indústria']

df.query('@imoveis_comerciais not in Tipo', inplace=True)
df.groupby('Tipo')[['Valor']].mean().sort_values('Valor')

# %%
### Same as the previous graph, with updated types
grafico_valor_tipo = df.groupby('Tipo')[['Valor']].mean().sort_values('Valor')
grafico_valor_tipo.plot(kind='barh')

# %%
### Vertical bar graph analysing the discrepancy in values between types
grafico_percentual_tipo = df['Tipo'].value_counts(normalize = True).to_frame(name = 'Percentual').sort_values('Percentual')
grafico_percentual_tipo.plot(kind='bar', xlabel= 'Tipos de imóveis', ylabel= 'Percentual')

# %%
### Removing all types other than 'Apartamento'
df.query('Tipo == "Apartamento"', inplace=True)
df

# %%
### Analysing "Apartamentos" with describe method
df.describe()

# %%
### Counting the number of unique values for "Bairro"
df['Bairro'].nunique()

# %%
### Horizontal bar graph with the 5 highest values
cinco_ultimos = df.groupby('Bairro')[['Valor']].mean().sort_values('Valor').tail()
cinco_ultimos.plot(kind='barh')

# %%
# Data processing
### Addressing NaN/null values
df.isnull().sum()

# %%
df.fillna(0, inplace=True)
df.isnull().sum()

# %%
### Removing unnecessary values
df.query('Valor != 0 & Condominio != 0', inplace=True)
df.drop('Tipo', axis='columns', inplace=True)
df

# %%
### Visualizing a filtered DataFrame
filtro_apartamento(df, 'Valor < 4000 & Area > 80')


# %%
### Exporting the data into the "data" folder
df.to_csv('data/dados_apartamentos.csv', index=False, sep=';')