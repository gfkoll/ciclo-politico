import requests
import pandas as pd
import sqlite3

# URL da API do Banco Mundial (PIB per capita)
url = "http://api.worldbank.org/v2/country/all/indicator/NY.GDP.PCAP.CD?format=json&date=2023"

# Fazer a requisição
response = requests.get(url)
data = response.json()

# Processar os dados
registros = []
for entry in data[1]:  
    if entry['value'] is not None:
        registros.append({
            "País": entry["country"]["value"],
            "Ano": entry["date"],
            "PIB per capita": entry["value"]
        })

df = pd.DataFrame(registros)

# Conectar ao banco de dados SQLite e salvar os dados
conn = sqlite3.connect('dados_politicos.db')
cursor = conn.cursor()

# Criar tabela
cursor.execute('''
CREATE TABLE IF NOT EXISTS paises (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    ano INTEGER,
    pib_per_capita REAL
)
''')

# Inserir os dados no banco
for _, row in df.iterrows():
    cursor.execute("INSERT INTO paises (nome, ano, pib_per_capita) VALUES (?, ?, ?)",
                   (row["País"], row["Ano"], row["PIB per capita"]))

# Salvar e fechar
conn.commit()
conn.close()

print("Dados coletados e armazenados com sucesso!")
