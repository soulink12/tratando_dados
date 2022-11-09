import matplotlib.pyplot as plt

from tratando_sinal import Sinal


def gerar_dados(sinal_path):
    sinal = Sinal(sinal_path)
    sinal_original = sinal.sinal
    sinal_modificado = sinal.sinal_modificado
    primeiro_pico = sinal.primeiro_pico
    freq, dominio, primeira_freq_caracteristica = sinal.freq, sinal.dominio, sinal.primeira_freq_caracteristica
    tempo_propagacao = sinal.tempo_propagacao

    return sinal_original, sinal_modificado, primeiro_pico, tempo_propagacao, freq, dominio, \
           primeira_freq_caracteristica


sinal_original, sinal_modificado, primeiro_pico, tempo_propagacao, freq, dominio, \
primeira_freq_caracteristica = gerar_dados("0.txt")

plt.close("all")
plt.plot(sinal_original)
plt.show()

