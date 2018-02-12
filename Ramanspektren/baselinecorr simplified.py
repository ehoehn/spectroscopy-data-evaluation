
'''
punkte_baseline are the wavenumbers were the spectrum is taken and pulled down to the baseline.
band_start: is the start of the interval where the script searches for the highest intensity. this highest intensity is than shown over time.
band_end: is the end of that interval.
'''


'''
imput file: .tvf-TriVista-File
output file: band intensity over time after baseline correction
'''
#written by EvaMaria Hoehn


import lib.analyte


#suffix_for_new_filename = '_graphIntensityOverTime.csv'
punkte_baseline = lib.analyte.kristallviolett_al_Raja()
band_start = 1152
band_end = 1215


import os
import plotly.graph_objs as go  #import Scatter, Layout
import plotly
import scipy.signal
import pandas as pd
from lib.allgemein import generate_filename
from lib.plotlygraphen import plotly_zeitlVerlauf_2dscatter_layout


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


def plotly_zeitlVerlauf_vergl(df_korregiert, smoothed, times, nwfile, xaxis_title, yaxis_title):
    data, ind = plotly_zeitlVerlauf_2dscatter_data(df_korregiert, smoothed, times)
    fig = go.Figure(data=data, layout=plotly_zeitlVerlauf_2dscatter_layout(ind, xaxis_title, yaxis_title))
    plotly.offline.plot(fig, filename=nwfile) #, auto_open=False) # , image='png', image_filename=nwfile, image_width=800, image_height=430)



for dateiname in os.listdir():
    if dateiname.endswith('_smoothed.csv') or dateiname.endswith('_smoothed.CSV'):
        print(dateiname)
        with open(dateiname, 'r') as fd:
            df = pd.read_csv(fd, sep=';', header=0, index_col=0) #, names=['time [s]', 'measured voltage [V]', 'leer'])
            intensities = pd.DataFrame(df.iloc[1:, 0:])
            times = pd.DataFrame(df.iloc[0, 0:]).transpose()
            df_out = intensities.transform(lambda x: x - x.min())
            all = times.append(df_out)
            all.to_csv(generate_filename(dateiname, '_drawnDown.csv'), sep=';')
