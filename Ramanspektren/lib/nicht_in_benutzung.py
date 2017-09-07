import regex as re


def get_idxfcore(df, spectrum_values):
    copy_df = df.copy()
    idxfcore = []
    for i in range(0, len(spectrum_values)):
        if i + 1 == len(spectrum_values):
            break
        else:
            points = [spectrum_values[i], spectrum_values[i + 1]]
            sp = copy_df.ix[points[0]:points[1]]
            x_bl = sp.index.values.tolist()
            for j in x_bl[:-1]:
                idxfcore.append(j)
            idxfcore.append(x_bl[-1])
    return idxfcore


def get_point_values(df, punkt):
    ind = df.ix[0].values.tolist()
    ind = liste_in_floats_umwandeln(ind)
    ks = []
    for i in range(0, len([punkt])):
        for k in ind:
            if re.match(str(punkt) + '\.[0-9]+', str(k)):
                ks.append(k)
    return ks