import os
import pandas as pd
import plotly
import plotly.graph_objs as go  # import Scatter, Layout
from Ramanspektren.lib.allgemein import generate_filename
from Ramanspektren.lib.plotlygraphen import plotly_zeitlVerlauf_2dscatter_layout
from Ramanspektren.lib.plotlygraphen import viridis_plus_rot_as_list
from Ramanspektren.lib.xml_import import get_times



suffix_for_new_filename = '_graph.html'


def plotly_zeitlVerlauf_2dscatter_data(highest_intensity):
    ind = []
    for i in highest_intensity:
        nr = i.split(' ')
        ind.append(nr[1])

    voltage = []
    for k in highest_intensity.index:
        nr = k.split('_')
        voltage.append(nr[6])

    nrCol = []
    for l in highest_intensity.index:
        measu = highest_intensity.ix[l].values.tolist()
        nrCol.append(measu)

    traces = []
    for t in range(0, len(highest_intensity.index)):
        trace = go.Scatter(
            x=ind,
            y=nrCol[t],
            mode='lines',
            line=go.Line(color=viridis_plus_rot_as_list()[t*2], width=3),
            name=voltage[t],
            showlegend=True)
        traces.append(trace)
    return traces, ind


def plotly_zeitlVerlauf(df, dateiname, suffix_for_new_filename, xaxis_title, yaxis_title):
    nwfile = generate_filename(dateiname, suffix_for_new_filename)
    data, ind = plotly_zeitlVerlauf_2dscatter_data(df)
    fig = go.Figure(data=data, layout=plotly_zeitlVerlauf_2dscatter_layout(ind, xaxis_title, yaxis_title, yrangestart=0, yrangestop=105))
    plotly.offline.plot(fig, filename=nwfile) # , image='png', image_filename=nwfile, image_width=800, image_height=430)



# for dateiname in os.listdir():
#     if dateiname.endswith('_beiF1Analyt_beiF20ElektrolythFlussAn_beiF200ProgStart.tvf') or dateiname.endswith('_beiF1Analyt_beiF20ElektrolythFlussAn_beiF200ProgStart.TVF'):
#      #   print(dateiname)
#         times = get_times(dateiname)
#
#         TimeVoltageOn = round(times['Frame 200']['time [s]'] + 100, 0)
#         FrameVoltageOn = times[times.columns[times.ix['time [s]'] > TimeVoltageOn - 1]].columns[0]


for dateiname in os.listdir():
    if dateiname.endswith('usammenfassung_Renata_grep.csv') or dateiname.endswith('usammenfassung_Renata_grep.CSV'):
        print(dateiname)
        with open(dateiname) as fd:
            df = pd.read_csv(fd, index_col=0, header=0, sep=';')
            df2 = df.apply(lambda x: x / df['Frame 200'] * 100, axis=0)  # Normalisierung

            plotly_zeitlVerlauf(df2, dateiname, suffix_for_new_filename, xaxis_title='Frame', yaxis_title='Intensity [a. u.]')
