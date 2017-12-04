'''
imput file: .tvf-TriVista-Datei
output file: Graph mit Spektrum: Spektrum des Frames mit höchster Intensität
'''
#written by EvaMaria Hoehn


import os
import plotly
import plotly.graph_objs as go  # import Scatter, Layout
from Ramanspektren.lib.auswertung import compute_frame_with_highest_intensity
from Ramanspektren.lib.plotlygraphen import plotly_Spectrum_2dscatter_layout
from Ramanspektren.lib import analyte
from Ramanspektren.lib.allgemein import generate_filename
from Ramanspektren.lib.baseline_corr import baselinecorrection
from Ramanspektren.lib.xml_import import get_intensities
from Ramanspektren.lib.xml_import import get_positions


suffix_for_new_filename = '_SpectrumMitHoesterIntensitaet_bestNachBaselineCorr.html'
punkte_baseline = analyte.methylbenzenethiol3()
band_start = 979
band_end = 1018


def plotly_SpectrumMitHoesterIntensitaet_2dscatter_data(intensities, framenumber):
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
    return [trace3], ind  #[trace1, trace2, trace3]

def plotly_SpectrumMitHoesterIntensitaet(intensities, dateiname):
    df_korregiert = baselinecorrection(intensities, punkte_baseline)
    framenumber = compute_frame_with_highest_intensity(df_korregiert, band_start, band_end)
    nwfile = generate_filename(dateiname, suffix_for_new_filename)
    data, ind = plotly_SpectrumMitHoesterIntensitaet_2dscatter_data(intensities, framenumber)
   # df_korregiert.to_csv('output.csv', sep=';')

    try:
        positions = get_positions(dateiname)
        positionsangabe = '(x, y, z) [µm] = <br>' + str(int(positions['Frame ' + str(framenumber)]['x [µm]'])) + ', ' + str(int(positions['Frame ' + str(framenumber)]['y [µm]'])) + ', ' + str(int(positions['Frame ' + str(framenumber)]['z [µm]']))
        annotation_y=intensities['Frame ' + str(framenumber)].max() - (intensities['Frame ' + str(framenumber)].max() - intensities['Frame ' + str(framenumber)].min()) / 9
        layout = plotly_Spectrum_2dscatter_layout(ind, xaxis_title='rel. Wavenumber [cm<sup>-1</sup>]', yaxis_title='Intensity [a. u.]', range_nr=[50, 2000], dtick_nr=200, ausan=True, positionsangabe=positionsangabe,  annotation_y=annotation_y)

    except:
        print('no positions')
        layout = plotly_Spectrum_2dscatter_layout(ind, xaxis_title='rel. Wavenumber [cm<sup>-1</sup>]', yaxis_title='Intensity [a. u.]', range_nr=[50, 2000], dtick_nr=200)

    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename=nwfile, auto_open=False) # , image='png', image_filename=nwfile, image_width=800, image_height=430)



for dateiname in os.listdir():
    if dateiname.endswith('.tvf') or dateiname.endswith('.TVF'):
        print(dateiname)
        try:
            intensities = get_intensities(dateiname)
            plotly_SpectrumMitHoesterIntensitaet(intensities, dateiname)
        except:
            print ('geht net')