'''
punkte_baseline are the wavenumbers were the spectrum is taken and pulled down to the baseline.
band_start: is the start of the interval where the script searches for the highest intensity. this highest intensity is than shown over time.
band_end: is the end of that interval.
'''


'''
imput file: .tvf-TriVista-File
output file: band intensity over time after baseline correction
'''
#written by EvaMaria Hoehn


import lib.analyte


punkte_baseline = lib.analyte.kristallviolett_al_Raja()
band_start = 1152
band_end = 1215


import os
import pandas as pd
from lib.xml_import import get_intensities
from lib.xml_import import get_times
from lib.allgemein import generate_filename



for dateiname in os.listdir():
    if dateiname.endswith('.tvf') or dateiname.endswith('.TVF'):
        print(dateiname)
        intensities = get_intensities(dateiname)
        times = get_times(dateiname)
        df_intensities = pd.DataFrame(data=intensities.iloc[:,:], index=intensities.index, columns=[intensities.columns],  copy=True)
        df_intensities.iloc[:] = intensities.iloc[:]
        all = times.append(df_intensities)
        all = all.fillna(0)
        all.to_csv(generate_filename(dateiname, '_justExport.csv'), sep=';')


