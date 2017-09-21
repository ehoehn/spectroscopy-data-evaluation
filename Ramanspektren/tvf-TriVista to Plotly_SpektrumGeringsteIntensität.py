'''
imput file: .tvf-TriVista-Datei
output file: Graph mit Spektrum: Spektrum des Frames mit höchster Intensität
'''
#written by EvaMaria Hoehn


import os
import plotly.graph_objs as go  #import Scatter, Layout
import plotly
from lib import analyte
from Ramanspektren.lib.xml_import import get_positions
from Ramanspektren.lib.xml_import import get_intensities
from Ramanspektren.lib.baseline_corr import baselinecorrection
from Ramanspektren.lib.allgemein import generate_filename
from Ramanspektren.lib.auswertung import compute_wn_with_highest_intensity
from Ramanspektren.lib.auswertung import grep_highest_intensity
from Ramanspektren.lib.auswertung import compute_frame_with_lowest_intensity
from Ramanspektren.lib.plotlygraphen import plotly_Spectrum_2dscatter_layout


suffix_for_new_filename = '_SpectrumMitNiedrigsterIntensitaet.html'
punkte_baseline = analyte.kristallviolett()
band_start = 1605
band_end = 1630


def plotly_SpectrumMitNiedrigsterIntensitaet_2dscatter_data(intensities, framenumber):
  #  print(intensities)
    ind = intensities.index.values.tolist()
   # firstCol = intensities['Frame 1'].values.tolist()
   # secondCol = intensities['Frame 100'].values.tolist()
    thirdCol = intensities['Frame ' + str(framenumber)].values.tolist()

    # trace1 = go.Scatter(
    #     x=ind,
    #     y=firstCol,
    #     mode='lines',
    #     line=go.Line(color="#000000", width=3),
    #     name='Frame 1')
    # trace2 = go.Scatter(
    #     x=ind,
    #     y=secondCol,
    #     mode='lines',
    #     line=go.Line(color="#a5a5a5", width=3),
    #     name='Frame 100')
    trace3 = go.Scatter(
        x=ind,
        y=thirdCol,
        mode='lines',
        line=go.Line(color="#000000", width=3),
        name='Frame ' + str(framenumber))
    #print([trace1, trace2, trace3])
    return [trace3]  #[trace1, trace2, trace3]

def plotly_SpectrumMitNiedrigsterIntensitaet(intensities, dateiname):
    framenumber = compute_frame_with_lowest_intensity(intensities, band_start, band_end)
    #print(framenumber)
    nwfile = generate_filename(dateiname, suffix_for_new_filename)
    data = plotly_SpectrumMitNiedrigsterIntensitaet_2dscatter_data(intensities, framenumber)
    layout = plotly_Spectrum_2dscatter_layout(ind, xaxis_title='rel. Wavenumber [cm<sup>-1</sup>]', yaxis_title='Intensity [a. u.]', range_nr=[50, 2000], dtick_nr=200)
    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename=nwfile) # , image='png', image_filename=nwfile, image_width=800, image_height=430)



for dateiname in os.listdir():
    if dateiname.endswith('.tvf') or dateiname.endswith('.TVF'):
        print(dateiname)
        intensities = get_intensities(dateiname)
        plotly_SpectrumMitNiedrigsterIntensitaet(intensities, dateiname)
        df_korregiert = baselinecorrection(intensities, punkte_baseline)
        wn_with_highest_intensity = compute_wn_with_highest_intensity(df_korregiert, band_start, band_end)
        highest_intensity = grep_highest_intensity(df_korregiert, wn_with_highest_intensity)

        try:
            positions = get_positions(dateiname)
        except:
            print('no positions')
