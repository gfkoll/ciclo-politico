import sqlite3

def ciclo_politico(T, E, C, CS, RI):
    """
    Calcula o Índice do Ciclo Político (CP)
    T  = Tecnologia (Índice Global de Inovação / Número de Patentes)
    E  = Economia (PIB)
    C  = Conflitos (Eventos de guerra, crises políticas)
    CS = Controle Social (Liberdade de imprensa, democracia)
    RI = Resiliência Institucional (Capacidade do governo de resistir a crises)
    """
    if RI == 0:
        return None  # Evita divisão por zero

    CP = (T + E + C + CS) / RI
    return round(CP, 2)  # Retorna o índice arredondado

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

def calcular_cp_para_paises():
    """Calcula o Índice do Ciclo Político para cada país armazenado no banco"""
    conn = sqlite3.connect("dados_politicos.db")
    cursor = conn.cursor()
    
    # Buscar todos os países com seus indicadores
    cursor.execute("SELECT nome, tecnologia, economia, conflitos, controle_social, resiliencia_institucional FROM dados_politicos")
    paises = cursor.fetchall()
    
    resultados = []
    
    for pais in paises:
        nome, T, E, C, CS, RI = pais
        CP = ciclo_politico(T, E, C, CS, RI)
        estagio = classificar_estagio(CP)

        resultados.append({
            "País": nome,
            "Índice CP": CP,
            "Estágio": estagio
        })

        print(f"{nome}: Índice CP = {CP}, Estágio = {estagio}")

    conn.close()
    return resultados  # Retorna os dados para possível uso em visualizações

if __name__ == "__main__":
    calcular_cp_para_paises()
