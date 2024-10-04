# %%
import pandas as pd
import warnings
import re
import plotly.express as px

# %%
# Function to handle all non-numeric values
def clean_population_value(value):
    if isinstance(value, str):  # Ensure the value is a string
        # Remove any parentheses and the content inside them
        value = re.sub(r'\(.*\)', '', value)
        # Remove periods and commas (adapt to your case if commas are used as thousands separator)
        value = value.replace('.', '').replace(',', '')
    return value

# %%
# ANALYSING THE EMISSION OF GASES
### Retrieve the names of all sheets from the specified Excel file.
pd.ExcelFile('data/1-SEEG10_GERAL-BR_UF_2022.10.27-FINAL-SITE.xlsx').sheet_names

# %%
### Ignore all warnings to keep the output clean.
warnings.simplefilter("ignore")
#### Load the specific sheet 'GEE Estados' from the Excel file into a DataFrame.
df_emissao = pd.read_excel('data/1-SEEG10_GERAL-BR_UF_2022.10.27-FINAL-SITE.xlsx', sheet_name='GEE Estados')

# %%
### Display the summary info (data types, non-null counts, etc.) of the DataFrame.
df_emissao.info()

# %%
### Get all unique values from the 'Emissão / Remoção / Bunker' column.
df_emissao['Emissão / Remoção / Bunker'].unique()

# %%
### Create a boolean condition where the 'Emissão / Remoção / Bunker' column is either 'Remoção NCI' or 'Remoção'.
(df_emissao['Emissão / Remoção / Bunker'] == 'Remoção NCI') | (df_emissao['Emissão / Remoção / Bunker'] == 'Remoção')

# %%
### Filter the DataFrame to keep only rows where 'Emissão / Remoção / Bunker' is either 'Remoção NCI' or 'Remoção'.
df_emissao[df_emissao['Emissão / Remoção / Bunker'].isin(['Remoção NCI', 'Remoção'])]

# %%
### Find the maximum value for columns from 1970 onward for rows where 'Emissão / Remoção / Bunker' is 'Remoção NCI' or 'Remoção'.
df_emissao.loc[df_emissao['Emissão / Remoção / Bunker'].isin(['Remoção NCI', 'Remoção']), 1970:].max()

# %%
### Get all unique values from the 'Estado' column where 'Emissão / Remoção / Bunker' is 'Bunker'.
df_emissao.loc[df_emissao['Emissão / Remoção / Bunker'] == 'Bunker', 'Estado'].unique()

# %%
### Filter the DataFrame to keep only rows where 'Emissão / Remoção / Bunker' is 'Emissão'.
df_emissao = df_emissao[df_emissao['Emissão / Remoção / Bunker'] == 'Emissão']
df_emissao

# %%
### Drop the 'Emissão / Remoção / Bunker' column from the DataFrame and modify the DataFrame in place.
df_emissao.drop(columns='Emissão / Remoção / Bunker', inplace=True)
df_emissao

# %%
colunas_info = df_emissao.loc[:, 'Nível 1 - Setor':'Produto'].columns.tolist()
colunas_info

# %%
colunas_emissao = df_emissao.loc[:, 1970:].columns.tolist()
colunas_emissao

# %%
emissoes_por_ano = df_emissao.melt(id_vars=colunas_info,
                           value_vars=colunas_emissao,
                           var_name='Ano',
                           value_name='Emissão')
emissoes_por_ano

# %%
emissoes_por_gas = emissoes_por_ano.groupby('Gás')[['Emissão']].sum().sort_values('Emissão', ascending=False)
emissoes_por_gas

# %%
emissoes_por_ano.groupby('Nível 1 - Setor')[['Emissão']].sum()

# %%
emissoes_por_gas.plot(kind='barh')

print(f'A emissão de CO2 corresponde a {float(emissoes_por_gas['Emissão'][:9].sum() / emissoes_por_gas['Emissão'].sum())*100:.2f}% de toda emissão de gases de efeito estufa no Brasil.')

# %%
gas_por_setor = emissoes_por_ano.groupby(['Gás', 'Nível 1 - Setor'])[['Emissão']].sum()
gas_por_setor

# %%
gas_por_setor.xs(('CO2 (t)', 'Agropecuária'))

# %%
gas_por_setor.loc[('CO2 (t)', 'Agropecuária')]

# %%
gas_por_setor.xs('Agropecuária', level=1)

# %%
setor_critico = gas_por_setor.groupby(level=0).idxmax()[['Emissão']].map(lambda x:x[1])
setor_critico

# %%
emissao_max = gas_por_setor.groupby(level=0).max()
emissao_max

# %%
valores_max = emissao_max.values

# %%
tabela_sumarizada = gas_por_setor.groupby(level=0).idxmax()
tabela_sumarizada.insert(1, 'Quantidade de emissão', valores_max)
tabela_sumarizada

# %%
max_emissao_gas = pd.concat([setor_critico, emissao_max],
                              axis='columns')
max_emissao_gas.columns = ['Setor crítico', 'Emissão máxima']
max_emissao_gas

# %%
setor_por_gas = gas_por_setor.swaplevel(0, 1).groupby(level= 0).idxmax()[['Emissão']].map(lambda x:x[1])
setor_por_gas

# %%
emissao_por_setor = gas_por_setor.swaplevel(0, 1).groupby(level= 0).max()
emissao_por_setor

# %%
emissoes_por_ano.groupby('Ano')[['Emissão']].mean().plot()

# %%
emissoes_por_ano.groupby('Ano')[['Emissão']].mean().idxmax()

# %%
emissoes_por_ano.groupby(['Ano', 'Gás'])[['Emissão']].mean()

# %%
media_emissao_anual = emissoes_por_ano.groupby(['Ano', 'Gás'])[['Emissão']].mean().reset_index()
media_emissao_anual

# %%
media_emissao_anual= media_emissao_anual.pivot_table(index='Ano',
                                                     columns='Gás',
                                                     values='Emissão')
media_emissao_anual

# %%
media_emissao_anual.plot(subplots=True, figsize=(10,40));

# %%
emissao_setores = emissoes_por_ano.pivot_table(index = 'Ano',
                                               columns = 'Nível 1 - Setor',
                                               values = 'Emissão')
emissao_setores

# %%
emissao_setores.plot(subplots=True);

# %%
# ANALYSING THE POPULATION OF THE STATES
df_populacao = pd.read_excel('data/POP2022_Municipios.xls', header=1, skipfooter=34)
df_populacao

# %%
### Verifying all non-numeric values
df_populacao[df_populacao['POPULAÇÃO'].str.contains('\(', na=False)]

# %%
### A more generic way to verify non-numeric values
df_populacao[~df_populacao['POPULAÇÃO'].astype(str).str.isnumeric()]

### Apply the cleaning function to the 'POPULAÇÃO' column
df_populacao['POPULAÇÃO corrigida'] = df_populacao['POPULAÇÃO'].apply(clean_population_value)

### Convert the cleaned column to numeric (integer)
df_populacao['POPULAÇÃO corrigida'] = pd.to_numeric(df_populacao['POPULAÇÃO corrigida'], errors='coerce')

# %%
df_populacao

# %%
populacao_por_estado = df_populacao.groupby('UF')[['POPULAÇÃO corrigida']].sum().reset_index()
populacao_por_estado

# %%
emissao_por_estado = emissoes_por_ano[emissoes_por_ano['Ano'] == 2021].groupby('Estado')[['Emissão']].sum().reset_index()
emissao_por_estado

# %%
emissao_por_estado.rename(columns={'Estado': 'UF'}, inplace=True)
emissao_per_capita = pd.merge(populacao_por_estado, emissao_por_estado, on='UF')
emissao_per_capita['Per capita'] = emissao_per_capita['Emissão']/emissao_per_capita['POPULAÇÃO corrigida']
emissao_per_capita

# %%
emissao_per_capita.sort_values('Per capita', ascending=False)

# %%
emissao_per_capita.plot(x='POPULAÇÃO corrigida',
                        y='Emissão',
                        kind='scatter');

# %%
px.scatter(emissao_per_capita,
           x='POPULAÇÃO corrigida',
           y='Emissão',
           text='UF')

# %%
px.scatter(emissao_per_capita,
           x='POPULAÇÃO corrigida',
           y='Emissão',
           text='UF', size='Per capita')

# %%
px.bar(emissao_per_capita,
       x='UF',
       y='Per capita').update_xaxes(categoryorder='total descending')
