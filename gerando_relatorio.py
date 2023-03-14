import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pandas as pd
import os
import tqdm
from tratando_sinal import Sinal


def gerar_dados_cisalhante(sinal_path):
    sinal = Sinal(sinal_path)
    sinal_original = sinal.sinal_original
    sinal_modificado = sinal.sinal_modificado
    primeiro_pico = sinal.pico_isolado
    amplitude, freq_amplitude, primeira_freq_caracteristica = sinal.amplitude, sinal.freq_amplitude, sinal.primeira_freq_caracteristica
    tempo_propagacao = sinal.tempo_propagacao
    phase, freq_phase = sinal.phase, sinal.freq_phase

    return sinal_original, sinal_modificado, primeiro_pico, tempo_propagacao, amplitude, freq_amplitude, \
        primeira_freq_caracteristica, freq_phase, phase

def gerar_dados_compressivo(sinal_path):
    sinal = Sinal(sinal_path)
    sinal_original = sinal.sinal_original
    sinal_modificado = sinal.sinal_modificado
    primeiro_pico = sinal.pico_isolado
    segundo_pico = sinal.isolar_picos(sinal_modificado, 10000,  1)[0]
    amplitude1, freq_amplitude1, primeira_freq_caracteristica1 = sinal.calcular_frequencia_caracteristica(primeiro_pico)
    amplitude2, freq_amplitude2, primeira_freq_caracteristica2 = sinal.calcular_frequencia_caracteristica(segundo_pico)
    phase1, freq_phase1 = sinal.espectro_de_fase(primeiro_pico)
    phase2, freq_phase2 = sinal.espectro_de_fase(segundo_pico)
    tempo_propagacao = sinal.tempo_propagacao

    return sinal_original, sinal_modificado, primeiro_pico, segundo_pico,  tempo_propagacao, amplitude1,\
        freq_amplitude1, amplitude2, freq_amplitude2, primeira_freq_caracteristica1,\
        primeira_freq_caracteristica2, phase1, freq_phase1, phase2, freq_phase2


def salvar_dados_angulo(tempo_propagacao, primeira_freq_caracteristica, path, nome_arquivo, angulo):
    with open(path + str(nome_arquivo) + '.txt', 'w') as arquivo:
        arquivo.write('Ângulo\t' + 'Tempo de Propagação\t' + 'Frequência Característica\n')
        for i in range(len(tempo_propagacao)):
            arquivo.write(
                str(i * angulo) + '\t' + str(tempo_propagacao[i]) + '\t' + str(primeira_freq_caracteristica[i]) + '\n')
        arquivo.close()


def salvar_tempo(tempo_propagacao, path, nome_arquivo, angulo):
    with open(path + str(nome_arquivo) + '_tempo.txt', 'w') as arquivo:
        arquivo.write('Ângulo\t' + 'Tempo de Propagação\n')
        for i in range(len(tempo_propagacao)):
            arquivo.write(str(i * angulo) + '\t' + str(tempo_propagacao[i]) + '\n')
        arquivo.close()


def contar_arquivos(path):
    count = 0
    for _, _, files in os.walk(path):
        count += len(files)
    return count


def processar_dados_cisalhante(path, diferenca_angulo):
    # Processando os arquivos individuais de cada pasta e salvando os dados em um arquivo txt.
    # O arquivo txt será usado para gerar o gráfico
    # Funcina apenas para a pasta cisalhante

    path_cisalhante = path
    #pastas = sorted(next(os.walk(path_cisalhante))[1], key=int)
    pastas = next(os.walk(path_cisalhante))[1]
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
                faseDF = pd.DataFrame()
                if not len(arquivos_da_pasta) == 0:
                    #isolar dois ecos consecutivos com seus respectivos tempos no índice
                    for arquivo in arquivos_da_pasta:
                        sinal_original, sinal_modificado, primeiro_pico, tempo_propagacao, amplitude, freq_amplitude, \
                            primeira_freq_caracteristica, freq_fase, fase = gerar_dados_cisalhante(
                            path_cisalhante + i + r"\\" + angulo + r"\\" + arquivo)
                        faseDF[arquivo] = fase
                        tempos_propagacao_lista.append(tempo_propagacao)
                        primeira_freq_caracteristica_lista.append(primeira_freq_caracteristica)
                        pbar.update(1)
                dsPhaseAngulo['freq'] = freq_fase[0:401]
                dsFreqAngulo['freq'] = freq_amplitude[0:401]
                dsPhaseAngulo[str((int(angulo)) * diferenca_angulo)] = faseDF.mean(axis=1)[0:401]
                dsFreqAngulo[str((int(angulo)) * diferenca_angulo)] = amplitude[0:401]
                tempos_propagacao_medio_lista.append(np.mean(tempos_propagacao_lista))
                primeiras_freqs_caracteristicas_media_lista.append(np.mean(primeira_freq_caracteristica_lista))
            if not np.isnan(tempos_propagacao_medio_lista[0]):
                dsFreq = dsFreqAngulo.drop(columns=['freq'])
                VoltMaxList = dsFreq.max()
                VoltMax = VoltMaxList.max()
                VoltRelation = VoltMaxList / VoltMax
                for j in range(len(VoltRelation)):
                    dsFreqAngulo.iloc[:, j + 1] = dsFreqAngulo.iloc[:, j + 1] / VoltRelation[j]

                dsDiferencaFase = pd.DataFrame()
                '''
                dsDiferencaFase['freq'] = calcular_diferenca_fase(dsPhaseAngulo, 11.25)['freq']
                for angulo in np.arange(0, 101.25, 11.25):
                    dsDiferencaFase[str(angulo) + ' - ' + str(angulo + 90)] = calcular_diferenca_fase(dsPhaseAngulo, angulo)[str(angulo)]

                dsDiferencaFase.to_csv(path_cisalhante + i + r'_dif_phase.csv', sep=',', encoding='windows-1252')
                '''
                dsPhaseAngulo.to_csv(path_cisalhante + i + r'_phase.csv', sep=',', encoding='windows-1252')
                dsFreqAngulo.to_csv(path_cisalhante + i + r'_freq.csv', sep=',', encoding='windows-1252')

                salvar_dados_angulo(tempos_propagacao_medio_lista, primeiras_freqs_caracteristicas_media_lista,
                                    path_cisalhante, i, diferenca_angulo)
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
        tempos_propagacao_medio_lista = np.array([0])
        for i in pastas:

            primeiras_freqs_caracteristicas_media_lista1 = []
            primeiras_freqs_caracteristicas_media_lista2= []
            arquivos_da_pasta = next(os.walk(path_compressivo + i))[2]
            tempos_propagacao_lista = []
            primeira_freq_caracteristica_lista1 = []
            primeira_freq_caracteristica_lista2 = []
            dsFreq = pd.DataFrame()
            dsPhase = pd.DataFrame()
            dsPhase1 = pd.DataFrame()
            dsPhase2 = pd.DataFrame()
            for arquivo in arquivos_da_pasta:

                sinal_original, sinal_modificado, primeiro_pico, segundo_pico, tempo_propagacao, amplitude1, \
                    freq_amplitude1, amplitude2, freq_amplitude2, primeira_freq_caracteristica1, \
                    primeira_freq_caracteristica2, phase1, freq_phase1, phase2, freq_phase2\
                    = gerar_dados_compressivo(path_compressivo + i + r"\\" + arquivo)
                dsPhase1[arquivo] = phase1
                dsPhase2[arquivo] = phase2
                tempos_propagacao_lista.append(tempo_propagacao)
                primeira_freq_caracteristica_lista1.append(primeira_freq_caracteristica1)
                primeira_freq_caracteristica_lista2.append(primeira_freq_caracteristica2)
                pbar.update(1)

            #tempos_propagacao_medio_lista.append(np.mean(tempos_propagacao_lista))
            tempos_propagacao_medio_lista = np.vstack((tempos_propagacao_medio_lista, np.mean(tempos_propagacao_lista)))
            dsPhase['freq'] = freq_phase1
            dsPhase['phase1'] = dsPhase1.mean(axis=1)
            dsPhase['phase2'] = dsPhase2.mean(axis=1)
            dsFreq['freq'] = freq_amplitude1[0:1600]
            primeiras_freqs_caracteristicas_media_lista1.append(np.mean(primeira_freq_caracteristica_lista1))
            dsFreq.to_csv(path_compressivo + i + r'_freq.csv', sep=',', encoding='windows-1252')
            dsPhase.to_csv(path_compressivo + i + r'_phase.csv', sep=',', encoding='windows-1252')
            #TODO: SALVAR AQUI EM BAIXO COM UM PANDAS
            #salvar_dados_angulo(tempos_propagacao_medio_lista, primeiras_freqs_caracteristicas_media_lista1,
            #                    path_compressivo, i, diferenca_angulo)
            print('\n' + 'Dados da pasta ' + str(i) + ' salvos com sucesso!')
        dsTempoPropagacao = pd.DataFrame(tempos_propagacao_medio_lista[1:], columns=['Tempo de Propagação'])
        dsTempoPropagacao.to_csv(path_compressivo + r'tempo_propagacao.csv', sep=',', encoding='windows-1252')



path = r'C:\Users\souli\OneDrive\Trabalho\UFPA\Mestrado\Trabalho\medições\ultrassom\chapa A3 auto\centro\cisalhante\\'

processar_dados_cisalhante(path, 90)
#processar_dados_compressivo(path)

# Gerando o gráfico a partir dos arquivos txt gerados anteriormente
