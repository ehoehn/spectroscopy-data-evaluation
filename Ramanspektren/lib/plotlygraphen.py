import plotly
from plotly import graph_objs as go
from lib.allgemein import generate_filename


def plotly_xy_yFehler_data(x_values, y_values, errorx_values, errory_values, errorx_ausan = False, errory_ausan = False):
    print(plotly.__version__)
    if errorx_values is not None:
        errorx_ausan = True
    if errory_values is not None:
        errory_ausan = True
    #print(y_values)
    trace = go.Scatter(
        x=x_values,
        y=y_values,
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
        mode='markers',
        marker=dict(
            sizemode='diameter',
            sizeref=1,  #relative Größe der Marker
            sizemin=20,
            size=10,
            color='#000000',
          #  opacity=0.8,
            line=dict(color='rgb(166, 166, 166)',
                      width=0)))
    data = [trace]
    return data


def plotly_xy_yFehler_layout(xaxis_title, yaxis_title, x_range, y_range, x_dtick, y_dtick):
    layout = go.Layout(
        autosize=True,
        width=650,
        height=430,
        xaxis=dict(
            title='<b>' + xaxis_title + '</b>',
            titlefont=dict(family='Arial bold, sans-serif',
                           size=20,
                           color='#000000'),
            showticklabels=True,
            tickangle=0,
            tickfont=dict(family='Arial, sans-serif',
                          size=20,
                          color='#000000'),
            showgrid=False,
            showline=True,
            linewidth=2,
            zeroline=False,
            autotick=False,
            ticks='outside',
            tick0=0,
            ticklen=5,
            tickwidth=1,
            tickcolor='#FFFFFF',
            range=x_range,
            #   range=[0, 2.5],
            dtick=x_dtick,
            ),
        yaxis=dict(
            title='<b>' + yaxis_title + '</b>',
            titlefont=dict(family='Arial bold, sans-serif',
                           size=20,
                           color='#000000'),
            showticklabels=True,
           # tickangle=0,
            tickfont=dict(family='Arial, sans-serif',
                          size=20,
                          color='#000000'),
            exponentformat=None,
            showgrid=False,
            showline=True,
            linewidth=2,
            zeroline=False,
            autotick=False,
            ticks='outside',
            tick0=0,
            ticklen=5,
            tickwidth=1,
            tickcolor='#FFFFFF',
            range=y_range,
            # range=[0, 105],
            dtick=y_dtick
        ))
    return layout


def plotly_xy_yFehler(x_values, y_values, errorx=None, errory=None, dateiname=None, suffix_for_new_filename=None, x_range=None, y_range=None, x_dtick=None, y_dtick=None, xaxis_title='', yaxis_title=''):
    nwfile = generate_filename(dateiname, suffix_for_new_filename)
    fig = dict(data=plotly_xy_yFehler_data(x_values, y_values, errorx, errory),
               layout=plotly_xy_yFehler_layout(xaxis_title, yaxis_title, x_range, y_range, x_dtick, y_dtick))
    plotly.offline.plot(fig, filename=nwfile) #,  image_filename=nwfile)  #, image='png', image_width=1600, image_height=860)
