import numpy as np
import pandas as pd

def calcular_diferenca_fase(fasedb0, fasedb90):
    fasedb0 = fasedb0.set_index('freq', inplace=False)
    fasedb90 = fasedb90.set_index('freq', inplace=False)
    freqs_a_serem_usadas = [4.25e6, 4.5e6, 4.75e6, 5.0e6, 5.25e6, 5.5e6, 5.75e6]
    diferencas_de_fase = []

    for freq in freqs_a_serem_usadas:
        fase_frequencia0= fasedb0.loc[freq]
        fase_frequencia90 = fasedb90.loc[freq]
        diferenca = fase_frequencia90 - fase_frequencia0
        print(fase_frequencia0)
        diferencas_de_fase.append(diferenca)
    return diferencas_de_fase

def calcular_phi(dPhi1, dPhi2, theta1, theta2):
    phi = 1/2 * np.arctan((np.tan(dPhi1/2)*np.cos(2*theta2) - np.tan(dPhi2/2)*np.cos(2*theta1)) / (np.tan(dPhi2/2)*np.sin(2*theta1) - np.tan(dPhi1/2)*np.sin(2*theta2)))
    return phi

def dTm(dPhi1, dPhi2, theta1, theta2, freq):
    theta1 = np.deg2rad(theta1)
    theta2 = np.deg2rad(theta2)
    phi = calcular_phi(dPhi1, dPhi2, theta1, theta2)
    dTm1 = 1/(np.pi * freq) * np.arctan(np.tan(dPhi1/2) / np.cos(2*(theta1 - phi)))
    dTm2 = 1/(np.pi * freq) * np.arctan(np.tan(dPhi2/2) / np.cos(2*(theta2 - phi)))
    return dTm1, dTm2


#dTm1, dTm2 = dTm(44.35448, 5.9745, 11.25, 56.25, 4250000)
#print(dTm1, dTm2)

fasedb0 = pd.read_csv(r"C:\Users\souli\OneDrive\Trabalho\UFPA\Mestrado\Trabalho\medições\ultrassom\acustoelasticidade\1\cisalhante\0_phase.csv")
fasedb90 = pd.read_csv(r"C:\Users\souli\OneDrive\Trabalho\UFPA\Mestrado\Trabalho\medições\ultrassom\acustoelasticidade\1\cisalhante\90_phase.csv")

diferencas_de_fase = calcular_diferenca_fase(fasedb0, fasedb90)

#print(calcular_diferenca_fase(fasedb0, fasedb90))