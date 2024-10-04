# %%
import pandas as pd

# %%
# Reading .csv files
url_csv = 'https://raw.githubusercontent.com/alura-cursos/pandas/main/superstore_data.csv'

df_csv = pd.read_csv(url_csv)
df_csv

# %%
# Reading .xlsx files
df_xlsx = pd.read_excel('data/emissoes_CO2.xlsx')
df_xlsx

# %%
# Reading .json files
import requests
import json

response = requests.get('https://fruityvice.com/api/fruit/all')
valores = json.loads(response.text)

df_json = pd.DataFrame(valores)
pd.json_normalize(valores)

# %%
# Reading .html files
url_html = 'https://en.wikipedia.org/wiki/AFI%27s_100_Years...100_Movies'

df_html = pd.read_html(url_html)[1]
df_html

# %%
# Reading .xml files
url_xml = 'https://raw.githubusercontent.com/alura-cursos/Pandas/main/imdb_top_1000.xml'

df_xml = pd.read_xml(url_xml)
df_xml

# %%
# Reading SQL database
import sqlalchemy as sa

url_csv_to_sql = 'https://raw.githubusercontent.com/alura-cursos/Pandas/main/clientes_banco.csv'
engine = sa.create_engine('sqlite:///:memory:')

# %%
df_sql = pd.read_csv(url_csv_to_sql)
df_sql.to_sql('clientes_sql', engine, index=False)

# %%
inspector = sa.inspect(engine)
print(inspector.get_table_names())

# %%
query = 'SELECT * FROM clientes_sql WHERE Categoria_de_renda="Empregado"'

employed = pd.read_sql(query, engine)
employed.to_sql('empregados', con=engine, index=False)

pd.read_sql_table('empregados', engine)

# %%
pd.read_sql_table('empregados', engine, columns=['ID_Cliente', 'Grau_escolaridade', 'Rendimento_anual'])

# %%
query = 'SELECT * FROM clientes_sql'
pd.read_sql(query, engine)

# %%
query = sa.text('DELETE FROM clientes_sql WHERE ID_Cliente="5008804"')
with engine.connect() as conn:
    conn.execute(query)
pd.read_sql_table('clientes_sql', engine)