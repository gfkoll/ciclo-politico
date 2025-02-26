import sqlite3
import pandas as pd

def ciclo_politico(T, E, C, CS, RI):
    """Calcula o Índice do Ciclo Político (CP)"""
    CP = (T + E + C + CS) / RI
    return CP

def classificar_estagio(cp):
    """Classifica o estágio do governo com base no índice CP"""
    if cp > 2:
        return "Expansão / Apogeu"
    elif 1 <= cp <= 2:
        return "Estável com riscos"
    elif 0 <= cp < 1:
        return "Declínio iminente"
    else:
        return "Colapso e Transição"

# Conectar ao banco de dados
conn = sqlite3.connect('dados_politicos.db')
df = pd.read_sql_query("SELECT * FROM paises", conn)
conn.close()

# Criar novas colunas no dataframe
df["Índice CP"] = df.apply(lambda row: ciclo_politico(
    row["pib_per_capita"],  # Tecnologia (proxy)
    row["pib_per_capita"] / 2,  # Economia (exemplo simplificado)
    0.5,  # Conflitos (fictício)
    1.0,  # Controle Social (fictício)
    1.5  # Resiliência Institucional (fictício)
), axis=1)

df["Estágio"] = df["Índice CP"].apply(classificar_estagio)

# Exibir resultados
print(df[["nome", "Índice CP", "Estágio"]].head())

# Salvar no banco de dados
conn = sqlite3.connect('dados_politicos.db')
df.to_sql('analise_politica', conn, if_exists='replace', index=False)
conn.close()
print("Dados de análise política salvos no banco.")
