'''
imput file: .csv-Datei aus Osziloskop
output file: #eine Datei mit xy-Graph
'''
#written by EvaMaria Hoehn


import os
import numpy as np
import pandas as pd
import plotly
from plotly import graph_objs as go


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
    df1 = df.replace('Null', np.nan)
    df1.dropna(axis=0, how='all', inplace=True)
    df2 = df1.apply(pd.to_numeric, errors='raise')
    return df2


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

    names = []

    traces = []
    for t in range(0, len(nrCol)):
        trace = go.Scatter(
            x=x_values,
            y=nrCol[t],
            error_x=dict(
                type='data',
                array=errorx_values,
                color='#000000',
                visible=errorx_ausan
            ),

            name=y_values.columns[t],
            line=dict(
                width='1',
                )
            )

        traces.append(trace)
    return traces


def plotly_xy_yFehler_layout(xaxis_title, yaxis_title, x_range, y_range, x_dtick, y_dtick):
    layout = go.Layout(
        autosize=True,
        width=600,
        height=430,
        margin=dict(l=100),
        legend=dict(x=1, y=1,
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
            autotick=True,
            ticks='outside',
            tick0=0,
            ticklen=5,
            tickwidth=1,
            tickcolor='#FFFFFF',
            range=x_range,
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
            dtick=y_dtick
        ))
    return layout


def plotly_xy_yFehler(x_values, y_values, errorx=None, errory=None, dateiname=None, suffix_for_new_filename=None, x_range=None, y_range=None, x_dtick=None, y_dtick=None, xaxis_title='', yaxis_title='', x_lables=True, y_lables=True, z_lables=True):
    nwfile = generate_filename(dateiname, suffix_for_new_filename)
    fig = dict(data=plotly_xy_yFehler_data(x_values, y_values, errorx, errory),
               layout=plotly_xy_yFehler_layout(xaxis_title, yaxis_title, x_range, y_range, x_dtick, y_dtick))
    plotly.offline.plot(fig, filename=nwfile)


for dateiname in os.listdir():
    if dateiname.endswith('.csv') or dateiname.endswith('.CSV'):
        with open(dateiname) as search:
            for c, line in enumerate(search, 1):
                line = line.rstrip()  # remove '\n' at end of line
                if 'Waveform Data,' == line:
                    ll = c
        print(dateiname)
        measured_data = import_from_oszi_data(dateiname, ll)
        df = pd.read_csv(dateiname, sep=',', nrows=ll, header=None, usecols=[0, 1], index_col=0, skiprows=0,
                         names=['parameter name', 'parameter value'])
        indexasnumeric = pd.to_numeric(measured_data.index)
        measured_data = measured_data.reindex(indexasnumeric)
        measured_data['time [s]'] = indexasnumeric - indexasnumeric[0]
        df = measured_data.set_index('time [s]')
        df.rename(columns={'intensity unit':'voltage [V]'}, inplace=True)
        x = df.index
        y = pd.DataFrame(df.iloc[:, 0:])
        plotly_xy_yFehler(x_values=x, y_values=y, dateiname=dateiname, suffix_for_new_filename=suffix_for_new_filename, xaxis_title=str(df.index.name), yaxis_title=str(str(y.columns[0])), x_lables=True, y_lables=True, z_lables=True)
