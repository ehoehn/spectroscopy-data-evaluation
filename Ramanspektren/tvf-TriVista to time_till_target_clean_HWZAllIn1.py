'''
imput file: .tvf-TriVista-Datei
output file: ein Graph mit 3 Spektren: Frame1, Frame100 und den Frame mit der Minimalintensität
output file: Zeit bis Target sauber ist nach baseline correctur und smoothing via Sawitzky-Golay-Filter
'''
#written by EvaMaria Hoehn

import os
from lib import analyte
import pandas as pd
import numpy as np
from Ramanspektren.lib.auswertung import compute_frame_with_lowest_intensity_from_smoothed
from Ramanspektren.lib.auswertung import compute_wn_with_highest_intensity
from Ramanspektren.lib.auswertung import grep_highest_intensity
from Ramanspektren.lib.baseline_corr import baselinecorrection
from Ramanspektren.lib.xml_import import get_intensities
from Ramanspektren.lib.xml_import import get_times
from Ramanspektren.lib.auswertung import savitzkygolay_for_pandas


suffix_for_new_filename_5spektren_in1graph = '_graph5spektren.html'
suffix_for_new_filename_zeitlVerlauf = '_smooth_HWZ_graphzeitlVerlauf.html'
punkte_baseline = analyte.kristallviolett()
band_start = 1605
band_end = 1630


list_dateiname = []
for dateiname in os.listdir():
    if dateiname.endswith('_beiF1Analyt_beiF20ElektrolythFlussAn_beiF200SpannungAn_beiF300SpannungAus.tvf') or dateiname.endswith('_beiF1Analyt_beiF20ElektrolythFlussAn_beiF200SpannungAn_beiF300SpannungAus.TVF'):
        print(dateiname)
        list_dateiname.append(dateiname)
for i in range(0, len(list_dateiname)):
    if i == 0:
        with open(list_dateiname[i]) as fd:
            intensities = get_intensities(list_dateiname[i])
            times = get_times(list_dateiname[i])
            df_korregiert = baselinecorrection(intensities, punkte_baseline)
            wn_with_highest_intensity = compute_wn_with_highest_intensity(df_korregiert, band_start, band_end)
            highest_intensity = grep_highest_intensity(df_korregiert, wn_with_highest_intensity)
            smoothed = savitzkygolay_for_pandas(highest_intensity, window_length=21, polyorder=3)
            framenumber = compute_frame_with_lowest_intensity_from_smoothed(smoothed)
            vonTangenteAus = smoothed - smoothed['Frame ' + str(framenumber)].values.tolist()[0]
            timeTillRegAfterDifferenzHWZ = []
            NoOfHWZ_list = []
            NoOfHWZ = 1  # wie viele Halbwertszeiten
            intNachHWZ = smoothed['Frame 200'] / (2 ** NoOfHWZ)
            SignalConsideredAway = vonTangenteAus.columns[
                vonTangenteAus.ix['highest intensity [a. u.]'] < (intNachHWZ.values.tolist()[0])]
            timeTillReg = times[SignalConsideredAway[0]] - times['Frame 200']
            timeTillReg = np.float64(timeTillReg)
            timeTillRegAfterDifferenzHWZ.append(timeTillReg)
            NoOfHWZ_list.append(NoOfHWZ)
            while len(SignalConsideredAway) > 1:
                NoOfHWZ = NoOfHWZ + 1  # wie viele Halbwertszeiten
                intNachHWZ = smoothed['Frame 200'] / (2 ** NoOfHWZ)
                SignalConsideredAway = vonTangenteAus.columns[
                    vonTangenteAus.ix['highest intensity [a. u.]'] < (intNachHWZ.values.tolist()[0])]
                timeTillReg = times[SignalConsideredAway[0]] - times['Frame 200']
                timeTillReg = np.float64(timeTillReg)
                timeTillRegAfterDifferenzHWZ.append(timeTillReg)
                NoOfHWZ_list.append(NoOfHWZ)
            df_timeTillRegAfterDifferentHZW = pd.DataFrame(timeTillRegAfterDifferenzHWZ, index=[NoOfHWZ_list], columns=[list_dateiname[i]])
            df_timeTillRegAfterDifferentHZW = df_timeTillRegAfterDifferentHZW.transpose()
            df_a = df_timeTillRegAfterDifferentHZW
            df_a = df_a.set_index([[list_dateiname[i]]])
          #  print(i)
    if i is not 0:
        with open(list_dateiname[i]) as fd:
            intensities = get_intensities(list_dateiname[i])
            times = get_times(list_dateiname[i])
            df_korregiert = baselinecorrection(intensities, punkte_baseline)
            wn_with_highest_intensity = compute_wn_with_highest_intensity(df_korregiert, band_start, band_end)
            highest_intensity = grep_highest_intensity(df_korregiert, wn_with_highest_intensity)
            smoothed = savitzkygolay_for_pandas(highest_intensity, window_length=21, polyorder=3)
            framenumber = compute_frame_with_lowest_intensity_from_smoothed(smoothed)
            vonTangenteAus = smoothed - smoothed['Frame ' + str(framenumber)].values.tolist()[0]
            timeTillRegAfterDifferenzHWZ = []
            NoOfHWZ_list = []
            NoOfHWZ = 1  # wie viele Halbwertszeiten
            intNachHWZ = smoothed['Frame 200'] / (2 ** NoOfHWZ)
            SignalConsideredAway = vonTangenteAus.columns[
                vonTangenteAus.ix['highest intensity [a. u.]'] < (intNachHWZ.values.tolist()[0])]
            timeTillReg = times[SignalConsideredAway[0]] - times['Frame 200']
            timeTillReg = np.float64(timeTillReg)
            timeTillRegAfterDifferenzHWZ.append(timeTillReg)
            NoOfHWZ_list.append(NoOfHWZ)
            while len(SignalConsideredAway) > 1:
                NoOfHWZ = NoOfHWZ + 1  # wie viele Halbwertszeiten
                intNachHWZ = smoothed['Frame 200'] / (2 ** NoOfHWZ)
                SignalConsideredAway = vonTangenteAus.columns[
                    vonTangenteAus.ix['highest intensity [a. u.]'] < (intNachHWZ.values.tolist()[0])]
                timeTillReg = times[SignalConsideredAway[0]] - times['Frame 200']
                timeTillReg = np.float64(timeTillReg)
                timeTillRegAfterDifferenzHWZ.append(timeTillReg)
                NoOfHWZ_list.append(NoOfHWZ)
            df_timeTillRegAfterDifferentHZW = pd.DataFrame(timeTillRegAfterDifferenzHWZ, index=[NoOfHWZ_list], columns=[list_dateiname[i]])
            df_timeTillRegAfterDifferentHZW = df_timeTillRegAfterDifferentHZW.transpose()
            df_b = df_timeTillRegAfterDifferentHZW
            df_b = df_b.set_index([[list_dateiname[i]]])
           # print(i)
        df_a = df_a.append(df_b)

df_a.to_csv('Zusammenfassung_time_till_target_clean_HWZ.csv', sep=';')

