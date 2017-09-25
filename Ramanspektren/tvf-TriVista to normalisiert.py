'''
imput file: .tvf-TriVista-Datei
output file: ein DataFrame mit wellenzahlen in Zeilen und Frames in Spalten mit korregierter Baseline
'''
#written by EvaMaria Hoehn


import os
from Ramanspektren.lib.xml_import import get_positions
from Ramanspektren.lib import analyte
from Ramanspektren.lib.allgemein import generate_filename
from Ramanspektren.lib.baseline_corr import baselinecorrection
from Ramanspektren.lib.xml_import import get_intensities


suffix_for_new_filename = '_normalisiert.csv'
punkte_baseline = analyte.kristallviolett()


for dateiname in os.listdir():
    if dateiname.endswith('.tvf') or dateiname.endswith('.TVF'):
        positions = get_positions(dateiname)
        intensities = get_intensities(dateiname)
        df_korregiert = baselinecorrection(intensities, punkte_baseline)
        nwfile = generate_filename(dateiname, suffix_for_new_filename)

        normalisiert = df_korregiert.apply(lambda x: x / df['Frame 100'] * 100, axis=0)

        normalisiert.to_csv(nwfile, sep=';')


# df2 = df.apply(lambda x: x + df['eee'], axis=0)
# print(df2)
# df3 = df.apply(lambda x: x + df.ix[1], axis=1)
# print(df3)

# either the DataFrame’s index (axis=0) or the columns (axis=1)