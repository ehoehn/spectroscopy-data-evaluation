
'''
punkte_baseline are the wavenumbers were the spectrum is taken and pulled down to the baseline.
band_start: is the start of the interval where the script searches for the highest intensity. this highest intensity is than shown over time.
band_end: is the end of that interval.
'''


'''
imput file: .tvf-TriVista-File
output file: band intensity over time after baseline correction
'''
#written by EvaMaria Hoehn


import lib.analyte



#suffix_for_new_filename = '_graphIntensityOverTime.csv'
punkte_baseline = lib.analyte.malachitegreen()
band_start = 1440
band_end = 1520
# 1440 - 1520


import os
import plotly.graph_objs as go  #import Scatter, Layout
import plotly
import scipy.signal
import pandas as pd
from lib.allgemein import generate_filename
import Ramanspektren.lib.xml_import
import Ramanspektren.lib.baseline_corr



for dateiname in os.listdir():
    if dateiname.endswith('.tvf') or dateiname.endswith('.TVF'):
        print(dateiname)
        intensities = Ramanspektren.lib.xml_import.get_intensities(dateiname)
        times = Ramanspektren.lib.xml_import.get_times(dateiname)

        smoothed_intensities = scipy.signal.savgol_filter(intensities, window_length=9, polyorder=1, axis=0, mode='nearest')
        smoothed_intensities = pd.DataFrame(smoothed_intensities, index=intensities.index, columns=intensities.columns)

        intensities = Ramanspektren.lib.baseline_corr.baselinecorrection(intensities, punkte_baseline)

        df_intensities = pd.DataFrame(data=intensities.iloc[:, :], index=intensities.index, columns=[intensities.columns],
                                   copy=True)
        df_intensities.iloc[:] = intensities.iloc[:]
        all = times.append(df_intensities)
        all = all.fillna(0)

        liste = dateiname.split('_')
        liste.insert(6, 'pH 3, 10,17 mS cm-1')
        liste = '_'.join(liste)

        all.to_csv(generate_filename(liste, '_w9_o1_s_drawnDown.csv'), sep=';')

