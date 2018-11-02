#!usr/bin/env python
"""Plots any dat file assuming time is in seconds.
"""
import numpy as np
from matplotlib import pyplot as plt
import sys
import math

nruns = 18
c = 0
leg = [None]*nruns
m = [0.01,0.1]
bac = [0.01,0.1,0.22]
bct = [0.02,0.14,0.4]

for i in range(2):
	for j in range(3):
		for k in range(3):
			print m[i]
			leg[c] = ['m=' + str(m[i]) + ' bac=' + str(bac[j]) + ' bct=' + str(bct[k])]
			c = c + 1

		

leg_ordered = [None]*18

# Low-sloping domains: simulations 1-9
# Hi-sloping domains: simulations 10-18

fix,axarr = plt.subplots(2,3,sharey=False,sharex=True)
c = 1
t1 = 9
t2 = 10
for i in range(2):
	for j in range(3):	
		mat = np.loadtxt('run.' + str(c) + '/subsurface_outlet_flux.dat')
		t = mat[:,0]/86400/365  # time in days
		y = mat[:,1] # thing we're plotting
		#leg_ordered[i-1] = leg[i-1]
		axarr[i,j].plot(t,np.log10(y))
		mat = np.loadtxt('run.' + str(c+3) + '/subsurface_outlet_flux.dat')
        	t = mat[:,0]/86400/365  # time in days
        	y = mat[:,1] # thing we're plotting
        	#leg_ordered[i-1] = leg[i-1]
        	axarr[i,j].plot(t,np.log10(y))
		mat = np.loadtxt('run.' + str(c+6) + '/subsurface_outlet_flux.dat')
		t = mat[:,0]/86400/365
		y = mat[:,1]
		axarr[i,j].plot(t,np.log10(y))
		c = c + 1
		plt.xlim(t1,t2)
		#plt.xlabel('Time [yrs]')
		#plt.title('subsuurface outlet flux')
		plt.legend(['min','mean','max'])
	c = c + 6
plt.show() 
