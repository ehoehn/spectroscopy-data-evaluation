'''
imput file: .tvf-TriVista-Datei
output file: ein Graph mit 3 Spektren: Frame1, Frame100 und den Frame mit der Minimalintensität
output file: zeitlicher Verlauf der Frames nach baseline correctur
'''
#written by EvaMaria Hoehn



from Ramanspektren.lib.allgemein import liste_in_floats_umwandeln
import os
import plotly
import pandas as pd
import plotly.graph_objs as go  # import Scatter, Layout
from Ramanspektren.lib.allgemein import generate_filename
from Ramanspektren.lib.plotlygraphen import plotly_zeitlVerlauf_2dscatter_layout
from Ramanspektren.lib.xml_import import get_intensities
import scipy.signal
from lib.allgemein import generate_filename
import Ramanspektren.lib.baseline_corr
import lib.analyte


suffix_for_new_filename_zeitlVerlauf = '_mitundohnesmooth.html'
punkte_baseline = lib.analyte.kristallviolett_al_Raja()
band_start = punkte_baseline[0]
band_end = punkte_baseline[1]


def plotly_zeitlVerlauf_2dscatter_data(highest_intensity, smoothed, zeiten):
    ind = highest_intensity.index.values.tolist()
    # print(highest_intensity, smoothed)
    firstCol = highest_intensity.values.tolist()
    secondCol = smoothed.values.tolist()
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
    plotly.offline.plot(fig, filename=nwfile, auto_open=True) # , image='png', image_filename=nwfile, image_width=800, image_height=430)


for dateiname in os.listdir():
    if dateiname.endswith('180503_0,05mM_MG_40erObjektiv_5%_9_rinsing_F20VoltageOn-4,01V_F50VoltageOff.tvf'):
        print(dateiname)
        intensities = Ramanspektren.lib.xml_import.get_intensities(dateiname)
        times = Ramanspektren.lib.xml_import.get_times(dateiname)
        smoothed_intensities = scipy.signal.savgol_filter(intensities, window_length=9, polyorder=1, axis=0, mode='nearest')
        smoothed_intensities = pd.DataFrame(smoothed_intensities, index=intensities.index, columns=intensities.columns)

        # print(intensities)
        # print(smoothed_intensities)

        plotly_zeitlVerlauf_vergl(intensities.iloc[:,0], smoothed_intensities.iloc[:,0], times, dateiname, suffix_for_new_filename_zeitlVerlauf, xaxis_title='', yaxis_title='Intensity [a. u.]') #zeitl Verlauf nach baseline correktur
