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
    freq_fase, fase = sinal.espectro_de_fase(sinal_modificado)

    return sinal_original, sinal_modificado, primeiro_pico, tempo_propagacao, freq, dominio, \
        primeira_freq_caracteristica, freq_fase, fase


def salvar_dados_angulo(tempo_propagacao, primeira_freq_caracteristica, path, nome_arquivo, angulo):
    with open(path + str(nome_arquivo) + '.txt', 'w') as arquivo:
        arquivo.write('Ângulo\t' + 'Tempo de Propagação\t' + 'Frequência Característica\n')
        for i in range(len(tempo_propagacao)):
            arquivo.write(
                str(i * angulo) + '\t' + str(tempo_propagacao[i]) + '\t' + str(primeira_freq_caracteristica[i]) + '\n')
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

    path_cisalhante = path
    pastas = sorted(next(os.walk(path_cisalhante))[1], key=int)
    #pastas = next(os.walk(path_cisalhante))[1]
    numero_de_arquivos = contar_arquivos(path_cisalhante)

    with tqdm.tqdm(total=numero_de_arquivos) as pbar:
        for i in pastas:
            tempos_propagacao_medio_lista = []
            primeiras_freqs_caracteristicas_media_lista = []
            pastas_da_pasta = sorted(next(os.walk(path_cisalhante + i))[1], key=int)
            dsFreqAngulo = pd.DataFrame()
            dsPhaseAngulo = pd.DataFrame()
            for angulo in pastas_da_pasta:
                arquivos_da_pasta = next(os.walk(path_cisalhante + i + r"\\" + angulo))[2]
                tempos_propagacao_lista = []
                primeira_freq_caracteristica_lista = []
                if not len(arquivos_da_pasta) == 0:
                    for arquivo in arquivos_da_pasta:
                        sinal_original, sinal_modificado, primeiro_pico, tempo_propagacao, freq, dominio, \
                            primeira_freq_caracteristica, freq_fase, fase = gerar_dados(
                            path_cisalhante + i + r"\\" + angulo + r"\\" + arquivo)
                        tempos_propagacao_lista.append(tempo_propagacao)
                        primeira_freq_caracteristica_lista.append(primeira_freq_caracteristica)
                        pbar.update(1)
                dsPhaseAngulo['freq'] = freq_fase[0:1600]
                dsFreqAngulo['freq'] = freq[0:1600]
                dsPhaseAngulo[str((int(angulo) - 1) * 11.25)] = fase[0:1600]
                dsFreqAngulo[str((int(angulo) - 1) * 11.25)] = dominio[0:1600]
                tempos_propagacao_medio_lista.append(np.mean(tempos_propagacao_lista))
                primeiras_freqs_caracteristicas_media_lista.append(np.mean(primeira_freq_caracteristica_lista))
            if not np.isnan(tempos_propagacao_medio_lista[0]):
                dsFreq = dsFreqAngulo.drop(columns=['freq'])
                VoltMaxList = dsFreq.max()
                VoltMax = VoltMaxList.max()
                VoltRelation = VoltMaxList / VoltMax
                for j in range(len(VoltRelation)):
                    dsFreqAngulo.iloc[:, j + 1] = dsFreqAngulo.iloc[:, j + 1] / VoltRelation[j]
                dsPhaseAngulo.to_csv(path_cisalhante + i + r'_phase.csv', sep=',', encoding='windows-1252')
                dsFreqAngulo.to_csv(path_cisalhante + i + r'_freq.csv', sep=',', encoding='windows-1252')
                salvar_dados_angulo(tempos_propagacao_medio_lista, primeiras_freqs_caracteristicas_media_lista,
                                    path_cisalhante, i, 11.25)
                print('\n' + 'Dados da pasta ' + str(i) + ' salvos com sucesso!')
    # criar_graficos_cisalhante(path_cisalhante)


def plot_signal(sinal_original):
    tempo = np.arange(0, len(sinal_original), 1) * 0.0000000004
    font = {'family': 'normal',
            'size': 22}
    matplotlib.rc('font', **font)
    plt.figure(figsize=(19, 10))
    plt.plot(tempo, sinal_original, linewidth=0.6, color='black')
    plt.ylim(-0.4, 0.4)
    plt.xlim(-0.0000000004 * 10000, 0.0000000004 * len(sinal_original) / 2 + 0.0000000004 * 10000)
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    plt.ylabel('Amplitude')
    plt.xlabel('Tempo')
    plt.savefig('teste.svg', bbox_inches='tight', format='svg')
    plt.show()


def criar_graficos_cisalhante(path):
    pastas = next(os.walk(path))[1]
    n_pastas = len(pastas)
    for i in range(n_pastas):
        fig = plt.figure(figsize=(16, 10))
        dados = pd.read_csv(path + str(i + 1) + '.txt', sep='\t', encoding='windows-1252')
        plt.plot(dados['Ângulo'], dados['Tempo de Propagação'], label=pastas[i])
        plt.legend()
        plt.show()


def processar_dados_compressivo(path):
    # Processando os arquivos individuais de cada pasta e salvando os dados em um arquivo txt.
    # O arquivo txt será usado para gerar o gráfico
    # Funciona apenas para a pasta transversal

    path_compressivo = path
    pastas = sorted(next(os.walk(path_compressivo))[1], key=int)
    #pastas = next(os.walk(path_compressivo))[1]
    numero_de_arquivos = contar_arquivos(path_compressivo)

    with tqdm.tqdm(total=numero_de_arquivos) as pbar:
        for i in pastas:
            tempos_propagacao_medio_lista = []
            primeiras_freqs_caracteristicas_media_lista = []
            arquivos_da_pasta = next(os.walk(path_compressivo + i))[2]
            tempos_propagacao_lista = []
            primeira_freq_caracteristica_lista = []
            dsFreq = pd.DataFrame()
            for arquivo in arquivos_da_pasta:
                sinal_original, sinal_modificado, primeiro_pico, tempo_propagacao, freq, dominio, \
                    primeira_freq_caracteristica, freq_fase, fase = gerar_dados(path_compressivo + i + r"\\" + arquivo)
                tempos_propagacao_lista.append(tempo_propagacao)
                primeira_freq_caracteristica_lista.append(primeira_freq_caracteristica)
                pbar.update(1)
            dsFreq['freq'] = freq[0:1600]
            tempos_propagacao_medio_lista.append(np.mean(tempos_propagacao_lista))
            primeiras_freqs_caracteristicas_media_lista.append(np.mean(primeira_freq_caracteristica_lista))
            dsFreq.to_csv(path_compressivo + i + r'_freq.csv', sep=',', encoding='windows-1252')
            salvar_dados_angulo(tempos_propagacao_medio_lista, primeiras_freqs_caracteristicas_media_lista,
                                path_compressivo, i, 11.25)
            print('\n' + 'Dados da pasta ' + str(i) + ' salvos com sucesso!')


path = r'C:\Users\souli\OneDrive\Trabalho\UFPA\Mestrado\Trabalho\medições\ultrassom\chapa g1\cisalhante\L1\\'

processar_dados_cisalhante(path)
#processar_dados_compressivo(path)

# Gerando o gráfico a partir dos arquivos txt gerados anteriormente
