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


punkte_baseline = lib.analyte.kristallviolett_al_Raja()
band_start = 1152
band_end = 1215


import scipy.signal
import os
import pandas as pd
import plotly
import plotly.graph_objs as go  # import Scatter, Layout
from lib.allgemein import generate_filename
from lib.plotlygraphen import plotly_zeitlVerlauf_2dscatter_layout


suffix_for_new_filename = '_graph.html'


def plotly_zeitlVerlaufAlle_2dscatter_data(highest_intensity):
    ind = highest_intensity.index.values.tolist()
    for i in highest_intensity:
        print(i)
        # nr = i.split(' ')
        # ind.append(nr[1])

    # voltage = []
    # for k in highest_intensity.index:
    #     nr = k.split('_')
    #     voltage.append(nr[6])

    nrCol = []
    for l in highest_intensity.index:
        measu = highest_intensity.ix[l].values.tolist()
        nrCol.append(measu)

    traces = []
    for i in highest_intensity:
    # for t in range(0, len(highest_intensity.index)):
        trace = go.Scatter(
            x=ind,
            y=highest_intensity[i],
            mode='lines',
        #    line=go.Line(color=viridis_plus_rot_as_list()[t*2], width=3),
            name=i,
            showlegend=True)
        traces.append(trace)
    return traces, ind


def plotly_zeitlVerlaufAlle(df, dateiname, suffix_for_new_filename, xaxis_title, yaxis_title):
    nwfile = generate_filename(dateiname, suffix_for_new_filename)
    data, ind = plotly_zeitlVerlaufAlle_2dscatter_data(df)
    fig = go.Figure(data=data, layout=plotly_zeitlVerlauf_2dscatter_layout(ind, xaxis_title, yaxis_title)) #, yrangestart=0, yrangestop=110))
    plotly.offline.plot(fig, filename=nwfile) # , image='png', image_filename=nwfile, image_width=800, image_height=430)



for dateiname in os.listdir():
    if dateiname.endswith('.csv') or dateiname.endswith('.CSV'):
        print(dateiname)
        with open(dateiname, 'r') as fd:
            df = pd.read_csv(fd, sep=';', header=0, index_col=0) #, names=['time [s]', 'measured voltage [V]', 'leer'])
            # df1 = df.apply(pd.to_numeric, errors='raise')
            intensities = pd.DataFrame(df.iloc[1:,0:])
            times = pd.DataFrame(df.iloc[0, 0:]).transpose()
            smoothed_intensities = pd.DataFrame(intensities['Frame 1'], index=intensities.index) #, columns=[intensities.columns])
         #   print(smoothed_intensities)
            for i in range(5, 15, 2): # window_length
                for j in range(1, 6): # polyorder
                    #print(i, j)
                    try:
                        interim = scipy.signal.savgol_filter(intensities['Frame 1'], window_length=i, polyorder=j, axis=0, mode='nearest')
                        smoothed_intensities['window=' + str(i) + ', order=' + str(j)] = pd.DataFrame(interim, index=intensities.index) #, columns=[intensities.columns])
                    except:
                        continue

            print(smoothed_intensities)

            plotly_zeitlVerlaufAlle(smoothed_intensities, dateiname, suffix_for_new_filename, xaxis_title='Frame', yaxis_title='Intensity [a. u.]')
