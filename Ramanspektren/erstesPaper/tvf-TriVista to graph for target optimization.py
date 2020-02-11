import os
from lib.xml_import import get_positions
from lib import analyte
from lib.allgemein import generate_filename
from lib.baseline_corr import baselinecorrection
from lib.xml_import import get_intensities
from lib.auswertung import compute_highest_intensity_within_interval
import pandas as pd
import regex as re
from lib.plotlygraphen import plotly_xy_yFehler

suffix_for_new_filename = '_means.csv'
# punkte_baseline = analyte.vier_mercaptobenzoesaeure()
punkte_baseline = analyte.PMBA_nach_Kevin()



def werte_einlesen(punkte_baseline):
    data = pd.DataFrame.from_dict({'intensity': [0], 'parameter': [0]})
    print(os.getcwd())
    #dirpath, dirnames, filenames = \
    for dirpath, dirnames, filenames in os.walk(os.getcwd()):
        # print(dirpath, dirnames, filenames)
        if 'lib' in dirnames:
            dirnames.remove('lib')
        if not dirpath.endswith('\lib'):
            # print(dirpath, dirnames) #, filenames)
            pfad = dirpath.split('\\')
            messungparameter = '_'.join([pfad[-2],pfad[-1]])
            # print(messungparameter)
            for dateiname in os.listdir(dirpath):
                if dateiname.endswith('.tvf') or dateiname.endswith('.TVF'):
                    # print(dirpath, dateiname)
                    # print('_'.join(dateiname.split(' ')))
                    # dst = '_'.join(dateiname.split(' '))
                    # os.rename(os.path.join(dirpath, dateiname), os.path.join(dirpath, dst))
                    intensities = get_intensities(os.path.join(dirpath, dateiname))
                    # print(intensities)
                    df_korregiert = baselinecorrection(intensities, punkte_baseline)
                    # print(df_korregiert)
                    highest_intensity_within_interval = compute_highest_intensity_within_interval(df_korregiert, punkte_baseline)
                    # print(highest_intensity_within_interval.__dict__)
                    # print(highest_intensity_within_interval.values[0])
                    data = data.append(pd.DataFrame.from_dict({'parameter': [messungparameter], 'intensity': [highest_intensity_within_interval.values[0]]}), sort=True)
    return data  # eingelesene werte




def generate_df_with_mean_and_std(data):
    # print(data)
    listofparams = []
    for i in data['parameter']:
        if i is not 0:
            # print(i)
            if i not in listofparams:
                listofparams.append(i)
    # print(listofparams)
    werte = {}
    for j in listofparams:
        subsetDataFrame = data[data['parameter'] == j]
        # print(subsetDataFrame)
        # print(subsetDataFrame.iloc[0, 0])
        # print(subsetDataFrame.iloc[0, 1])
        # print(subsetDataFrame.iloc[1, 0])
        # print(subsetDataFrame.iloc[:, 0])
        # print(subsetDataFrame.iloc[:, 0].mean())
        # print(subsetDataFrame.iloc[:, 0].std())
        # print(j)
        jlist = j.split('_')
        # print(jlist[1], jlist[3], re.sub('s', '', re.sub(',', '.', jlist[-1])))
        dictkeys = str(jlist[1]) + ' ' + str(jlist[3]) + ' ' + str(re.sub('s', '', re.sub(',', '.', jlist[-1])))
        # print(dictkeys)
        # print(dictkeys.split(' '))
        if dictkeys.split(' ')[1] == 'time':
            dictkeys = dictkeys + ' s'
        elif dictkeys.split(' ')[1] == 'conc':
            ratio = dictkeys.split(' ').pop()
            dictkeys = dictkeys + ' ' + str(float(ratio) * 69) + ' %'
        # print(dictkeys)
        werte[dictkeys] = [dictkeys.split(' ')[-2], dictkeys.split(' ')[-1], subsetDataFrame.iloc[:, 0].mean(), subsetDataFrame.iloc[:, 0].std()]
    # print(werte)
    df1 = pd.DataFrame(werte, index=['x_value', 'x_value_dim', 'mean', 'std'])
    df1 = df1.transpose()
    # print(df1)
    return df1


def safe_stuff(data, nwfile):
    data.to_csv(nwfile, sep=';')


def make3_df_from_one(nwfile):
    for datei in os.listdir():
        if datei.endswith('.cv') or datei.endswith(nwfile):
            # print(datei)
            df2 = pd.read_csv(datei, sep=';', index_col=0)
            # print(df2)
            dictwithdf = {'hno3time': df2[df2.index.str.startswith('HNO3 time')],
                          'hno3conc': df2[df2.index.str.startswith('HNO3 conc')],
                          'nh3time': df2[df2.index.str.startswith('NH4OH time')]}
            # print(dictwithdf)
            # print(hno3conc)
            # print(hno3time)
            # print(nh3time)
            return dictwithdf


def generate_graph(dictdf):
    for i in dictdf:  # if i == 'nh3time':
        # print(i)
        # print(dictdf[i])
        # print(type(i))
        # print(dictdf[i].__dict__)
        # print(dictdf['hno3time'].__dict__)
        dictdf['hno3time'].xaxis_title = 'time [s]'
        dictdf['hno3time'].yaxis_title = 'intensity [a. u.]'
        dictdf['hno3time'].x_dtick = 15
        dictdf['hno3conc'].xaxis_title = 'concentration [%]'
        dictdf['hno3conc'].yaxis_title = 'intensity [a. u.]'
        dictdf['hno3conc'].x_dtick = 15
        dictdf['nh3time'].xaxis_title = 'time [s]'
        dictdf['nh3time'].yaxis_title = 'intensity [a. u.]'
        dictdf['nh3time'].x_dtick = 15

        # print(dictdf['hno3time'].__dict__)

        plotly_xy_yFehler(dictdf[i]['x_value'], dictdf[i]['mean'],
                          errory=dictdf[i]['std'],
                          # x_range=[0,dictdf[i]['x_value'].max()],
                          x_dtick=dictdf['nh3time'].x_dtick,
                          dateiname=str(i + '.html'), suffix_for_new_filename=suffix_for_new_filename,
                          xaxis_title=dictdf[i].xaxis_title, yaxis_title=dictdf[i].yaxis_title)



data = werte_einlesen(punkte_baseline)
print(data)
filename = 'optimization'
nwfile = generate_filename(filename, suffix_for_new_filename)
safe_stuff(data, nwfile)
df = generate_df_with_mean_and_std(data)
# print(nwfile)
# safe_stuff(df, nwfile)
            # print(df)
            # print(os.getcwd())

# print(dictdf)

# dictdf = make3_df_from_one(nwfile)
# generate_graph(dictdf)
