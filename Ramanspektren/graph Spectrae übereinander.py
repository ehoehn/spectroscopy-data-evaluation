import pandas as pd
import os


import plotly
from plotly import graph_objs as go
from lib.allgemein import generate_filename
import Ramanspektren.lib.plotlygraphen
import numpy as np


suffix_for_new_filename = '_spectrae.html'


def plotly_xy_yFehler_data(x_values, y_values, errorx_values, errory_values, errorx_ausan = False, errory_ausan = False):
    colors = Ramanspektren.lib.plotlygraphen.jet()
    lineform = Ramanspektren.lib.plotlygraphen.lineforms()
    names_numbers = Ramanspektren.lib.plotlygraphen.numbers()
    names_letters = Ramanspektren.lib.plotlygraphen.letters()
    print(plotly.__version__)
    if errorx_values is not None:
        errorx_ausan = True
    if errory_values is not None:
        errory_ausan = True

    # print(x_values)
    # x = x_values.values.tolist()
    print(x)
    x_values = x

    y = y_values.values.tolist()
    print(y_values)
    # print(y)
    # y = y_values.values.tolist(),
    # y = list(y)
    #    print(y)
    y2 = []
    # print(range(0, len(y)))
    #
    for i in range(0, len(y)):
        y2.append(np.float64(y[i][0]))
    print(y2)
    nrCol = [y2]
    print(y)

    #  print(y)
    # y = y_values.values.tolist(),
    # y = list(y[0])
    # y2 = []
    # for i in range(0, len(y)):
    #     y2.append(np.float64((y[i][0])))
    # y = y2
    # print(len(y))
    #   print(y)
    # z2 = []
#    z = z_values.transpose().values.tolist()
#    print(z_values.transpose())
    # for t in range(0, len(z_values.columns)):
    #     z = z_values[z_values.columns[t]]
    #      z2.append(z.values.tolist())
    # # print(z_values[z_values.columns[t]].values.tolist())
    #  z = z2
    #  print(len(z))
#    print(z)


    nrCol = []
    for l in y_values:
        measu = y_values[l].values.tolist()
        nrCol.append(measu)
    print(nrCol)

  #  names = []
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
            name=names_letters[t],
            line=dict(
                width='3',
           #     color='#FF0000',
                dash=lineform[t]
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
            rangemode='tozero',
          #  range=[0, 105],
            dtick=y_dtick,

        ))
    return layout


def plotly_xy_yFehler(x_values, y_values, errorx=None, errory=None, dateiname=None, suffix_for_new_filename=None, x_range=None, y_range=None, x_dtick=None, y_dtick=None, xaxis_title='', yaxis_title='', x_lables=True, y_lables=True, z_lables=True):
    nwfile = generate_filename(dateiname, suffix_for_new_filename)
    fig = dict(data=plotly_xy_yFehler_data(x_values, y_values, errorx, errory),
               layout=plotly_xy_yFehler_layout(xaxis_title, yaxis_title, x_range, y_range, x_dtick, y_dtick))
    plotly.offline.plot(fig, filename=nwfile)#, auto_open=False) #,  image_filename=nwfile)  #, image='png', image_width=1600, image_height=860)



for dateiname in os.listdir():
    if dateiname.endswith('.csv'):
        print(dateiname)
        with open(dateiname) as fd:
            df = pd.read_csv(fd, index_col=0, header=0, sep=';')
            # print(df)
            df.reset_index(level=0, inplace=True)
            # #   print(df)
            # x = pd.DataFrame(df.iloc[0, 1:])

            x = df.iloc[1:, 0]
      #      print(x) # Wellenlängenverschiebung
            y = pd.DataFrame(df.iloc[1:, 1:])
      #      print(y) # Intensitäten
            plotly_xy_yFehler(x_values=x, y_values=y, x_range=[150,2000], y_range=None, dateiname=dateiname, suffix_for_new_filename=suffix_for_new_filename, xaxis_title='rel. wavenumber [cm<sup>-1</sup>]', yaxis_title='intensity [a. u.]', x_lables=True, y_lables=True)
