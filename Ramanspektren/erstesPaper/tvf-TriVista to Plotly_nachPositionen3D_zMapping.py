﻿'''
imput file: .tvf-TriVista-Datei mit y-Mapping
output file: output file: ein 3D-Graph mit Intensität gegen z-Position
'''
#written by EvaMaria Hoehn



import os
import plotly
from Ramanspektren.lib import analyte
from Ramanspektren.lib.allgemein import generate_filename
from Ramanspektren.lib.auswertung import compute_wn_with_highest_intensity
from Ramanspektren.lib.auswertung import grep_highest_intensity
from Ramanspektren.lib.baseline_corr import baselinecorrection
from Ramanspektren.lib.plotlygraphen import plotly_nach_positionen_3dscatter_layout
from Ramanspektren.lib.xml_import import get_intensities
from Ramanspektren.lib.xml_import import get_positions
from Ramanspektren.lib.plotlygraphen import plotly_nach_positionen_3dscatter_data


suffix_for_new_filename = '_graphMapping.html'
punkte_baseline = analyte.kristallviolett()
band_start = 1605
band_end = 1630


def plotly_nach_positionen(highest_intensity, positions, dateiname, suffix_for_new_filename):
    nwfile = generate_filename(dateiname, suffix_for_new_filename)
    fig = dict(data=plotly_nach_positionen_3dscatter_data(x_positions=[0] * len(positions.ix['y [µm]'].values.tolist()),
                                                          y_positions=[0] * len(positions.ix['y [µm]'].values.tolist()),
                                                          z_positions=positions.ix['z [µm]'].values.tolist(),
                                                          highest_intensities=highest_intensity.ix['highest intensity [a. u.]'].values.tolist()
                                                          ), layout=plotly_nach_positionen_3dscatter_layout(x_lables=False, y_lables=False, z_lables=True))
    plotly.offline.plot(fig, filename=nwfile, auto_open=False)  #, image_filename=nwfile, image='png', image_width=1600, image_height=860)



for dateiname in os.listdir():
    if dateiname.endswith('.tvf') or dateiname.endswith('uche.TVF'):
        print(dateiname)
        intensities = get_intensities(dateiname)
        df_korregiert = baselinecorrection(intensities, punkte_baseline)
        wn_with_highest_intensity = compute_wn_with_highest_intensity(df_korregiert, band_start, band_end)
        highest_intensity = grep_highest_intensity(df_korregiert, wn_with_highest_intensity)
        try:
            positions = get_positions(dateiname)
            plotly_nach_positionen(highest_intensity, positions, dateiname, suffix_for_new_filename)
        except:
            print('no positions')
