import numpy as np
import pandas as pd

def ciclo_politico(T, E, C, CS, RI):
    """
    Calcula o Índice do Ciclo Político (CP)
    T  = Tecnologia
    E  = Economia
    C  = Conflitos
    CS = Controle Social
    RI = Resiliência Institucional
    """
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

def processar_dados(historico):
    """Processa os dados históricos e retorna um DataFrame com os resultados."""
    df = pd.DataFrame(historico)
    for index, row in df.iterrows():
        cp = ciclo_politico(row["T"], row["E"], row["C"], row["CS"], row["RI"])
        df.loc[index, "Índice CP"] = round(cp, 2)
        df.loc[index, "Estágio"] = classificar_estagio(cp)
    return df

def main():
    """Função principal para executar o código."""
    historico = [
        {"Nome": "Império Romano", "T": 60, "E": 50, "C": 100, "CS": -10, "RI": 50},
        {"Nome": "Revolução Francesa", "T": 70, "E": -30, "C": 200, "CS": -50, "RI": 20},
        {"Nome": "China Atual", "T": 90, "E": 80, "C": 50, "CS": 30, "RI": 100},
    ]
    
    df_resultado = processar_dados(historico)
    print(df_resultado)

if __name__ == "__main__":
    main()
