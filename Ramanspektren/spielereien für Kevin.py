import pandas as pd
import os
import plotly
from plotly import graph_objs as go
# from lib.allgemein import generate_filename
# import lib.plotlygraphen


suffix_for_new_filename = '_xy.html'


def plotly_data(x_values, y_values):
    # colors = lib.plotlygraphen.jet()
    # lineform = lib.plotlygraphen.lineforms()
    # names_numbers = lib.plotlygraphen.numbers()
    # names_letters = lib.plotlygraphen.letters()
    print(plotly.__version__)

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
            mode='lines',
            # name=names_numbers[t],
            name=y_values.columns[t],
            line=dict(
               # width='1',
                 ))

        traces.append(trace)

    return traces


def plotly_layout(xaxis_title, yaxis_title, x_range, y_range):
    layout = go.Layout(
        autosize=True,
        width=500,
        height=500,
        margin=dict(l=100),
        legend=dict(x=1, y=1,       # legend=dict(x=0.85, y=1,
                    font=dict(family='Arial, sans-serif',
                             # size=10,
                              color='#000000')),
        xaxis=dict(
            title='<b>' + xaxis_title + '</b>',
            titlefont=dict(family='Arial, sans-serif',
                           #size=10,
                           color='#000000'),
            showticklabels=True,
        #    tickangle=0,
            tickfont=dict(family='Arial, sans-serif',
                          #size=10,
                          color='#000000'),
            showgrid=False,
            showline=True,
            linewidth=2,
            zeroline=False,
            #autotick=True,
            ticks='outside',
            # tick0=0,
            # ticklen=5,
            # tickwidth=1,
            # tickcolor='#FFFFFF',
            # range=x_range,
            #   range=[0, 2.5],
            ),
        yaxis=dict(
            title='<b>' + yaxis_title + '</b>',
            titlefont=dict(family='Arial, sans-serif',
                           # size=14,
                           color='#000000'),
            showticklabels=True,
         #   tickangle=0,
            tickfont=dict(family='Arial, sans-serif',
                          # size=10,
                          color='#000000'),
            showgrid=False,
            showline=True,
            linewidth=2,
            zeroline=False,
            #autotick=True,
            ticks='outside',
            # tick0=0,
            # ticklen=5,
            # tickwidth=1,
            # tickcolor='#555555',
            # range=y_range,
          #  range=[0, 105],
        ),
        xaxis2=dict(
            title='<b>' + '</b>',
            showticklabels=False,
            overlaying='x',
            side='top',
            showline=True,
            linewidth=2,
            zeroline=False,
            showgrid=False,
        ),
        yaxis2=dict(
            title='<b>' + '</b>',
            showticklabels=False,
            overlaying='y',
            side='right',
            showline=True,
            linewidth=2,
            zeroline=False,
            showgrid=False,
        )
    )
    return layout


def plotly_Graph(x_values, y_values, errorx=None, errory=None, dateiname=None, suffix_for_new_filename=None, x_range=None, y_range=None, xaxis_title='', yaxis_title=''):
    # nwfile = generate_filename(dateiname, suffix_for_new_filename)
    fig = dict(data=plotly_data(x_values, y_values),
               layout=plotly_layout(xaxis_title, yaxis_title, x_range, y_range))
    plotly.offline.plot(fig, filename='nwfile.html')#, auto_open=False)



for dateiname in os.listdir():
    if dateiname.endswith('.csv'):
        print(dateiname)
        with open(dateiname) as fd:
            df = pd.read_csv(fd, index_col=0, header=0, sep=';')
        #    print(df)
            df.reset_index(level=0, inplace=True)
            x = df.iloc[1:, 0]
           # print(x)
            # print(x.iloc[-1])
            y = pd.DataFrame(df.iloc[1:, 1:])
          #  print(y)
            # print(y.iloc[:, 0].max())

        #  print(y)
            plotly_Graph(x_values=x, y_values=y, x_range=[x.iloc[0], x.iloc[-1]], y_range=[y.iloc[:, 0].min(), y.iloc[:, 0].max()], dateiname=dateiname, suffix_for_new_filename=suffix_for_new_filename, xaxis_title='time [s]', yaxis_title='intensity [a. u.]')
