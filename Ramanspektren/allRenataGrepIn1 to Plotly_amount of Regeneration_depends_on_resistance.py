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
    if dateiname.endswith('usammenfassung_Renata_grep_und_Stromzeug.csv') or dateiname.endswith('usammenfassung_Renata_grep_und_Stromzeug.CSV'):
        print(dateiname)
        with open(dateiname) as fd:
            df = pd.read_csv(fd, index_col=0, header=0, sep=';')
            print(df)

            # print(df.ix[:, 'Frame 1':'Frame 2'])
            df2 = df.ix[:, 'Frame 1':'Frame 400'].apply(lambda x: x / df['Frame 200'] * 100, axis=0)  # Normalisierung
#            print(df2)

            x_values = df['in chip resistance [Ohm]']
           # x_values = liste_in_floats_umwandeln(x_values)
            print(x_values)

            interval = df2.ix[:, 'Frame 200':]
            y_values = 100 - interval.min(axis=1)
            print(y_values)

            plotly_y_dependent_of_x(x_values, y_values, dateiname, suffix_for_new_filename='_RegVsResistance.html',
                                    x_range=None, y_range=[0, 105],
                                    x_dtick=5000, y_dtick=10,
                                    xaxis_title='resistance [Ohm]', yaxis_title='signal decrease [%]')
