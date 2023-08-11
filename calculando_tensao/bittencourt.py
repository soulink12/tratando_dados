import pandas as pd
import numpy as np


def calcular_birrefringencia(tempo_0, tempo_90):
    # tempo_0 = tempo de propagação do sinal paralelo com a laminação
    # tempo_90 = tempo de propagação do sinal perpendicular com a laminação
    return 2 * (tempo_0 - tempo_90) / (tempo_90 + tempo_0)


def calcular_razao_tempos(tempo_0, tempo_90, tempo_compressivo):
    return (2*tempo_0*tempo_90)/(tempo_compressivo*(tempo_0 + tempo_90))


def get_tempo_cisalhante(path, angulo_0, angulo_90):
    # Para L1, angulo_0 = 180 (ou 0), angulo_90 = 90
    # Para L2, angulo_0 = 90, angulo_90 = 180 (ou 0)
    # Para L3, angulo_0 = 0 ou 180, angulo_90 = 90
    arquivo = pd.read_csv(path, sep='\t', encoding='windows-1252', index_col=0)
    tempo_0 = arquivo.loc[angulo_0][0]
    tempo_90 = arquivo.loc[angulo_90][0]
    return tempo_0, tempo_90


def get_tempo_compressivo(path):
    tempo_compressivo_pd = pd.read_csv(path, sep=',', encoding='windows-1252', index_col=0)
    return tempo_compressivo_pd


def mapear_dados_cisalhante_compressivo(path_cisalhante, path_compressivo, numero_de_pastas, angulo_0, angulo_90):
    lista_birrefringencia = []
    lista_razao_velocidades = []
    lista_tempo_0 = []
    lista_tempo_90 = []
    tempo_compressivo_pd = get_tempo_compressivo(path_compressivo)

    for i in range(numero_de_pastas):
        try:
            tempo_0, tempo_90 = get_tempo_cisalhante(path_cisalhante + str(i + 1) + '.txt', angulo_0, angulo_90)
            lista_tempo_0.append(tempo_0)
            lista_tempo_90.append(tempo_90)
            birrefringencia = calcular_birrefringencia(tempo_0, tempo_90)
            tempo_compressivo = tempo_compressivo_pd.loc[i][0]
            lista_razao_velocidades.append(calcular_razao_tempos(tempo_0, tempo_90, tempo_compressivo))
            lista_birrefringencia.append(birrefringencia)
        except:
            print('Erro na pasta ' + str(i + 1))
    return pd.DataFrame({'tempo 0':lista_tempo_0, 'tempo 90':lista_tempo_90, 'tempo compressivo':tempo_compressivo_pd['Tempo de Propagação'].to_list(), 'birrefringencia': lista_birrefringencia, 'razao_velocidades': lista_razao_velocidades})


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


path_cisalhante = r"C:\Users\souli\OneDrive\Trabalho\UFPA\Mestrado\Trabalho\medições\ultrassom-refeito\G2\cisalhante\automatic\L3\\"
path_compressivo = r"C:\Users\souli\OneDrive\Trabalho\UFPA\Mestrado\Trabalho\medições\ultrassom-refeito\G2\compressivo\L3\tempo_propagacao.csv"
numero_de_pastas = 14
dados = mapear_dados_cisalhante_compressivo(path_cisalhante, path_compressivo, numero_de_pastas, 90, 180)
#dados = mapear_dados_cisalhante(path_cisalhante, numero_de_pastas, 90, 0)
dados.to_csv(r'C:\Users\souli\OneDrive\Trabalho\UFPA\Mestrado\Trabalho\medições\ultrassom-refeito\G2\L3-automatic-180-90.csv', sep=',', encoding='windows-1252')
