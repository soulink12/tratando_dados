import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mathmate as mm
from scipy.signal import butter, sosfilt, sosfreqz
from matplotlib import pyplot


class Sinal:

    def __init__(self, sinal_path):
        self.fs = 2.5e9
        self.xinterval = 1 / self.fs
        sinal = pd.read_table(sinal_path, header=None, decimal=',', names=["sinal_original"])
        self.sinal_original = np.abs(np.array(sinal['sinal_original']))
        self.inicio = self.detectar_comprimento(self.sinal_original)
        self.sinal_modificado = self.criar_sinal_modificado(self.sinal_original, self.inicio, 0.1)
        self.pico_isolado, _ = self.selecionar_maior_pico(self.sinal_modificado, self.inicio)
        self.amplitude, self.freq_amplitude, self.primeira_freq_caracteristica = self.calcular_frequencia_caracteristica(
            self.pico_isolado)
        self.phase, self.freq_phase = self.espectro_de_fase(self.sinal_modificado)


    @staticmethod
    def detectar_comprimento(sinal):
        inicio = 0
        if len(sinal) == 10000:
            inicio = 1000
        elif len(sinal) == 100000:
            inicio = 10000
        elif len(sinal) == 1000000:
            inicio = 40000
        return inicio

    def criar_sinal_modificado(self, sinal, inicio, db):
        sinal_modificado = self.remover_pico_inicial(sinal, inicio)
        sinal_modificado = self.arredondando_para_zero(sinal_modificado)
        #sinal_modificado = self.filtrando_band_pass(sinal_modificado, 1.5e6, 8.5e6, self.fs, order=1)
        sinal_modificado = self.removendo_amplitude(sinal_modificado, db)
        self.tempo_propagacao = self.calcular_tempo_propagacao(sinal_modificado, self.inicio)
        return sinal_modificado

    def calcular_tempo_propagacao(self, sinal, inicio):
        #sinal = np.abs(sinal)
        pico1, indice_valor_max0 = self.isolar_picos(sinal, inicio, 0)
        pico2, indice_valor_max1 = self.isolar_picos(sinal, inicio, 1)
        intervalo = int(np.floor(inicio/2))
        if(indice_valor_max0 >= intervalo):
            sinal_cortado = sinal[indice_valor_max0 - intervalo:indice_valor_max1 + intervalo]
        else:
            sinal_cortado = sinal[0:indice_valor_max1 + intervalo]
        if len(sinal_cortado) % 2 == 1:
            sinal_cortado = sinal_cortado[1:]
        tempo_propagacao = mm.calculation(sinal_cortado, self.xinterval)
        return tempo_propagacao

    def calcular_frequencia_caracteristica(self, sinal):
        amplitude, frequency, _ = pyplot.magnitude_spectrum(sinal, Fs=self.fs, pad_to=100000)
        pyplot.cla()
        primeira_freq_caracteristica = frequency[np.argmax(amplitude[:len(frequency)])]
        return amplitude, frequency, primeira_freq_caracteristica

    def espectro_de_fase(self, sinal):
        phase, frequency, _ = pyplot.phase_spectrum(sinal, Fs=self.fs)
        loc = 0
        for i in frequency:
            frequency[loc] = round(i)
            loc += 1
        pyplot.cla()
        return phase, frequency

    def filtrando_band_pass(self, sinal, lowcut, highcut, fs, order=5):
        y = self.butter_bandpass_filter(sinal, lowcut, highcut, fs, order=order)
        y = np.array(y)
        return y

    def butter_bandpass(self, lowcut, highcut, fs, order=5):
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        sos = butter(order, [low, high], analog=False, btype='band', output='sos')
        return sos

    def butter_bandpass_filter(self, data, lowcut, highcut, fs, order=5):
        sos = self.butter_bandpass(lowcut, highcut, fs, order=order)
        y = sosfilt(sos, data)
        return y

    @staticmethod
    def remover_pico_inicial(sinal, inicio):
        sinal_sem_pico_inicial = sinal[inicio:]
        return sinal_sem_pico_inicial

    @staticmethod
    def arredondando_para_zero(sinal):
        sinal_arredondado = sinal - sinal.mean()
        return sinal_arredondado


    @staticmethod
    def removendo_amplitude(sinal, queda_percentual):
        amplitude = max(sinal)
        amplitude_max = amplitude * queda_percentual
        dbLoss = 20 * np.log10(amplitude / amplitude_max)
        dbArray = 20 * np.log10(sinal / amplitude)
        sinal_sem_ruido = np.array([0 if abs(20 * np.log10(abs(sinal[i])/amplitude)) >= dbLoss else sinal[i] for i in np.arange(0, len(sinal), 1)])
        for i in np.arange(0, len(sinal), 1):
            if dbArray[i] >= dbLoss:
                sinal[i] = 0
        return sinal_sem_ruido

    @staticmethod
    def isolar_picos(sinal, inicio, numero_do_pico):
        range_valores = int(inicio/2)
        indice_valor_max = np.argmax(sinal)
        i = 0
        k = 0
        while i <= numero_do_pico:
            lim_max = indice_valor_max + range_valores * k
            indice_valor_max = lim_max + np.argmax(sinal[lim_max:])
            k = 1
            i += 1
        if(indice_valor_max >= range_valores):
            pico_isolado = sinal[indice_valor_max - range_valores:indice_valor_max + range_valores]
        else:
            dif = range_valores - indice_valor_max
            pico_isolado = np.zeros(dif).tolist() + sinal[0:indice_valor_max + range_valores].tolist()

        return pico_isolado, indice_valor_max

    def selecionar_maior_pico(self, sinal, inicio):
        pico_max = np.argmax(sinal)
        eh_pico_maximo = True
        i=0
        while eh_pico_maximo:
            pico_isolado, indice_valor_max = self.isolar_picos(sinal, inicio, i)
            if indice_valor_max ==  pico_max:
                eh_pico_maximo = False
                return pico_isolado, indice_valor_max
            else:
                i += 1


#sinal = Sinal(r'D:\ultrassom\0 - 45.txt')
#sinal.sinal_modificado.tofile(r'D:\ultrassom\0 - 45mod', sep = "\n")
#sinal = Sinal(r'D:\ultrassom\0 - 135.txt')
#sinal.sinal_modificado.tofile(r'D:\ultrassom\0 - 135mod', sep = "\n")


