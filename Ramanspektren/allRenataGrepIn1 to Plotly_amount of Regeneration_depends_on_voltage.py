import os
import pandas as pd
from Ramanspektren.lib.allgemein import liste_in_floats_umwandeln
from Ramanspektren.lib.xml_import import get_times
from Ramanspektren.lib.plotlygraphen import plotly_y_dependent_of_x


suffix_for_new_filename = '_RegenerationVsVoltage.html'


'''
imput file: eine .csv-Datei Datei mit zeitl Verlauf in einer Tabelle nach baseline korrektur
output file: schlichter Graph mit 2D-Scatterplot in Plotly

'''

for dateiname in os.listdir():
    if dateiname.endswith('_beiF1Analyt_beiF20ElektrolythFlussAn_beiF200ProgStart.tvf') or dateiname.endswith('_beiF1Analyt_beiF20ElektrolythFlussAn_beiF200ProgStart.TVF'):
     #   print(dateiname)
        times = get_times(dateiname)

        TimeVoltageOn = round(times['Frame 200']['time [s]'] + 100, 0)
        FrameVoltageOn = times[times.columns[times.ix['time [s]'] > TimeVoltageOn - 1]].columns[0]
# break

for dateiname in os.listdir():
    if dateiname.endswith('usammenfassung_Renata_grep.csv') or dateiname.endswith('usammenfassung_Renata_grep.CSV'):
        print(dateiname)
        with open(dateiname) as fd:
            df = pd.read_csv(fd, index_col=0, header=0, sep=';')
            df2 = df.apply(lambda x: x / df[FrameVoltageOn] * 100, axis=0)  # Normalisierung

            voltage = []
            for k in df2.index:
                nr = k.split('_')
                nr = nr[6]
                nr = nr[:-1]
                nr = nr.replace(',', '.')
                voltage.append(nr)
            x_values = voltage
            x_values = liste_in_floats_umwandeln(x_values)
           # print(x_values)

            interval = df2.ix[:, FrameVoltageOn:]
            y_values = 100 - interval.min(axis=1)
        #    print(y_values)
            print(y_values)
            df2['signal decrease [%]'] = y_values
            print(df2)
            df2.to_csv('Zusammenfassung_Renata_grep_mitSignalDecrease.csv', sep=';')

            plotly_y_dependent_of_x(x_values, y_values, dateiname, suffix_for_new_filename,
                                    x_range=None, y_range=[0, 105],
                                    x_dtick=2.5, y_dtick=10,
                                    xaxis_title='U [V]', yaxis_title='signal decrease [%]')
