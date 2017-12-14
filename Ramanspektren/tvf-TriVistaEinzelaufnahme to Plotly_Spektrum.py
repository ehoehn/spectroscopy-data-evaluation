'''
imput file: .tvf-TriVista-Datei mit Einzelaufnahme/ Einzelspektrum
output file: Graph mit Spektrum: Spektrum des Frames
'''
#written by EvaMaria Hoehn


import os
import plotly
import plotly.graph_objs as go  # import Scatter, Layout
from lib.allgemein import generate_filename
from lib.plotlygraphen import plotly_Spectrum_2dscatter_layout
from lib.xml_import import get_intensities


suffix_for_new_filename = '_1Spectrum.html'



def plotly_Spectrum_1Spektrum_2dscatter_data(intensities, framenumber):
    ind = intensities.index.values.tolist()
    thirdCol = intensities[framenumber].values.tolist()  # trace1 = go.Scatter(
    showlegend = False
    trace3 = go.Scatter(
        x=ind,
        y=thirdCol,
        mode='lines',
        line=go.Line(color="#000000", width=3),
        name=framenumber
    )
    return [trace3], ind

def plotly_Spectrum_1Spectrum(intensities, dateiname, suffix_for_new_filename):
    indexes = intensities.index.values.tolist()
    print(indexes[0])
    nwfile = generate_filename(dateiname, suffix_for_new_filename)
    data, ind = plotly_Spectrum_1Spektrum_2dscatter_data(intensities, 'Intensity [a. u.]')
    layout = plotly_Spectrum_2dscatter_layout(ind, xaxis_title='rel. Wavenumber [cm<sup>-1</sup>]', yaxis_title='Intensity [a. u.]', range_nr=[indexes[0], indexes[-1]], dtick_nr=(indexes[0]-indexes[-1])/15)
    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename=nwfile, auto_open=False) # , image='png', image_filename=nwfile, image_width=800, image_height=430)



for dateiname in os.listdir():
    if dateiname.endswith('.tvf') or dateiname.endswith('.TVF'):
        print(dateiname)


        try:
            intensities = get_intensities(dateiname)
            plotly_Spectrum_1Spectrum(intensities, dateiname, suffix_for_new_filename)
        except:
            print('does not work')
