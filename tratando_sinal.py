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
        self.sinal = np.array(sinal['sinal_original'])
        self.inicio = self.detectar_comprimento(self.sinal)
        self.sinal_modificado = self.criar_sinal_modificado(self.sinal, self.inicio, 0.20)
        self.pico_isolado, _ = self.selecionar_maior_pico(self.sinal_modificado, self.inicio)
        self.freq, self.dominio, self.primeira_freq_caracteristica = self.calcular_frequencia_caracteristica(
            self.pico_isolado)

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
        sinal_modificado = self.filtrando_band_pass(sinal_modificado, 1.5e6, 8.5e6, self.fs, order=1)
        self.tempo_propagacao = self.calcular_tempo_propagacao(sinal_modificado, self.inicio)
        sinal_modificado = self.removendo_amplitude(sinal_modificado, db)
        return sinal_modificado

    def calcular_tempo_propagacao(self, sinal, inicio):
        _, indice_valor_max0 = self.isolar_picos(sinal, inicio, 0)
        _, indice_valor_max1 = self.isolar_picos(sinal, inicio, 1)
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
        '''
        sinalPlus = np.append(sinal, np.zeros(len(sinal) * 10))
        n = len(sinalPlus)
        fr = np.fft.rfftfreq(n, self.xinterval)
        Y = 2 / n * np.abs(np.fft.fft(sinalPlus))
        plt.clf()
        plt.plot(fr,Y[:len(fr)])
        plt.xlim(0, 1e7)
        plt.show()
        plt.close()
        '''
        spectrum, frequency, _ = pyplot.phase_spectrum(sinal, Fs=self.fs, pad_to=1000000)

        primeira_freq_caracteristica = spectrum[np.argmax(frequency[:len(spectrum)])]
        return spectrum, frequency, primeira_freq_caracteristica

    def espectro_de_fase(self, sinal):
        n = len(sinal)
        fft = np.fft.rfft(sinal)
        fft_phase = np.angle(fft)
        fft_freq = np.arange(n) * self.fs / n
        return fft_freq[:int(n/2+1)], np.unwrap(fft_phase)

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
            pico_isolado = sinal[0:indice_valor_max + range_valores]
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

'''
sinal = Sinal(r'C:\Users\souli\OneDrive\Trabalho\UFPA\Mestrado\Trabalho\medições\ultrassom\chapa g1\cisalhante\L1\1\1\0.txt')
sinal2 = Sinal(r'C:\Users\souli\OneDrive\Trabalho\UFPA\Mestrado\Trabalho\medições\ultrassom\chapa g1\cisalhante\L1\1\9\0.txt')
sinal_selecionado1 = sinal.sinal_modificado
fft_freq1, fft_phase1 = sinal.espectro_de_fase(sinal_selecionado1)
sinal_selecionado2 = sinal2.sinal_modificado
fft_freq2, fft_phase2 = sinal2.espectro_de_fase(sinal_selecionado2)
print(len(fft_freq1))
print(len(fft_phase1))
plt.plot(fft_freq1, np.unwrap(fft_phase1))
plt.plot(fft_freq2, np.unwrap(fft_phase2))
plt.xlim(0, 1e7)
plt.ylim(100, -600)
plt.show()

spectrum, frequency, line = pyplot.phase_spectrum(sinal_selecionado1, Fs=sinal.fs)
pyplot.xlim(0, 1e7)
pyplot.ylim(100, -600)
pyplot.show()

plt.plot(frequency,spectrum)
plt.xlim(0, 1e7)
plt.ylim(100, -600)
plt.show()

spectrum, frequency, line = pyplot.magnitude_spectrum(sinal.pico_isolado, Fs=sinal.fs, pad_to=1000000)
pyplot.show()

plt.plot(frequency,spectrum)
plt.show()
'''

#np.savetxt(r"C:\Users\souli\OneDrive\Trabalho\UFPA\Mestrado\Trabalho\medições\ultrassom\chapa g1\cisalhante\L1\1\1\teste.txt", fft_phase , '%.18e' , delimiter=',')

