import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import tqdm
from tratando_sinal import Sinal


def gerar_dados(sinal_path):
    sinal = Sinal(sinal_path)
    sinal_original = sinal.sinal
    sinal_modificado = sinal.sinal_modificado
    tempo_propagacao = sinal.tempo_propagacao

    return sinal_original, sinal_modificado, tempo_propagacao


def salvar_dados(tempo_propagacao, primeira_freq_caracteristica, path, nome_arquivo):
    with open(path + str(nome_arquivo) + '.txt', 'w') as arquivo:
        arquivo.write('Ângulo\t' + 'Tempo de Propagação\t' + 'Frequência Característica\n')
        for i in range(len(tempo_propagacao)):
            arquivo.write(str(i * 11.25) + '\t' + str(tempo_propagacao[i]) + '\t' + str(primeira_freq_caracteristica[i]) + '\n')
        arquivo.close()

def salvar_tempo(tempo_propagacao, path, nome_arquivo):
    with open(path + str(nome_arquivo) + '_tempo.txt', 'w') as arquivo:
        arquivo.write('Ângulo\t' + 'Tempo de Propagação\n')
        for i in range(len(tempo_propagacao)):
            arquivo.write(str(i * 11.25) + '\t' + str(tempo_propagacao[i]) + '\n')
        arquivo.close()

def contar_arquivos(path):
    count = 0
    for _, _, files in os.walk(path):
        count += len(files)
    return count


def processar_dados_cisalhante(path):
    # Processando os arquivos individuais de cada pasta e salvando os dados em um arquivo txt.
    # O arquivo txt será usado para gerar o gráfico
    # Funcina apenas para a pasta cisalhante

    path_cisalhante = path + r'cisalhante\\'
    pastas = next(os.walk(path_cisalhante))[1]
    numero_de_arquivos = contar_arquivos(path_cisalhante)

    with tqdm.tqdm(total=numero_de_arquivos) as pbar:
        for i in pastas:
            tempos_propagacao_medio_lista = []
            pasta_raiz = next(os.walk(path_cisalhante + i))[0]
            pastas_da_pasta = next(os.walk(path_cisalhante + i))[1]
            dsFreqAngulo = pd.DataFrame()
            for j in pastas_da_pasta:
                arquivos_da_pasta = next(os.walk(path_cisalhante + i + r"\\" + j))[2]
                tempos_propagacao_lista = []
                primeira_freq_caracteristica_lista = []
                for z in arquivos_da_pasta:
                    sinal_original, sinal_modificado, tempo_propagacao = gerar_dados(path_cisalhante + i + r"\\" + j + r"\\" + z)
                    tempos_propagacao_lista.append(tempo_propagacao)
                    pbar.update(1)
                tempos_propagacao_medio_lista.append(np.mean(tempos_propagacao_lista))
            #dsFreqAngulo.to_csv(path_cisalhante + i + r'_freq.csv', sep=',', encoding='windows-1252')
            salvar_tempo(tempos_propagacao_medio_lista, path_cisalhante, i)
            print('\n' + 'Dados da pasta ' + str(i) + ' salvos com sucesso!')
    #criar_graficos_cisalhante(path_cisalhante)


def processar_dados_compressivo(path):
    # Processando os arquivos individuais de cada pasta e salvando os dados em um arquivo txt.
    # O arquivo txt será usado para gerar o gráfico
    # Funciona apenas para a pasta transversal

    path_compressivo = path + r'compressivo\\'
    pastas = next(os.walk(path_compressivo))[1]
    numero_de_arquivos = contar_arquivos(path_compressivo)

    with tqdm.tqdm(total=numero_de_arquivos) as pbar:
        for i in pastas:
            tempos_propagacao_medio_lista = []
            primeiras_freqs_caracteristicas_media_lista = []
            pasta_raiz = next(os.walk(path_compressivo + i))[0]
            pastas_da_pasta = next(os.walk(path_compressivo + i))[1]

            arquivos_da_pasta = next(os.walk(path_compressivo + i))[2]
            tempos_propagacao_lista = []
            primeira_freq_caracteristica_lista = []
            for z in arquivos_da_pasta:
                sinal_original, sinal_modificado, primeiro_pico, tempo_propagacao, freq, dominio, \
                primeira_freq_caracteristica = gerar_dados(path_compressivo + i + r"\\" + z)
                tempos_propagacao_lista.append(tempo_propagacao)
                primeira_freq_caracteristica_lista.append(primeira_freq_caracteristica)
                pbar.update(1)
            tempos_propagacao_medio_lista.append(np.mean(tempos_propagacao_lista))
            primeiras_freqs_caracteristicas_media_lista.append(np.mean(primeira_freq_caracteristica_lista))
            salvar_dados(tempos_propagacao_medio_lista, primeiras_freqs_caracteristicas_media_lista, path_compressivo, i)
            print('\n' + 'Dados da pasta ' + str(i) + ' salvos com sucesso!')


path = r'D:\\medicoes\\AMOSTRA S12\\boleto\\'

processar_dados_cisalhante(path)
#processar_dados_compressivo(path)

# Gerando o gráfico a partir dos arquivos txt gerados anteriormente

