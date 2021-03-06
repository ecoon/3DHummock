#!usr/bin/env python
"""Plots any dat file assuming time is in seconds.
"""
import numpy as np
from matplotlib import pyplot as plt
import sys
import math
from scipy import stats

runPrefixList = ['DwarfShrubsHi','DwarfShrubsLo','WoodyShrubsHillslope','WoodyShrubsRiparianHi','WoodyShrubsRiparianLo','TussockTundraHi','TussockTundraLo','WaterTrack','SedgeHi','SedgeLo']
runDate = '05Dec18'

nruns = 32

t1 = 9
t2 = 10
t1 = t1*365
t2 = t2*365
ndays = (t2-t1)
y = np.nan*np.ones([ndays,nruns],'d')
meany = np.nan*np.ones([ndays,len(runPrefixList)],'d')
t = np.nan*np.ones([ndays,nruns],'d')
for i in range(2):#len(runPrefixList)):
	for j in range(nruns):	
		mat = np.loadtxt(runPrefixList[i] + '_' + runDate + '.' + str(j+1) + '/subsurface_outlet_flux.dat')
		matSubset = mat[t1:-1,:]
		matShape = matSubset.shape
		if matShape[0] > ndays:
			t = mat[t1:t2,0]/86400/365  # time in days
			y[:,j] = mat[t1:t2,1] # thing we're plotting
		else:
			y[0:matShape[0],j] = mat[t1:-1,1]
	meany[:,i]= stats.nanmean(y,1) # in the 1st dimension
	print(meany[:,i])
	plt.plot(t,np.log10(meany[:,i]))
	plt.hold(True)
	#plt.set_ylabel('Flow [log10 cms]')
	#plt.set_xlabel('Time [yrs of sim]')
plt.legend(runPrefixList)
plt.show() 
