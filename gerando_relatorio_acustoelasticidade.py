import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pandas as pd
import os
import tqdm
from tratando_sinal import Sinal


def gerar_dados(sinal_path):
    sinal = Sinal(sinal_path)
    sinal_original = sinal.sinal
    sinal_modificado = sinal.sinal_modificado
    primeiro_pico = sinal.pico_isolado
    freq, dominio, primeira_freq_caracteristica = sinal.freq, sinal.dominio, sinal.primeira_freq_caracteristica
    tempo_propagacao = sinal.tempo_propagacao

    return sinal_original, sinal_modificado, primeiro_pico, tempo_propagacao, freq, dominio, \
           primeira_freq_caracteristica


def contar_arquivos(path):
    count = 0
    for _, _, files in os.walk(path):
        count += len(files)
    return count


def processar_dados_ensaio_acustoelasticidade(path):
    path_cisalhante = path + r'cisalhante\\'
    pastas_angulos = next(os.walk(path_cisalhante))[1]
    numero_de_arquivos = contar_arquivos(path_cisalhante)
    db = pd.DataFrame()

    for angulos in pastas_angulos:
        path_angulo = path_cisalhante + angulos + r'\\'
        pastas_do_angulo = next(os.walk(path_angulo))[1]
        lista_tempos_angulo_medio = []
        print(angulos)
        for pastas in pastas_do_angulo:
            path_pasta = path_angulo + pastas + r'\\'
            lista_de_arquivos = next(os.walk(path_pasta))[2]
            lista_tempos_angulo = []
            for arquivo in lista_de_arquivos:
                sinal_original, sinal_modificado, primeiro_pico, tempo_propagacao, freq, dominio, \
                    primeira_freq_caracteristica = gerar_dados(path_pasta + arquivo)
                lista_tempos_angulo.append(tempo_propagacao)
            lista_tempos_angulo_medio.append(np.mean(lista_tempos_angulo))
        db[angulos] = pd.Series(lista_tempos_angulo_medio)
    lista_birrefringencia = []
    for i in range(len(db)):
        birrefringencia = 2 * (db.iloc[i, 0] - db.iloc[i, 1]) / (db.iloc[i, 0] + db.iloc[i, 1])
        lista_birrefringencia.append(birrefringencia)
    db['birrefringencia'] = pd.Series(lista_birrefringencia)
    db.to_csv(path + r'birrefringencia.csv', index=False, sep='\t')
    print(db)


path = r'C:\Users\souli\OneDrive\Trabalho\UFPA\Trabalhos\Projeto Cátedra\ultrassom\Rute\S16 CTT\BOLETO\ZTA\\'
processar_dados_ensaio_acustoelasticidade(path)
