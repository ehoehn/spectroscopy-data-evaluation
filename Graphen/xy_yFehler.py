import os
# from plotly import graph_objs as go
import pandas as pd
from lib.plotlygraphen import plotly_xy_yFehler


suffix_for_new_filename = '_xyGraph_yFehler.html'


for dateiname in os.listdir():
    if dateiname.endswith('.csv') or dateiname.endswith('.CSV'):
        print(dateiname)
        with open(dateiname) as fd:


            df = pd.read_csv(fd, index_col=0, header=0, sep=';')
            print(df)

            x = df.index.values.tolist()
            y = df['intensity [a. u.]'].values.tolist()
            error_y = df['error [a. u.]'].values.tolist()

          #  plotly_xy_yFehler(x_values=x, y_values=y, errory=error_y, dateiname=dateiname, suffix_for_new_filename=suffix_for_new_filename, xaxis_title='time [s]', yaxis_title='intensity [a. u.]')

