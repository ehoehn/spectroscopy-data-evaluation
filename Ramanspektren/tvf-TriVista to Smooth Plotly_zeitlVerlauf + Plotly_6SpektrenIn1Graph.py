'''
imput file: .tvf-TriVista-Datei
output file: ein Graph mit 3 Spektren: Frame1, Frame100 und den Frame mit der Minimalintensität
output file: zeitlicher Verlauf der Frames nach baseline correctur
'''
#written by EvaMaria Hoehn

import regex as re
from lib.allgemein import liste_in_floats_umwandeln
import os
import plotly
import numpy as np
import pandas as pd
import plotly.graph_objs as go  # import Scatter, Layout
from lib import analyte
from lib.allgemein import generate_filename
from lib.auswertung import compute_wn_with_highest_intensity
from lib.auswertung import compute_frame_with_lowest_intensity
from lib.auswertung import grep_highest_intensity
from lib.baseline_corr import baselinecorrection, get_spectrum_values
from lib.plotlygraphen import plotly_zeitlVerlauf_2dscatter_layout
from lib.xml_import import get_intensities
from lib.xml_import import get_times
from lib.auswertung_fremdcode import smooth


suffix_for_new_filename_zeitlVerlauf = '_smooth_graphzeitlVerlauf.html'
suffix_for_new_filename_6spektren_in1graph = '_smooth_graph6spektren.html'
punkte_baseline = analyte.kristallviolett()
band_start = 1605
band_end = 1630


def get_point_values(df, punkt):
    ind = df.ix[0].values.tolist()
    ind = liste_in_floats_umwandeln(ind)
    ks = []
    for i in range(0, len([punkt])):
        for k in ind:
            if re.match(str(punkt) + '\.[0-9]+', str(k)):
                ks.append(k)
    return ks


def plotly_zeitlVerlauf_2dscatter_data(highest_intensity, zeiten):
    ind = zeiten.ix['time [s]'].values.tolist()
    #print(ind)
    firstCol = highest_intensity.ix['highest intensity [a. u.]'].values.tolist()
    #print(firstCol)
    # for i in range(0, len(ind)):
    #     ind[i] = i + 1
    trace1 = go.Scatter(
        x=ind,
        y=firstCol,
        mode='lines',
        line=go.Line(color="#000000", width=3),
        name='Verlauf',
        showlegend=False)
    data = [trace1]
    return data, ind

def plotly_zeitlVerlauf(df, times, dateiname, suffix_for_new_filename_zeitlVerlauf, xaxis_title, yaxis_title):
    nwfile = generate_filename(dateiname, suffix_for_new_filename_zeitlVerlauf)
    data, ind = plotly_zeitlVerlauf_2dscatter_data(df, times)
    fig = go.Figure(data=data, layout=plotly_zeitlVerlauf_2dscatter_layout(ind, xaxis_title, yaxis_title))
    plotly.offline.plot(fig, filename=nwfile, auto_open=False) # , image='png', image_filename=nwfile, image_width=800, image_height=430)


def plotly_zeiten3spektren_in1graph_2dscatter_layout():
    layout = go.Layout(
        autosize=False,
        width=800,
        height=430,
        showlegend=True,
        legend=dict(
            x=0.05, y=1,
                    font=dict(family='Arial, sans-serif',
                              size=16,
                              color='#000000')),
        yaxis=dict(title='<b>Intensity [a. u.]</b>',
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
                   autotick=True,
                   ticks='outside',
                   tick0=0,
                   ticklen=5,
                   tickwidth=1,
                   tickcolor='#FFFFFF'
                   ),
        xaxis=dict(title='<b>rel. Wavenumber [cm<sup>-1</sup>]</b>',
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
                   tick0=50,
                   ticklen=5,
                   tickwidth=1,
                   tickcolor='#FFFFFF',
                   range=[50, 2000],
                   dtick=200
                   ))
    return layout

def plotly_zeiten6spektren_in1graph_2dscatter_data(intensities, framenumber, VoltageOn, VoltageOff):
  #  print(intensities)
    ind = intensities.index.values.tolist()
    firstCol = intensities['Frame 1'].values.tolist()
    secondCol = intensities['Frame 20'].values.tolist()
    thirdCol = intensities['Frame 200'].values.tolist()
    fourthCol = intensities[VoltageOn].values.tolist()
    fifthCol = intensities[VoltageOff].values.tolist()
    sixthCol = intensities['Frame ' + str(framenumber)].values.tolist()

    trace1 = go.Scatter(
        x=ind,
        y=firstCol,
        mode='lines',
        line=go.Line(color="#ff9933", width=3),
        name='Frame 1')
    trace2 = go.Scatter(
        x=ind,
        y=secondCol,
        mode='lines',
        line=go.Line(color="#0000cd", width=3),
        name='Frame 20 - flow on')
    trace3 = go.Scatter(
        x=ind,
        y=thirdCol,
        mode='lines',
        line=go.Line(color="#009933", width=3),
        name='Frame 200 - program on')
    trace4 = go.Scatter(
        x=ind,
        y=fourthCol,
        mode='lines',
        line=go.Line(color="#000000", width=3),
        name='Frame 200 + 100 s - At the start of regeration (voltage on)')
    trace5 = go.Scatter(
        x=ind,
        y=fifthCol,
        mode='lines',
        line=go.Line(color="#660066", width=3),
        name='Frame 200 + 200 s - voltage off')
    trace6 = go.Scatter(
        x=ind,
        y=sixthCol,
        mode='lines',
        line=go.Line(color="#ff0000", width=3),
        name='position of least intense signal')

  # name='Frame ' + str(framenumber))
    #print([trace1, trace2, trace3])
    return [trace1, trace2, trace3, trace4, trace5, trace6]

def plotly_zeiten6spektren_in1graph(intensities, dateiname, suffix_for_new_filename_3spektren_in1graph, VoltageOn, VoltageOff):
    framenumber = compute_frame_with_lowest_intensity(intensities, band_start, band_end)
    #print(framenumber)
    nwfile = generate_filename(dateiname, suffix_for_new_filename_3spektren_in1graph)
    data = plotly_zeiten6spektren_in1graph_2dscatter_data(intensities, framenumber, VoltageOn, VoltageOff)
    layout = plotly_zeiten3spektren_in1graph_2dscatter_layout()
    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename=nwfile, auto_open=False) # , image='png', image_filename=nwfile, image_width=800, image_height=430)



for dateiname in os.listdir():
    if dateiname.endswith('_beiF1Analyt_beiF20ElektrolythFlussAn_beiF200ProgStart.tvf') or dateiname.endswith('_beiF1Analyt_beiF20ElektrolythFlussAn_beiF200ProgStart.TVF'):
        print(dateiname)
        intensities = get_intensities(dateiname)
      #  print(intensities.columns)
        # times = get_times(dateiname)
        #
        # TimeVoltageOn = round(times['Frame 200']['time [s]'] + 100, 0)
        # FrameVoltageOn = times[times.columns[times.ix['time [s]'] > TimeVoltageOn - 1]].columns[0]
        # TimeVoltageOff = round(times['Frame 200']['time [s]'] + 200, 0)
        # FrameVoltageOff = times[times.columns[times.ix['time [s]'] > TimeVoltageOff - 1]].columns[0]
        #
        # plotly_zeiten6spektren_in1graph(intensities, dateiname, suffix_for_new_filename_6spektren_in1graph, FrameVoltageOn, FrameVoltageOff)
        df_korregiert = baselinecorrection(intensities, punkte_baseline)
        wn_with_highest_intensity = compute_wn_with_highest_intensity(df_korregiert, band_start, band_end)
        highest_intensity = grep_highest_intensity(df_korregiert, wn_with_highest_intensity)
     #   print(highest_intensity)
        print(np.array(highest_intensity.ix['highest intensity [a. u.]'].values.tolist()))
        smoothed_highest_intensity = smooth(np.array(highest_intensity.ix['highest intensity [a. u.]'].values.tolist()))
        print(smoothed_highest_intensity)
        print(len(list(smoothed_highest_intensity)))
        ssmoothed_highest_intensity = pd.DataFrame(list(smoothed_highest_intensity), columns=['highest intensity [a. u.]'], index=[intensities.columns])
        print(ssmoothed_highest_intensity)
       # plotly_zeitlVerlauf(smoothed_highest_intensity, times, dateiname, suffix_for_new_filename_zeitlVerlauf, xaxis_title='Time [s]', yaxis_title='Intensity [a. u.]') #zeitl Verlauf nach baseline correktur
