import pandas as pd
import os


import plotly
from plotly import graph_objs as go
from lib.allgemein import generate_filename
import lib.plotlygraphen


suffix_for_new_filename = '_xy_everyOther.html'


def plotly_xy_yFehler_data(x_values, y_values, errorx_values, errory_values, errorx_ausan = False, errory_ausan = False):
    colors = lib.plotlygraphen.jet()
    lineform = lib.plotlygraphen.lineforms()
    names_numbers = lib.plotlygraphen.numbers()
    names_letters = lib.plotlygraphen.letters()
    print(plotly.__version__)
    if errorx_values is not None:
        errorx_ausan = True
    if errory_values is not None:
        errory_ausan = True

    print(y_values.columns)

    nrCol = []
    for l in y_values:
        measu = y_values[l].values.tolist()
        nrCol.append(measu)
 #   print(nrCol)

    # names = []
    # for k in y_values:
    #     nr = k.split('_')
    #     n = nr[7]
    #   #  print(nr)
    #     r = n.split('n')
    #     names.append(r)
    # print(names)


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
            name=y_values.columns[t],
          #  name=names_numbers[t],
            line=dict(
                width='3',
      #          color=colors[t],
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
#        margin=dict(l=100),
      #  legend=dict(x=0.95, y=1,
        legend=dict(x=1, y=1,   # legend=dict(x=0.95, y=1,     # legend=dict(x=0.85, y=1,
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
          #  range=[0, 105],
            dtick=y_dtick
        ))
    return layout


def plotly_xy_yFehler(x_values, y_values, errorx=None, errory=None, dateiname=None, suffix_for_new_filename=None, x_range=None, y_range=None, x_dtick=None, y_dtick=None, xaxis_title='', yaxis_title='', x_lables=True, y_lables=True, z_lables=True):
    nwfile = generate_filename(dateiname, suffix_for_new_filename)
    fig = dict(data=plotly_xy_yFehler_data(x_values, y_values, errorx, errory),
               layout=plotly_xy_yFehler_layout(xaxis_title, yaxis_title, x_range, y_range, x_dtick, y_dtick))
    plotly.offline.plot(fig, filename=nwfile) # , auto_open=False) #,  image_filename=nwfile)  #, image='png', image_width=1600, image_height=860)



for dateiname in os.listdir():
    if dateiname.endswith('_normalized.csv'):
        print(dateiname)
        with open(dateiname) as fd:
            df = pd.read_csv(fd, index_col=0, header=1, sep=';')
          #  print(df)
            df = lib.allgemein.leave_every_other_datapoint_except_range(df, 18, 21)
            x = df.iloc[:, 0]
           # print(x)
            y = pd.DataFrame(df.iloc[:, 1:])
          #  y = pd.DataFrame(df.iloc[:, 3])

            #y = pd.DataFrame(df.iloc[:, 0:])                 #  y = pd.DataFrame(df.iloc[:, 1:])
         #   print(y)
            plotly_xy_yFehler(x_values=x, y_values=y, x_range=[0,50], y_range=[0,150], dateiname=dateiname, suffix_for_new_filename=suffix_for_new_filename, xaxis_title='time [s]', yaxis_title='norm. intensity [a. u.]', x_lables=True, y_lables=True, z_lables=True)
