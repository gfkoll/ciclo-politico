import requests
import sqlite3
import concurrent.futures

# APIs de diferentes indicadores
APIS = {
    "economia": "https://api.worldbank.org/v2/country/all/indicator/NY.GDP.MKTP.CD?format=json",
    "conflitos": "https://api.acleddata.com/acled/read?key=YOUR_API_KEY&format=json",
    "controle_social": "https://api.freedomhouse.org/api/v1/data/countries",
    "resiliencia_institucional": "https://api.v-dem.net/data/latest?format=json"
}

# Função para buscar dados de uma API
def buscar_dados(api_nome, url):
    print(f"Coletando dados de {api_nome}...")
    response = requests.get(url)
    if response.status_code == 200:
        return api_nome, response.json()
    else:
        print(f"Erro ao acessar {api_nome}: {response.status_code}")
        return api_nome, None

# Criando Banco de Dados SQLite
def criar_banco():
    conn = sqlite3.connect("dados_politicos.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dados_politicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            economia REAL,
            conflitos REAL,
            controle_social REAL,
            resiliencia_institucional REAL
        )
    """)
    conn.commit()
    conn.close()

# Processar e inserir dados no banco
def inserir_dados(dados_coletados):
    conn = sqlite3.connect("dados_politicos.db")
    cursor = conn.cursor()

    for nome_pais in dados_coletados["economia"].keys():
        economia = dados_coletados["economia"].get(nome_pais, None)
        conflitos = dados_coletados["conflitos"].get(nome_pais, None)
        controle_social = dados_coletados["controle_social"].get(nome_pais, None)
        resiliencia = dados_coletados["resiliencia_institucional"].get(nome_pais, None)

        cursor.execute("""
            INSERT INTO dados_politicos (nome, economia, conflitos, controle_social, resiliencia_institucional)
            VALUES (?, ?, ?, ?, ?)
        """, (nome_pais, economia, conflitos, controle_social, resiliencia))

    conn.commit()
    conn.close()

# Função principal para coletar dados simultaneamente
def coletar_todos_os_dados():
    criar_banco()
    dados_coletados = {key: {} for key in APIS.keys()}

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futuros = {executor.submit(buscar_dados, key, url): key for key, url in APIS.items()}
        
        for futuro in concurrent.futures.as_completed(futuros):
            api_nome, dados = futuro.result()
            if dados:
                for item in dados:
                    nome_pais = item.get("country", {}).get("value", "Desconhecido")
                    valor = item.get("value", None)
                    dados_coletados[api_nome][nome_pais] = valor
    
    inserir_dados(dados_coletados)
    print("Coleta e armazenamento concluídos!")

# Executando a função
if __name__ == "__main__":
    coletar_todos_os_dados()
