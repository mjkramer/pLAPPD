import numpy as np
import matplotlib.pyplot as plt

def read_wfm(fname):
    return np.loadtxt(fname, delimiter=',', skiprows=6, usecols=(3,4), unpack=True)

def plot_dir(dirname):
    from glob import glob
    import os

    files = sorted(glob(os.path.join(dirname, '*.csv')))
    for fname in files:
        t, v = read_wfm(fname)
        plt.plot(t, v)
        plt.xlabel('[s]')
        plt.ylabel('[V]')
