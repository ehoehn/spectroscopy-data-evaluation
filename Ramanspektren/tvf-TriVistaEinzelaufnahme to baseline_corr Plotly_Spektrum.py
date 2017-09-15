'''
imput file: .tvf-TriVista-Datei mit Einzelaufnahme/ Einzelspektrum
output file: Graph mit Spektrum: Spektrum des Frames nach Baselinekorrektur

Version für Anna mit allen Funktionen drin
'''
#written by EvaMaria Hoehn


import os
import plotly
import plotly.graph_objs as go  # import Scatter, Layout
import untangle
import numpy as np
import pandas as pd
import regex as re
from scipy import stats


suffix_for_new_filename = '_1Spectrum.html'
punkte_baseline = [1566, 1685, 1873]



def split_in_frames_and_back(df, spectrum_values):
    copy_df = df.copy()
    predf=[]
    for frame in copy_df:
        framenummer = frame
        nframe = split_in_baselines(copy_df[frame], spectrum_values, framenummer)
        predf.append(nframe)
    ndf = pd.DataFrame(predf)
    ndf = ndf.transpose()
    return ndf


def split_in_baselines(frame, spectrum_values, framenummer):
    copy_frame = frame.copy()
    for i in range(0, len(spectrum_values) - 1):
        if i == 0:
            points = [spectrum_values[i], spectrum_values[i + 1]]
            kurvenabschnitt = copy_frame.ix[points[0]:points[1]]
            gefittet = fitten(kurvenabschnitt, spectrum_values, i, framenummer)
            a = gefittet.ix[spectrum_values[i]:spectrum_values[i + 1]]
        else:
            points = [spectrum_values[i], spectrum_values[i + 1]]
            kurvenabschnitt = copy_frame.ix[points[0]:points[1]]
            gefittet = fitten(kurvenabschnitt, spectrum_values, i, framenummer)
            b = gefittet.ix[spectrum_values[i] + 1:spectrum_values[i + 1]]
            a = a.append(b)
    nframe = copy_frame - copy_frame + a
    nframe = nframe.fillna(0)
    return nframe


def fitten(kurvenabschnitt, spectrum_values, i, framenummer):   #, [spectrum_values[i]: spectrum_values[i + 1]]):
    copy_kurvenabschnitt = kurvenabschnitt.copy()
    dataset = copy_kurvenabschnitt.ix[[spectrum_values[i], spectrum_values[i + 1]]]
    x = dataset.index.values.tolist()
    y = dataset.values.tolist()
    m, t = lin_fit(x, y)
    x_bl = copy_kurvenabschnitt
    zwischenDF = pd.DataFrame(x_bl)
    zwischenDF[framenummer] = (copy_kurvenabschnitt.index * m) + t
    zwischenDF = pd.Series(zwischenDF[framenummer])
    return zwischenDF


def lin_fit(x, y, xlab=None, ylab=None, **kwargs):
    """Fit a set of data with stats.lingress and plot it."""
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    ''' #https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.linregress.html
    slope : float
    slope of the regression line
    intercept : float
    intercept of the regression line
    rvalue : float
    correlation coefficient
    pvalue : float
    two-sided p-value for a hypothesis test whose null hypothesis is that the slope is zero.
    stderr : float
    Standard error of the estimated gradient.
    '''
    return slope, intercept

def get_spectrum_values(df,punkte_baseline):
    ind = df.index.values.tolist()
    ks = []
    for i in range(0, len(punkte_baseline)):
        for k in ind:
            if re.match(str(punkte_baseline[i]) + '\.[0-9]+', str(k)):
                ks.append(k)
    return ks

def baselinecorrection(intensities, punkte_baseline):
    df = intensities.copy()
    punkte_baseline.sort()
    spectrum_values = get_spectrum_values(df, punkte_baseline)
    dff_neue_BL = split_in_frames_and_back(df, spectrum_values)
    df_korregiert = df - dff_neue_BL
    return df_korregiert

def liste_in_floats_umwandeln(input):
    ft = []
    for i in input:
        k = np.float64(i)
        ft.append(k)
    return ft

def get_relwavenumber(dateiname):
    obj = untangle.parse(dateiname)
    relwavenumber = obj.XmlMain.Documents.Document.xDim.Calibration['ValueArray']
    relwavenumber = relwavenumber.split('|')
    predf = liste_in_floats_umwandeln(relwavenumber)
    del predf[0]
    df1 = pd.DataFrame(predf, columns=['relWavenumber [1/cm]'])
    relwavenumbers = 1 / 473 * 10000000 - 1 / df1 * 10000000
    return relwavenumbers

def get_intensities(filename):
    relwavenumbers = get_relwavenumber(filename)
    obj = untangle.parse(filename)
    try:
        df = get_intensities_1Spectrum(relwavenumbers, obj)
    except:
        df = get_intensities_morethanoneSpectra(relwavenumbers, obj)
    return df

def get_intensities_morethanoneSpectra(relwavenumbers, obj):
    predf = []
    for i in range(0,len(obj.XmlMain.Documents.Document.Data.Frame)):
        inte = obj.XmlMain.Documents.Document.Data.Frame[i].cdata
        z = inte.split(";")
        z1 = liste_in_floats_umwandeln(z)
        predf.append(z1)
    colu = list(range(0,len(predf),1))
    colunames=[]
    for i in colu:
        colu='Frame ' + str(i+1)
        colunames.append(colu)
    df = pd.DataFrame(predf, index=colunames, columns=relwavenumbers['relWavenumber [1/cm]'])
    df = df.transpose()
    return df


def get_intensities_1Spectrum(relwavenumbers, obj):
    inte = obj.XmlMain.Documents.Document.Data.Frame.cdata
    z = inte.split(";")
    predf = liste_in_floats_umwandeln(z)
    colu = list(range(0,len(predf),1))
    colunames=[]
    for i in colu:
        colu='Frame ' + str(i+1)
        colunames.append(colu)
    df = pd.DataFrame(predf, columns=['Intensity [a. u.]'], index=relwavenumbers['relWavenumber [1/cm]'])
    return df


def plotly_Spectrum_2dscatter_layout(ind, xaxis_title, yaxis_title, range_nr, dtick_nr, ausan=False, positionsangabe='', annotation_y=''):
    layout = go.Layout(
        autosize=False,
        width=800,
        height=430,
        showlegend=True,
        legend=dict(
            x=0.85, y=1,
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
            autotick=False,
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


def generate_filename(dateiname, suffix_for_new_filename):
    name = dateiname.split('.')
    del name[-1]
    separator = "."
    nwname = separator.join(name)
    nwfile = nwname + suffix_for_new_filename
    return nwfile

def plotly_Spectrum_1Spektrum_2dscatter_data(intensities, framenumber):
    ind = intensities.index.values.tolist()
    thirdCol = intensities[framenumber].values.tolist()  # trace1 = go.Scatter(
    trace3 = go.Scatter(
        x=ind,
        y=thirdCol,
        mode='lines',
        line=go.Line(color="#000000", width=3),
        name=framenumber)
    return [trace3], ind

def plotly_Spectrum_1Spectrum(intensities, dateiname, suffix_for_new_filename):
    nwfile = generate_filename(dateiname, suffix_for_new_filename)
    data, ind = plotly_Spectrum_1Spektrum_2dscatter_data(intensities, 'Intensity [a. u.]')
    layout = plotly_Spectrum_2dscatter_layout(ind, xaxis_title='rel. Wavenumber [cm<sup>-1</sup>]', yaxis_title='Intensity [a. u.]', range_nr=[50, 2000], dtick_nr=200)
    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename=nwfile) #, auto_open=False) # , image='png', image_filename=nwfile, image_width=800, image_height=430)



for dateiname in os.listdir():
    if dateiname.endswith('nahme.tvf') or dateiname.endswith('nahme.TVF'):
        print(dateiname)

        #try:
        intensities = get_intensities(dateiname)
        df_korregiert = baselinecorrection(intensities, punkte_baseline)
        plotly_Spectrum_1Spectrum(df_korregiert, dateiname, suffix_for_new_filename)
        # except:
        #     print('does not work')
