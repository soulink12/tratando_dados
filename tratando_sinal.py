import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Sinal:

    def __init__(self, sinal_path):
        self.sinal = pd.read_table(sinal_path, header=None, decimal=',', names=["sinal_original"])

    def __str__(self):
        return str(self.sinal)

    def removendo_ruido(self, db):
        self.sinal.loc[self.sinal["sinal_original"].abs() < db, 'tratado'] = 0.0
        self.sinal.loc[self.sinal["sinal_original"].abs() > db, 'tratado'] = self.sinal["sinal_original"].loc[
            self.sinal["sinal_original"].abs() > db]
        return self.sinal


    def plot_sinal(self, tipo_sinal):
        if tipo_sinal == "original":
            plt.plot(self.sinal["sinal_original"])
            plt.title("Sinal Original")
            plt.show()
        elif tipo_sinal == "tratado":
            plt.plot(self.sinal["tratado"])
            plt.title("Sinal Tratado")
            plt.show()
        plt.show()

    def remover_pico_inicial(self):
        inicio = 0
        if len(self.sinal) == 10000:
            inicio = 1000
        elif len(self.sinal) == 100000:
            inicio = 10000
        elif len(self.sinal) == 1000000:
            inicio = 10000

        data_modificado = pd.DataFrame(self.sinal["sinal_original"].iloc[inicio:])

        return data_modificado

    def arredondando_para_zero(self):
        pass
'''
    def convert_frequencia(self):
        dados_refinados = np.append(np.array(self.sinal.tratado.iloc[MIN:MAX].copy()),
                                    np.zeros(len(self.sinal.tratado.iloc[MIN:MAX]) * 10))
        self.sinal["frequencia"] = frequencia
        return self.sinal
'''