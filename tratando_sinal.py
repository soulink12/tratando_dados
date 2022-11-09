import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mathmate as mm

class Sinal:

    def __init__(self, sinal_path):
        self.xinterval = 1 / 2.5e9

        sinal = pd.read_table(sinal_path, header=None, decimal=',', names=["sinal_original"])
        self.sinal = np.array(sinal['sinal_original'])

        inicio = self.detectar_comprimento(self.sinal)
        self.sinal_modificado = self.criar_sinal_modificado(self.sinal, inicio, 0.014)
        self.primeiro_pico, _ = self.isolar_picos(self.sinal_modificado, 0)
        self.tempo_propagacao = self.calcular_tempo_propagacao(self.sinal_modificado, inicio)
        self.freq, self.dominio, self.primeira_freq_caracteristica = self.calcular_frequencia_caracteristica(
            self.primeiro_pico)

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
        sinal_modificado = self.remover_pico_inicial(sinal, inicio)
        sinal_modificado = self.arredondando_para_zero(sinal_modificado)
        sinal_modificado = self.removendo_ruido(sinal_modificado, db)
        return sinal_modificado

    def calcular_tempo_propagacao(self, sinal, inicio):
        _, indice_valor_max0 = self.isolar_picos(sinal, 0)
        _, indice_valor_max1 = self.isolar_picos(sinal, 1)
        intervalo = int(np.floor(inicio/2))
        sinal_cortado = sinal[indice_valor_max0 - intervalo:indice_valor_max1 + intervalo]
        if len(sinal_cortado) % 2 == 1:
            sinal_cortado = sinal_cortado[1:]
        tempo_propagacao = mm.calculation(sinal_cortado, self.xinterval)
        return tempo_propagacao

    def calcular_frequencia_caracteristica(self, sinal):
        sinalPlus = np.append(sinal, np.zeros(len(sinal) * 100))
        n = len(sinalPlus)

        fr = np.fft.rfftfreq(n, self.xinterval)
        X = 2 / n * np.abs(np.fft.fft(sinalPlus))
        plt.plot(fr, X[:len(fr)])
        primeira_freq_caracteristica = fr[np.argmax(X[:len(fr)])]
        return fr, X[:len(fr)], primeira_freq_caracteristica


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
        # TODO: Fazer o cálculo para diminuir pelo decibel. Olhar no manual do transdutor
        sinal_sem_ruido = np.array([0 if abs(sinal[i]) < db else sinal[i] for i in np.arange(0, len(sinal), 1)])
        return sinal_sem_ruido

    @staticmethod
    def isolar_picos(sinal, numero_do_pico):
        range_valores = 5000
        indice_valor_max = np.argmax(sinal)
        i = 0
        k = 0
        while i <= numero_do_pico:
            lim_max = indice_valor_max + range_valores * k
            indice_valor_max = lim_max + np.argmax(sinal[lim_max:])
            k = 1
            i += 1
        pico_isolado = sinal[indice_valor_max - range_valores:indice_valor_max + range_valores]
        return pico_isolado, indice_valor_max