import numpy as np
from numpy.fft import fft, ifft
from scipy.interpolate import interp1d

def MYXCORR(A, B):
    T = len(A)
    C = np.zeros_like(A)
    Va = np.hstack((C, A, C))
    Vb = np.hstack((B, C, C))
    AF = fft(Va)
    BF = fft(Vb)
    corr = np.real(ifft(AF * np.conj(BF)))
    xcorr = corr[1:2 * T]
    return xcorr

def myinterp(v, Np):
    v2 = np.arange(0, len(v) - 1, 1)
    Npv = np.arange(0, Np, 1)
    V = []
    k = 1
    for i in v2:
        h = (v[i + 1] - v[i]) / Np
        for j in Npv:
            V.append(v[i] + h * j)

        k = k + Np
    V.append(v[-1])
    return V

def calculation(scaled_wave, tscale):
    time_vector = np.arange(0,len(scaled_wave), 1) * tscale
    new_time_vector = np.arange(0, len(scaled_wave)-1, 0.0625) * tscale
    fy = interp1d(time_vector, scaled_wave, kind='cubic')
    y1INT = fy(new_time_vector[0:int(len(new_time_vector)/2)])
    y2INT = fy(new_time_vector[int(len(new_time_vector)/2):len(new_time_vector)])
    c2 = MYXCORR(y2INT, y1INT)
    diff = np.argmax(c2)
    tempo = new_time_vector[diff]
    return tempo