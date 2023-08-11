from time import sleep

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def calcular_derivada(vetor_inicial, x_increment):
    derivadas = np.array([])
    inicial = 5
    final = 30
    i = inicial
    vetor = vetor_inicial[inicial:final]
    derivada = (-3 * vetor[i * x_increment] + 4 * vetor[(i + 1) * x_increment] - vetor[(i + 2) * x_increment]) / (
                x_increment * 2)
    derivadas = np.append(derivadas, derivada)
    for i in range(inicial + 1, final - 1, 1):
        derivada = (vetor[(i + 1) * x_increment] - vetor[(i - 1) * x_increment]) / (x_increment * 2)
        derivadas = np.append(derivadas, derivada)
    i = len(vetor) - 1
    derivada = (3 * vetor[i * x_increment] - 4 * vetor[(i - 1) * x_increment] + vetor[(i - 2) * x_increment]) / (
                x_increment * 2)
    derivadas = np.append(derivadas, derivada)
    return derivadas


def gerar_eq_reta(vetor, derivadas):
    a_max = max(derivadas)
    argmax_gradiente = derivadas.argmax() * 5 + 25
    a_min = min(derivadas)
    argmin_gradiente = derivadas.argmin() * 5 + 25
    b_max = vetor["Tempo de Propagação"][argmax_gradiente] - a_max * argmax_gradiente
    x_max = np.arange(25, 125, 2)
    c_max = a_max * x_max + b_max
    b_min = vetor["Tempo de Propagação"][argmin_gradiente] - a_min * argmin_gradiente
    x_min = np.arange(75, 150, 2)
    c_min = a_min * x_min + b_min

    angulo_max_min = (b_min - b_max) / (a_max - a_min)
    # plt.plot(x_max, c_max, color='red')
    # plt.plot(x_min, c_min, color='orange')
    # plt.plot(vetor["Tempo de Propagação"], color='blue')
    # plt.show()
    # print(f"angulo_max_min: {angulo_max_min}")
    return a_max, b_max, c_max, a_min, b_min, c_min


# for i in range(1, 15, 1):
#    arquivo = pd.read_csv(rf"D:\ultrassom\chapa g2-auto\cisalhante\L2\{i}.txt", sep='\t', encoding='windows-1252', index_col=0)
#    derivadas = calcular_derivada(arquivo["Tempo de Propagação"], 5)
#    a_max, b_max, c_max, a_min, b_min, c_min = gerar_eq_reta(arquivo, derivadas)


def criar_grafico_linhas_angulo():
    global arquivo
    n_pastas = 14
    for i in range(1, n_pastas + 1, 1):
        globals()["ax1" + str(i)] = []
    for j in range(1, n_pastas + 1, 1):
        globals()["ax2" + str(j)] = []
    for z in range(1, n_pastas + 1, 1):
        globals()["ax3" + str(z)] = []
    fig, [globals()["ax1"], globals()["ax2"], globals()["ax3"]] = plt.subplots(3, n_pastas,
                                                                               subplot_kw={'projection': 'polar'})
    path_inicial = r"C:\Users\souli\OneDrive\Trabalho\UFPA\Mestrado\Trabalho\medições\ultrassom-refeito\G2\cisalhante\automatic"
    print(globals()["ax1"])
    print(len(globals()["ax1"]))
    print(globals()["ax1"][1])
    for i in range(0, int(n_pastas / 2), 1):
        path = path_inicial + r"\L1\\" + str(i + 1) + ".txt"
        arquivo = pd.read_csv(path, sep='\t', encoding='windows-1252', index_col=0)

        derivadas = calcular_derivada(arquivo["Tempo de Propagação"], 5)

        a_max, b_max, c_max, a_min, b_min, c_min = gerar_eq_reta(arquivo, derivadas)

        angulo_max_min = (b_min - b_max) / (a_max - a_min) - 90

        globals()["ax1"][i].vlines(angulo_max_min * np.pi / 180, 0, 1, color='red')
        globals()["ax1"][i].vlines((angulo_max_min + 90) * np.pi / 180, 0, 1, color='red')
        globals()["ax1"][i].vlines((angulo_max_min + 180) * np.pi / 180, 0, 1, color='red')
        globals()["ax1"][i].vlines((angulo_max_min + 270) * np.pi / 180, 0, 1, color='red')
        globals()["ax1"][i].set_rmax(1)
        globals()["ax1"][i].set_rticks([])
        globals()["ax1"][i].axis('off')
        globals()["ax1"][i].set_theta_zero_location("S")
        globals()["ax1"][i].set_rlabel_position(-22.5)  # get radial labels away from plotted line
        globals()["ax1"][i].grid(False)
    for i in range(int(n_pastas / 2), n_pastas, 1):
        path = path_inicial + r"\L1\\" + str(i + 1) + ".txt"
        arquivo = pd.read_csv(path, sep='\t', encoding='windows-1252', index_col=0)

        derivadas = calcular_derivada(arquivo["Tempo de Propagação"], 5)

        a_max, b_max, c_max, a_min, b_min, c_min = gerar_eq_reta(arquivo, derivadas)

        angulo_max_min = 90 - (b_min - b_max) / (a_max - a_min)

        globals()["ax1"][i].vlines(angulo_max_min * np.pi / 180, 0, 1, color='red')
        globals()["ax1"][i].vlines((angulo_max_min + 90) * np.pi / 180, 0, 1, color='red')
        globals()["ax1"][i].vlines((angulo_max_min + 180) * np.pi / 180, 0, 1, color='red')
        globals()["ax1"][i].vlines((angulo_max_min + 270) * np.pi / 180, 0, 1, color='red')
        globals()["ax1"][i].set_rmax(1)
        globals()["ax1"][i].set_rticks([])
        globals()["ax1"][i].axis('off')
        globals()["ax1"][i].set_theta_zero_location("S")
        globals()["ax1"][i].set_rlabel_position(-22.5)  # get radial labels away from plotted line
        globals()["ax1"][i].grid(False)
    for i in range(0, int(n_pastas/2), 1):
        path = path_inicial + r"\L2\\" + str(i + 1) + ".txt"
        arquivo = pd.read_csv(path, sep='\t', encoding='windows-1252', index_col=0)

        derivadas = calcular_derivada(arquivo["Tempo de Propagação"], 5)

        a_max, b_max, c_max, a_min, b_min, c_min = gerar_eq_reta(arquivo, derivadas)

        angulo_max_min = (b_min - b_max) / (a_max - a_min) - 90

        globals()["ax2"][i].vlines(angulo_max_min * np.pi / 180, 0, 1, color='red')
        globals()["ax2"][i].vlines((angulo_max_min + 90) * np.pi / 180, 0, 1, color='red')
        globals()["ax2"][i].vlines((angulo_max_min + 180) * np.pi / 180, 0, 1, color='red')
        globals()["ax2"][i].vlines((angulo_max_min + 270) * np.pi / 180, 0, 1, color='red')
        globals()["ax2"][i].set_rmax(1)
        globals()["ax2"][i].set_rticks([])
        globals()["ax2"][i].axis('off')
        globals()["ax2"][i].set_theta_zero_location("S")
        globals()["ax2"][i].set_rlabel_position(-22.5)  # get radial labels away from plotted line
        globals()["ax2"][i].grid(False)

    for i in range(int(n_pastas/2), n_pastas, 1):
        path = path_inicial + r"\L2\\" + str(i + 1) + ".txt"
        arquivo = pd.read_csv(path, sep='\t', encoding='windows-1252', index_col=0)

        derivadas = calcular_derivada(arquivo["Tempo de Propagação"], 5)

        a_max, b_max, c_max, a_min, b_min, c_min = gerar_eq_reta(arquivo, derivadas)

        angulo_max_min = 90 - (b_min - b_max) / (a_max - a_min)

        globals()["ax2"][i].vlines(angulo_max_min * np.pi / 180, 0, 1, color='red')
        globals()["ax2"][i].vlines((angulo_max_min + 90) * np.pi / 180, 0, 1, color='red')
        globals()["ax2"][i].vlines((angulo_max_min + 180) * np.pi / 180, 0, 1, color='red')
        globals()["ax2"][i].vlines((angulo_max_min + 270) * np.pi / 180, 0, 1, color='red')
        globals()["ax2"][i].set_rmax(1)
        globals()["ax2"][i].set_rticks([])
        globals()["ax2"][i].axis('off')
        globals()["ax2"][i].set_theta_zero_location("S")
        globals()["ax2"][i].set_rlabel_position(-22.5)  # get radial labels away from plotted line
        globals()["ax2"][i].grid(False)

    for i in range(0, int(n_pastas / 2), 1):
        path = path_inicial + r"\L3\\" + str(i + 1) + ".txt"
        arquivo = pd.read_csv(path, sep='\t', encoding='windows-1252', index_col=0)

        derivadas = calcular_derivada(arquivo["Tempo de Propagação"], 5)

        a_max, b_max, c_max, a_min, b_min, c_min = gerar_eq_reta(arquivo, derivadas)

        angulo_max_min = 90 - ((b_min - b_max) / (a_max - a_min))

        globals()["ax3"][i].vlines(angulo_max_min * np.pi / 180, 0, 1, color='red')
        globals()["ax3"][i].vlines((angulo_max_min + 90) * np.pi / 180, 0, 1, color='red')
        globals()["ax3"][i].vlines((angulo_max_min + 180) * np.pi / 180, 0, 1, color='red')
        globals()["ax3"][i].vlines((angulo_max_min + 270) * np.pi / 180, 0, 1, color='red')
        globals()["ax3"][i].set_rmax(1)
        globals()["ax3"][i].set_rticks([])
        globals()["ax3"][i].axis('off')
        globals()["ax3"][i].set_theta_zero_location("S")
        globals()["ax3"][i].set_rlabel_position(-22.5)  # get radial labels away from plotted line
        globals()["ax3"][i].grid(False)
    for i in range(int(n_pastas / 2), n_pastas, 1):
        path = path_inicial + r"\L3\\" + str(i + 1) + ".txt"
        arquivo = pd.read_csv(path, sep='\t', encoding='windows-1252', index_col=0)

        derivadas = calcular_derivada(arquivo["Tempo de Propagação"], 5)

        a_max, b_max, c_max, a_min, b_min, c_min = gerar_eq_reta(arquivo, derivadas)

        angulo_max_min = ((b_min - b_max) / (a_max - a_min)) - 90

        globals()["ax3"][i].vlines(angulo_max_min * np.pi / 180, 0, 1, color='red')
        globals()["ax3"][i].vlines((angulo_max_min + 90) * np.pi / 180, 0, 1, color='red')
        globals()["ax3"][i].vlines((angulo_max_min + 180) * np.pi / 180, 0, 1, color='red')
        globals()["ax3"][i].vlines((angulo_max_min + 270) * np.pi / 180, 0, 1, color='red')
        globals()["ax3"][i].set_rmax(1)
        globals()["ax3"][i].set_rticks([])
        globals()["ax3"][i].axis('off')
        globals()["ax3"][i].set_theta_zero_location("S")
        globals()["ax3"][i].set_rlabel_position(-22.5)  # get radial labels away from plotted line
        globals()["ax3"][i].grid(False)
    plt.savefig(fr"C:\Users\souli\OneDrive\Trabalho\UFPA\Mestrado\Trabalho\medições\organizando arquivos\chapa g2-angulo-phi.png", dpi=300)
    plt.show()


#criar_grafico_linhas_angulo()

def encontrar_direcao_polarizacao(path_inicial, n_pastas, intervalo_angulo):
    lista_angulo_maxL11 = []
    lista_angulo_maxL12 = []

    lista_angulo_maxL2 = []

    lista_angulo_maxL31 = []
    lista_angulo_maxL32 = []

    dados_corrigidos = pd.DataFrame()

    for i in range(0, int(n_pastas / 2), 1):
        path_final = path_inicial + r"\L1\\" + str(i + 1) + ".txt"
        arquivo = pd.read_csv(path_final, sep='\t', encoding='windows-1252', index_col=0)

        derivadas = calcular_derivada(arquivo["Tempo de Propagação"], 5)

        a_max, b_max, c_max, a_min, b_min, c_min = gerar_eq_reta(arquivo, derivadas)

        angulo_maxL11 = (b_min - b_max) / (a_max - a_min)
        lista_angulo_maxL11.append(angulo_maxL11)

    for i in range(int(n_pastas / 2), n_pastas, 1):
        path = path_inicial + r"\L1\\" + str(i + 1) + ".txt"
        arquivo = pd.read_csv(path, sep='\t', encoding='windows-1252', index_col=0)

        derivadas = calcular_derivada(arquivo["Tempo de Propagação"], 5)

        a_max, b_max, c_max, a_min, b_min, c_min = gerar_eq_reta(arquivo, derivadas)

        angulo_maxL12 = (b_min - b_max) / (a_max - a_min)
        lista_angulo_maxL12.append(angulo_maxL12)

    for i in range(0, n_pastas, 1):
        path = path_inicial + r"\L2\\" + str(i + 1) + ".txt"
        arquivo = pd.read_csv(path, sep='\t', encoding='windows-1252', index_col=0)

        derivadas = calcular_derivada(arquivo["Tempo de Propagação"], 5)

        a_max, b_max, c_max, a_min, b_min, c_min = gerar_eq_reta(arquivo, derivadas)

        angulo_maxL2 = (b_min - b_max) / (a_max - a_min)
        lista_angulo_maxL2.append(angulo_maxL2)

    for i in range(0, int(n_pastas / 2), 1):
        path = path_inicial + r"\L3\\" + str(i + 1) + ".txt"
        arquivo = pd.read_csv(path, sep='\t', encoding='windows-1252', index_col=0)

        derivadas = calcular_derivada(arquivo["Tempo de Propagação"], 5)

        a_max, b_max, c_max, a_min, b_min, c_min = gerar_eq_reta(arquivo, derivadas)

        angulo_maxL31 = ((b_min - b_max) / (a_max - a_min))
        lista_angulo_maxL31.append(angulo_maxL31)

    for i in range(int(n_pastas / 2), n_pastas, 1):
        path = path_inicial + r"\L3\\" + str(i + 1) + ".txt"
        arquivo = pd.read_csv(path, sep='\t', encoding='windows-1252', index_col=0)

        derivadas = calcular_derivada(arquivo["Tempo de Propagação"], 5)

        a_max, b_max, c_max, a_min, b_min, c_min = gerar_eq_reta(arquivo, derivadas)

        angulo_maxL32 = ((b_min - b_max) / (a_max - a_min))
        lista_angulo_maxL32.append(angulo_maxL32)

    lista_de_angulos_corrigido = corrigir_angulos(lista_angulo_maxL11, lista_angulo_maxL12,
                                                  lista_angulo_maxL2, lista_angulo_maxL31,
                                                  lista_angulo_maxL32, intervalo_angulo)

    dados_corrigidos["L1"] = lista_angulo_maxL11 + lista_angulo_maxL12
    dados_corrigidos["L2"] = lista_angulo_maxL2
    dados_corrigidos["L3"] = lista_angulo_maxL31 + lista_angulo_maxL32

    dados_corrigidos["L1-corrigido"] = lista_de_angulos_corrigido[0] + lista_de_angulos_corrigido[1]
    dados_corrigidos["L2-corrigido"] = lista_de_angulos_corrigido[2]
    dados_corrigidos["L3-corrigido"] = lista_de_angulos_corrigido[3] + lista_de_angulos_corrigido[4]

    tempo_maximo_L1 = []
    tempo_maximo_L2 = []
    tempo_maximo_L3 = []

    tempo_minimo_L1 = []
    tempo_minimo_L2 = []
    tempo_minimo_L3 = []

    for i in range(0, n_pastas, 1):
        path = path_inicial + r"\L1\\" + str(i + 1) + ".txt"
        arquivo = pd.read_csv(path, sep='\t', encoding='windows-1252', index_col=0)

        tempo_maximo_L1.append(arquivo["Tempo de Propagação"].loc[dados_corrigidos["L1-corrigido"][i][0]])

    for i in range(0, n_pastas, 1):
        path = path_inicial + r"\L1\\" + str(i + 1) + ".txt"
        arquivo = pd.read_csv(path, sep='\t', encoding='windows-1252', index_col=0)

        tempo_minimo_L1.append(arquivo["Tempo de Propagação"].loc[dados_corrigidos["L1-corrigido"][i][1]])

    for i in range(0, n_pastas, 1):
        path = path_inicial + r"\L2\\" + str(i + 1) + ".txt"
        arquivo = pd.read_csv(path, sep='\t', encoding='windows-1252', index_col=0)

        tempo_maximo_L2.append(arquivo["Tempo de Propagação"].loc[dados_corrigidos["L2-corrigido"][i][1]])

    for i in range(0, n_pastas, 1):
        path = path_inicial + r"\L2\\" + str(i + 1) + ".txt"
        arquivo = pd.read_csv(path, sep='\t', encoding='windows-1252', index_col=0)

        tempo_minimo_L2.append(arquivo["Tempo de Propagação"].loc[dados_corrigidos["L2-corrigido"][i][0]])

    for i in range(0, n_pastas, 1):
        path = path_inicial + r"\L3\\" + str(i + 1) + ".txt"
        arquivo = pd.read_csv(path, sep='\t', encoding='windows-1252', index_col=0)

        tempo_maximo_L3.append(arquivo["Tempo de Propagação"].loc[dados_corrigidos["L3-corrigido"][i][0]])

    for i in range(0, n_pastas, 1):
        path = path_inicial + r"\L3\\" + str(i + 1) + ".txt"
        arquivo = pd.read_csv(path, sep='\t', encoding='windows-1252', index_col=0)

        tempo_minimo_L3.append(arquivo["Tempo de Propagação"].loc[dados_corrigidos["L3-corrigido"][i][1]])

    dados_corrigidos["Tempo-max-L1"] = tempo_maximo_L1
    dados_corrigidos["Tempo-min-L1"] = tempo_minimo_L1
    dados_corrigidos["Tempo-max-L2"] = tempo_maximo_L2
    dados_corrigidos["Tempo-min-L2"] = tempo_minimo_L2
    dados_corrigidos["Tempo-max-L3"] = tempo_maximo_L3
    dados_corrigidos["Tempo-min-L3"] = tempo_minimo_L3

    #print(dados_corrigidos["L1"][0:7]-90)
    #print(90-dados_corrigidos["L1"][7:14])

    dados_corrigidos["L1"] = (dados_corrigidos["L1"][0:7]-90).tolist() + (90-dados_corrigidos["L1"][7:14]).tolist()
    dados_corrigidos["L2"] = (dados_corrigidos["L2"][0:7]-90).tolist() + (90-dados_corrigidos["L2"][7:14]).tolist()
    dados_corrigidos["L3"] = (90-dados_corrigidos["L3"][0:7]).tolist() + (dados_corrigidos["L3"][7:14]-90).tolist()

    return dados_corrigidos


def corrigir_angulos(angulo_max_minL11, angulo_max_minL12, angulo_max_minL2, angulo_max_minL31, angulo_max_minL32,
                     intervalo_angulo):
    angulo_max_minL11_corrigido = []
    angulo_max_minL12_corrigido = []
    angulo_max_minL2_corrigido = []
    angulo_max_minL31_corrigido = []
    angulo_max_minL32_corrigido = []
    lista_de_listas_corrigido = [angulo_max_minL11_corrigido, angulo_max_minL12_corrigido, angulo_max_minL2_corrigido,
                                 angulo_max_minL31_corrigido, angulo_max_minL32_corrigido]
    lista_de_listas = [angulo_max_minL11, angulo_max_minL12, angulo_max_minL2, angulo_max_minL31, angulo_max_minL32]
    i = 0
    for lista in lista_de_listas:
        for angulo in lista:
            if angulo % intervalo_angulo > intervalo_angulo / 2:
                angulo_maior = angulo // intervalo_angulo * intervalo_angulo + intervalo_angulo
                angulo_menor = check_angulo(angulo_maior)
            elif angulo % intervalo_angulo < intervalo_angulo / 2:
                angulo_maior = angulo // intervalo_angulo * intervalo_angulo
                angulo_menor = check_angulo(angulo_maior)
            else:
                print('igual')
            '''
            if angulo_maior > angulo_menor:
                angulo_0 = angulo_maior
                angulo_90 = angulo_menor
            else:
                angulo_0 = angulo_menor
                angulo_90 = angulo_maior
            '''
            angulo_0 = angulo_maior
            angulo_90 = angulo_menor
            lista_de_listas_corrigido[i].append([angulo_0, angulo_90])
        i += 1

    return lista_de_listas_corrigido


def check_angulo(angulo_maior):
    if angulo_maior == 90:
        angulo_menor = 0
    elif angulo_maior > 90:
        angulo_menor = angulo_maior - 90
    else:
        angulo_menor = angulo_maior + 90
    return angulo_menor
