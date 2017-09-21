from Ramanspektren.lib.allgemein import liste_in_floats_umwandeln
import pandas as pd
import untangle
from decimal import *


#written by EvaMaria Hoehn


def get_xml_RecordTime_excitationwl(dateiname):
    obj = untangle.parse(dateiname)
    RecordTime = obj.XmlMain.Documents.Document['RecordTime']
    excitationwl = float(obj.XmlMain.Documents.Document.xDim.Calibration['LaserWave'])
    return RecordTime, excitationwl


def get_timestamps(dateiname):
    obj = untangle.parse(dateiname)
    predf = []
    for i in range(0, len(obj.XmlMain.Documents.Document.Data.Frame)):
        timestamp = obj.XmlMain.Documents.Document.Data.Frame[i]['TimeStamp']
        timestamp = Decimal(timestamp)
        predf.append(timestamp)
    posi = list(range(0, len(predf), 1))
    colunames = []
    for i in posi:
        colu = 'Frame ' + str(i + 1)
        colunames.append(colu)
    df = pd.DataFrame(predf, index=colunames, columns=['timestamp'])
    df_timestamps = df.transpose()
    return df_timestamps


def get_positions(dateiname):
    obj = untangle.parse(dateiname)
    predf = []
    for i in range(0,len(obj.XmlMain.Documents.Document.Data.Frame)):
        positions = obj.XmlMain.Documents.Document.Data.Frame[i]['ValuePosition']
        z = positions.split(";")
        ft = liste_in_floats_umwandeln(z)
        predf.append(ft)
    posi=list(range(0, len(predf),1))
    colunames = []
    for i in posi:
        colu = 'Frame ' + str(i + 1)
        colunames.append(colu)
    df = pd.DataFrame(predf, index=colunames, columns=['x [µm]','y [µm]','z [µm]'])
    df = df.transpose()
    return df


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


def get_times(dateiname):
    df_timestamps = get_timestamps(dateiname)
    nwtime = []
    colunames=[]
    for frame in df_timestamps:
        colunames.append(frame)
    for i in range(0, len(colunames)):
        df2 = (df_timestamps[colunames[i]]['timestamp'] - df_timestamps[colunames[0]]['timestamp']) / Decimal(10000000)
        # df2 = float(df1)
        nwtime.append(df2)
    df = pd.DataFrame(nwtime, columns=['time [s]'], index=[colunames])
    df = df.transpose()
    return df