'''
imput file: .csv-Datei aus Osziloskop
'''


import os

import pandas as pd
import plotly
import plotly.graph_objs as go  # import Scatter, Layout
from Ramanspektren.lib.allgemein import generate_filename


suffix_for_new_filename = '_zeitlicherVerlauf.html'


def plotly_nach_zeiten_2dscatter_data(df):
    ind = df.index.values.tolist()
    #print(ind, ind[-1], len(ind) )

    firstCol = df[str(df.columns[0])].values.tolist()
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
    trace1 = go.Scatter(
        x=ind,
        y=firstCol,
        yaxis='y2',
        mode='lines',
        line=go.Line(color="#0000FF", width=3),
        name=df.columns[0],
        showlegend=True)
    # trace2 = go.Scatter(
    #     x=ind,
    #     y=secondCol,
    #     mode='lines',
    #     line=go.Line(color="#FF0000", width=3),
    #     name='Differenz Current (uA)',
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
    data = [trace1] #, trace3, trace4]
    return data, ind

def plotly_nach_zeiten_2dscatter_layout(ind):
    layout = go.Layout(
        autosize=False,
        #width=800,
        width=900,
        height=430,
        showlegend=True,
        legend=dict(x=1.2, y=1),
        yaxis=dict(title='<b>Current (uA)</b>',
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
                   tickcolor='#FFFFFF'
                   ),
        yaxis2=dict(title='<b>Voltage (V)</b>',
                    overlaying='y',
                    side='right',
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
                    tickcolor='#FFFFFF'
                    ),
        xaxis=dict(title='<b>time [s]</b>',
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
                   autotick=False,
                   ticks='outside',
                   tick0=0,
                   ticklen=5,
                   tickwidth=1,
                   tickcolor='#FFFFFF',
                   range=[0, ind[-1]],
                   dtick=round(ind[-1] / 10, -1)
                   ))
    return layout


def plotly_zeitlVerlauf(df, dateiname):
    nwfile = generate_filename(dateiname, suffix_for_new_filename)
    data, ind = plotly_nach_zeiten_2dscatter_data(df)
    fig = go.Figure(data=data, layout=plotly_nach_zeiten_2dscatter_layout(ind))
    plotly.offline.plot(fig, filename=nwfile) #, image='png', image_filename=nwfile) #, image_width=800, image_height=430)






for dateiname in os.listdir():
    if dateiname.endswith('.csv') or dateiname.endswith('.CSV'):
        print(dateiname)
        with open(dateiname, 'r') as fd:
            df = pd.read_csv(fd, sep=',', header=0, index_col=0, skiprows=16, names=['time [s]', 'voltage [V]', 'leer'])
            del df['leer']
            print(df)
            print(df['voltage [V]'])
           # print(df['voltage [V]'])
          #  print(df[str(df.columns[0])])
         #   df.to_csv(dateiname + '.csv', sep=';')

            # wds = (df['Ch. A Voltage (V)'] - df['Ch. B Voltage (V)']) / ((df['Ch. A Current (uA)'] - df['Ch. B Current (uA)'])/1000000)
            # #print(wds)
            # wds.to_csv(dateiname + '_Widerstände.csv', sep=';', header=0)
            #
            plotly_zeitlVerlauf(df, dateiname)
