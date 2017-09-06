'''
imput file: .tvf-TriVista-Datei
output file: ein Graph mit 3 Spektren: Frame1, Frame100 und den Frame mit der Minimalintensität
output file: zeitlicher Verlauf der Frames nach baseline correctur
'''
#written by EvaMaria Hoehn


import os
import plotly
import plotly.graph_objs as go  # import Scatter, Layout
from lib import analyte
from lib.allgemein import generate_filename
from lib.auswertung import compute_wn_with_highest_intensity
from lib.auswertung import compute_frame_with_lowest_intensity
from lib.auswertung import grep_highest_intensity
from lib.baseline_corr import baselinecorrection
from lib.plotlygraphen import plotly_zeitlVerlauf_2dscatter_layout
from lib.xml_import import get_intensities
from lib.xml_import import get_positions
from lib.xml_import import get_times


suffix_for_new_filename_zeitlVerlauf = '_graphzeitlVerlauf.html'
suffix_for_new_filename_3spektren_in1graph = '_graph3spektren.html'
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
    plotly.offline.plot(fig, filename=nwfile) # , image='png', image_filename=nwfile, image_width=800, image_height=430)


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

def plotly_zeiten3spektren_in1graph_2dscatter_data(intensities, framenumber):
  #  print(intensities)
    ind = intensities.index.values.tolist()
    firstCol = intensities['Frame 1'].values.tolist()
    secondCol = intensities['Frame 100'].values.tolist()
    thirdCol = intensities['Frame ' + str(framenumber)].values.tolist()

    trace1 = go.Scatter(
        x=ind,
        y=firstCol,
        mode='lines',
        line=go.Line(color="#000000", width=3),
        name='Frame 1')
    trace2 = go.Scatter(
        x=ind,
        y=secondCol,
        mode='lines',
        line=go.Line(color="#000000", width=3),
        name='At the start of regeration')
    trace3 = go.Scatter(
        x=ind,
        y=thirdCol,
        mode='lines',
        line=go.Line(color="#ff0000", width=3),
        name='position of least intense signal')

  # name='Frame ' + str(framenumber))
    #print([trace1, trace2, trace3])
    return [trace2, trace3]

def plotly_zeiten3spektren_in1graph(intensities, dateiname, suffix_for_new_filename_3spektren_in1graph):
    framenumber = compute_frame_with_lowest_intensity(intensities, band_start, band_end)
    #print(framenumber)
    nwfile = generate_filename(dateiname, suffix_for_new_filename_3spektren_in1graph)
    data = plotly_zeiten3spektren_in1graph_2dscatter_data(intensities, framenumber)
    layout = plotly_zeiten3spektren_in1graph_2dscatter_layout()
    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename=nwfile, image='png', image_filename=nwfile, image_width=800, image_height=430)



for dateiname in os.listdir():
    if dateiname.endswith('.tvf') or dateiname.endswith('.TVF'):
        print(dateiname)
        intensities = get_intensities(dateiname)
        plotly_zeiten3spektren_in1graph(intensities, dateiname, suffix_for_new_filename_3spektren_in1graph)
        df_korregiert = baselinecorrection(intensities, punkte_baseline)
        wn_with_highest_intensity = compute_wn_with_highest_intensity(df_korregiert, band_start, band_end)
        highest_intensity = grep_highest_intensity(df_korregiert, wn_with_highest_intensity)

        try:
            positions = get_positions(dateiname)
        except:
            print('no positions')

        times = get_times(dateiname)
        plotly_zeitlVerlauf(highest_intensity, times, dateiname, suffix_for_new_filename_zeitlVerlauf, xaxis_title='Time [s]', yaxis_title='Intensity [a. u.]') #zeitl Verlauf nach baseline correktur
