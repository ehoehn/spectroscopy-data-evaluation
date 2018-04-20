import pandas as pd
import os


import plotly
from plotly import graph_objs as go
from lib.allgemein import generate_filename
import Ramanspektren.lib.plotlygraphen
import numpy as np



suffix_for_new_filename = '_waterf.html'


def plotly_xyz_yFehler_data(x_values, y_values, z_values, errorx_values, errory_values, errorz_values, errorx_ausan = False, errory_ausan = False, errorz_ausan = False):
    colors = Ramanspektren.lib.plotlygraphen.br()
    lineform = Ramanspektren.lib.plotlygraphen.lineforms()
    names_numbers = Ramanspektren.lib.plotlygraphen.numbers()
    names_letters = Ramanspektren.lib.plotlygraphen.letters()
    print(plotly.__version__)
    if errorx_values is not None:
        errorx_ausan = True
    if errory_values is not None:
        errory_ausan = True
    if errorz_values is not None:
        errorz_ausan = True

  #   nrCol = []
  #   for l in z_values:
  # #      print(l)
  #       measu = z_values[l].values.tolist()
  #       nrCol.append(measu)
  #   print(nrCol)
  #   print(z_values[l])
  #  names = []
    # for k in y_values:
    #     nr = k.split('_')
    #     n = nr[7]
    #   #  print(nr)
    #     r = n.split('n')
    #     names.append(r)
   # print(z_values)
  #  print(range(0, len(z_values.columns)-1))
  #   for t in range(0, len(z_values.columns)):
  #       print(t)
 #   print(x_values)
    x = x_values.values.tolist()
   # print(x)

    y = y_values.values.tolist()
    # print(y_values)
    # print(y)
    # y = y_values.values.tolist(),
    #y = list(y)
#    print(y)
    y2 = []
    # print(range(0, len(y)))
    #
    for i in range(0, len(y)):
        y2.append(np.float64(y[i][0]))
   # print(y2)
    y = y2
   # print(y)


  #  print(y)
    #y = y_values.values.tolist(),
    # y = list(y[0])
    # y2 = []
    # for i in range(0, len(y)):
    #     y2.append(np.float64((y[i][0])))
    # y = y2
    # print(len(y))
 #   print(y)
    # z2 = []
    z = z_values.transpose().values.tolist()
  #  print(z_values.transpose())
    # for t in range(0, len(z_values.columns)):
    #     z = z_values[z_values.columns[t]]
   #      z2.append(z.values.tolist())
   # # print(z_values[z_values.columns[t]].values.tolist())
   #  z = z2
   #  print(len(z))
   # print(z)

 #   print(isinstance(x_values[0].values.tolist()[1], str))


    traces = []
    for t in range(len(x)-1, 0-1, -1):
 #        print(t)
 # #       print([t]*len(y_values))
 #        print(len(x_values[0].values.tolist()[t])),
 #        print(len([t]*len(y_values)))
# print([t]*len(y_values))
        # print(y_values['index'])
        # print(z_values.iloc[:, t])

     #   print(t)
        trace = go.Scatter3d(
            #type='scatter3d',
        #    name=x_values[0].values.tolist()[t],
         #   legendgroup=x_values[0].values.tolist()[t],
            showlegend=False,
            x=[t]*len(y_values),
          #  x=x_values[0].values.tolist() * 2 + x_values[0].values.tolist()[0],
            y=y,
            z=z_values.iloc[:, t],
       #     surfaceaxis=0,
            error_x=dict(
                type='data',
                array=errorx_values,
                #  thickness=1,
                # width=0,
                color='#000000',
                visible=errorx_ausan
            ),
            error_y=dict(
                type='data',
                array=errory_values,
              #  thickness=1,
               # width=0,
                color='#000000',
                visible=errory_ausan
                ),
            error_z=dict(
                type='data',
                array=errorz_values,
                #  thickness=1,
                # width=0,
                color='#000000',
                visible=errorz_ausan
                ),
            mode='lines',
         #   name=names_numbers[t],
            line=dict(
                width='6',
                color=colors[t],
          #      dash=lineform[t]
              #  colorscale = Ramanspektren.lib.plotlygraphen.jet[t]
            #    color='rgb(166, 166, 166)'
            )

            )
            # marker=dict(
            #     sizemode='diameter',
            #     sizeref=1,  #relative Größe der Marker
            #     sizemin=20,
            #     size=10,
            #     color='#000000',
            #   #  opacity=0.8,
            #     line=dict(color='rgb(166, 166, 166)',
            #               width=0)))

     #   print(trace)
        traces.append(trace)

    return traces


def plotly_xyz_yFehler_layout(xaxis_title, yaxis_title, zaxis_title, x_range, y_range, z_range, x_dtick, y_dtick, z_dtick, x_lables, y_lables, z_lables, ticktext, tickvals):
    layout = dict(
        autosize=True,
        width=1000,
        height=717,
        legend=dict(x=0.65, y=0.65,
                    # legend=dict(x=0.85, y=1,
                    font=dict(family='Arial, sans-serif',
                              size=14,
                              color='#000000')),
        scene=dict(
            xaxis=dict(
                title=xaxis_title,
                titlefont=dict(family='Arial bold, sans-serif',
                               size=18,
                               color='#000000'),
                showticklabels=x_lables,
                tickangle=0,
                tickfont=dict(family='Arial, sans-serif',
                              size=16,
                              color='#000000'),
           #     showgrid=False,
           #     showline=True,
          #      linewidth=2,
           #      zeroline=False,
        #         autotick=True,
      #           ticks='outside',
        #         tick0=0,
        #         ticklen=5,
        #         tickwidth=1,
        #         tickcolor='#FFFFFF',
#                tickvals=list(range(1, len(x), 2)),
                tickvals=list(range(0, len(x))),

                ticktext=ticktext,
                tickmode='array',
                range=x_range,
                dtick=x_dtick,
                gridcolor='rgb(100, 100, 100)',
                zerolinecolor = 'rgb(0, 0, 0)',
                showbackground=False,
             #   backgroundcolor='rgb(230, 230, 230)',
            ),
            yaxis=dict(
                 title=yaxis_title,
                 titlefont=dict(family='Arial, sans-serif',
                                size=18,
                                color='#000000'),
                 showticklabels=y_lables,
                 tickangle=0,
                 tickfont=dict(family='Arial, sans-serif',
                               size=16,
                               color='#000000'),
        #         showgrid=False,
        #         showline=True,
        #         linewidth=2,
        #         zeroline=False,
        #    #     autotick=True,
        #         ticks='outside',
        #         # tick0=0,
        #         # ticklen=5,
        #         # tickwidth=1,
        #         tickcolor='#FFFFFF',

                range=y_range,
                dtick=y_dtick,
                gridcolor='rgb(100, 100, 100)',
                zerolinecolor='rgb(0, 0, 0)',
                showbackground=False,
               #   backgroundcolor='rgb(230, 230, 230)',
            ),
            zaxis=dict(
                 title=zaxis_title,
                 titlefont=dict(family='Arial, sans-serif',
                                size=18,
                                color='#000000'),
                 showticklabels=z_lables,
                 tickangle=0,
                 tickfont=dict(family='Arial, sans-serif',
                               size=16,
                               color='#000000'),
        #         showgrid=False,
        #         showline=True,
        #         linewidth=2,
        #         zeroline=False,
        #    #     autotick=True,
        #         ticks='outside',
        #         tick0=0,
        #         ticklen=5,
        #         tickwidth=1,
        #         tickcolor='#FFFFFF',
                range=z_range,

                dtick=z_dtick,
                gridcolor='rgb(100, 100, 100)',
                zerolinecolor='rgb(0, 0, 0)',
                showbackground=False,
                #   backgroundcolor='rgb(230, 230, 230)',
        ),
            aspectratio=dict(x=0.6, y=1, z=1),
            aspectmode='manual',
            camera=dict(eye=dict(x=1.7, y=1.7, z=0.5),
                        center=dict(x=0, y=0, z=-0.3))))
    return layout


def plotly_xyz_yFehler(x_values, y_values, z_values, errorx=None, errory=None, errorz=None, dateiname=None, suffix_for_new_filename=None, x_range=None, y_range=None, z_range=None, x_dtick=None, y_dtick=None, z_dtick=None, xaxis_title='', yaxis_title='', zaxis_title='', x_lables=False, y_lables=False, z_lables=False, ticktext=None, tickvals=None):
    nwfile = generate_filename(dateiname, suffix_for_new_filename)
    fig = dict(data=plotly_xyz_yFehler_data(x_values, y_values, z_values, errorx, errory, errorz),
               layout=plotly_xyz_yFehler_layout(xaxis_title, yaxis_title, zaxis_title, x_range, y_range, z_range, x_dtick, y_dtick, z_dtick, x_lables, y_lables, z_lables, ticktext, tickvals))
    plotly.offline.plot(fig, filename=nwfile)#, auto_open=False) #,  image_filename=nwfile)  #, image='png', image_width=1600, image_height=860)





for dateiname in os.listdir():
    if dateiname.endswith('_pdD_reversed.csv'):
        print(dateiname)
        with open(dateiname) as fd:
            df = pd.read_csv(fd, index_col=0, header=0, sep=';')
           # print(df)
            df.reset_index(level=0, inplace=True)
         #   print(df)
            x = pd.DataFrame(df.iloc[0, 1:])

         #   print(x.index) # Zeit
            y = pd.DataFrame(df.iloc[1:, 0])
       #     print(y) # Wellenlängenverschiebung
            z = pd.DataFrame(df.iloc[1:, 1:])
        #    print(z) # Intensitäten
            plotly_xyz_yFehler(x_values=x, y_values=y, z_values=z, x_range=None, y_range=[150,2000], z_range=None, dateiname=dateiname, suffix_for_new_filename=suffix_for_new_filename, xaxis_title=' ',
                               #yaxis_title='rel. wavenumber [cm<sup>-1</sup>]', zaxis_title='intensity [a. u.]',
                               x_lables=True, y_lables=True, z_lables=True, ticktext=x.values.tolist(), tickvals=[x,y])

