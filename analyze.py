import numpy as np
import matplotlib.pyplot as plt
import ROOT as R
from glob import glob
import os

def read_wfm(fname):
    return np.loadtxt(fname, delimiter=',', usecols=(3,4), unpack=True)

def plot_dir(dirname):
    files = sorted(glob(os.path.join(dirname, '*.csv')))
    for fname in files:
        t, v = read_wfm(fname)
        plt.plot(t, v)
        plt.xlabel('[s]')
        plt.ylabel('[V]')

def get_template(dirname):
    files = sorted(glob(os.path.join(dirname, '*.csv')))

    t0, _ = read_wfm(files[0])  # use t0 to verify alignment

    wfms = []                   # list of waveforms

    for fname in files:
        t, wfm = read_wfm(fname)
        assert (t == t0).all()
        wfms.append(wfm)

    mtx = np.vstack(wfms)       # one waveform per row

    means = np.mean(mtx, axis=0)
    errs = np.std(mtx, axis=0)

    t0 = t0.copy()              # won't work unless i do this. WHY?!?

    gph = R.TGraphErrors(len(t0), t0 * 1e9, means * 1e3, np.array([0]*len(t0)), errs * 1e3)
    gph.GetXaxis().SetTitle('[ns]')
    gph.GetYaxis().SetTitle('[mV]')
    return gph

def gen_spe_2p2ft_templates():
    outf = R.TFile('Templates/SPE_2.2ft_5mV.root', 'RECREATE')

    for side in ['R', 'L']:
        for chan in range(1, 8):
            dirname = glob('RawData/SinglePhotoelectron/%s%d_2pt2*_5mV' % (side, chan))[0]
            gph = get_template(dirname)
            gph.SetName('%s%d' % (side, chan))
            gph.SetTitle('%s%d, 2.2 ft cable, -5 mV trigger' % (side, chan))
            gph.Write()
