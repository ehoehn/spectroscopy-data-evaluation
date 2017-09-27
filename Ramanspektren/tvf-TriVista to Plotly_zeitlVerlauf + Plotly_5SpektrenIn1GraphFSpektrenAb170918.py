'''
imput file: .tvf-TriVista-Datei
output file: ein Graph mit 5 Spektren: Frame1, Frame 20 - flow on, Frame 200 - At the start of regeration (voltage on), Frame 300 - voltage off, position of least intense signal
output file: zeitlicher Verlauf der Frames nach baseline correctur
'''
#written by EvaMaria Hoehn

import regex as re
import decimal
from Ramanspektren.lib.allgemein import liste_in_floats_umwandeln
import os
import plotly
import plotly.graph_objs as go  # import Scatter, Layout
from Ramanspektren.lib import analyte
from Ramanspektren.lib.allgemein import generate_filename
from Ramanspektren.lib.auswertung import compute_wn_with_highest_intensity
from Ramanspektren.lib.auswertung import compute_frame_with_lowest_intensity
from Ramanspektren.lib.auswertung import grep_highest_intensity
from Ramanspektren.lib.baseline_corr import baselinecorrection, get_spectrum_values
from Ramanspektren.lib.plotlygraphen import plotly_zeitlVerlauf_2dscatter_layout
from Ramanspektren.lib.xml_import import get_intensities
from Ramanspektren.lib.xml_import import get_positions
from Ramanspektren.lib.xml_import import get_times
from Ramanspektren.lib.plotlygraphen import plotly_Spectrum_2dscatter_layout


suffix_for_new_filename_zeitlVerlauf = '_graphzeitlVerlauf.html'
suffix_for_new_filename_5spektren_in1graph = '_graph5spektren.html'
punkte_baseline = analyte.kristallviolett()
band_start = 1605
band_end = 1630


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


def plotly_zeiten5spektren_in1graph_2dscatter_data(intensities, framenumber):
  #  print(intensities)
    ind = intensities.index.values.tolist()
    firstCol = intensities['Frame 1'].values.tolist()
    secondCol = intensities['Frame 20'].values.tolist()
    thirdCol = intensities['Frame 200'].values.tolist()
    fourthCol = intensities['Frame 300'].values.tolist()
    sixthCol = intensities['Frame ' + str(framenumber)].values.tolist()

    trace1 = go.Scatter(
        x=ind,
        y=firstCol,
        mode='lines',
        line=go.Line(color="#660066", width=3),
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
        name='Frame 200 - At the start of regeration (voltage on)')
    trace4 = go.Scatter(
        x=ind,
        y=fourthCol,
        mode='lines',
        line=go.Line(color="#000000", width=3),
        name='Frame 300 - voltage off')
    trace6 = go.Scatter(
        x=ind,
        y=sixthCol,
        mode='lines',
        line=go.Line(color="#ff0000", width=3),
        name='position of least intense signal')

  # name='Frame ' + str(framenumber))
    #print([trace1, trace2, trace3])
    return [trace1, trace2, trace3, trace4, trace6], ind


def plotly_zeiten5spektren_in1graph(intensities, dateiname, suffix_for_new_filename_3spektren_in1graph):
    framenumber = compute_frame_with_lowest_intensity(intensities, band_start, band_end)
    #print(framenumber)
    nwfile = generate_filename(dateiname, suffix_for_new_filename_3spektren_in1graph)
    data, ind = plotly_zeiten5spektren_in1graph_2dscatter_data(intensities, framenumber)
    layout = plotly_Spectrum_2dscatter_layout(ind, xaxis_title='rel. Wavenumber [cm<sup>-1</sup>]', yaxis_title='Intensity [a. u.]',
                                              range_nr=[50, 2000], dtick_nr=200, ausan=False, positionsangabe='', annotation_y='', graphwidth=800)
    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename=nwfile, auto_open=False) # , image='png', image_filename=nwfile, image_width=800, image_height=430)



for dateiname in os.listdir():
    if dateiname.endswith('beiF1Analyt_beiF20ElektrolythFlussAn_beiF200SpannungAn_beiF300SpannungAus.tvf') or dateiname.endswith('beiF1Analyt_beiF20ElektrolythFlussAn_beiF200SpannungAn_beiF300SpannungAus.TVF'):
        print(dateiname)
        intensities = get_intensities(dateiname)
        times = get_times(dateiname)

        plotly_zeiten5spektren_in1graph(intensities, dateiname, suffix_for_new_filename_5spektren_in1graph)
        df_korregiert = baselinecorrection(intensities, punkte_baseline)
        wn_with_highest_intensity = compute_wn_with_highest_intensity(df_korregiert, band_start, band_end)
        highest_intensity = grep_highest_intensity(df_korregiert, wn_with_highest_intensity)

        plotly_zeitlVerlauf(highest_intensity, times, dateiname, suffix_for_new_filename_zeitlVerlauf, xaxis_title='Time [s]', yaxis_title='Intensity [a. u.]') #zeitl Verlauf nach baseline correktur
