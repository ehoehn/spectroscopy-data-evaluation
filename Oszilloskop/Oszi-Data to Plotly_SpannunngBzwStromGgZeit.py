﻿'''
imput file: .csv-Datei aus Osziloskop
'''


import os
import numpy as np
import pandas as pd
import decimal
import plotly
import plotly.graph_objs as go  # import Scatter, Layout
from Ramanspektren.lib.allgemein import generate_filename


#applyed_voltage = 10 # in [V]
used_resistor = 1000 # in [Ohm]
suffix_for_new_filename = '_SpannunngBzwStromGgZeit.html'


def plotly_zeitlVerlauf_2dscatter_data(df):
    ind = df.index.values.tolist()
    #print(ind, ind[-1], len(ind) )

 #   firstCol = df[str(df.columns[0])].values.tolist()
    secondCol = df['current [µA]'].values.tolist()
  #  thirdCol = df['in chip voltage [V]'].values.tolist()

    # secondCol = list(map(abs, (df['Ch. A Current (uA)'] - df['Ch. B Current (uA)'])))
    # thirdCol = (df['Ch. A Voltage (V)'] - df['Ch. B Voltage (V)']) / ((df['Ch. A Current (uA)'] - df['Ch. B Current (uA)'])/1000000).values.tolist()

    # wds = (df['Ch. A Voltage (V)'] - df['Ch. B Voltage (V)']) / (df['Ch. A Current (uA)'] - df['Ch. B Current (uA)'])


    # firstCol = df['Ch. A Voltage (V)'].values.tolist()
    # secondCol = df['Ch. A Current (uA)'].values.tolist()
    # thirdCol = df['Ch. B Voltage (V)'].values.tolist()
    # forthCol = df['Ch. B Current (uA)'].values.tolist()
    #print(firstCol)
    # for i in range(0, len(ind)):
    #     ind[i] = i + 1
    # trace1 = go.Scatter(
    #     x=ind,
    #     y=firstCol,
    #     yaxis='y2',
    #     mode='lines',
    #     line=go.Line(color="#0000FF", width=3),
    #     name=df.columns[0],
    #     showlegend=True)
    trace2 = go.Scatter(
        x=ind,
        y=secondCol,
      #  yaxis='y2',
        mode='lines',
        line=go.Line(color="rgb(47,110,115)", width=3),
        name='current [uA]',
        showlegend=True)
    # trace3 = go.Scatter(
    #     x=ind,
    #     y=thirdCol,
    #     mode='lines',
    #     line=go.Line(color="#FF0000", width=3),
    #     name='in chip voltage [V]',
    #     showlegend=True)
    # trace3 = go.Scatter(
    #     x=ind,
    #     y=thirdCol,
    #     yaxis='y2',
    #     mode='lines',
    #     line=go.Line(color="#0099FF", width=3),
    #     name='Widerstand (Ohm)',
    #     showlegend=True)
    # trace4 = go.Scatter(
    #     x=ind,
    #     y=forthCol,
    #     mode='lines',
    #     line=go.Line(color="#FF6666", width=3),
    #     name='Ch. B Current (uA)',
    #     showlegend=True)
    data = [trace2] #, trace3] # , trace3, trace4]
    return data, ind

def plotly_zeitlVerlauf_2dscatter_layout(
        ind, xaxis_title, yaxis_title, yaxis2_title, yrangestart=None, yrangestop=None, y2rangestart=None, y2rangestop=None, graphwidth=800):
    layout = go.Layout(
        autosize=False,
        width=graphwidth,
        height=430,
        showlegend=True,
        legend=dict(x=1.2, y=1),
        xaxis=dict(
            title='<b>' + xaxis_title + '</b>',
            titlefont=dict(family='Arial, sans-serif',
                           size=20,
                           color='#000000'),
            showticklabels=True,
            tickangle=0,
            tickfont=dict(family='Arial bold, sans-serif',
                          size=20,
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
            # range=[0, ind[-1]],
            range=None,
            dtick=round((ind[-1]-ind[0]) / 10, -1)
        ),
        yaxis=dict(
            title='<b>' + yaxis_title + '</b>',
            titlefont=dict(family='Arial, sans-serif',
                           size=20,
                           color='#000000'),
            showticklabels=True,
            tickangle=0,
            tickfont=dict(family='Arial, sans-serif',
                          size=20,
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
            range=[yrangestart, yrangestop]
        ),
        # yaxis2=dict(
        #     title='<b>' + yaxis2_title + '</b>',
        #     overlaying='y',
        #     side='right',
        #     titlefont=dict(family='Arial, sans-serif',
        #                    size=20,
        #                    color='#000000'),
        #     showticklabels=True,
        #     tickangle=0,
        #     tickfont=dict(family='Arial, sans-serif',
        #                   size=20,
        #                   color='#000000'),
        #     showgrid=False,
        #     showline=True,
        #     linewidth=2,
        #     zeroline=False,
        #     autotick=True,
        #     ticks='outside',
        #     tick0=0,
        #     ticklen=5,
        #     tickwidth=1,
        #     tickcolor='#FFFFFF',
        #     range=[y2rangestart, y2rangestop]
        # ),
    )
    return layout


def plotly_zeitlVerlauf(df, dateiname):
    nwfile = generate_filename(dateiname, suffix_for_new_filename)
    data, ind = plotly_zeitlVerlauf_2dscatter_data(df)
    fig = go.Figure(data=data, layout=plotly_zeitlVerlauf_2dscatter_layout(ind, xaxis_title='Time [s]', yaxis_title='Current (uA)', yaxis2_title='voltage (V)', yrangestart=None, yrangestop=None, graphwidth=900))
    plotly.offline.plot(fig, filename=nwfile, auto_open=False) #, image='png', image_filename=nwfile) #, image_width=800, image_height=430)


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


for dateiname in os.listdir():
    if dateiname.endswith('.csv') or dateiname.endswith('.CSV'):
        print(dateiname)
        with open(dateiname, 'r') as fd:
            df = pd.read_csv(fd, sep=',', header=0, index_col=0, skiprows=16, names=['time [s]', 'measured voltage [V]', 'leer'])
            del df['leer']
            df1 = df.replace('Null', np.nan)
            df1.dropna(axis=0, how='all', inplace=True)
            df2 = df1.apply(pd.to_numeric, errors='raise')
            # print(df2)
            df2['current [A]'] = df2['measured voltage [V]']/used_resistor  # voltage is the measured voltage
            df2['current [mA]'] = df2['current [A]'] * 1000
            df2['current [µA]'] = df2['current [mA]'] * 1000

 #           df2['in chip voltage [V]'] = split_in_sections(df2['measured voltage [V]'], [34, 145], applyed_voltage)
            # print(df2)  #  voltage is the voltage in the chip

            # wds.to_csv(dateiname + '_Widerstände.csv', sep=';', header=0)
            #
            plotly_zeitlVerlauf(df2, dateiname)
