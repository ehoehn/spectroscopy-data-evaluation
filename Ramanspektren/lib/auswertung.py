import pandas as pd


def compute_wn_with_highest_intensity(df_korregiert, band_start, band_end):
    interval = df_korregiert.ix[band_start:band_end]
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


def compute_frame_with_lowest_intensity_from_smoothed(smoothed):
    copy_smoothed = smoothed.copy()
    lowest = copy_smoothed.idxmin(axis=1)
    lowest = lowest.values.tolist()[0]
    dfn = lowest.split(' ')
    framenumber = int(dfn[1])
    return framenumber