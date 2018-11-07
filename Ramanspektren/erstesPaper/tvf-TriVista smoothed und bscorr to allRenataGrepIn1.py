'''
imput files: mehrere .tvf-TriVista-Dateien mit zeitl Verlauf
output file: eine Datei mit zeitl Verlauf in einer Tabelle nach baseline korrektur
'''
#written by EvaMaria Hoehn


import os
from lib import analyte
from lib.xml_import import get_intensities, get_times
from lib.baseline_corr import baselinecorrection
from lib.auswertung import compute_wn_with_highest_intensity_labelbased
from lib.auswertung import grep_highest_intensity
import scipy.signal
import pandas as pd


# suffix_for_new_filename = '_graphMapping.html'
punkte_baseline = analyte.kristallviolett_al_Raja()
band_start = punkte_baseline[0]
band_end = punkte_baseline[1]


list_dateiname = []
for dateiname in os.listdir():
    if dateiname.endswith('.tvf') or dateiname.endswith('.TVF'):
        print(dateiname)
        list_dateiname.append(dateiname)
for i in range(0, len(list_dateiname)):
    if i == 0:
        with open(list_dateiname[i]) as fd:
            intensities = get_intensities(list_dateiname[i])
            times = get_times(list_dateiname[i])
            smoothed_intensities = scipy.signal.savgol_filter(intensities, window_length=9, polyorder=1, axis=0, mode='nearest')
            smoothed_intensities = pd.DataFrame(smoothed_intensities, index=intensities.index, columns=intensities.columns)
            df_korregiert = baselinecorrection(smoothed_intensities, punkte_baseline)
            wn_with_highest_intensity = compute_wn_with_highest_intensity_labelbased(df_korregiert, band_start, band_end)
            highest_intensity = grep_highest_intensity(df_korregiert, wn_with_highest_intensity)
            df_a = highest_intensity
            df_a = df_a.set_index([[list_dateiname[i]]])
            df_a = df_a.transpose()
            df_a = df_a.set_index([list(range(1, len(df_a.index) + 1))])
            df_a = df_a.transpose()
            times = times.transpose()
            times = times.set_index([list(range(1, len(times.index) + 1))])
            times = times.transpose()
            df_a = times.append(df_a)
          #  print(i)
    if i is not 0:
        with open(list_dateiname[i]) as fd:
            intensities = get_intensities(list_dateiname[i])
            smoothed_intensities = scipy.signal.savgol_filter(intensities, window_length=9, polyorder=1, axis=0, mode='nearest')
            smoothed_intensities = pd.DataFrame(smoothed_intensities, index=intensities.index, columns=intensities.columns)
            df_korregiert = baselinecorrection(smoothed_intensities, punkte_baseline)
            wn_with_highest_intensity = compute_wn_with_highest_intensity_labelbased(df_korregiert, band_start, band_end)
            highest_intensity = grep_highest_intensity(df_korregiert, wn_with_highest_intensity)
            df_b = highest_intensity
            df_b = df_b.set_index([[list_dateiname[i]]])
            df_b = df_b.transpose()
            df_b = df_b.set_index([list(range(1, len(df_b.index) + 1))])
            df_b = df_b.transpose()
#            # print(i)
        df_a = df_a.append(df_b)

df_a = df_a.transpose()
df_a.to_csv('smoothed_bscorrOneband_BandsInOne.csv', sep=';')
