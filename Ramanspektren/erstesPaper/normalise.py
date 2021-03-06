import os
import pandas as pd
import plotly
import plotly.graph_objs as go  # import Scatter, Layout
from lib.allgemein import generate_filename
from lib.plotlygraphen import plotly_zeitlVerlauf_2dscatter_layout


suffix_for_new_filename = '_graph.html'


def plotly_zeitlVerlauf_2dscatter_data(highest_intensity):
    ind =[]
    for i in highest_intensity:
        #print(i)
        nr = i.split(' ')
        ind.append(nr[1])
   # print(ind)
  #  ind = highest_intensity.ix.values.tolist()
    firstCol = highest_intensity.ix[0].values.tolist()
    secondCol = highest_intensity.ix[1].values.tolist()
    thirdCol = highest_intensity.ix[2].values.tolist()
    forthCol = highest_intensity.ix[3].values.tolist()
 #   fifthCol = highest_intensity.ix[4].values.tolist()
 #   sixthCol = highest_intensity.ix[5].values.tolist()
    # for i in range(0, len(ind)):
    #     ind[i] = i + 1
    trace1 = go.Scatter(
        x=ind,
        y=firstCol,
        mode='lines',
        line=go.Line(color="#440154FF", width=3),
        name=highest_intensity.index[0],
        showlegend=True)
    trace2 = go.Scatter(
        x=ind,
        y=secondCol,
        mode='lines',
        line=go.Line(color="#404788FF", width=3),
        name=highest_intensity.index[1],
        showlegend=True)
    trace3 = go.Scatter(
        x=ind,
        y=thirdCol,
        mode='lines',
        line=go.Line(color="#287D8EFF", width=3),
        name=highest_intensity.index[2],
        showlegend=True)
    trace4 = go.Scatter(
        x=ind,
        y=forthCol,
        mode='lines',
        line=go.Line(color="#29AF7FFF", width=3),
        name=highest_intensity.index[3],
        showlegend=True)
    # trace5 = go.Scatter(
    #     x=ind,
    #     y=fifthCol,
    #     mode='lines',
    #     line=go.Line(color="#95D840FF", width=3),
    #     name='Verlauf',
    #     showlegend=False)
    data = [trace1, trace2, trace3, trace4]
    return data, ind


def plotly_zeitlVerlauf(df, dateiname, suffix_for_new_filename, xaxis_title, yaxis_title):
    nwfile = generate_filename(dateiname, suffix_for_new_filename)
    data, ind = plotly_zeitlVerlauf_2dscatter_data(df)
    fig = go.Figure(data=data, layout=plotly_zeitlVerlauf_2dscatter_layout(ind, xaxis_title, yaxis_title))
    plotly.offline.plot(fig, filename=nwfile) # , image='png', image_filename=nwfile, image_width=800, image_height=430)



for dateiname in os.listdir():
    if dateiname.startswith('allIndicatorBandsInOne') or dateiname.endswith('IndBand.csv'):
        print(dateiname)
        with open(dateiname) as fd:
            df = pd.read_csv(fd, index_col=0, header=0, sep=';')
           # print(df)
            # times = pd.DataFrame(df.iloc[:, 0])
            # print(times)
         #   intensities = pd.DataFrame(df.iloc[:, 1:])
           # print(intensities)
          #  times = pd.DataFrame(df.iloc[0, 0:]).transpose()
            #print(intensities.ix[19])
            df2 = df.apply(lambda x: x / df.ix[19] * 100, axis=1)
            df2['time [s]'] = df['time [s]']
         #   print(df2)
            df2.to_csv(generate_filename(dateiname, '_normalized.csv'), sep=';')
