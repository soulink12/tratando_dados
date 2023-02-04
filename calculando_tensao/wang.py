import numpy as np
import pandas as pd
import sys

sys.path.insert(1, r'C:\Users\souli\OneDrive\Trabalho\UFPA\Mestrado\Trabalho\processando_resultados\py')

#import gerando_relatorio as gr
#from tratando_sinal import Sinal

#TODO: Organizar os dados Força x Frequência
def calcular_diferenca_fase(fasedb0, fasedb90):
    fasedb0 = fasedb0.set_index('freq', inplace=False)
    fasedb90 = fasedb90.set_index('freq', inplace=False)
    freqs_a_serem_usadas = [4.25e6, 4.5e6, 4.75e6, 5.0e6, 5.25e6, 5.5e6, 5.75e6]
    diferencas_de_fase = pd.DataFrame()

    for freq in freqs_a_serem_usadas:
        fase_frequencia0= fasedb0.loc[freq].to_list()[1:]
        fase_frequencia90 = fasedb90.loc[freq].to_list()[1:]
        diferenca = []
        for i, j in zip(fase_frequencia90, fase_frequencia0):
            diferenca.append(i - j)
        diferencas_de_fase[freq] = diferenca
    return diferencas_de_fase

def calcular_diferenca_fase_angulo(pathFasedb):
    diferencas_de_fase = pd.DataFrame()
    fasedb = pd.read_csv(pathFasedb, sep=',', encoding='windows-1252')
    fasedb = fasedb.set_index('freq', inplace=False)
    freqs_a_serem_usadas = [4.25e6, 4.5e6, 4.75e6, 5.0e6, 5.25e6, 5.5e6, 5.75e6]
    numero_de_angulos = int(np.ceil(17 / 2))
    angulos_a_serem_usados = []

    for i in range(numero_de_angulos):
        angulos_a_serem_usados.append(i*11.25)

    for angulo in angulos_a_serem_usados:

        diferencas_de_fase[angulo] = fasedb[str(angulo + 90)] - fasedb[str(angulo)]
    diferencas_de_fase_frequencia = pd.DataFrame()
    diferencas_de_fase_frequencia['angulos'] = angulos_a_serem_usados
    diferencas_de_fase_frequencia.set_index('angulos', inplace=True)
    for freq in freqs_a_serem_usadas:
        diferencas_de_fase_frequencia[freq] = diferencas_de_fase.loc[freq].to_list()

    return diferencas_de_fase_frequencia

def calcular_dtm_com_phase_path(pathDifFasedb, angulos_a_serem_usados):
    diferenca_de_fase_frequencia = pd.read_csv(pathDifFasedb, sep=',', encoding='windows-1252', index_col=0)
    theta1 = angulos_a_serem_usados[0]
    theta2 = angulos_a_serem_usados[1]
    dPhi1 = diferenca_de_fase_frequencia.loc[theta1]
    dPhi2 = diferenca_de_fase_frequencia.loc[theta2]
    dtmDF = pd.DataFrame()
    phi = 0
    dtmDF['angulos'] = [theta1, theta2]
    for i in range(len(dPhi1)):
        for freq in diferenca_de_fase_frequencia.columns[1:]:
            dTm1, dTm2, phi = dTm_para_dois_angulos(dPhi1[i], dPhi2[i], theta1, theta2, float(freq))
            dtmDF[freq] = [dTm1, dTm2]
    dtmDF['phi'] = [phi, phi]
    return dtmDF

def calcular_phi(dPhi1, dPhi2, theta1, theta2):
    phi = 1/2 * np.arctan((np.tan(dPhi1/2)*np.cos(2*theta2) - np.tan(dPhi2/2)*np.cos(2*theta1)) / (np.tan(dPhi2/2)*np.sin(2*theta1) - np.tan(dPhi1/2)*np.sin(2*theta2)))
    return phi

def dTm_para_dois_angulos(dPhi1, dPhi2, theta1, theta2, freq):
    theta1 = np.deg2rad(theta1)
    theta2 = np.deg2rad(theta2)
    phi = calcular_phi(dPhi1, dPhi2, theta1, theta2)
    dTm1 = 1/(np.pi * freq) * np.arctan(np.tan(dPhi1/2) / np.cos(2*(theta1 - phi)))
    dTm2 = 1/(np.pi * freq) * np.arctan(np.tan(dPhi2/2) / np.cos(2*(theta2 - phi)))
    phi = np.rad2deg(phi)
    return dTm1, dTm2, phi

def calcular_dTm(dPhi, theta, freq):
    theta = np.deg2rad(theta)
    dTm = 1/(np.pi * freq) * np.arctan(np.tan(dPhi/2) / np.cos(2*theta))
    return dTm

def tratar_constante_parte_cisalhante():
    fasedb0 = pd.read_csv(
        r"C:\Users\souli\OneDrive\Trabalho\UFPA\Mestrado\Trabalho\medições\ultrassom\acustoelasticidade\1\cisalhante\0_phase.csv")
    fasedb90 = pd.read_csv(
        r"C:\Users\souli\OneDrive\Trabalho\UFPA\Mestrado\Trabalho\medições\ultrassom\acustoelasticidade\1\cisalhante\90_phase.csv")
    diferencas_de_fase_frequencia = calcular_diferenca_fase(fasedb0, fasedb90)
    dTm_por_diferencas_de_fase_frequencia = pd.DataFrame()
    for frequencia in diferencas_de_fase_frequencia:
        diferencas_de_fase = diferencas_de_fase_frequencia[frequencia]
        dTm_por_diferencas_de_fase = []
        for diferenca in diferencas_de_fase:
            dTm = calcular_dTm(diferenca, 0, frequencia)
            dTm_por_diferencas_de_fase.append(dTm)
        dTm_por_diferencas_de_fase_frequencia[frequencia] = dTm_por_diferencas_de_fase
    dTm_por_diferencas_de_fase_frequencia.to_csv(
        r'C:\Users\souli\OneDrive\Trabalho\UFPA\Mestrado\Trabalho\medições\ultrassom\acustoelasticidade\1\dTm.csv')

def criar_difenca_fase(path, numero_de_pastas):
    for i in range(numero_de_pastas + 1):
        path_phase = path + str(i) + r'_phase.csv'
        try:
            diferenca_de_fase_frequencia = calcular_diferenca_fase_angulo(path_phase)
            diferenca_de_fase_frequencia.to_csv(path + str(i) + r'_dif_phase.csv')
        except:
            pass

def criar_dTm(path, numero_de_pastas, angulos):
    for i in range(numero_de_pastas + 1):
        path_phase = path + str(i) + r'_dif_phase.csv'
        try:
            dTmFrequencia = calcular_dtm_com_phase_path(path_phase, angulos)
            dTmFrequencia.to_csv(path + str(i) + r'_dTm.csv')
        except:
            pass



#calcular_diferenca_fase_angulo(r'C:\Users\souli\OneDrive\Trabalho\UFPA\Mestrado\Trabalho\medições\ultrassom\chapa g1\cisalhante\L1\1_phase.csv')

#calcular_dtm_com_phase_path(r'C:\Users\souli\OneDrive\Trabalho\UFPA\Mestrado\Trabalho\medições\ultrassom\chapa g1\cisalhante\L1\1_dif_phase.csv', [33.75, 56.25])

#criar_dTm(path, numero_de_pastas, [33.75, 56.25])

def calculando_constante(A, B, C, D, E):
    # A, B e C são ao parâmetros do plano
    # D (angular) e E (linear) são os parâmetros da reta
    d4 = A
    d2 = B
    d5 = C
    d1 = D + d4
    d3 = E + d5
    print(d1, d2, d3, d4, d5)
    return [d1, d2, d3, d4, d5]

def s11s22(constantes, dTm, phi):
    d1, d2, d3, d4, d5 = constantes
    phi = np.deg2rad(phi)
    s11s22 = (d1 - d4) * dTm * np.cos(2 * phi) + (d3 - d5)
    return s11s22

def s11(constantes, dTm, t,  phi):
    d1, d2, d3, d4, d5 = constantes
    phi = np.deg2rad(phi)
    s11 = d1 * dTm * np.cos(2 * phi) + d2 * 1/(t**2) + d3
    return s11

def s22(constantes, dTm, t,  phi):
    d1, d2, d3, d4, d5 = constantes
    phi = np.deg2rad(phi)
    s22 = d4 * dTm * np.cos(2 * phi) + d2 * 1/(t**2) + d5
    return s22

def s12(constantes, dTm,  phi):
    d1, d2, d3, d4, d5 = constantes
    phi = np.deg2rad(phi)
    s12 = (d1 - d4) / 2 * dTm * np.sin(2 * phi)
    return s12


numero_de_pastas = 14
path_cisalhante = r'C:\Users\souli\OneDrive\Trabalho\UFPA\Mestrado\Trabalho\medições\ultrassom\chapa g1\cisalhante\L1\\'
path_tempo_propagacao_compressivo = r'C:\Users\souli\OneDrive\Trabalho\UFPA\Mestrado\Trabalho\medições\ultrassom\chapa g1\compressivo\L1\tempo_propagacao.csv'

tempos_propagacao = pd.read_csv(path_tempo_propagacao_compressivo, index_col=0, sep=',', encoding='windows-1252')
A = 2.13598
B = 1
C = -2.11664E11
D = -5.12858E-17
E = 3.0414E-8
constantes = calculando_constante(A, B, C, D, E)



for i in range(numero_de_pastas + 1):
    path_dtm = path_cisalhante + str(i) + r'_dtm.csv'
    try:
        dtm_freq = pd.read_csv(path_dtm, index_col=0, sep=',', encoding='windows-1252')
        dtm = dtm_freq[str(5000000.0)][0]
        phi = dtm_freq['phi'][0]
        tempo_propagacao = tempos_propagacao.iloc[i-1][0]
        S11S22 = s11s22(constantes, dtm, phi)
        S11 = s11(constantes, dtm, tempo_propagacao, phi)
        S22 = s22(constantes, dtm, tempo_propagacao, phi)
        S12 = s12(constantes, dtm, phi)
        #print(S11S22, S11, S22, S12)
        #diferenca_de_fase_frequencia.to_csv(path_cisalhante + str(i) + r'_dif_phase.csv')
    except Exception as e:
        pass










