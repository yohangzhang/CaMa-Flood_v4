import calendar
from datetime import datetime
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tick
import pandas as pd
import matplotlib.dates as mdates
from matplotlib import colors
from scipy.signal import argrelmax
import sys

print(os.path.basename(__file__))

#### initial setting =====================================

syear, eyear = int(sys.argv[1]), int(sys.argv[2])

outdir = './inp/natsim/'

dt = int(sys.argv[3])

tag = sys.argv[4]

mapdir = './inp/map/'

dam_file = '../'+tag+'/damloc_modified_'+tag+'.csv'

####=======================================================

## get map nx, ny ----------------------------------------

f = open(mapdir+'/params.txt', 'r')
data = f.readline()
nx = int(data.strip().split(' ')[0])
data = f.readline()
ny = int(data.strip().split(' ')[0])
f.close()
damcsv = pd.read_csv(dam_file)
ndams = len(damcsv)
print('number of dams:', ndams)

##--------------------------------------------------

maxdays = 1   #number of days to consider extreme values in a year

max_outf = '../'+tag+'/tmp_p01_AnnualMax.bin'
mean_outf = '../'+tag+'/tmp_p01_AnnualMean.bin'


### calculate annual maximum -------------------------------

years = eyear - syear + 1
max_finarray = np.zeros((years*maxdays, ndams))
mean_yeararray = np.zeros((years, ndams))

x_arr = damcsv['ix'].values - 1
y_arr = damcsv['iy'].values - 1

for i, year in enumerate(range(syear, eyear+1, 1)):
    print(' ')
    print(year)

    ## read NAT outflw
    outflw_file = outdir + '/outflw' + str(year) + '.bin'
    outflw_all = np.fromfile(outflw_file, 'float32').reshape(-1,ny,nx)
    print(outflw_file)

    outflw_dam = outflw_all[:,y_arr,x_arr]
    print('outflw_dam.shape:', outflw_dam.shape)

    ## annual mean
    mean_yeararray[i,:] = np.mean(outflw_dam, axis=0)
    print('mean:', mean_yeararray[i,:5])

    ## annual maximum
    for j, row in damcsv.iterrows():
        outflw = outflw_dam[:,j]
        maxindex = argrelmax(outflw, order=8*7)
        maxarray = outflw[maxindex]
        maxarray_sorted = np.sort(maxarray)[::-1]
        if len(maxarray_sorted) > 0:
            max_finarray[i*maxdays:(i+1)*maxdays, j] = maxarray_sorted[0:maxdays]
        else:
            outflw_sorted = np.sort(outflw)[::-1]
            max_finarray[i*maxdays:(i+1)*maxdays, j] = outflw_sorted[0:maxdays]
    print('max:', max_finarray[i*maxdays,:5])
    

max_finarray.astype('float32').tofile(max_outf)

mean_finarray = np.mean(mean_yeararray, axis=0)
mean_finarray.astype('float32').tofile(mean_outf)
print(max_outf)
print(mean_outf)
print('#########################')
print(' ')
    
# %%
