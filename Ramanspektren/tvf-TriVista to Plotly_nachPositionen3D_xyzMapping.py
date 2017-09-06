'''
imput file: .tvf-TriVista-Datei mit xyz-Mappting
output file: ein Graph mit Positionen eines Mappings xyz
'''
#written by EvaMaria Hoehn


import os
import plotly
import plotly.graph_objs as go  # import Scatter, Layout
from lib.xml_import import get_positions
from lib import analyte
from lib.xml_import import get_intensities
from lib.baseline_corr import baselinecorrection
from lib.allgemein import generate_filename
from lib.auswertung import compute_wn_with_highest_intensity
from lib.auswertung import grep_highest_intensity
from lib.plotlygraphen import viridis_plus_rot, plotly_nach_positionen_3dscatter_layout
from lib.plotlygraphen import plotly_nach_positionen_3dscatter_data


suffix_for_new_filename = '_graphMapping.html'
punkte_baseline = analyte.kristallviolett()
band_start = 1605
band_end = 1630


def plotly_nach_positionen(highest_intensity, positions, dateiname):
    nwfile = generate_filename(dateiname, suffix_for_new_filename)
    fig = dict(data=plotly_nach_positionen_3dscatter_data(x_positions=positions.ix['x [µm]'].values.tolist(),
                                                          y_positions=positions.ix['y [µm]'].values.tolist(),
                                                          z_positions=positions.ix['z [µm]'].values.tolist(),
                                                          highest_intensities=highest_intensity.ix['highest intensity [a. u.]'].values.tolist()
                                                          ), layout=plotly_nach_positionen_3dscatter_layout(x_lables=True, y_lables=True, z_lables=True))
    plotly.offline.plot(fig, filename=nwfile,  image_filename=nwfile)  #, image='png', image_width=1600, image_height=860)



for dateiname in os.listdir():
    if dateiname.endswith('xyz.tvf') or dateiname.endswith('xyz.TVF'):
        print(dateiname)
        intensities = get_intensities(dateiname)
        df_korregiert = baselinecorrection(intensities, punkte_baseline)
        wn_with_highest_intensity = compute_wn_with_highest_intensity(df_korregiert, band_start, band_end)
        highest_intensity = grep_highest_intensity(df_korregiert, wn_with_highest_intensity)

        try:
            positions = get_positions(dateiname)
            plotly_nach_positionen(highest_intensity, positions, dateiname)
        except:
            print('no positions')
