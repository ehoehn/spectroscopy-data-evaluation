import plotly
from plotly import graph_objs as go
from lib.allgemein import generate_filename
import plotly.io as pio
pio.templates.default = "none"


grenzfarbe = 0.7
schritte = 20 - 1


def viridis_plus_rot():
    farbe = [[grenzfarbe - grenzfarbe / schritte * 19, '#440154FF'], [grenzfarbe - grenzfarbe / schritte * 18, '#481567FF'], [grenzfarbe - grenzfarbe / schritte * 17, '#482677FF'], [grenzfarbe - grenzfarbe / schritte * 16, '#453781FF'], [grenzfarbe - grenzfarbe / schritte * 15, '#404788FF'], [grenzfarbe - grenzfarbe / schritte * 14, '#39568CFF'], [grenzfarbe - grenzfarbe / schritte * 13, '#33638DFF'], [grenzfarbe - grenzfarbe / schritte * 12, '#2D708EFF'], [grenzfarbe - grenzfarbe / schritte * 11, '#287D8EFF'], [grenzfarbe - grenzfarbe / schritte * 10, '#238A8DFF'], [grenzfarbe - grenzfarbe / schritte * 9, '#1F968BFF'], [grenzfarbe - grenzfarbe / schritte * 8, '#20A387FF'], [grenzfarbe - grenzfarbe / schritte * 7, '#29AF7FFF'], [grenzfarbe - grenzfarbe / schritte * 6, '#3CBB75FF'], [grenzfarbe - grenzfarbe / schritte * 5, '#55C667FF'], [grenzfarbe - grenzfarbe / schritte * 4, '#73D055FF'], [grenzfarbe - grenzfarbe / schritte * 3, '#95D840FF'], [grenzfarbe - grenzfarbe / schritte * 2, '#B8DE29FF'], [grenzfarbe - grenzfarbe / schritte * 1, '#DCE319FF'], [grenzfarbe, '#FDE725FF'], [1, '#B20A28FF']]
    return farbe


def viridis_plus_rot_as_list():
    farbe = ['#440154FF', '#481567FF', '#482677FF', '#453781FF', '#404788FF', '#39568CFF', '#33638DFF', '#2D708EFF', '#287D8EFF', '#238A8DFF', '#1F968BFF', '#20A387FF', '#29AF7FFF', '#3CBB75FF', '#55C667FF', '#73D055FF', '#95D840FF', '#B8DE29FF', '#DCE319FF', '#FDE725FF', '#B20A28FF']
    return farbe


def jet():
    farbe = ['#000000', '#ff0000', '#0000ff', '#0ed145', '#ff00ff', '#800080', '#008000', '#9467bd'] #lila
    return farbe

def br():
    farbe = ['#000000', '#ff0000', '#000000', '#ff0000','#000000', '#ff0000','#000000', '#ff0000','#000000', '#ff0000','#000000', '#ff0000','#000000', '#ff0000','#000000', '#ff0000','#000000', '#ff0000']
    return farbe

def lineforms():
    lineform = ['solid', 'dot', 'dash', '20px', 'dashdot', '20px,3px', '20px,2px,2px', '7px,2px,2px', '1px', 'solid', 'dot', 'dash', '20px', 'dashdot', '20px,3px', '20px,2px,2px', '7px,2px,2px', '1px']
    return lineform

def letters():
    letterlist = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o']
    return letterlist

def numbers():
    numberlist = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18']
    return numberlist

def romannumbers():
    letterlist = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV']
    return letterlist



def plotly_nach_positionen_3dscatter_layout(x_lables, y_lables, z_lables):
    layout = go.Layout(
        # title='<b>Titel</b>',
        # titlefont=dict(family='Arial, sans-serif',
        #                size=14,
        #                color='#000000'),
        scene=dict(
            xaxis=dict(
                title='x [µm]',
                showticklabels=x_lables,
                titlefont=dict(family='Arial bold, sans-serif',
                               size=20,
                               color='#000000'),
                gridcolor='rgb(100, 100, 100)',
                # zerolinecolor = 'rgb(0, 0, 0)',
                showbackground=True,
                backgroundcolor='rgb(230, 230, 230)',
                tickfont=dict(family='Arial, sans-serif',
                              size=16,
                              color='#000000')),
            yaxis=dict(
                title='y [µm]',
                showticklabels=y_lables,
                titlefont=dict(family='Arial bold, sans-serif',
                               size=20,
                               color='#000000'),
                gridcolor='rgb(100, 100, 100)',
                # zerolinecolor = 'rgb(0, 0, 0)',
                showbackground=True,
                backgroundcolor='rgb(230, 230, 230)',
                tickfont = dict(family='Arial, sans-serif',
                                size=16,
                                color='#000000')),
            zaxis=dict(
                title='z [µm]',
                showticklabels=z_lables,
                titlefont=dict(family='Arial, sans-serif',
                               size=20,
                               color='#000000'),
                gridcolor='rgb(100, 100, 100)',
                # zerolinecolor = 'rgb(0, 0, 0)',
                showbackground=True,
                backgroundcolor='rgb(230, 230, 230)',
                tickfont = dict(family='Arial, sans-serif',
                                size=16,
                                color='#000000')),
        #     aspectratio=dict(x=0.4, y=2, z=0.4),
        #     aspectmode='manual',
        #     camera=dict(eye=dict(x=2, y=2, z=2))),
        # margin=dict(r=0, l=0, t=0, b=0)
    ))
    return layout


def plotly_nach_positionen_3dscatter_data(x_positions, y_positions, z_positions, highest_intensities):
    print(plotly.__version__)
   # print(highest_intensity.applymap(abs))
    trace = go.Scatter3d(
        x=x_positions,
        y=y_positions,
        z=z_positions,
        text=highest_intensities,
        mode='markers',
        marker=dict(
            sizemode='diameter',
            sizeref=100,  #relative Größe der Marker
            sizemin=20,
            size=list(map(abs, highest_intensities)),
            color=highest_intensities,
            opacity=0.8,
            colorbar=dict(
                title='Intensity [a.u.]',
                titlefont=dict(family='Arial, sans-serif',
                               size=20,
                               color='#000000'),
                tickfont=dict(family='Arial, sans-serif',
                              size=20,
                              color='#000000')),
            colorscale=viridis_plus_rot(),
            line=dict(
                color='rgb(166, 166, 166)',
                width=0)))
    data = [trace]
    return data


def plotly_zeitlVerlauf_2dscatter_layout(
        ind, xaxis_title, yaxis_title, yrangestart=None, yrangestop=None, graphwidth=800):
    layout = go.Layout(
        autosize=False,
        width=graphwidth,
        height=600,
        showlegend=True,
        legend=dict(x=0.85, y=-1.3),

        xaxis=dict(
            title='<b>' + xaxis_title + '</b>',
            titlefont=dict(family='Arial, sans-serif',
                           size=20,
                           color='#000000'),
            showticklabels=True,
            tickangle=0,
            tickfont=dict(family='Arial bold, sans-serif',
                          size=20,
                          color='#000000'),
            showgrid=False,
            showline=True,
            linewidth=2,
            autotick=True,
            ticks='outside',
            tick0=0,
            ticklen=5,
            tickwidth=1,
            tickcolor='#FFFFFF',
            range=[0, ind],
            dtick=round(len(ind) / 10, -1)),
        yaxis=dict(
            title='<b>' + yaxis_title + '</b>',
            titlefont=dict(family='Arial, sans-serif',
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
            autotick=True,
            ticks='outside',
            tick0=0,
            ticklen=5,
            tickwidth=1,
            tickcolor='#FFFFFF',
            range=[yrangestart, yrangestop]
        ))
    return layout


def plotly_Spectrum_2dscatter_layout(ind, xaxis_title, yaxis_title, range_nr, dtick_nr, ausan=False, positionsangabe='', annotation_y='', graphwidth=800):
    layout = go.Layout(
        autosize=False,
        width=graphwidth,
        height=430,
        showlegend=False,
        legend=dict(
            x=0.05, y=1,
            font=dict(family='Arial, sans-serif',
                      size=16,
                      color='#000000')),
        yaxis=dict(
            title='<b>' + yaxis_title + '</b>',
            titlefont=dict(family='Arial, sans-serif',
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
            autotick=True,
            ticks='outside',
            tick0=0,
            ticklen=5,
            tickwidth=1,
            tickcolor='#FFFFFF'),
        xaxis=dict(
            title='<b>' + xaxis_title + '</b>',
            titlefont=dict(family='Arial, sans-serif',
                           size=20,
                           color='#000000'),
            showticklabels=True,
            tickangle=0,
            tickfont=dict(family='Arial bold, sans-serif',
                          size=20,
                          color='#000000'),
            showgrid=False,
            showline=True,
            linewidth=2,
            autotick=True,
            ticks='outside',
            tick0=50,
            ticklen=5,
            tickwidth=1,
            tickcolor='#FFFFFF',
            range=range_nr,
            dtick=dtick_nr),
        annotations=[dict(
            visible=ausan,
            text=positionsangabe,
            font=dict(family='Arial, sans-serif',
                      size=14,
                      color='#000000'),
            x=range_nr[1] - range_nr[1] / 15, y=annotation_y,
            showarrow=False,
        )])
    return layout


def plotly_y_dependent_of_x_2dscatter_data(x_values, y_values):
    print(plotly.__version__)
    trace = go.Scatter(
        x=x_values,
        y=y_values,
        mode='markers',
        marker=dict(
            sizemode='diameter',
            sizeref=1,  #relative Größe der Marker
            sizemin=20,
            size=10,
            color='#000000',
            opacity=0.8,
            line=dict(color='rgb(166, 166, 166)',
                      width=0)))
    data = [trace]
    return data


def plotly_y_dependent_of_x_2dscatter_layout(xaxis_title, yaxis_title, x_range=None, y_range=None, x_dtick=None, y_dtick=None):
    #data = [trace]
    layout = go.Layout(
        autosize=False,
        width=800,
        height=430,
        # title='<b>Titel</b>',
        # titlefont=dict(family='Arial, sans-serif',
        #                size=14,
        #                color='#000000'),
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
            dtick=x_dtick),
        yaxis=dict(
            title='<b>' + yaxis_title + '</b>',
            titlefont=dict(family='Arial bold, sans-serif',
                           size=20,
                           color='#000000'),
            showticklabels=True,
            tickangle=0,
            tickfont=dict(family='Arial, sans-serif',
                          size=20,
                          color='#000000'),
            showgrid=True,
            gridwidth=1,
            gridcolor='#8F8F8F',
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
            dtick=y_dtick))
    return layout


def plotly_y_dependent_of_x(x_values, y_values, dateiname, suffix_for_new_filename, x_range, y_range, x_dtick, y_dtick, xaxis_title, yaxis_title):
    nwfile = generate_filename(dateiname, suffix_for_new_filename)
    fig = dict(data=plotly_y_dependent_of_x_2dscatter_data(x_values, y_values),
               layout=plotly_y_dependent_of_x_2dscatter_layout(xaxis_title, yaxis_title, x_range, y_range, x_dtick, y_dtick))
    plotly.offline.plot(fig, filename=nwfile,  image_filename=nwfile)  #, image='png', image_width=1600, image_height=860)


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
      #      color='#000000',
          #  opacity=0.8,
          #   line=dict(color='rgb(166, 166, 166)',
          #             width=0)
        ))
    data = [trace]
    return data


def plotly_xy_yFehler_layout(xaxis_title, yaxis_title, x_range, y_range, x_dtick, y_dtick):
    layout = go.Layout(
        autosize=True,
        width=600,
        height=430,
        separators='. ',

        # margin=dict(l=115),
        #  legend=dict(x=0.95, y=1,
        legend=dict(x=1, y=1,  # legend=dict(x=0.95, y=1,     # legend=dict(x=0.85, y=1,
                    font=dict(family='Arial, sans-serif',
                              size=20,
                              color='#000000')),
        xaxis=dict(
            title='<b>' + xaxis_title + '</b>',
            titlefont=dict(family='Arial bold, sans-serif',
                           size=24,
                           color='#000000'),
            showticklabels=True,
            tickangle=0,
            tickfont=dict(family='Arial, sans-serif',
                          size=24,
                          color='#000000'),
            showgrid=False,
            showline=True,
            linewidth=2,
            zeroline=False,
            # autotick=False,
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
                           size=24,
                           color='#000000'),
            showticklabels=True,
           # tickangle=0,
            tickfont=dict(family='Arial, sans-serif',
                          size=24,
                          color='#000000'),
            # separatethousands=True,
            exponentformat='none',
            automargin=True,
            showgrid=False,
            showline=True,
            linewidth=2,
            zeroline=False,
            # autotick=False,
            ticks='outside',
            tick0=0,
            ticklen=5,
            tickwidth=1,
            tickcolor='#FFFFFF',
            range=y_range,
            # range=[0, 105],
            dtick=y_dtick,
            ))
    return layout


def plotly_xy_yFehler(x_values, y_values, errorx=None, errory=None,
                      dateiname=None, suffix_for_new_filename=None,
                      x_range=None, y_range=None,
                      x_dtick=None, y_dtick=None,
                      xaxis_title='', yaxis_title='',
                      x_lables=True, y_lables=True, z_lables=True):
    nwfile = generate_filename(dateiname, suffix_for_new_filename)
    fig = dict(data=plotly_xy_yFehler_data(x_values, y_values, errorx, errory),
               layout=plotly_xy_yFehler_layout(xaxis_title, yaxis_title, 
                                               x_range, y_range, 
                                               x_dtick, y_dtick))
    #plotly.offline.plot(fig, filename=nwfile) # , auto_open=False) #,  image_filename=nwfile)  #, image='png', image_width=1600, image_height=860)
    plotly.offline.plot(fig, filename=nwfile, auto_open=True, 
                      #  image_filename=nwfile, image='svg',
                        image_width=600, image_height=430)