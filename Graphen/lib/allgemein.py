#from Cython.Includes.numpy import __init__ as np
import numpy as np


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

def generate_filename(dateiname, suffix_for_new_filename):
    name = dateiname.split('.')
    del name[-1]
    separator = "."
    nwname = separator.join(name)
    nwfile = nwname + suffix_for_new_filename
    return nwfile

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
