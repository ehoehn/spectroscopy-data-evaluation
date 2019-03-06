'''
imput file: .csv-Datei aus Osziloskop
output file: #eine Datei mit allen Kennzahlen, die nach Glattung einer berechnet wurden
'''
#written by EvaMaria Hoehn


import os
import numpy as np
import pandas as pd
import scipy.signal
import plotly
from plotly import graph_objs as go
#import lib.plotlygraphen


suffix_for_new_filename = '_xy.html'


def generate_filename(dateiname, suffix_for_new_filename):
    name = dateiname.split('.')
    del name[-1]
    separator = "."
    nwname = separator.join(name)
    nwfile = nwname + suffix_for_new_filename
    return nwfile

def import_from_oszi_data(dateiname, ll):
    df = pd.read_csv(dateiname, sep=',', header=0, usecols=[0,1], index_col=0, skiprows=ll-1, names=['time stamp', 'intensity unit'])
    print(df)
    df1 = df.replace('Null', np.nan)
    df1.dropna(axis=0, how='all', inplace=True)
    df2 = df1.apply(pd.to_numeric, errors='raise')
    return df2

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



def plotly_xy_yFehler_data(x_values, y_values, errorx_values, errory_values, errorx_ausan = False, errory_ausan = False):
    print(plotly.__version__)
    if errorx_values is not None:
        errorx_ausan = True
    if errory_values is not None:
        errory_ausan = True

    nrCol = []
    for l in y_values:
        measu = y_values[l].values.tolist()
        nrCol.append(measu)
 #   print(nrCol)

    names = []
    # for k in y_values:
    #     nr = k.split('_')
    #     n = nr[7]
    #   #  print(nr)
    #     r = n.split('n')
    #     names.append(r)

    traces = []
    for t in range(0, len(nrCol)):
     #   print(t)
        trace = go.Scatter(
            x=x_values,
            y=nrCol[t],
            error_x=dict(
                type='data',
                array=errorx_values,
                #  thickness=1,
                # width=0,
                color='#000000',
                visible=errorx_ausan
            ),
            error_y=dict(
                type='data',
                array=errory_values,
              #  thickness=1,
               # width=0,
                color='#000000',
                visible=errory_ausan
                ),
            mode='lines',
            # name=names_numbers[t],
            name=y_values.columns[t],
            line=dict(
                width='1',
      #          color=colors[t],
              #  dash=lineform[t]
              #  colorscale = Ramanspektren.lib.plotlygraphen.jet[t]
            #    color='rgb(166, 166, 166)'

            )
            )
            # marker=dict(
            #     sizemode='diameter',
            #     sizeref=1,  #relative Größe der Marker
            #     sizemin=20,
            #     size=10,
            #     color='#000000',
            #   #  opacity=0.8,
            #     line=dict(color='rgb(166, 166, 166)',
            #               width=0)))

        traces.append(trace)

    return traces


def plotly_xy_yFehler_layout(xaxis_title, yaxis_title, x_range, y_range, x_dtick, y_dtick):
    layout = go.Layout(
        autosize=True,
        width=600,
        height=430,
        margin=dict(l=100),
        legend=dict(x=1, y=1,       # legend=dict(x=0.85, y=1,
                    font=dict(family='Arial, sans-serif',
                              size=20,
                              color='#000000')),
        xaxis=dict(
            title='<b>' + xaxis_title + '</b>',
            titlefont=dict(family='Arial bold, sans-serif',
                           size=24,
                           color='#000000'),
            showticklabels=True,
            tickangle=0,
            tickfont=dict(family='Arial, sans-serif',
                          size=24,
                          color='#000000'),
            showgrid=False,
            showline=True,
            linewidth=2,
            zeroline=False,
            # autotick=True,
            autotick=True,
            ticks='outside',
            tick0=0,
            ticklen=5,
            tickwidth=1,
            tickcolor='#FFFFFF',
            range=x_range,
            #   range=[0, 2.5],
            dtick=x_dtick
            ),
        yaxis=dict(
            title='<b>' + yaxis_title + '</b>',
            titlefont=dict(family='Arial bold, sans-serif',
                           size=24,
                           color='#000000'),
            showticklabels=True,
            tickangle=0,
            tickfont=dict(family='Arial, sans-serif',
                          size=24,
                          color='#000000'),
            showgrid=False,
            showline=True,
            linewidth=2,
            zeroline=False,
            autotick=True,
            ticks='outside',
            tick0=0,
            ticklen=5,
            tickwidth=1,
            tickcolor='#FFFFFF',
            range=y_range,
          #  range=[0, 105],
            dtick=y_dtick
        ))
    return layout


def plotly_xy_yFehler(x_values, y_values, errorx=None, errory=None, dateiname=None, suffix_for_new_filename=None, x_range=None, y_range=None, x_dtick=None, y_dtick=None, xaxis_title='', yaxis_title='', x_lables=True, y_lables=True, z_lables=True):
    nwfile = generate_filename(dateiname, suffix_for_new_filename)
    fig = dict(data=plotly_xy_yFehler_data(x_values, y_values, errorx, errory),
               layout=plotly_xy_yFehler_layout(xaxis_title, yaxis_title, x_range, y_range, x_dtick, y_dtick))
    plotly.offline.plot(fig, filename=nwfile, auto_open=False) #,  image_filename=nwfile)  #, image='png', image_width=1600, image_height=860)




for dateiname in os.listdir():
    if dateiname.endswith('.csv') or dateiname.endswith('.CSV'):
        with open(dateiname) as search:
            for c, line in enumerate(search, 1):
                line = line.rstrip()  # remove '\n' at end of line
                if 'Waveform Data,' == line:
                    ll = c

        # with open(dateiname) as fd:
        print(dateiname)
        measured_data = import_from_oszi_data(dateiname, ll)
        # measured_voltages['measured voltage [V] smoothed'] = scipy.signal.savgol_filter(measured_voltages, window_length=21, polyorder=1, axis=0, mode='nearest')  # ggf auch polyorder=2 oder 3
        #    print(measured_data)
        df = pd.read_csv(dateiname, sep=',', nrows=ll, header=None, usecols=[0, 1], index_col=0, skiprows=0,
                         names=['parameter name', 'parameter value'])
        # print(df)
        #  print(df.loc['Vertical Units'])
        #  print(df.loc['Vertical Scale'])
        # print(measured_data.index*float(df.loc['Vertical Scale']))
        indexasnumeric = pd.to_numeric(measured_data.index)
        #  print(indexasnumeric)
        measured_data = measured_data.reindex(indexasnumeric)
        #  print(measured_data)
        #  measured_data.index.names = ['time [s]']
        # measured_data.rename({'time stamp':'time [s]', 'intensity unit':'intensssss'}, inplace=True)
        #   print(measured_data)
        measured_data['time [s]'] = indexasnumeric - indexasnumeric[0]
        # print(measured_data)
        df = measured_data.set_index('time [s]')
        df.rename(columns={'intensity unit':'voltage [V]'}, inplace=True)

     #   print(df)

        # #measured_voltages.to_csv('OsziData_allImportantNumbersIn1.csv', sep=';')
        # current = get_current(measured_voltages, used_resistor)
        # print(current)
        # measured_voltages['current [µA]'] = current['current [µA]']
        # print(measured_voltages)
        # measured_voltages.to_csv(generate_filename(dateiname, '_w21_o1_s.csv'), sep = ';')
        # in_chip_voltage = get_voltage_in_chip(measured_voltages, get_voltage(list_dateiname[i]))
        # df_in_chip_data = in_chip_voltage.copy()
        # df_in_chip_data['current [µA]'] = current['current [µA]']
        # maxima = df_in_chip_data.apply(max, axis=0)
        # maxima['in chip resistance [Ohm]'] = maxima['in chip voltage [V]'] * 1000000 / maxima['current [µA]']  # resistance [Ohm]
        # df_maxima = (pd.DataFrame(maxima, index=maxima.index)).transpose()
        # df_a = df_maxima
        # df_a = df_a.set_index([[list_dateiname[i]]])
        # if i is not 0:
        #     with open(list_dateiname[i]) as fd:
        #         measured_voltages = import_from_oszi_data(list_dateiname[i])
        #         measured_voltages['measured voltage [V] smoothed'] = scipy.signal.savgol_filter(measured_voltages, window_length=21, polyorder=1, axis=0, mode='nearest')  # ggf auch polyorder=2 oder 3
        #         current = get_current(measured_voltages, used_resistor)
        #         in_chip_voltage = get_voltage_in_chip(measured_voltages, get_voltage(list_dateiname[i]))
        #         df_in_chip_data = in_chip_voltage.copy()
        #         df_in_chip_data['current [µA]'] = current['current [µA]']
        #         maxima = df_in_chip_data.apply(max, axis=0)
        #         maxima['in chip resistance [Ohm]'] = maxima['in chip voltage [V]'] * 1000000 / maxima['current [µA]']  # resistance [Ohm]
        #         df_maxima = (pd.DataFrame(maxima, index=maxima.index)).transpose()
        #         df_b = df_maxima
        #         df_b = df_b.set_index([[list_dateiname[i]]])
        #        # print(i)
        #     df_a = df_a.append(df_b)

        # df_a.to_csv('OsziData_allImportantNumbersIn1.csv', sep=';')

      #  print(df)
        x = df.index
        #print(x)
        # print(x.iloc[-1])
        y = pd.DataFrame(df.iloc[:, 0:])
     #   print(y)
       # print(str(y.columns[0]))
        # print(y.iloc[:, 0].max())
      #  print(df.index.names)
    #  print(y)
        plotly_xy_yFehler(x_values=x, y_values=y, dateiname=dateiname, suffix_for_new_filename=suffix_for_new_filename, xaxis_title=str(df.index.name), yaxis_title=str(str(y.columns[0])), x_lables=True, y_lables=True, z_lables=True)
