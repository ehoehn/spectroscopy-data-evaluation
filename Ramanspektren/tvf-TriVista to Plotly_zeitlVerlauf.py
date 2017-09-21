'''
imput file: .tvf-TriVista-Datei
output file: zeitlicher Verlauf der Frames nach baseline correctur
'''
#written by EvaMaria Hoehn


import os
import plotly
import plotly.graph_objs as go  # import Scatter, Layout
from lib import analyte
from Ramanspektren.lib.baseline_corr import baselinecorrection
from Ramanspektren.lib.xml_import import get_intensities
from Ramanspektren.lib.xml_import import get_positions
from Ramanspektren.lib.xml_import import get_times
from Ramanspektren.lib.allgemein import generate_filename
from Ramanspektren.lib.auswertung import compute_wn_with_highest_intensity
from Ramanspektren.lib.auswertung import grep_highest_intensity
from Ramanspektren.lib.plotlygraphen import plotly_zeitlVerlauf_2dscatter_layout


suffix_for_new_filename = '_graphzeitlVerlauf.html'
punkte_baseline = analyte.kristallviolett()
band_start = 1605
band_end = 1630


def plotly_zeitlVerlauf_2dscatter_data(highest_intensity, zeiten):
    ind = zeiten.ix['time [s]'].values.tolist()
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

def plotly_zeitlVerlauf(df, times, dateiname, suffix_for_new_filename, xaxis_title, yaxis_title):
    nwfile = generate_filename(dateiname, suffix_for_new_filename)
    data, ind = plotly_zeitlVerlauf_2dscatter_data(df, times)
    fig = go.Figure(data=data, layout=plotly_zeitlVerlauf_2dscatter_layout(ind, xaxis_title, yaxis_title))
    plotly.offline.plot(fig, filename=nwfile, image='png', image_filename=nwfile, image_width=800, image_height=430)



for dateiname in os.listdir():
    if dateiname.endswith('.tvf') or dateiname.endswith('.TVF'):
        print(dateiname)
        intensities = get_intensities(dateiname)
        df_korregiert = baselinecorrection(intensities, punkte_baseline)
        wn_with_highest_intensity = compute_wn_with_highest_intensity(df_korregiert, band_start, band_end)
        highest_intensity = grep_highest_intensity(df_korregiert, wn_with_highest_intensity)

        times = get_times(dateiname)
        plotly_zeitlVerlauf(highest_intensity, times, dateiname, suffix_for_new_filename, xaxis_title='Time [s]', yaxis_title='Intensity [a. u.]') #zeitl Verlauf nach baseline correktur

