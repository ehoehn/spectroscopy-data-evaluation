'''
imput files: mehrere .tvf-TriVista-Dateien mit zeitl Verlauf
output file: eine Datei mit zeitl Verlauf in einer Tabelle nach baseline korrektur
'''
#written by EvaMaria Hoehn


import os
import lib.analyte
from lib.xml_import import get_intensities
from lib.baseline_corr import baselinecorrection
from lib.auswertung import compute_wn_with_highest_intensity_labelbased
from lib.auswertung import grep_highest_intensity
import pandas as pd
from lib.allgemein import generate_filename


# suffix_for_new_filename = '_graphMapping.html'
punkte_baseline = lib.analyte.kristallviolett_al_Raja()
band_start = punkte_baseline[0]
band_end = punkte_baseline[1]


# for dateiname in os.listdir():
#     if dateiname.endswith('smoothed.csv') or dateiname.endswith('smoothed.CSV'):
#         print(dateiname)
#         with open(dateiname, 'r') as fd:
#             df = pd.read_csv(fd, sep=';', header=0, index_col=0) #, names=['time [s]', 'measured voltage [V]', 'leer'])
#             intensities = pd.DataFrame(df.iloc[1:,0:])
#             df_out = intensities.transform(lambda x: x - x.min())
#             df_out.to_csv(generate_filename(dateiname, '_drawnDown.csv'), sep=';')
# list_dateiname = []
for dateiname in os.listdir():
    if dateiname.endswith('_dD.csv') or dateiname.endswith('_drawnDown.csv'):
        print(dateiname)
#         list_dateiname.append(dateiname)
# for i in range(0, len(list_dateiname)):
#     if i == 0:
        with open(dateiname) as fd:
            df = pd.read_csv(fd, sep=';', header=0, index_col=0)  # , names=['time [s]', 'measured voltage [V]', 'leer'])
            times = pd.DataFrame(df.iloc[0, 0:]).transpose()
            intensities = pd.DataFrame(df.iloc[1:, 0:])
        #    print(intensities)
            wn_with_highest_intensity = compute_wn_with_highest_intensity_labelbased(intensities, band_start, band_end)
         #   print(wn_with_highest_intensity)
            highest_intensity = pd.DataFrame(grep_highest_intensity(intensities, wn_with_highest_intensity))
            df_a = highest_intensity
            df_a = df_a.set_index([['Intensity [a. u.]']])
            df_a = df_a.transpose()
            df_a = df_a.set_index([list(range(1, len(df_a.index)+1))])
            df_a = df_a.transpose()
            times = times.transpose()
            times = times.set_index([list(range(1, len(times.index) + 1))])
            times = times.transpose()
            df_a = times.append(df_a)
            df_a = df_a.transpose()
        #    print(df_a)
    # if i is not 0:
    #     with open(list_dateiname[i]) as fd:
    #         df = pd.read_csv(fd, sep=';', header=0, index_col=0)  # , names=['time [s]', 'measured voltage [V]', 'leer'])
    #         intensities = pd.DataFrame(df.iloc[1:, 0:])
    #         wn_with_highest_intensity = compute_wn_with_highest_intensity_labelbased(intensities, band_start, band_end)
    #         highest_intensity = pd.DataFrame(grep_highest_intensity(intensities, wn_with_highest_intensity))
    #         df_b = highest_intensity
    #         df_b = df_b.set_index([[list_dateiname[i]]])
    #         df_b = df_b.transpose()
    #         df_b = df_b.set_index([list(range(1, len(df_b.index) + 1))])
    #         df_b = df_b.transpose()
    #        # print(df_b)
    # # #        # print(i)
    #     df_a = df_a.append(df_b)
#print(df_a)
# df_a = df_a.transpose()
# #print(df_a)
# if list_dateiname[0].split('_').count('primitive') == 1:
#     df_a.to_csv('allIndicatorBandsInOne_primitive_bscorr.csv', sep=';')
# else:
#     df_a.to_csv('allIndicatorBandsInOne.csv', sep=';')

            df_a.to_csv(generate_filename(dateiname, '_IndBand.csv'), sep=';')


#plotly_zeitlVerlauf_normalisiert(all_highest_intensities)
