import os
import pandas as pd
import plotly
import plotly.graph_objs as go  # import Scatter, Layout
from lib.allgemein import generate_filename
from lib.xml_import import get_times
from lib.allgemein import liste_in_floats_umwandeln


suffix_for_new_filename = '_RegenerationVsVoltage.html'


'''
imput file: eine .csv-Datei Datei mit zeitl Verlauf in einer Tabelle nach baseline korrektur
output file: schlichter Graph mit 2D-Scatterplot in Plotly
'''


def plotly_nach_positionen_2dscatter_data(x_values, y_values):
    print(plotly.__version__)
    trace = go.Scatter(
        x=x_values,
        y=y_values,
        mode='markers',
        marker=dict(
            sizemode='diameter',
            sizeref=1,  #relative Größe der Marker
            sizemin=20,
            size=10,
            color='#000000',
            opacity=0.8,
            line=dict(color='rgb(166, 166, 166)',
                      width=0)))
    data = [trace]
    return data


def plotly_nach_positionen_2dscatter_layout():
    #data = [trace]
    layout = go.Layout(
        autosize=False,
        width=800,
        height=430,
        # title='<b>Titel</b>',
        # titlefont=dict(family='Arial, sans-serif',
        #                size=14,
        #                color='#000000'),
        xaxis=dict(
            title='<b>U [V]</b>',
            titlefont=dict(family='Arial bold, sans-serif',
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
            autotick=False,
            ticks='outside',
            tick0=0,
            ticklen=5,
            tickwidth=1,
            tickcolor='#FFFFFF',
            #   range=[0, 2.5],
            dtick=2.5),
        yaxis=dict(
            title='<b>signal decrease [%]</b>',
            titlefont=dict(family='Arial bold, sans-serif',
                           size=20,
                           color='#000000'),
            showticklabels=True,
            tickangle=0,
            tickfont=dict(family='Arial, sans-serif',
                          size=20,
                          color='#000000'),
            showgrid=True,
            gridwidth=1,
            gridcolor='#8F8F8F',
            showline=True,
            linewidth=2,
            autotick=False,
            ticks='outside',
            tick0=0,
            ticklen=5,
            tickwidth=1,
            tickcolor='#FFFFFF',
            range=[0, 105],
            dtick=10))
    return layout


def plotly_nach_spannungen(x_values, y_values, dateiname):
    nwfile = generate_filename(dateiname, suffix_for_new_filename)
    fig = dict(data=plotly_nach_positionen_2dscatter_data(x_values, y_values), layout=plotly_nach_positionen_2dscatter_layout())
    plotly.offline.plot(fig, filename=nwfile,  image_filename=nwfile)  #, image='png', image_width=1600, image_height=860)


for dateiname in os.listdir():
    if dateiname.endswith('_beiF1Analyt_beiF20ElektrolythFlussAn_beiF200ProgStart.tvf') or dateiname.endswith('_beiF1Analyt_beiF20ElektrolythFlussAn_beiF200ProgStart.TVF'):
     #   print(dateiname)
        times = get_times(dateiname)

        TimeVoltageOn = round(times['Frame 200']['time [s]'] + 100, 0)
        FrameVoltageOn = times[times.columns[times.ix['time [s]'] > TimeVoltageOn - 1]].columns[0]
# break

for dateiname in os.listdir():
    if dateiname.endswith('usammenfassung_Renata_grep.csv') or dateiname.endswith('usammenfassung_Renata_grep.CSV'):
        print(dateiname)
        with open(dateiname) as fd:
            df = pd.read_csv(fd, index_col=0, header=0, sep=';')
            df2 = df.apply(lambda x: x / df[FrameVoltageOn] * 100, axis=0)  # Normalisierung

            voltage = []
            for k in df2.index:
                nr = k.split('_')
                nr = nr[6]
                nr = nr[:-1]
                nr = nr.replace(',', '.')
                voltage.append(nr)
            x_values = voltage
            x_values = liste_in_floats_umwandeln(x_values)
           # print(x_values)

            interval = df2.ix[:, FrameVoltageOn:]
            y_values = 100 - interval.min(axis=1)
        #    print(y_values)

            plotly_nach_spannungen(x_values, y_values, dateiname)
