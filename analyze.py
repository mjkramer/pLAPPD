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
            gph.SetName('g_spe_%s%d' % (side, chan))
            gph.SetTitle('%s%d, 2.2 ft cable, -5 mV trigger' % (side, chan))
            gph.Write()

def gen_cosmic_templates():
    outf = R.TFile('Templates/Cosmics_2.2ft_15mV.root', 'RECREATE')

    for side in ['R', 'L']:
        for chan in [6, 7]:
            dirname = glob('RawData/CosmicRays/%s%d_2pt2*_15mV' % (side, chan))[0]
            gph = get_template(dirname)
            gph.SetName('g_cosmic_%s%d' % (side, chan))
            gph.SetTitle('%s%d, 2.2 ft cable, -15 mV trigger (cosmics)' % (side, chan))
            gph.Write()

def gen_scint_templates():
    outf = R.TFile('Templates/ScintCosmics_2.2ft_15mV.root', 'RECREATE')

    for side in ['R', 'L']:
        for chan in [6, 7]:
            dirname = glob('RawData/WithScintilator/%s%d_2pt2*_15mV' % (side, chan))[0]
            gph = get_template(dirname)
            gph.SetName('g_scint_%s%d' % (side, chan))
            gph.SetTitle('%s%d, 2.2 ft cable, -15 mV trigger (cosmics), w/ scintillator' % (side, chan))
            gph.Write()

def gen_length_templates():
    outf = R.TFile('Templates/DifferentLengths_5mV.root', 'RECREATE')

    for cid in ['R3', 'R4', 'L4']:
        for length in ['2pt2', '12pt5', '25', '50']:
            if cid == 'R4' and length == '12pt5':
                continue        # last measurement, board went haywire

            dirname = glob('RawData/DifferentLengths/%s/%s_%s*_5mV' % (cid, cid, length))[0]
            gph = get_template(dirname)
            gph.SetName('g_%sft_%s' % (length, cid))
            gph.SetTitle('%s, %s ft cable, -5 mV trigger' % (cid, length))
            gph.Write()
