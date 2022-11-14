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
    primeiro_pico = sinal.primeiro_pico
    freq, dominio, primeira_freq_caracteristica = sinal.freq, sinal.dominio, sinal.primeira_freq_caracteristica
    tempo_propagacao = sinal.tempo_propagacao

    return sinal_original, sinal_modificado, primeiro_pico, tempo_propagacao, freq, dominio, \
           primeira_freq_caracteristica

def salvar_dados(tempo_propagacao, primeira_freq_caracteristica, path, nome_arquivo):
    with open(path + str(nome_arquivo) + '.txt', 'w') as arquivo:
        arquivo.write('Ângulo\t' + 'Tempo de Propagação\t' + 'Frequência Característica\n')
        for i in range(len(tempo_propagacao)):
            arquivo.write(str(i * 11.25) + '\t' + str(tempo_propagacao[i]) + '\t' + str(primeira_freq_caracteristica[i]) + '\n')
        arquivo.close()

def contar_arquivos(path):
    count = 0
    for _, _, files in os.walk(path):
        count += len(files)
    return count

def processar_dados_cisalhante(path, pastas, numero_de_arquivos):
    # Processando os arquivos individuais de cada pasta e salvando os dados em um arquivo txt.
    # O arquivo txt será usado para gerar o gráfico
    # Funcina apenas para a pasta cisalhante

    with tqdm.tqdm(total=numero_de_arquivos) as pbar:
        for i in pastas:
            tempos_propagacao_medio_lista = []
            primeiras_freqs_caracteristicas_media_lista = []
            pasta_raiz = next(os.walk(path + i))[0]
            pastas_da_pasta = next(os.walk(path + i))[1]
            for j in pastas_da_pasta:
                arquivos_da_pasta = next(os.walk(path + i + r"\\" + j))[2]
                tempos_propagacao_lista = []
                primeira_freq_caracteristica_lista = []
                for z in arquivos_da_pasta:
                    sinal_original, sinal_modificado, primeiro_pico, tempo_propagacao, freq, dominio, \
                    primeira_freq_caracteristica = gerar_dados(path + i + r"\\" + j + r"\\" + z)
                    tempos_propagacao_lista.append(tempo_propagacao)
                    primeira_freq_caracteristica_lista.append(primeira_freq_caracteristica)
                    pbar.update(1)
                tempos_propagacao_medio_lista.append(np.mean(tempos_propagacao_lista))
                primeiras_freqs_caracteristicas_media_lista.append(np.mean(primeira_freq_caracteristica_lista))
            salvar_dados(tempos_propagacao_medio_lista, primeiras_freqs_caracteristicas_media_lista, path, i)
            print('\n' + 'Dados da pasta ' + str(i) + ' salvos com sucesso!')

path = r'referencia\\cisalhante\\'
pastas = next(os.walk(path))[1]
numero_de_arquivos = contar_arquivos(path)

processar_dados_cisalhante(path, pastas, numero_de_arquivos)



# Gerando o gráfico a partir dos arquivos txt gerados anteriormente
n_pastas = len(pastas)

for i in range(n_pastas):
    fig = plt.figure(figsize=(16, 10))
    dados = pd.read_csv(path + str(i+1) + '.txt', sep='\t', encoding='windows-1252')
    plt.plot(dados['Ângulo'], dados['Tempo de Propagação'], label=pastas[i])
    plt.legend()
    plt.show()