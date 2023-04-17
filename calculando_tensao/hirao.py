import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from scipy.optimize import fsolve
from calculando_tensao.angulo import encontrar_direcao_polarizacao


def calcular_birrefringencia(tempo_0, tempo_90):
    # tempo_0 = tempo de propagação do sinal paralelo com a laminação
    # tempo_90 = tempo de propagação do sinal perpendicular com a laminação
    return -2 * (tempo_0 - tempo_90) / (tempo_90 + tempo_0)

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


def calcular_theta_s1s2(B, phi, i1, i2, intervalo):
    def func(x):
        return [(B0 ** 2 + 2 * B0 * Cb * x[1] * sp.cos(2 * x[0]) + (Cb ** 2) * (x[1] ** 2)) ** (1 / 2) - B,
                ((Cb * x[1] * sp.sin(2 * x[0])) / (B0 + Cb * x[1] * sp.cos(2 * x[0]))) - sp.tan(2 * phi)]

    chutes_tensao = np.arange(i1, i2, intervalo)
    solucoes = []
    for chute_tensao in chutes_tensao:
        sol_dict = fsolve(func, [10 * np.pi / 180, chute_tensao])
        solucoes.append(sol_dict)
        # print(sol_dict[0] * 180 / np.pi, sol_dict[1])
    media_theta = np.mean([solucao[0] % (2 * np.pi) * (180 / np.pi) for solucao in solucoes])
    media_s1s2 = np.mean([solucao[1] for solucao in solucoes])
    i = 0
    for solucao in solucoes:
        theta = solucao[0] % (2 * np.pi) * (180 / np.pi)
        if theta - media_theta > 1:
            print(theta, media_theta)
            print("theta errado")

        s1s2 = solucao[1]
        if s1s2 - media_s1s2 > 1:
            print(s1s2, media_s1s2)
            print("s1s2 errado")
        i+=1

    thetas.append(media_theta)
    s1s2s.append(media_s1s2)

    fig, ax1 = plt.subplots()

    ax1.plot(chutes_tensao,[solucao[0] % (2 * np.pi) * (180 / np.pi) for solucao in solucoes])
    ax2 = ax1.twinx()
    ax2.plot(chutes_tensao,[solucao[1] for solucao in solucoes], color='r')


    return thetas, s1s2s

path_inicial = r"D:\ultrassom\chapa g1-auto\cisalhante"

n_pastas = 14

dados_corrigidos = encontrar_direcao_polarizacao(path_inicial, n_pastas, 5)

print(dados_corrigidos.columns)

B0 = 0.00425214285714286
Cb = 9.54423 * 10 ** -6
#B = 0.00479
#phi = ((0*2 +5.4)* np.pi) / 180

thetas = []
s1s2s = []

#L1
n_pontos = 14
'''
print("L1")
for i in range(n_pontos):
    phi = dados_corrigidos["L1"][i]
    phi = (phi - 90)*np.pi/180
    B = calcular_birrefringencia(dados_corrigidos["Tempo-min-L1"][i], dados_corrigidos["Tempo-max-L1"][i])

    thetas, s1s2s = calcular_theta_s1s2(B, phi, 300, 1000, 100)
    plt.title("L1 " + str(i))
    plt.show()

print(len(thetas))
dados_corrigidos["theta-L1"] = thetas
dados_corrigidos["s1s2-L1"] = s1s2s
'''
thetas = []
s1s2s = []

print("L2")
for i in range(n_pontos):
    a = i
    phi = dados_corrigidos["L2"][a]
    phi = (phi - 90)*np.pi/180
    B = calcular_birrefringencia(dados_corrigidos["Tempo-min-L2"][a], dados_corrigidos["Tempo-max-L2"][a])

    thetas, s1s2s = calcular_theta_s1s2(B, phi, -300, -100, 10)
    plt.title("L2 " + str(i))
    plt.show()

print(len(thetas))
dados_corrigidos["theta-L2"] = thetas
dados_corrigidos["s1s2-L2"] = s1s2s
print(s1s2s)

thetas = []
s1s2s = []
'''
print("L3")
for i in range(n_pontos):
    phi = dados_corrigidos["L3"][i]
    phi = (phi - 90)*np.pi/180
    B = calcular_birrefringencia(dados_corrigidos["Tempo-min-L3"][i], dados_corrigidos["Tempo-max-L3"][i])

    thetas, s1s2s = calcular_theta_s1s2(B, phi, 500, 1000, 25)
    plt.title("L3 " + str(i))
    plt.show()

dados_corrigidos["theta-L3"] = thetas
dados_corrigidos["s1s2-L3"] = s1s2s

print(dados_corrigidos)
'''

'''
grau = np.arange(0, 180, 0.1)

theta = grau * np.pi / 180

s1s2 = (-2 * B0 * Cb * np.cos(2 * theta) - 2 ** (1/2) * (2 * B **2 * Cb ** 2 - B0 ** 2 * Cb ** 2 + B0**2 * Cb **2 * np.cos(4*theta)) ** (1/2))/ (2 * Cb ** 2)

plt.plot(grau, s1s2)
plt.show()
'''
dados_corrigidos.to_csv(r"D:\ultrassom\chapa g1-auto\cisalhante\hirao-dados-angulos.csv", sep='\t', encoding='windows-1252')

#path_cisalhante = r"D:\ultrassom\chapa A3 auto\centro\cisalhante\\"
#path_compressivo = r"D:\ultrassom\chapa A3 auto\centro\compressivo\tempo_propagacao.csv"
#numero_de_pastas = 14
#dados = mapear_dados_cisalhante(path_cisalhante, numero_de_pastas, 90, 0)


#get_tempo_cisalhante(r"D:\ultrassom\chapa g1-auto\cisalhante\L1\1.txt", 0, 90)

