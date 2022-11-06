import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Sinal:

    def __init__(self, sinal_path):
        sinal = pd.read_table(sinal_path, header=None, decimal=',', names=["sinal_original"])
        self.sinal = np.array(sinal['sinal_original'])

        inicio = self.detectar_comprimento(self.sinal)
        self.sinal_modificado = self.criar_sinal_modificado(self.sinal, inicio, 0.014)

    def __str__(self):
        return str(self.sinal)


    def plot_sinal(self, tipo_sinal):
        if tipo_sinal == "original":
            plt.plot(self.sinal)
            plt.title("Sinal Original")
            plt.show()
        elif tipo_sinal == "modificado":
            plt.plot(self.sinal_modificado)
            plt.title("Sinal Modificado")
            plt.show()

    @staticmethod
    def detectar_comprimento(sinal):
        inicio = 0
        if len(sinal) == 10000:
            inicio = 1000
        elif len(sinal) == 100000:
            inicio = 10000
        elif len(sinal) == 1000000:
            inicio = 10000
        return inicio
    
    def criar_sinal_modificado(self, sinal, inicio, db):
        # remover pico inicial
        # remover o ruído
        # arredondar para zero

        #criar função para isolar os picos

        sinal_modificado = self.remover_pico_inicial(sinal, inicio)
        sinal_modificado = self.arredondando_para_zero(sinal_modificado)
        sinal_modificado = self.removendo_ruido(sinal_modificado, db)
        return sinal_modificado

    @staticmethod
    def remover_pico_inicial(sinal, inicio):
        sinal_sem_pico_inicial = sinal[inicio:]
        return sinal_sem_pico_inicial

    @staticmethod
    def arredondando_para_zero(sinal):
        sinal_arredondado = sinal - sinal.mean()
        return sinal_arredondado

    @staticmethod
    def removendo_ruido(sinal, db):
        # TODO:
        sinal_sem_ruido = np.array([0 if abs(sinal[i]) < db else sinal[i] for i in np.arange(0,len(sinal),1)])
        return sinal_sem_ruido
        
'''
    def convert_frequencia(self):
        dados_refinados = np.append(np.array(self.sinal.tratado.iloc[MIN:MAX].copy()),
                                    np.zeros(len(self.sinal.tratado.iloc[MIN:MAX]) * 10))
        self.sinal["frequencia"] = frequencia
        return self.sinal
'''
sinal = Sinal("0.txt")
sinal.plot_sinal("modificado")