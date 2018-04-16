
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



#suffix_for_new_filename = '_graphIntensityOverTime.csv'
punkte_baseline = lib.analyte.kristallviolett_al_Raja()
band_start = punkte_baseline[0]
band_end = punkte_baseline[1]


import os
import plotly.graph_objs as go  #import Scatter, Layout
import plotly
import scipy.signal
import pandas as pd
from lib.allgemein import generate_filename
import Ramanspektren.lib.xml_import
import Ramanspektren.lib.baseline_corr



for dateiname in os.listdir():
    if dateiname.endswith('.tvf') or dateiname.endswith('.TVF'):
        print(dateiname)
        intensities = Ramanspektren.lib.xml_import.get_intensities(dateiname)
        times = Ramanspektren.lib.xml_import.get_times(dateiname)
        smoothed_intensities = scipy.signal.savgol_filter(intensities, window_length=9, polyorder=1, axis=0,
                                                          mode='nearest')
        smoothed_intensities = pd.DataFrame(smoothed_intensities, index=intensities.index,
                                            columns=intensities.columns)

        intensities = intensities.apply(lambda x: x - x.min())

        df_intensities = pd.DataFrame(data=intensities.iloc[:, :], index=intensities.index,
                                      columns=[intensities.columns],
                                      copy=True)
        df_intensities.iloc[:] = intensities.iloc[:]

        liste = dateiname.split('_')
        #   liste.insert(6, '100%buffer')
        liste = '_'.join(liste)

        if times.empty is False:
            all = times.append(df_intensities)
            all = all.fillna(0)

        else:
            # df = pd.DataFrame([{generate_filename(liste, '_w9_o1_s_pdD.csv')}], columns=['Intensity [a. u.]'], index=['filename'])
            # print(df)
            # df = df.transpose()
            # print(df)
       #     print(df['filename'])
      #      print(df_intensities)
        #     df_intensities = df_intensities.transpose()
        #     print(df_intensities)
        # #    df_intensities.insert(0, 'filename', df['filename'].values.tolist())
        #     print(df_intensities)
        #     df_intensities = df_intensities.transpose()
       #     print(df_intensities)
            all = df_intensities.rename(columns={"Intensity [a. u.]": str(generate_filename(liste, '_w9_o1_s_pdD.csv'))})
        #    all = df.append(df_intensities)
       #     all = all.fillna(0)
           # print(all)
           #  print(df.iloc[0][0])
           #  print(isinstance(df.iloc[0][0], tuple))
           #  print(df_intensities.iloc[0][0])
           #  print(isinstance(df_intensities.iloc[0][0], object))
           #  all = df.append(df_intensities, ignore_index=True)
       #
#            print(df_intensities)
 #           print('aslkdfj')

        all.to_csv(generate_filename(liste, '_w9_o1_s_pdD.csv'), sep=';')
