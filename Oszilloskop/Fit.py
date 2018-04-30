'''
imput file: .csv-Datei aus Osziloskop
output file: eine Datei mit allen Kennzahlen, die nach Glattung einer berechnet wurden
'''
#written by EvaMaria Hoehn


import os
import numpy as np
import pandas as pd
import scipy.signal
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from decimal import *

# used_resistor = 1000 # in [Ohm]
#
# def generate_filename(dateiname, suffix_for_new_filename):
#     name = dateiname.split('.')
#     del name[-1]
#     separator = "."
#     nwname = separator.join(name)
#     nwfile = nwname + suffix_for_new_filename
#     return nwfile
#
# def get_voltage(dateiname):
#     nr = dateiname.split('_')
#     for i in nr:
#         if i.endswith('V'):
#             if not i.endswith('CSV'):
#                 nr = i[:-1]
#                 nr = nr.replace(',', '.')
#                 voltage = float(nr)
#     return voltage
#
# def import_from_oszi_data(dateiname):
#     df = pd.read_csv(dateiname, sep=',', header=0, index_col=0, skiprows=16, names=['time [s]', 'measured voltage [V]', 'leer'])
#     del df['leer']
#     df1 = df.replace('Null', np.nan)
#     df1.dropna(axis=0, how='all', inplace=True)
#     df2 = df1.apply(pd.to_numeric, errors='raise')
#     return df2
#
# def get_current(df, used_resistor):
#     df_current = pd.DataFrame(df['measured voltage [V] smoothed'] / used_resistor).rename(columns={'measured voltage [V] smoothed':'current [A]'})
#     df_current['current [mA]'] = df_current['current [A]'] * 1000
#     df_current['current [µA]'] = df_current['current [mA]'] * 1000
#     return df_current
#
# def split_in_sections(data_to_cut, cutting_points, applyed_voltage):
#     copy_data_to_cut = data_to_cut.copy()
#     for i in range(0, len(cutting_points) - 1):
#         if i == 0:
#             points = [cutting_points[i], cutting_points[i + 1]]
#             kurvenabschnitt = copy_data_to_cut.ix[points[0]:points[1]]
#             bearbeitet = bearbeitung(kurvenabschnitt, cutting_points, i, applyed_voltage)
#             a = bearbeitet.ix[cutting_points[i]:cutting_points[i + 1]]
#         else:
#             points = [cutting_points[i], cutting_points[i + 1]]
#             kurvenabschnitt = copy_data_to_cut.ix[points[0]:points[1]]
#             bearbeitet = bearbeitung(kurvenabschnitt, cutting_points, i, applyed_voltage)
#             b = bearbeitet.ix[cutting_points[i] + 1:cutting_points[i + 1]]
#             a = a.append(b)
#     ndata_to_cut = copy_data_to_cut - copy_data_to_cut + a
#     ndata_to_cut = ndata_to_cut.fillna(0)
#     return ndata_to_cut
#
# def bearbeitung(kurvenabschnitt, cutting_points, i, applyed_voltage):  # , [spectrum_values[i]: spectrum_values[i + 1]]):
#     copy_kurvenabschnitt = kurvenabschnitt.copy()
#     dataset = copy_kurvenabschnitt.ix[cutting_points[i] : cutting_points[i + 1]]
#     dataset = applyed_voltage - abs(dataset)
#     return dataset
#
# def get_voltage_in_chip(df, applyed_voltage):
#     predf_voltage = split_in_sections(df['measured voltage [V] smoothed'], [34, 145], applyed_voltage)
#     df_voltage = pd.DataFrame(predf_voltage).rename(columns={'measured voltage [V] smoothed':'in chip voltage [V]'})
#     return df_voltage
#
# # list_dateiname = []
# # for dateiname in os.listdir():
# #     if dateiname.endswith('.csv') or dateiname.endswith('.CSV'):
# #         print(dateiname)
# #         list_dateiname.append(dateiname)
# # for i in range(0, len(list_dateiname)):
# #     if i == 0:
# #         with open(list_dateiname[i]) as fd:
# #             measured_voltages = import_from_oszi_data(list_dateiname[i])
# #           #  print(measured_voltages)


def liste_in_decimals_umwandeln(input):
    ft = []
    for i in input:
        k = Decimal(i)
        ft.append(k)
    return ft

def liste_in_floats_umwandeln(input):
    ft = []
    for i in input:
        k = np.float64(i)
        ft.append(k)
    return ft

def generate_filename(dateiname, suffix_for_new_filename):
    name = dateiname.split('.')
    del name[-1]
    separator = "."
    nwname = separator.join(name)
    nwfile = nwname + suffix_for_new_filename
    return nwfile


def fit_func(x, A0, frequ, Lambda):
    return A0 * np.sin(x * 2 * np.pi * 1/frequ + Lambda)


for dateiname in os.listdir():
    if dateiname.endswith('180427_16_5MHz_DS0008_w21_o1_s.csv'): # or dateiname.endswith('.CSV'):
        with open(dateiname, 'r') as fd:
            print(dateiname)
            df = pd.read_csv(fd, sep=';', header=0, index_col=0)  # , names=['time [s]', 'measured voltage [V]', 'leer'])
          #  print(df)
            x = df.index.values.tolist()
       #     print(x)
            y = df['current [µA]'].values.tolist()
        #    print(y)
         #   print(int(df['current [µA]'].max()))
            A = int(df['current [µA]'].max())
        #    print(A)
    # x = np.array([1, 2, 3, 9])
    # y = np.array([1, 4, 1, 3])



    # def fit_func(x, a, b):
    #     return a * x + b


    # params = curve_fit(fit_func, x, y)
            params, r = curve_fit(fit_func, x, y, p0=[1, 1000000, 0.5])
            # print(x)
            # # for i in x:
            # #     print(i)
            # print(np.dtype(params[0]))
            # print(np.dtype(params[1]))
            # print(np.dtype(params[2]))
            # #           # print(np.dtype(params[0]))
            # #           #  x = liste_in_floats_umwandeln(x)
            # print(isinstance(x[0], float))
            # print(x[1])
            # x = liste_in_decimals_umwandeln(x)

            # print(x)
            print(params)
            yaj = fit_func(df.index,
                           A0=params[0],
                           frequ=params[1],
                           Lambda=params[2])
       #     print(yaj)
            data = pd.DataFrame(params, index=['A0=','frequenz=','Lambda='], columns=['A0 * np.sin(x * 2 * np.pi * 1/frequ + Lambda'])
            # data.append('A0 * np.sin(x * 2 * np.pi * 1/frequ + Lambda')
            # data.append('A0=')
            # data.append(params[0])
            # data.append('frequenz=')
            # data.append(params[1])
            # data.append('Lambda=')
            # data.append(params[2])

            print(data)
            data.to_csv(generate_filename(dateiname, '_FitParameters.csv'), sep=';')

            plt.plot(x, y, 'x', x, yaj, 'r-')
            plt.show()

#             measured_voltages = import_from_oszi_data(dateiname)
#             measured_voltages['measured voltage [V] smoothed'] = scipy.signal.savgol_filter(measured_voltages, window_length=21, polyorder=1, axis=0, mode='nearest')  # ggf auch polyorder=2 oder 3
#             print(measured_voltages)
#             #measured_voltages.to_csv('OsziData_allImportantNumbersIn1.csv', sep=';')
#             current = get_current(measured_voltages, used_resistor)
#             print(current)
#             measured_voltages['current [µA]'] = current['current [µA]']
#             print(measured_voltages)
#             measured_voltages.to_csv(generate_filename(dateiname, '_w21_o1_s.csv'), sep = ';')
#             #in_chip_voltage = get_voltage_in_chip(measured_voltages, get_voltage(list_dateiname[i]))
#             # df_in_chip_data = in_chip_voltage.copy()
#             # df_in_chip_data['current [µA]'] = current['current [µA]']
#             # maxima = df_in_chip_data.apply(max, axis=0)
#             # maxima['in chip resistance [Ohm]'] = maxima['in chip voltage [V]'] * 1000000 / maxima['current [µA]']  # resistance [Ohm]
#             # df_maxima = (pd.DataFrame(maxima, index=maxima.index)).transpose()
#             # df_a = df_maxima
#             # df_a = df_a.set_index([[list_dateiname[i]]])
#     # if i is not 0:
#     #     with open(list_dateiname[i]) as fd:
#     #         measured_voltages = import_from_oszi_data(list_dateiname[i])
#     #         measured_voltages['measured voltage [V] smoothed'] = scipy.signal.savgol_filter(measured_voltages, window_length=21, polyorder=1, axis=0, mode='nearest')  # ggf auch polyorder=2 oder 3
#     #         current = get_current(measured_voltages, used_resistor)
#     #         in_chip_voltage = get_voltage_in_chip(measured_voltages, get_voltage(list_dateiname[i]))
#     #         df_in_chip_data = in_chip_voltage.copy()
#     #         df_in_chip_data['current [µA]'] = current['current [µA]']
#     #         maxima = df_in_chip_data.apply(max, axis=0)
#     #         maxima['in chip resistance [Ohm]'] = maxima['in chip voltage [V]'] * 1000000 / maxima['current [µA]']  # resistance [Ohm]
#     #         df_maxima = (pd.DataFrame(maxima, index=maxima.index)).transpose()
#     #         df_b = df_maxima
#     #         df_b = df_b.set_index([[list_dateiname[i]]])
#     #        # print(i)
#     #     df_a = df_a.append(df_b)
#
# # df_a.to_csv('OsziData_allImportantNumbersIn1.csv', sep=';')
