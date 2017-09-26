'''
imput file: .csv-Datei aus Osziloskop
output file: eine Datei mit allen Kennzahlen
'''
#written by EvaMaria Hoehn


import os
import numpy as np
import pandas as pd
import scipy.signal


used_resistor = 1000 # in [Ohm]


def get_voltage(dateiname):
    nr = dateiname.split('_')
    nr = nr[3]
    nr = nr.split('.')
    nr = nr[0]
    nr = nr[:-1]
    nr = nr.replace(',', '.')
    voltage = float(nr)
    return voltage


def import_from_oszi_data(dateiname):
    df = pd.read_csv(dateiname, sep=',', header=0, index_col=0, skiprows=16, names=['time [s]', 'measured voltage [V]', 'leer'])
    del df['leer']
    df1 = df.replace('Null', np.nan)
    df1.dropna(axis=0, how='all', inplace=True)
    df2 = df1.apply(pd.to_numeric, errors='raise')
    return df2

def get_current(df, used_resistor):
    df_current = pd.DataFrame(df['measured voltage [V] smoothed'] / used_resistor).rename(columns={'measured voltage [V] smoothed':'current [A]'})
    df_current['current [mA]'] = df_current['current [A]'] * 1000
    df_current['current [µA]'] = df_current['current [mA]'] * 1000
    return df_current

def split_in_sections(data_to_cut, cutting_points, applyed_voltage):
    copy_data_to_cut = data_to_cut.copy()
    for i in range(0, len(cutting_points) - 1):
        if i == 0:
            points = [cutting_points[i], cutting_points[i + 1]]
            kurvenabschnitt = copy_data_to_cut.ix[points[0]:points[1]]
            bearbeitet = bearbeitung(kurvenabschnitt, cutting_points, i, applyed_voltage)
            a = bearbeitet.ix[cutting_points[i]:cutting_points[i + 1]]
        else:
            points = [cutting_points[i], cutting_points[i + 1]]
            kurvenabschnitt = copy_data_to_cut.ix[points[0]:points[1]]
            bearbeitet = bearbeitung(kurvenabschnitt, cutting_points, i, applyed_voltage)
            b = bearbeitet.ix[cutting_points[i] + 1:cutting_points[i + 1]]
            a = a.append(b)
    ndata_to_cut = copy_data_to_cut - copy_data_to_cut + a
    ndata_to_cut = ndata_to_cut.fillna(0)
    return ndata_to_cut

def bearbeitung(kurvenabschnitt, cutting_points, i, applyed_voltage):  # , [spectrum_values[i]: spectrum_values[i + 1]]):
    copy_kurvenabschnitt = kurvenabschnitt.copy()
    dataset = copy_kurvenabschnitt.ix[cutting_points[i] : cutting_points[i + 1]]
    dataset = applyed_voltage - abs(dataset)
    return dataset

def get_voltage_in_chip(df, applyed_voltage):
    predf_voltage = split_in_sections(df['measured voltage [V] smoothed'], [34, 145], applyed_voltage)
    df_voltage = pd.DataFrame(predf_voltage).rename(columns={'measured voltage [V] smoothed':'in chip voltage [V]'})
    return df_voltage

list_dateiname = []
for dateiname in os.listdir():
    if dateiname.endswith('.csv') or dateiname.endswith('.CSV'):
        print(dateiname)
        list_dateiname.append(dateiname)
for i in range(0, len(list_dateiname)):
    if i == 0:
        with open(list_dateiname[i]) as fd:
            measured_voltages = import_from_oszi_data(list_dateiname[i])
            measured_voltages['measured voltage [V] smoothed'] = scipy.signal.savgol_filter(measured_voltages, window_length=21, polyorder=1, axis=0, mode='nearest')  # ggf auch polyorder=2 oder 3
            current = get_current(measured_voltages, used_resistor)
            in_chip_voltage = get_voltage_in_chip(measured_voltages, get_voltage(list_dateiname[i]))
            df_in_chip_data = in_chip_voltage.copy()
            df_in_chip_data['current [µA]'] = current['current [µA]']
            maxima = df_in_chip_data.apply(max, axis=0)
            maxima['in chip resistance [Ohm]'] = maxima['in chip voltage [V]'] * 1000000 / maxima['current [µA]']  # resistance [Ohm]
            df_maxima = (pd.DataFrame(maxima, index=maxima.index)).transpose()
            df_a = df_maxima
            df_a = df_a.set_index([[list_dateiname[i]]])
    if i is not 0:
        with open(list_dateiname[i]) as fd:
            measured_voltages = import_from_oszi_data(list_dateiname[i])
            measured_voltages['measured voltage [V] smoothed'] = scipy.signal.savgol_filter(measured_voltages, window_length=21, polyorder=1, axis=0, mode='nearest')  # ggf auch polyorder=2 oder 3
            current = get_current(measured_voltages, used_resistor)
            in_chip_voltage = get_voltage_in_chip(measured_voltages, get_voltage(list_dateiname[i]))
            df_in_chip_data = in_chip_voltage.copy()
            df_in_chip_data['current [µA]'] = current['current [µA]']
            maxima = df_in_chip_data.apply(max, axis=0)
            maxima['in chip resistance [Ohm]'] = maxima['in chip voltage [V]'] * 1000000 / maxima['current [µA]']  # resistance [Ohm]
            df_maxima = (pd.DataFrame(maxima, index=maxima.index)).transpose()
            df_b = df_maxima
            df_b = df_b.set_index([[list_dateiname[i]]])
           # print(i)
        df_a = df_a.append(df_b)

df_a.to_csv('OsziData_allImportantNumbersIn1.csv', sep=';')
