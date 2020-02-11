import pandas as pd
import scipy.signal
import regex as re


def compute_highest_intensity_within_interval(df_korregiert, punkte_baseline):
    interval = df_korregiert.ix[punkte_baseline[0]:punkte_baseline[1]]
    highest_intensity = interval.max()
    return highest_intensity

def compute_wn_with_highest_intensity(df_korregiert, band_start, band_end):
    interval = df_korregiert.ix[band_start:band_end]
    wn_with_highest_intensity = interval.idxmax(axis=0)
    return wn_with_highest_intensity

def compute_wn_with_highest_intensity_labelbased(df, band_start, band_end):
    ind = df.index.values.tolist()
    k = []
    for i in ind:
        if re.match(str(band_start) + '\.[0-9]+', str(i)):
    #        print(i)
            break
        elif re.match(str(band_start+1) + '\.[0-9]+', str(i)):
    #        print(i)
            break
    for j in ind:
        if re.match(str(band_end) + '\.[0-9]+', str(j)):
     #       print(j)
            break
        elif re.match(str(band_end+1) + '\.[0-9]+', str(j)):
     #       print(j)
            break
    interval = df.loc[i:j]
    wn_with_highest_intensity = interval.idxmax(axis=0)
    return wn_with_highest_intensity


def grep_highest_intensity(df_korregiert, wn_with_highest_intensity):
    highest_intensity = []
    for i in range(0, len(wn_with_highest_intensity)):
        highest_intensity.append(df_korregiert[wn_with_highest_intensity.index[i]][wn_with_highest_intensity[i]])
    df_highest_intensity = pd.DataFrame(highest_intensity, index=wn_with_highest_intensity.index, columns=['highest intensity [a. u.]'])
    df_highest_intensity = df_highest_intensity.transpose()
    return df_highest_intensity


def compute_frame_with_highest_intensity(intensities, band_start, band_end):
    copy_intensities = intensities.copy()
    interval = copy_intensities.ix[band_start:band_end]
    band = interval.apply(max, axis=0)
    lowest = band.idxmax()
    dfn = lowest.split(' ')
    framenumber = int(dfn[1])
    return framenumber


def compute_frame_with_lowest_intensity(intensities, band_start, band_end):
    copy_intensities = intensities.copy()
    interval = copy_intensities.ix[band_start:band_end]
    band = interval.apply(max, axis=0)
    lowest = band.idxmin()
    dfn = lowest.split(' ')
    framenumber = int(dfn[1])
    return framenumber


def compute_frame_with_lowest_intensity_labelbased(intensities, band_start, band_end):
    ind = intensities.index.values.tolist()
  #  print(ind)
    k = []
    for i in ind:
        if re.match(str(band_start) + '\.[0-9]+', str(i)):
            #        print(i)
            break
    for j in ind:
        if re.match(str(band_end) + '\.[0-9]+', str(j)):
            #       print(j)
            break
    interval = intensities.loc[i:j]
    band = interval.apply(max, axis=0)
    lowest = band.idxmin()
    dfn = lowest.split(' ')
    framenumber = int(dfn[1])
    return framenumber


def compute_frame_with_lowest_intensity_from_smoothed(smoothed):
    copy_smoothed = smoothed.copy()
    lowest = copy_smoothed.idxmin(axis=1)
    lowest = lowest.values.tolist()[0]
    dfn = lowest.split(' ')
    framenumber = int(dfn[1])
    return framenumber


def savitzkygolay_for_pandas(df, window_length=21, polyorder=3):
    smoothed = scipy.signal.savgol_filter(df.transpose(), window_length, polyorder, axis=0, mode='nearest')  # https://docs.scipy.org/doc/scipy-0.16.1/reference/generated/scipy.signal.savgol_filter.html
    smoothed = smoothed.transpose()
    smoothed = pd.DataFrame(smoothed, index=[df.index], columns=[df.columns])
    return smoothed


def savitzkygolay_for_malgucken(df, window_length=21, polyorder=3):
    smoothed = scipy.signal.savgol_filter(df.transpose(), window_length, polyorder, axis=0, mode='nearest')  # https://docs.scipy.org/doc/scipy-0.16.1/reference/generated/scipy.signal.savgol_filter.html
    return smoothed
