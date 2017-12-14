import pandas as pd
import regex as re
from scipy import stats
from lib.allgemein import liste_in_string_umwandeln


def baselinecorrection(intensities, punkte_baseline):
    df = intensities.copy()
    punkte_baseline.sort()
    spectrum_values = get_spectrum_values(df, punkte_baseline)
    dff_neue_BL = split_in_frames_and_back(df, spectrum_values)
    df_korregiert = df - dff_neue_BL
    return df_korregiert


def get_spectrum_values(df,punkte_baseline):
    ind = df.index.values.tolist()
    ks = []
    for i in range(0, len(punkte_baseline)):
        for k in ind:
            if re.match(str(punkte_baseline[i]) + '\.[0-9]+', str(k)):
                ks.append(k)
                break
    return ks


def split_in_frames_and_back(df, spectrum_values):
    copy_df = df.copy()
    predf=[]
    for frame in copy_df:
        framenummer = frame
        nframe = split_in_baselines(copy_df[frame], spectrum_values, framenummer)
        predf.append(nframe)
    ndf = pd.DataFrame(predf)
    ndf = ndf.transpose()
    return ndf


def split_in_baselines(frame, spectrum_values, framenummer):
    copy_frame = frame.copy()
    for i in range(0, len(spectrum_values) - 1):
        if i == 0:
            points = [spectrum_values[i], spectrum_values[i + 1]]
            kurvenabschnitt = copy_frame.ix[points[0]:points[1]]
            gefittet = fitten(kurvenabschnitt, spectrum_values, i, framenummer)
            a = gefittet.ix[spectrum_values[i]:spectrum_values[i + 1]]
        else:
            points = [spectrum_values[i], spectrum_values[i + 1]]
            kurvenabschnitt = copy_frame.ix[points[0]:points[1]]
            gefittet = fitten(kurvenabschnitt, spectrum_values, i, framenummer)
            b = gefittet.iloc[1:]
            a = a.append(b)
    nframe = copy_frame - copy_frame + a
    nframe = nframe.fillna(0)
    return nframe


def fitten(kurvenabschnitt, spectrum_values, i, framenummer):   #, [spectrum_values[i]: spectrum_values[i + 1]]):
    copy_kurvenabschnitt = kurvenabschnitt.copy()
    dataset = copy_kurvenabschnitt.ix[[spectrum_values[i], spectrum_values[i + 1]]]
    x = dataset.index.values.tolist()
    y = dataset.values.tolist()
    m, t = lin_fit(x, y)
    x_bl = copy_kurvenabschnitt
    zwischenDF = pd.DataFrame(x_bl)
    zwischenDF[framenummer] = (copy_kurvenabschnitt.index * m) + t
    zwischenDF = pd.Series(zwischenDF[framenummer])
    return zwischenDF


def lin_fit(x, y, xlab=None, ylab=None, **kwargs):
    """Fit a set of data with stats.lingress and plot it."""
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    ''' #https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.linregress.html
    slope : float
    slope of the regression line
    intercept : float
    intercept of the regression line
    rvalue : float
    correlation coefficient
    pvalue : float
    two-sided p-value for a hypothesis test whose null hypothesis is that the slope is zero.
    stderr : float
    Standard error of the estimated gradient.
    '''
    return slope, intercept
