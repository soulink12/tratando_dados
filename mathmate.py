import numpy as np
import cupy as cp
from cupy.fft import fft, ifft
from scipy.interpolate import interp1d


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
    y1INT = fy[0:int(len(fy) / 2)]
    y2INT = fy[int(len(fy) / 2):len(fy)]
    #y1INT = fy(new_time_vector[0:int(len(new_time_vector)/2)])
    #y2INT = fy(new_time_vector[int(len(new_time_vector)/2):len(new_time_vector)])
    c2 = MYXCORR(y2INT, y1INT)
    diff = np.argmax(c2)
    tempo = new_time_vector[diff]
    return tempo