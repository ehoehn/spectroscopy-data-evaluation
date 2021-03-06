﻿'''
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
from Ramanspektren.lib.xml_import import get_intensities
from Ramanspektren.lib.allgemein import generate_filename
from Ramanspektren.lib.auswertung import compute_frame_with_lowest_intensity_labelbased
from Ramanspektren.lib.plotlygraphen import plotly_Spectrum_2dscatter_layout
import scipy.signal
import pandas as pd
import os
import plotly.graph_objs as go  #import Scatter, Layout
import plotly
import scipy.signal
import pandas as pd
from lib.allgemein import generate_filename
import Ramanspektren.lib.xml_import
import Ramanspektren.lib.baseline_corr


# suffix_for_new_filename = '_graphMapping.html'
# punkte_baseline = analyte.kristallviolett_al_Raja()
# band_start = punkte_baseline[0]
# band_end = punkte_baseline[1]


def verarbeitungderdaten(dateinamei):
    intensities = get_intensities(dateinamei)
    smoothed_intensities = scipy.signal.savgol_filter(intensities, window_length=9, polyorder=1, axis=0, mode='nearest')
    smoothed_intensities = pd.DataFrame(smoothed_intensities, index=intensities.index, columns=intensities.columns)
    df_out = smoothed_intensities.apply(lambda x: x - x.min())
    df_a = pd.DataFrame(df_out['Intensity [a. u.]'])
    df_a[dateinamei] = df_a['Intensity [a. u.]']
    df_a = df_a.drop(labels=['Intensity [a. u.]'], axis=1)
    return df_a


list_dateiname = []
for dateiname in os.listdir():
   if dateiname.endswith('.tvf') or dateiname.endswith('.TVF'):
        print(dateiname)
        list_dateiname.append(dateiname)
for i in range(0, len(list_dateiname)):
    if i == 0:
        with open(list_dateiname[i]) as fd:
            output = verarbeitungderdaten(list_dateiname[i])
          #  print(output)
            df_a = output
          #  print(df_a)
            # wn_with_highest_intensity = compute_wn_with_highest_intensity_labelbased(df_out, band_start, band_end)
            # highest_intensity = grep_highest_intensity(df_out, wn_with_highest_intensity)
            # df_a = highest_intensity
            # df_a = df_a.set_index([[list_dateiname[i]]])
            # df_a = df_a.transpose()
            # df_a = df_a.set_index([list(range(1, len(df_a.index) + 1))])
            # df_a = df_a.transpose()
         #   print(df_a)
         #    framenumber = compute_frame_with_lowest_intensity_labelbased(df_out, band_start, band_end)
         #    print(framenumber)
         #    df_a[list_dateiname[i] + ' Frame ' + str(framenumber)] = df_out['Frame ' + str(framenumber)]
         #    print(df_a)
#             times = times.transpose()
#             times = times.set_index([list(range(1, len(times.index) + 1))])
#             times = times.transpose()
#             df_a = times.append(df_a)
#           #  print(i)
    if i is not 0:
        with open(list_dateiname[i]) as fd:
            output = verarbeitungderdaten(list_dateiname[i])
            df_b = output
            # print(output)
          #  df_a[list_dateiname[i]] = df_b.iloc[:,0]
          #   print(df_a)
          #   print(df_b.iloc[:,0])
          #   print(df_a.index)
            df_b = df_b.set_index(df_a.index)
            # df_voltage = pd.DataFrame(df_b).rename(index=df_a.index)
            # print(df_b)
        df_a[list_dateiname[i]] = df_b.iloc[:,0]
print(df_a)

#             smoothed_intensities = scipy.signal.savgol_filter(intensities, window_length=9, polyorder=1, axis=0, mode='nearest')
#             smoothed_intensities = pd.DataFrame(smoothed_intensities, index=intensities.index, columns=intensities.columns)
#             df_korregiert = baselinecorrection(smoothed_intensities, punkte_baseline)
#             wn_with_highest_intensity = compute_wn_with_highest_intensity_labelbased(df_korregiert, band_start, band_end)
#             highest_intensity = grep_highest_intensity(df_korregiert, wn_with_highest_intensity)
#             df_b = highest_intensity
#             df_b = df_b.set_index([[list_dateiname[i]]])
#             df_b = df_b.transpose()
#             df_b = df_b.set_index([list(range(1, len(df_b.index) + 1))])
#             df_b = df_b.transpose()
# #            # print(i)
#         df_a = df_a.append(df_b)
#
# df_a = df_a.transpose()
df_a.to_csv('alleSpektrenInEinem_w9_o1_s_pdD Brilliantblau.csv', sep=';')
#df_a.to_csv(generate_filename(list_dateiname[i], 'spec_alt_F1_lowest_int_w9_o1_s_pdD.csv'), sep=';')

#


 #       print(intensities)

#
#
#         print(df_a)
#     df_a.to_csv('spectra alternating F1 and lowest intensities.csv', sep=';')
#
#         # plotly_SpectrumMitNiedrigsterIntensitaet(intensities, dateiname)
#         # df_korregiert = baselinecorrection(intensities, punkte_baseline)
#         # wn_with_highest_intensity = compute_wn_with_highest_intensity(df_korregiert, band_start, band_end)
#         # highest_intensity = grep_highest_intensity(df_korregiert, wn_with_highest_intensity)
#         #
#         # try:
#         #     positions = get_positions(dateiname)
#         # except:
#         #     print('no positions')
#     #    df_out.to_csv('alks.csv', sep=';')
