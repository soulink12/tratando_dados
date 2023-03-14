import matplotlib.pyplot as plt
import numpy as np
import cupy as cp
from cupy.fft import fft, ifft
from scipy.interpolate import interp1d
from scipy import signal


mempool = cp.get_default_memory_pool()
pinned_mempool = cp.get_default_pinned_memory_pool()
cache = cp.fft.config.get_plan_cache()

def MYXCORR(A, B):
    Ac = cp.array(A)
    Bc = cp.array(B)
    T = len(Ac)
    C = cp.zeros_like(Ac)
    Va = cp.hstack((C, Ac, C))
    Vb = cp.hstack((Bc, C, C))
    AF = fft(Va)
    BF = fft(Vb)
    corr = cp.real(ifft(AF * cp.conj(BF)))
    xcorr = corr[1:2 * T]
    xcorrCPU = xcorr.get()
    mempool.free_all_blocks()
    pinned_mempool.free_all_blocks()
    cache.clear()
    return xcorrCPU

def MYXCORR2(A, B):
    xcorr = signal.correlate(A, B, mode='full')
    return xcorr

def MYXCORR3(A, B):
    xcorr = np.correlate(A, B, mode='full')
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
    #fy = interp1d(time_vector, scaled_wave, kind='cubic')
    fy = np.interp(new_time_vector, time_vector, scaled_wave)
    y1INT = fy[0:int(len(fy) / 2)].tolist()
    y2INT = fy[int(len(fy) / 2):len(fy)].tolist()
    #y1INT = fy(new_time_vector[0:int(len(new_time_vector)/2)])
    #y2INT = fy(new_time_vector[int(len(new_time_vector)/2):len(new_time_vector)])
    c2 = MYXCORR(y2INT, y1INT)
    c22 = MYXCORR2(y2INT, y1INT)
    diff = np.argmax(c2)
    #diff2 = np.argmax(c22)
    tempo = new_time_vector[diff]
    #tempo2 = new_time_vector[diff2]
    #teste sem interpolação
    #y1 = scaled_wave[0:int(len(scaled_wave) / 2)]
    #y2 = scaled_wave[int(len(scaled_wave) / 2):len(scaled_wave)]
    #c = MYXCORR(y2, y1)
    #diffc = np.argmax(c)
    #tempoc = time_vector[diffc]
    return tempo