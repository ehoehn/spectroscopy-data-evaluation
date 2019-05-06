import os
from lib.xml_import import get_intensities, get_times
from lib.baseline_corr import baselinecorrection
from lib.auswertung import compute_wn_with_highest_intensity_labelbased
from lib.auswertung import grep_highest_intensity
from lib.xml_import import get_intensities
from lib.allgemein import generate_filename
from lib.auswertung import compute_frame_with_lowest_intensity_labelbased
from lib.plotlygraphen import plotly_Spectrum_2dscatter_layout
import scipy.signal
import pandas as pd
import os
from lib.xml_import import get_intensities
from lib.baseline_corr import baselinecorrection
from lib.auswertung import compute_wn_with_highest_intensity_labelbased
from lib.auswertung import grep_highest_intensity
import pandas as pd



list_dateiname = []
for dateiname in os.listdir():
    if dateiname.endswith('.csv') or dateiname.endswith('.TVF'):
        print(dateiname)
        list_dateiname.append(dateiname)
for i in range(0, len(list_dateiname)):
    if i == 0:
        with open(list_dateiname[i]) as fd:
            df = pd.read_csv(fd, sep=';', header=None,
                             index_col=None)  # , names=['time [s]', 'measured voltage [V]', 'leer'])
            df_a = pd.DataFrame(df[0])
            print(df[df.columns[0]])
            for c in df.columns:
              #  print(c)

                df_a[list_dateiname[i] + ' ' + str(df.columns[c])] = df[df.columns[c]]
                #df_a = df_a.drop(labels=['0'], axis=1)
                #df_a([list_dateiname[i] + df.columns[c]] = df.columns[c])
 #           df_a = df_a.drop(labels=['Frame 1'], axis=1)
 #    if i is not 0:
 #        with open(list_dateiname[i]) as fd:
 #            df = pd.read_csv(fd, sep=';', header=None,
 #                             index_col=None)  # , names=['time [s]', 'measured voltage [V]', 'leer'])
 #            df_a = df
           # print(df)
            print(df_a)




"""

'''
imput files: mehrere .tvf-TriVista-Dateien mit zeitl Verlauf
output file: eine Datei mit zeitl Verlauf in einer Tabelle nach baseline korrektur
'''
#written by EvaMaria Hoehn





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
            #      print(smoothed_intensities)
            df_out = smoothed_intensities.apply(lambda x: x - x.min())
            df_a = pd.DataFrame(df_out['Frame 1'])
            df_a[list_dateiname[i] + ' Frame 1'] = df_a['Frame 1']
            df_a = df_a.drop(labels=['Frame 1'], axis=1)
            # wn_with_highest_intensity = compute_wn_with_highest_intensity_labelbased(df_out, band_start, band_end)
            # highest_intensity = grep_highest_intensity(df_out, wn_with_highest_intensity)
            # df_a = highest_intensity
            # df_a = df_a.set_index([[list_dateiname[i]]])
            # df_a = df_a.transpose()
            # df_a = df_a.set_index([list(range(1, len(df_a.index) + 1))])
            # df_a = df_a.transpose()
         #   print(df_a)
            framenumber = compute_frame_with_lowest_intensity_labelbased(df_out, band_start, band_end)
            print(framenumber)
            df_a[list_dateiname[i] + ' Frame ' + str(framenumber)] = df_out['Frame ' + str(framenumber)]
            print(df_a)
#             times = times.transpose()
#             times = times.set_index([list(range(1, len(times.index) + 1))])
#             times = times.transpose()
#             df_a = times.append(df_a)
#           #  print(i)
    if i is not 0:
        with open(list_dateiname[i]) as fd:
            intensities = get_intensities(list_dateiname[i])
            smoothed_intensities = scipy.signal.savgol_filter(intensities, window_length=9, polyorder=1, axis=0, mode='nearest')
            smoothed_intensities = pd.DataFrame(smoothed_intensities, index=intensities.index, columns=intensities.columns)
            #      print(smoothed_intensities)
            df_out = smoothed_intensities.apply(lambda x: x - x.min())
            df_b = pd.DataFrame(df_out['Frame 1'])
            df_a[list_dateiname[i] + ' Frame 1'] = df_b['Frame 1']
            df_b = df_b.drop(labels=['Frame 1'], axis=1)
            # wn_with_highest_intensity = compute_wn_with_highest_intensity_labelbased(df_out, band_start, band_end)
            # highest_intensity = grep_highest_intensity(df_out, wn_with_highest_intensity)
            # df_a = highest_intensity
            # df_a = df_a.set_index([[list_dateiname[i]]])
            # df_a = df_a.transpose()
            # df_a = df_a.set_index([list(range(1, len(df_a.index) + 1))])
            # df_a = df_a.transpose()
            #   print(df_a)
            framenumber = compute_frame_with_lowest_intensity_labelbased(df_out, band_start, band_end)
            print(framenumber)
            df_a[list_dateiname[i] + ' Frame ' + str(framenumber)] = df_out['Frame ' + str(framenumber)]
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
df_a.to_csv('spectra alternating F1 and lowest intensities_w9_o1_s_pdD.csv', sep=';')
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


"""



"""

'''
imput files: mehrere .tvf-TriVista-Dateien mit zeitl Verlauf
output file: eine Datei mit zeitl Verlauf in einer Tabelle nach baseline korrektur
'''
#written by EvaMaria Hoehn





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
list_dateiname = []
for dateiname in os.listdir():
    if dateiname.endswith('_dD.csv') or dateiname.endswith('_drawnDown.csv'):
        print(dateiname)
        list_dateiname.append(dateiname)
for i in range(0, len(list_dateiname)):
    if i == 0:
        with open(list_dateiname[i]) as fd:
            df = pd.read_csv(fd, sep=';', header=0, index_col=0)  # , names=['time [s]', 'measured voltage [V]', 'leer'])
            times = pd.DataFrame(df.iloc[0, 0:]).transpose()
            intensities = pd.DataFrame(df.iloc[1:, 0:])
        #    print(intensities)
            wn_with_highest_intensity = compute_wn_with_highest_intensity_labelbased(intensities, band_start, band_end)
         #   print(wn_with_highest_intensity)
            highest_intensity = pd.DataFrame(grep_highest_intensity(intensities, wn_with_highest_intensity))
            df_a = highest_intensity
            df_a = df_a.set_index([[list_dateiname[i]]])
            df_a = df_a.transpose()
            df_a = df_a.set_index([list(range(1, len(df_a.index)+1))])
            df_a = df_a.transpose()
            times = times.transpose()
            times = times.set_index([list(range(1, len(times.index) + 1))])
            times = times.transpose()
            df_a = times.append(df_a)
      #  print(df_a)
    if i is not 0:
        with open(list_dateiname[i]) as fd:
            df = pd.read_csv(fd, sep=';', header=0, index_col=0)  # , names=['time [s]', 'measured voltage [V]', 'leer'])
            intensities = pd.DataFrame(df.iloc[1:, 0:])
            wn_with_highest_intensity = compute_wn_with_highest_intensity_labelbased(intensities, band_start, band_end)
            highest_intensity = pd.DataFrame(grep_highest_intensity(intensities, wn_with_highest_intensity))
            df_b = highest_intensity
            df_b = df_b.set_index([[list_dateiname[i]]])
            df_b = df_b.transpose()
            df_b = df_b.set_index([list(range(1, len(df_b.index) + 1))])
            df_b = df_b.transpose()
           # print(df_b)
    # #        # print(i)
        df_a = df_a.append(df_b)
#print(df_a)
df_a = df_a.transpose()
#print(df_a)
if list_dateiname[0].split('_').count('primitive') == 1:
    df_a.to_csv('allIndicatorBandsInOne_primitive_bscorr.csv', sep=';')
else:
    df_a.to_csv('allIndicatorBandsInOne.csv', sep=';')


#plotly_zeitlVerlauf_normalisiert(all_highest_intensities)


"""