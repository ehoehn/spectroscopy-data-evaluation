import os
import regex as re


for dateiname in os.listdir():
    if dateiname.endswith('170814_0,01mM_CV_40erObjektiv_1%_20_1,00V_beiF1Analyt_beiF20ElektrolythFlussAn_beiF200ProgStart.tvf'): # or dateiname.endswith('.TVF'):
        print(dateiname)

        # ".*_[0-9]*\.[0-9]*[V]_.*"
 #       ks = []
  #      if re.match("[0-9]*,[0-9]*V", dateiname):
        print(re.match('.*[0-9],[0-9]', dateiname))
        print(re.match('[0-9]+.[0-9]+', dateiname))
#            print(k)
     #           ks.append(k)
    #print(ks)


#
# position = re.findall('ValuePosition="\W?[0-9]*\W?[0-9]*\W*[0-9]*\W?[0-9]*\W*[0-9]*\W?[0-9]"', content)
