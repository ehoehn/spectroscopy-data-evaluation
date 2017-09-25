'''
imput file: .tvf-TriVista-Datei
output file: ein Graph mit 3 Spektren: Frame1, Frame100 und den Frame mit der Minimalintensität
output file: zeitlicher Verlauf der Frames nach baseline correctur
'''
#written by EvaMaria Hoehn

import regex as re
from Ramanspektren.lib.allgemein import liste_in_floats_umwandeln
import os
import plotly
import numpy as np
import pandas as pd
import plotly.graph_objs as go  # import Scatter, Layout
from lib import analyte
from Ramanspektren.lib.allgemein import generate_filename
from Ramanspektren.lib.auswertung import compute_wn_with_highest_intensity
from Ramanspektren.lib.auswertung import compute_frame_with_lowest_intensity
from Ramanspektren.lib.auswertung import grep_highest_intensity
from Ramanspektren.lib.baseline_corr import baselinecorrection, get_spectrum_values
from Ramanspektren.lib.plotlygraphen import plotly_zeitlVerlauf_2dscatter_layout
from Ramanspektren.lib.xml_import import get_intensities
from Ramanspektren.lib.xml_import import get_times
import scipy.signal


suffix_for_new_filename_zeitlVerlauf = '_mitundohnesmooth_graphzeitlVerlauf.html'
punkte_baseline = analyte.kristallviolett()
band_start = 1605
band_end = 1630


def plotly_zeitlVerlauf_2dscatter_data(highest_intensity, smoothed, zeiten):
    ind = zeiten.ix['time [s]'].values.tolist()
    # print(highest_intensity, smoothed)
    firstCol = highest_intensity.ix['highest intensity [a. u.]'].values.tolist()
    secondCol = smoothed.ix['highest intensity [a. u.]'].values.tolist()
    #print(firstCol)
    # for i in range(0, len(ind)):
    #     ind[i] = i + 1
    trace1 = go.Scatter(
        x=ind,
        y=firstCol,
        mode='lines',
        line=go.Line(color="#000000", width=3),
        name='unbearbeitet',
        showlegend=False)
    trace2 = go.Scatter(
        x=ind,
        y=secondCol,
        mode='lines',
        line=go.Line(color="#ff0000", width=3),
        name='geglättet',
        showlegend=False)

    data = [trace1, trace2]
    return data, ind

def plotly_zeitlVerlauf_vergl(df_korregiert, smoothed, times, dateiname, suffix_for_new_filename_zeitlVerlauf, xaxis_title, yaxis_title):
    nwfile = generate_filename(dateiname, suffix_for_new_filename_zeitlVerlauf)
    data, ind = plotly_zeitlVerlauf_2dscatter_data(df_korregiert, smoothed, times)
    fig = go.Figure(data=data, layout=plotly_zeitlVerlauf_2dscatter_layout(ind, xaxis_title, yaxis_title))
    plotly.offline.plot(fig, filename=nwfile, auto_open=False) # , image='png', image_filename=nwfile, image_width=800, image_height=430)


for dateiname in os.listdir():
    if dateiname.endswith('_beiF1Analyt_beiF20ElektrolythFlussAn_beiF200SpannungAn_beiF300SpannungAus.tvf') or dateiname.endswith('_beiF1Analyt_beiF20ElektrolythFlussAn_beiF200SpannungAn_beiF300SpannungAus.TVF'):
        print(dateiname)
        intensities = get_intensities(dateiname)

        times = get_times(dateiname)
        #
        # TimeVoltageOn = round(times['Frame 200']['time [s]'] + 100, 0)
        # FrameVoltageOn = times[times.columns[times.ix['time [s]'] > TimeVoltageOn - 1]].columns[0]
        # TimeVoltageOff = round(times['Frame 200']['time [s]'] + 200, 0)
        # FrameVoltageOff = times[times.columns[times.ix['time [s]'] > TimeVoltageOff - 1]].columns[0]
        #
#        plotly_zeiten6spektren_in1graph(intensities, dateiname, suffix_for_new_filename_6spektren_in1graph, FrameVoltageOn, FrameVoltageOff)
        df_korregiert = baselinecorrection(intensities, punkte_baseline)
        wn_with_highest_intensity = compute_wn_with_highest_intensity(df_korregiert, band_start, band_end)
        highest_intensity = grep_highest_intensity(df_korregiert, wn_with_highest_intensity)
    #    print(highest_intensity.transpose())
        smoothed = scipy.signal.savgol_filter(highest_intensity.transpose(), window_length=21, polyorder=3, axis=0, mode='nearest')
        smoothed = smoothed.transpose()
        smoothed = pd.DataFrame(smoothed, index=['highest intensity [a. u.]'], columns=[df_korregiert.columns])

        plotly_zeitlVerlauf_vergl(highest_intensity, smoothed, times, dateiname, suffix_for_new_filename_zeitlVerlauf, xaxis_title='Time [s]', yaxis_title='Intensity [a. u.]') #zeitl Verlauf nach baseline correktur
