import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Sinal:

    def __init__(self, sinal_path):
        self.sinal = pd.read_table(sinal_path, header=None, decimal=',', names=["sinal_original"])
        self.inicio = self.detectar_comprimento(self.sinal)
        self.sinal_modificado = self.criar_sinal_modificado(self.sinal, self.inicio, 0.014)

    def __str__(self):
        return str(self.sinal)

    def plot_sinal(self, tipo_sinal):
        if tipo_sinal == "original":
            plt.plot(self.sinal["sinal_original"])
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
        #sinal_modificado = self.removendo_ruido(sinal_modificado, db)
        return sinal_modificado

    def removendo_ruido(self, sinal, db):
        sinal.loc[sinal["sinal_original"].abs() < db, 'modificado'] = 0.0
        sinal.loc[sinal["sinal_original"].abs() > db, 'modificado'] = sinal["sinal_original"].loc[
            sinal["sinal_original"].abs() > db]
        return sinal

    def remover_pico_inicial(self, sinal, inicio):
        sinal_sem_pico_incial = pd.DataFrame(self.sinal["sinal_original"].iloc[self.inicio:]) #renomear o sinal
        return sinal_sem_pico_incial

    def arredondando_para_zero(self):
        self.data_modificado = pd.DataFrame(self.data_original["sinal_original"].iloc[self.inicio:]
                                            - self.data_original["sinal_original"].iloc[self.inicio:].mean())
        print(self.data_modificado.mean())

        
'''
    def convert_frequencia(self):
        dados_refinados = np.append(np.array(self.sinal.tratado.iloc[MIN:MAX].copy()),
                                    np.zeros(len(self.sinal.tratado.iloc[MIN:MAX]) * 10))
        self.sinal["frequencia"] = frequencia
        return self.sinal
'''