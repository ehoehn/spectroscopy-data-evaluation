import os
import numpy as np
import pandas as pd
from datetime import time, timedelta, datetime
#import datetime, time


def liste_in_string_umwandeln(input):
    ft = []
    for i in input:
        k = np.str(i)
        ft.append(k)
    return ft


def separate_the_two_columns(fd):
    timestamp = []
    intensity = []
    cnt = 0
    for l in fd:
        # print(l)
        if cnt % 2 == 0:
            timestamp.append(l.strip()[0:-1])
        if cnt % 2 == 1:
            intensity.append(l.strip())
        cnt += 1
    #print(len(timestamp))
    #print(len(intensity))
    return timestamp, intensity


def split_the_merged_stuff(intensity):
    for m in range(len(intensity)):
        # print(len(i))
        if len(intensity[m]) > 3:
            #        print(intensity[m])
            subs = []
            for i in range(0, len(intensity[m]), 3):
                subs.append(intensity[m][i:i + 3])
                #print(subs)
            intensity[m] = subs
    #print(intensity)
    return subs, intensity


for dateiname in os.listdir():
    if dateiname.endswith('.log') and dateiname.startswith('output_2019-02-04_16-04-53Einspritzen'):
        print(dateiname)
        with open(dateiname) as fd:
            timestamp, intensity = separate_the_two_columns(fd)

          #  subs, intensity = split_the_merged_stuff(intensity)



           # print(timestamp)
           # print(len(timestamp), len(intensity))

            newtimestamp = []
            newintensity = []
            #print(newtimestamp)

            for ti in range(len(timestamp)-1, -1, -1):
              #  print(ti)
                #print(timestamp[ti])
               # print(intensity[ti])
                if isinstance(intensity[ti], list):
                    #print(True)
                    #print(len(intensity[ti]))
                    for k in range(len(intensity[ti])-1, -1, -1):
                       # print(timestamp[ti], intensity[ti][k])
                        newtimestamp.insert(0, timestamp[ti])
                        newintensity.insert(0, intensity[ti][k])
                else:
                    #print(timestamp[ti], intensity[ti])
                    newtimestamp.insert(0, timestamp[ti])
                    newintensity.insert(0, intensity[ti])

            #print(newtimestamp)
           # print(newintensity)
            #tim = pd.to_datetime(newtimestamp)
            #print(tim)
            #periodenindex = pd.PeriodIndex(tim, freq='ms')
            #print(periodenindex)
           # print(isinstance(newtimestamp[0], str))
          #  print(newtimestamp[0])
          #  t = time()
            #t = time.strptime(str(newtimestamp[0]), '%H:%M:%S.%f')
            #t = time.strptime('02:02:03.574', '%H:%M:%S.%f')

            #s=time()
            # s.fromisoformat(newtimestamp[1])
            # delta=t-s
            # print(delta)
            # timdelta = pd.to_timedelta(newtimestamp)
            # DateTime(newtimestamp[0])
            # print(pd.to_datetime(newtimestamp[1]) - pd.to_datetime(newtimestamp[0]))
            # print(timdelta[1] + newtimestamp[0])
            timee = [datetime.strptime(newtimestamp[0], '%H:%M:%S.%f') - datetime.strptime(newtimestamp[0],'%H:%M:%S.%f')]
            for n in range(len(newtimestamp)-1):
                timeelapsed = datetime.strptime(newtimestamp[n+1], '%H:%M:%S.%f') - datetime.strptime(newtimestamp[0],'%H:%M:%S.%f')
                timee.append(str(timeelapsed))
            timee = liste_in_string_umwandeln(timee)
           #     print(timeelapsed)
            print(timee)

           # print(str(datetime.strptime(newtimestamp[1], '%H:%M:%S.%f')) + ' - ' + str(datetime.strptime(newtimestamp[0], '%H:%M:%S.%f')))

            #print(datetime.strptime(newtimestamp[1], '%H:%M:%S.%f') - datetime.strptime(newtimestamp[0], '%H:%M:%S.%f'))
            #print(datetime.combine(datetime.strptime(newtimestamp[1], '%H:%M:%S.%f')))
            # #- datetime.combine(datetime.strptime(newtimestamp[0], '%H:%M:%S.%f')))

            #timee = periodenindex.to_timestamp(freq='ms')
            #print(timee.nanosecond[0]-timee.nanosecond[5])
            #print(time[0])
            #print(pd.Period(time[0], freq='ms') - pd.Period(time[1], freq='ms'))
           # print(newintensity)
            df = pd.DataFrame(timee, columns=['time[hh:mm:ss]'])
            df2 = pd.DataFrame(newintensity, columns=['intensity[a. u.]'])
            #print(df2)
            df['intensity[a. u.]'] = df2['intensity[a. u.]']
          #  df = df.groupby(df['time[hh:mm:ss]'])['intensity[a. u.]'].sum()
          #  print(df)
            df.to_csv(dateiname.split('.')[0]+'_.csv', sep=';')

