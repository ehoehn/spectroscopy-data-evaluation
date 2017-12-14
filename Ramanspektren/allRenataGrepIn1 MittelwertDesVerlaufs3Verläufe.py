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
    fifthCol = highest_intensity.ix[4].values.tolist()
    
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
        line=go.Line(color="#FF0000", width=3),
        name=highest_intensity.index[4],
        showlegend=True,
        error_y=dict(
            type='data',
            array=fifthCol,
          #  thickness=1,
           # width=0,
            color='#DDDDDD',
            visible=True))

    data = [trace4, trace1, trace2, trace3]
    return data, ind


def plotly_zeitlVerlauf(df, dateiname, suffix_for_new_filename, xaxis_title, yaxis_title):
    nwfile = generate_filename(dateiname, suffix_for_new_filename)
    data, ind = plotly_zeitlVerlauf_2dscatter_data(df)
    fig = go.Figure(data=data, layout=plotly_zeitlVerlauf_2dscatter_layout(ind, xaxis_title, yaxis_title))
    plotly.offline.plot(fig, filename=nwfile) # , image='png', image_filename=nwfile, image_width=800, image_height=430)



for dateiname in os.listdir():
    if dateiname.endswith('Zusammenfassung_Renata_grep.csv'):
        print(dateiname)
        with open(dateiname) as fd:
            dfimportiert = pd.read_csv(fd, index_col=0, header=0, sep=';')
            dfnormalisiert = dfimportiert.apply(lambda x: x / dfimportiert['Frame 100'] * 100, axis=0)
            dfmean = dfnormalisiert.mean(axis=0)
            dfmean = pd.DataFrame(dfmean, columns = ['mean [%]'])
            dfmean['std [%]'] = dfnormalisiert.std(axis=0)
            dfmean = dfmean.transpose()
            df2 = dfnormalisiert.append(dfmean)
            print(df2)
            plotly_zeitlVerlauf(df2, dateiname, suffix_for_new_filename, xaxis_title='Frame', yaxis_title='Intensity [a. u.]')


         #   df2 = df.apply(lambda x: x / df['Frame 100'] * 100, axis=0)
           # print(df2)
         #   plotly_zeitlVerlauf(df2, dateiname, suffix_for_new_filename, xaxis_title='Frame', yaxis_title='Intensity [a. u.]')
