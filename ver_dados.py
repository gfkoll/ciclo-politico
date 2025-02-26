import sqlite3
import pandas as pd

# Conectar ao banco de dados
conn = sqlite3.connect('dados_politicos.db')

# Ler os dados armazenados na tabela
df = pd.read_sql_query("SELECT * FROM paises", conn)

# Fechar a conexão
conn.close()

# Exibir os dados
print(df.head())  # Mostra os primeiros registros
