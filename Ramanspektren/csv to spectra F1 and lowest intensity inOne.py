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
from Ramanspektren.lib.xml_import import get_intensities
from Ramanspektren.lib.allgemein import generate_filename
from Ramanspektren.lib.auswertung import compute_frame_with_lowest_intensity_labelbased
from Ramanspektren.lib.auswertung import compute_frame_with_lowest_intensity
from Ramanspektren.lib.plotlygraphen import plotly_Spectrum_2dscatter_layout
import scipy.signal
import pandas as pd


# suffix_for_new_filename = '_graphMapping.html'
punkte_baseline = analyte.kristallviolett_al_Raja()
band_start = punkte_baseline[0]
band_end = punkte_baseline[1]



list_dateiname = []
for dateiname in os.listdir():
    if dateiname.endswith('_pdD.csv') or dateiname.endswith('_dD.CSV'):
        print(dateiname)
        list_dateiname.append(dateiname)
for i in range(0, len(list_dateiname)):
    if i == 0:
        with open(list_dateiname[i]) as fd:
            df = pd.read_csv(fd, sep=';', header=0, index_col=0)  # , names=['time [s]', 'measured voltage [V]', 'leer'])
            intensities = pd.DataFrame(df.iloc[1:, 0:])
            times = pd.DataFrame(df.iloc[0, 0:]).transpose()
            # intensities = get_intensities(list_dateiname[i])
            # times = get_times(list_dateiname[i])
            # smoothed_intensities = scipy.signal.savgol_filter(intensities, window_length=9, polyorder=1, axis=0, mode='nearest')
            # smoothed_intensities = pd.DataFrame(smoothed_intensities, index=intensities.index, columns=intensities.columns)
            # #      print(smoothed_intensities)
            # #df_out = smoothed_intensities.apply(lambda x: x - x.min())
            # df_out = baselinecorrection(smoothed_intensities, punkte_baseline)

          #  print(df_out)
            df_a = pd.DataFrame(intensities['Frame 1'])
            df_a[list_dateiname[i] + ' Frame 1'] = df_a['Frame 1']
            df_a = df_a.drop(labels=['Frame 1'], axis=1)
            #print(df_a)
            # wn_with_highest_intensity = compute_wn_with_highest_intensity_labelbased(df_out, band_start, band_end)
            # highest_intensity = grep_highest_intensity(df_out, wn_with_highest_intensity)
            # df_a = highest_intensity
            # df_a = df_a.set_index([[list_dateiname[i]]])
            # df_a = df_a.transpose()
            # df_a = df_a.set_index([list(range(1, len(df_a.index) + 1))])
            # df_a = df_a.transpose()
         #   print(df_a)
       #     print(intensities)
            framenumber = compute_frame_with_lowest_intensity(intensities, band_start, band_end)
    #       print(framenumber)
            df_a[list_dateiname[i] + ' Frame ' + str(framenumber)] = intensities['Frame ' + str(framenumber)]
     #       print(df_a)
#             times = times.transpose()
#             times = times.set_index([list(range(1, len(times.index) + 1))])
#             times = times.transpose()
#             df_a = times.append(df_a)
#           #  print(i)
    if i is not 0:
        with open(list_dateiname[i]) as fd:
            df = pd.read_csv(fd, sep=';', header=0, index_col=0)  # , names=['time [s]', 'measured voltage [V]', 'leer'])
            intensities = pd.DataFrame(df.iloc[1:, 0:])
            times = pd.DataFrame(df.iloc[0, 0:]).transpose()
            # intensities = get_intensities(list_dateiname[i])
            # smoothed_intensities = scipy.signal.savgol_filter(intensities, window_length=9, polyorder=1, axis=0, mode='nearest')
            # smoothed_intensities = pd.DataFrame(smoothed_intensities, index=intensities.index, columns=intensities.columns)
            # #      print(smoothed_intensities)
            # df_out = smoothed_intensities.apply(lambda x: x - x.min())
            df_b = pd.DataFrame(intensities['Frame 1'])
            df_a[list_dateiname[i] + ' Frame 1'] = df_b['Frame 1']
         #   print(df_b)
            df_b = df_b.drop(labels=['Frame 1'], axis=1)
        #    print(df_b)
            # wn_with_highest_intensity = compute_wn_with_highest_intensity_labelbased(df_out, band_start, band_end)
            # highest_intensity = grep_highest_intensity(df_out, wn_with_highest_intensity)
            # df_a = highest_intensity
            # df_a = df_a.set_index([[list_dateiname[i]]])
            # df_a = df_a.transpose()
            # df_a = df_a.set_index([list(range(1, len(df_a.index) + 1))])
            # df_a = df_a.transpose()
            #   print(df_a)
            framenumber = compute_frame_with_lowest_intensity(intensities, band_start, band_end)
            print(framenumber)
            df_a[list_dateiname[i] + ' Frame ' + str(framenumber)] = intensities['Frame ' + str(framenumber)]
            print(df_b)
        #df_a = df_a.append(df_b)
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
df_a.to_csv('spectra alternating F1 and lowest intensities_w9_o1_s_pdDGraph.csv', sep=';')
#
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
