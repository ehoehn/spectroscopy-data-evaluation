import pandas as pd
import os


import plotly
from plotly import graph_objs as go
from lib.allgemein import generate_filename
import lib.plotlygraphen
import numpy as np
import lib.auswertung
import lib.analyte



band_start = 1152
band_end = 1215


suffix_for_new_filename = '_bar.html'


def plotly_barChart_data(x_values, y_values, errorx_values, errory_values, errorx_ausan = False, errory_ausan = False):
    colors = [['#2ca02c', '#9467bd', '#2ca02c', '#9467bd', '#2ca02c', '#9467bd', '#2ca02c', '#9467bd'],['#000000']]
  #  colors = Ramanspektren.lib.plotlygraphen.br()
    lineform = lib.plotlygraphen.lineforms()
    names_numbers = lib.plotlygraphen.numbers()
    names_letters = lib.plotlygraphen.letters()
    legend = [['MG', 'CV'], ['after reg.']]
    print(plotly.__version__)
    if errorx_values is not None:
        errorx_ausan = True
    if errory_values is not None:
        errory_ausan = True
    # print(names_letters[2])
  #  print(isinstance(x_values, object))
  #  print(y_values.ix[0])
   # print(x_values)

    # print(y_values.values.tolist())
    # nrCol = []
    # for l in y_values:
    #     measu = y_values[l].values.tolist()
    #     nrCol.append(measu)
    # print(nrCol)

    names = []
    # for k in y_values:
    #     nr = k.split('_')
    #     n = nr[7]
    #   #  print(nr)
    #     r = n.split('n')
    #     names.append(r)
    # print(y_values.ix)
    # print(len(y_values.index))
    traces = []
    for t in range(len(y_values.index)):
        print(t)
        trace = go.Bar(
            x=y_values.columns,
            y=y_values.ix[t],
            # error_x=dict(
            #     type='data',
            #     array=errorx_values,
            #     #  thickness=1,
            #     # width=0,
            #     color='#000000',
            #     visible=errorx_ausan
            # ),
      #       error_y=dict(
      #           type='data',
      #           array=errory_values,
      #         #  thickness=1,
      #          # width=0,
            #color='#000000',
      #           visible=errory_ausan
      #           ),
      #       mode='lines',
      #      name=names_letters[t],
            name=legend,

            # line=dict(
            # #     width='3',
            #      color=colors[t],
      #           dash=lineform[t]
              #  colorscale = Ramanspektren.lib.plotlygraphen.jet[t]
                #color='rgb(166, 166, 166)'

           # ),
         #   )
            marker=dict(
            #     sizemode='diameter',
            #     sizeref=1,  #relative Größe der Marker
            #     sizemin=20,
            #     size=10,
                color=colors[t],
            #   #  opacity=0.8,
            #     line=dict(color='rgb(166, 166, 166)',
            #               width=0))
                ))

        traces.append(trace)

    return traces


def plotly_barChart_layout(xaxis_title, yaxis_title, x_range, y_range, x_dtick, y_dtick):
    layout = go.Layout(
        autosize=True,
#        width=600,
        width=600,
        height=430,
        margin=dict(l=100),

        # legend=dict(x=1, y=1,       # legend=dict(x=0.85, y=1,
                    font=dict(family='Arial, sans-serif',
                              size=20,
                              color='#000000'),
        xaxis=dict(
        #     title='<b>' + xaxis_title + '</b>',
        #     titlefont=dict(family='Arial bold, sans-serif',
        #                    size=24,
        #                    color='#000000'),
        #     showticklabels=True,
            tickangle=50,
            tickfont=dict(family='Arial, sans-serif',
                          size=24,
                          color='#000000'),
            showgrid=False,
            showline=True,
            linewidth=2,
        #     zeroline=False,
        #     autotick=True,
        #     ticks='outside',
        #     tick0=0,
        #     ticklen=5,
        #     tickwidth=1,
        #     tickcolor='#FFFFFF',
            range=x_range,
        #     #   range=[0, 2.5],
        #     dtick=x_dtick
           ),
        yaxis=dict(
            title='<b>' + yaxis_title + '</b>',
            titlefont=dict(family='Arial bold, sans-serif',
                           size=24,
                           color='#000000'),
        #     showticklabels=True,
        #     tickangle=0,
            tickfont=dict(family='Arial, sans-serif',
                          size=24,
                          color='#000000'),
            showgrid=False,
            showline=True,
            linewidth=2,
        #     zeroline=False,
        #     autotick=True,
        #     ticks='outside',
        #     tick0=0,
        #     ticklen=5,
        #     tickwidth=1,
        #     tickcolor='#FFFFFF',
            range=y_range,
        #   #  range=[0, 105],
        #     dtick=y_dtick
        )
    )
    return layout


def plotly_barChart(x_values, y_values, errorx=None, errory=None, dateiname=None, suffix_for_new_filename=None, x_range=None, y_range=None, x_dtick=None, y_dtick=None, xaxis_title='', yaxis_title='', x_lables=True, y_lables=True, z_lables=True):
    nwfile = generate_filename(dateiname, suffix_for_new_filename)
    fig = dict(data=plotly_barChart_data(x_values, y_values, errorx, errory),
               layout=plotly_barChart_layout(xaxis_title, yaxis_title, x_range, y_range, x_dtick, y_dtick))
    plotly.offline.plot(fig, filename=nwfile)#, auto_open=False) #,  image_filename=nwfile)  #, image='png', image_width=1600, image_height=860)



for dateiname in os.listdir():
    if dateiname.endswith('Graph.csv'):
        print(dateiname)
        with open(dateiname) as fd:
            df = pd.read_csv(fd, index_col=0, header=1, sep=';')

       #     print(df)
       #     df.reset_index(level=0, inplace=True)
       #     print(df)
            x = pd.DataFrame(df.columns)
       #     print(x) # Label
  #         print(x.index) # Zeit
            y = pd.DataFrame(df.iloc[0:, 0:])
      #      print(y) # Wellenlängenverschiebung
            # z = df.iloc[1:, 0:]
            # print(z) # Intensitäten

            # wn_with_highest_intensity = Ramanspektren.lib.auswertung.compute_wn_with_highest_intensity_labelbased(z, band_start,
            #                                                                                            band_end)
            # #   print(wn_with_highest_intensity)
            # highest_intensity = pd.DataFrame(
            #     Ramanspektren.lib.auswertung.grep_highest_intensity(z, wn_with_highest_intensity))
       #     print(highest_intensity)

            plotly_barChart(x_values=x, y_values=y, x_range=None, y_range=[0,2000], dateiname=dateiname, suffix_for_new_filename=suffix_for_new_filename, xaxis_title=' ', yaxis_title='Intensity at 1180 cm<sup>-1</sup> (a. u.)', x_lables=True, y_lables=True, z_lables=True)
