import sqlite3
from coletar_todos_dados import coletar_todos_os_dados  # Importa a coleta automática

def ciclo_politico(T, E, C, CS, RI):
    """Calcula o Índice do Ciclo Político (CP)"""
    CP = (T + E + C + CS) / RI if RI != 0 else None
    return CP

def classificar_estagio(cp):
    """Classifica o estágio do governo com base no índice CP"""
    if cp is None:
        return "Dados insuficientes"
    elif cp > 2:
        return "Expansão / Apogeu"
    elif 1 <= cp <= 2:
        return "Estável com riscos"
    elif 0 <= cp < 1:
        return "Declínio iminente"
    else:
        return "Colapso e Transição"

def obter_dados_pais(nome_pais):
    """Consulta o banco e obtém os dados do país"""
    conn = sqlite3.connect("dados_politicos.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT economia, conflitos, controle_social, resiliencia_institucional
        FROM dados_politicos
        WHERE nome = ?
    """, (nome_pais,))
    
    dados = cursor.fetchone()
    conn.close()
    
    if dados:
        return {"T": 1.0, "E": dados[0], "C": dados[1], "CS": dados[2], "RI": dados[3]}
    else:
        return None

def analisar_pais(nome_pais):
    """Executa a fórmula para um país específico"""
    dados = obter_dados_pais(nome_pais)
    
    if not dados:
        print("País não encontrado no banco. Execute a coleta de dados primeiro.")
        return
    
    CP = ciclo_politico(dados["T"], dados["E"], dados["C"], dados["CS"], dados["RI"])
    estagio = classificar_estagio(CP)

    print(f"\n🔹 País: {nome_pais}")
    print(f"📊 Índice do Ciclo Político: {round(CP, 2) if CP else 'Indefinido'}")
    print(f"🏛️ Estágio Atual: {estagio}\n")

if __name__ == "__main__":
    coletar_todos_os_dados()  # Atualiza os dados antes de rodar a análise
    pais = input("Digite o nome do país: ")
    analisar_pais(pais)

