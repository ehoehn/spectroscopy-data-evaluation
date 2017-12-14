'''
imput files: mehrere .tvf-TriVista-Dateien mit zeitl Verlauf
output file: eine Datei mit zeitl Verlauf in einer Tabelle nach baseline korrektur
'''
#written by EvaMaria Hoehn


import os
from lib import analyte
from lib.xml_import import get_intensities
from lib.baseline_corr import baselinecorrection
from lib.auswertung import compute_wn_with_highest_intensity
from lib.auswertung import grep_highest_intensity


# suffix_for_new_filename = '_graphMapping.html'
punkte_baseline = analyte.kristallviolett()
band_start = 1605
band_end = 1630


list_dateiname = []
for dateiname in os.listdir():
    if dateiname.endswith('.tvf') or dateiname.endswith('.TVF'):
        print(dateiname)
        list_dateiname.append(dateiname)
for i in range(0, len(list_dateiname)):
    if i == 0:
        with open(list_dateiname[i]) as fd:
            intensities = get_intensities(list_dateiname[i])
            df_korregiert = baselinecorrection(intensities, punkte_baseline)
            wn_with_highest_intensity = compute_wn_with_highest_intensity(df_korregiert, band_start, band_end)
            highest_intensity = grep_highest_intensity(df_korregiert, wn_with_highest_intensity)
            df_a = highest_intensity
            df_a = df_a.set_index([[list_dateiname[i]]])
          #  print(i)
    if i is not 0:
        with open(list_dateiname[i]) as fd:
            intensities = get_intensities(list_dateiname[i])
            df_korregiert = baselinecorrection(intensities, punkte_baseline)
            wn_with_highest_intensity = compute_wn_with_highest_intensity(df_korregiert, band_start, band_end)
            highest_intensity = grep_highest_intensity(df_korregiert, wn_with_highest_intensity)
            df_b = highest_intensity
            df_b = df_b.set_index([[list_dateiname[i]]])
           # print(i)
        df_a = df_a.append(df_b)

df_a.to_csv('Zusammenfassung_Renata_grep.csv', sep=';')


#plotly_zeitlVerlauf_normalisiert(all_highest_intensities)
