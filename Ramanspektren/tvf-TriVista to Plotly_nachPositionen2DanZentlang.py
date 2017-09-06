'''
imput file: .tvf-TriVista-Datei
output file: ein 2D-Graph mit Intensität gegen z-Position
'''
#written by EvaMaria Hoehn


import os
import plotly
import plotly.graph_objs as go  # import Scatter, Layout
from lib import analyte
from lib.baseline_corr import baselinecorrection
from lib.xml_import import get_intensities
from lib.xml_import import get_positions
from lib.allgemein import generate_filename
from lib.auswertung import compute_wn_with_highest_intensity
from lib.auswertung import grep_highest_intensity


suffix_for_new_filename = '_graphPositionen2D.html'
punkte_baseline = analyte.kristallviolett()
band_start = 1605
band_end = 1630


def plotly_nach_positionen_2dscatter_layout(ind):
    layout = go.Layout(
        autosize=False,
        width=800,
        height=430,
        showlegend=True,
        legend=dict(x=0.85, y=1),
        yaxis=dict(title='<b>Intensity [a. u.]</b>',
                   titlefont=dict(family='Arial, sans-serif',
                                  size=14,
                                  color='#000000'),
                   showticklabels=True,
                   tickangle=0,
                   tickfont=dict(family='Arial, sans-serif',
                                 size=14,
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
        xaxis=dict(title='<b>z [µm]</b>',
                   titlefont=dict(family='Arial, sans-serif',
                                  size=14,
                                  color='#000000'),
                   showticklabels=True,
                   tickangle=0,
                   tickfont=dict(family='Arial bold, sans-serif',
                                 size=14,
                                 color='#000000'),
                   showgrid=False,
                   showline=True,
                   linewidth=2,
                   autotick=False,
                   # ticks='outside',
                   # tick0=0,
                   # ticklen=5,
                   # tickwidth=1,
                   # tickcolor='#FFFFFF',
                   dtick=20
                   # range=[0, ind],
                   # dtick=round(len(ind) / 10, -1)
                   ))
    return layout


def plotly_nach_positionen_2dscatter_data(highest_intensity, positions):
    ind = positions.ix['z [µm]'].values.tolist()
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


def plotly_positionen2D(highest_intensity, positions, dateiname):
    nwfile = generate_filename(dateiname, suffix_for_new_filename)
    data, ind = plotly_nach_positionen_2dscatter_data(highest_intensity, positions)
    fig = go.Figure(data=data, layout=plotly_nach_positionen_2dscatter_layout(ind))
    plotly.offline.plot(fig, filename=nwfile, image='png', image_filename=nwfile, image_width=800, image_height=430)



for dateiname in os.listdir():
    if dateiname.endswith('.tvf') or dateiname.endswith('.TVF'):
        print(dateiname)
        intensities = get_intensities(dateiname)
        df_korregiert = baselinecorrection(intensities, punkte_baseline)
        wn_with_highest_intensity = compute_wn_with_highest_intensity(df_korregiert, band_start, band_end)
        highest_intensity = grep_highest_intensity(df_korregiert, wn_with_highest_intensity)
        positions = get_positions(dateiname)
        plotly_positionen2D(highest_intensity, positions, dateiname)
