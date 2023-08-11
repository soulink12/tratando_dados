import pandas as pd

from calculando_tensao.angulo import encontrar_direcao_polarizacao


def calcular_birrefringencia(tempo_0, tempo_90):
    # tempo_0 = tempo de propagação do sinal paralelo com a laminação
    # tempo_90 = tempo de propagação do sinal perpendicular com a laminação
    return 2 * (tempo_0 - tempo_90) / (tempo_90 + tempo_0)

# def get_angulo_polarizacao(path):


def get_tempo_cisalhante(path, angulo_0, angulo_90):
    # Para L1, angulo_0 = 180 (ou 0), angulo_90 = 90
    # Para L2, angulo_0 = 90, angulo_90 = 180 (ou 0)
    # Para L3, angulo_0 = 0 ou 180, angulo_90 = 90
    arquivo = pd.read_csv(path, sep='\t', encoding='windows-1252', index_col=0)
    tempo_0 = arquivo.loc[angulo_0][0]
    tempo_90 = arquivo.loc[angulo_90][0]
    return tempo_0, tempo_90

#TODO: calcular a birrefringencia para cada pasta usando a função abaixo
# e a de get_angulos. Depois, criar um dataframe com os dados
def mapear_dados_cisalhante(path_cisalhante, numero_de_pastas, angulo_0, angulo_90):
    lista_birrefringencia = []
    lista_tempo_0 = []
    lista_tempo_90 = []

    for i in range(numero_de_pastas):
        try:
            tempo_0, tempo_90 = get_tempo_cisalhante(path_cisalhante + str(i + 1) + '.txt', angulo_0, angulo_90)
            lista_tempo_0.append(tempo_0)
            lista_tempo_90.append(tempo_90)
            birrefringencia = calcular_birrefringencia(tempo_0, tempo_90)
            lista_birrefringencia.append(birrefringencia)
        except Exception as e:
            print('Erro na pasta ' + str(i + 1))
            print(e)
    return pd.DataFrame({'tempo 0':lista_tempo_0, 'tempo 90':lista_tempo_90, 'birrefringencia': lista_birrefringencia})


path_inicial = r"C:\Users\souli\OneDrive\Trabalho\UFPA\Mestrado\Trabalho\medições\ultrassom-refeito\G1\cisalhante\automatic"

n_pastas = 14

dados_corrigidos = encontrar_direcao_polarizacao(path_inicial, n_pastas, 5)

dados_corrigidos.to_csv(r"C:\Users\souli\OneDrive\Trabalho\UFPA\Mestrado\Trabalho\medições\ultrassom-refeito\G1\clark-dados-angulos-g1.csv", sep='\t', encoding='windows-1252')

#path_cisalhante = r"D:\ultrassom\chapa A3 auto\centro\cisalhante\\"
#path_compressivo = r"D:\ultrassom\chapa A3 auto\centro\compressivo\tempo_propagacao.csv"
#numero_de_pastas = 14
#dados = mapear_dados_cisalhante(path_cisalhante, numero_de_pastas, 90, 0)


#get_tempo_cisalhante(r"D:\ultrassom\chapa g1-auto\cisalhante\L1\1.txt", 0, 90)

