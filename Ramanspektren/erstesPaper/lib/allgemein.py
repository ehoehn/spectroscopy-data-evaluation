#from Cython.Includes.numpy import __init__ as np
import numpy as np
import pandas as pd


def liste_in_floats_umwandeln(input):
    ft = []
    for i in input:
        k = np.float64(i)
        ft.append(k)
    return ft

def liste_in_string_umwandeln(input):
    ft = []
    for i in input:
        k = np.str(i)
        ft.append(k)
    return ft

def add_value_to_listelements(input, value):
    ft = []
    for i in input:
        k = i + value
        ft.append(k)
    return ft

def generate_filename(dateiname, suffix_for_new_filename):
    name = dateiname.split('.')
    del name[-1]
    separator = "."
    nwname = separator.join(name)
    nwfile = nwname + suffix_for_new_filename
    return nwfile


def innerFunktionOf_leave_every_other_datapoint_except_range(df, rangestart, rangeend):
    df2 = df.iloc[:rangestart]
    df3 = df.iloc[rangestart:rangeend]
    df4 = df.iloc[rangeend:]
  #  print(df2)
    for index, row in df2.iterrows():
        if index == 1:
            df_a = pd.DataFrame(row)
            df_a = df_a.transpose()
        else:
            if index % 2 == 0:
                df_b = row
                df_a = df_a.append(df_b)
    df_a = df_a.append(df3)
    for index, row in df4.iterrows():
        if index == df4.index[0]:
            df_c = pd.DataFrame(row)
            df_c = df_c.transpose()
        else:
            if index % 2 == 0:
                df_b = row
                df_c = df_c.append(df_b)
    df_c = df_a.append(df_c)
    return df_c


def leave_every_other_datapoint_except_range(df, rangestart, rangeend):
    try:
        df_c = innerFunktionOf_leave_every_other_datapoint_except_range(df, rangestart, rangeend)
    except:
        df = df.set_index([list(range(1, len(df.index) + 1))])
        df_c = innerFunktionOf_leave_every_other_datapoint_except_range(df, rangestart, rangeend)
    return df_c



# '_graphPositionen2D.html'
# '_graphMapping.html'
# '_graph3spektren.html'
# '_neuesBSCorr.csv'
# '_graphzeitlVerlaufForAll.html'
# '_RegenerationVsVoltage.html'
# '_graphzeitlVerlauf.html'
# '_graphMappingIn2D.html'
# '_SpectrumMitNiedrigsterIntensitaet.html'
# '_SpectrumMitHoesterIntensitaet.html'
# '_neuesRenataGrep.csv'
# '_1Spectrum.html'
