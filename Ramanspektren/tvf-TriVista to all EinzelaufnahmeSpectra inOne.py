'''
imput files: mehrere .tvf-TriVista-Dateien mit zeitl Verlauf
output file: eine Datei mit zeitl Verlauf in einer Tabelle nach baseline korrektur
'''
#written by EvaMaria Hoehn


import os
from lib.xml_import import get_intensities, get_times
from Ramanspektren.lib.xml_import import get_intensities
import scipy.signal
import pandas as pd


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
            df_a = output
    if i is not 0:
        with open(list_dateiname[i]) as fd:
            output = verarbeitungderdaten(list_dateiname[i])
            df_b = output
            df_b = df_b.set_index(df_a.index)
        df_a[list_dateiname[i]] = df_b.iloc[:,0]

df_a.to_csv('alleSpektrenInEinem_w9_o1_s_pdD para-Mercaptobenzoic acid.csv', sep=';')
