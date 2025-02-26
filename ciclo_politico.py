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
    """Função principal interativa para executar o código."""
    historico = []
    
    while True:
        nome = input("Nome da civilização/estado: ")
        T = float(input("Tecnologia: "))
        E = float(input("Economia: "))
        C = float(input("Conflitos: "))
        CS = float(input("Controle Social: "))
        RI = float(input("Resiliência Institucional: "))
        
        historico.append({"Nome": nome, "T": T, "E": E, "C": C, "CS": CS, "RI": RI})
        
        continuar = input("Deseja adicionar outra civilização? (s/n): ").strip().lower()
        if continuar != "s":
            break
    
    df_resultado = processar_dados(historico)
    print(df_resultado)
    
    # Salvar os resultados em um arquivo CSV
    df_resultado.to_csv("resultado_ciclo_politico.csv", index=False)
    print("Resultados salvos em 'resultado_ciclo_politico.csv'.")

if __name__ == "__main__":
    main()

