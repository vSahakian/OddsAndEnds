#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 14:30:19 2020

@author: vjs
"""

### Plot raw core data for a few cores
## VJS 7/2020 for OC2006A



import numpy as np
import MSTtools as mst
import matplotlib.pyplot as plt

fig_dir = '/Users/vjs/OC2006A/data/MSTfigs/'

# %% 2GC
####################  Core 2GC ####################
proc_outfile = '/Users/vjs/OC2006A/data/MST/outfiles/volume_normalized/OC2006A-2GC_vol_MS.out'

## Read Data:
data,units,coreinfoJ = mst.read_MSToutfile(proc_outfile,clean=False)

## Make figure path:
figpath = fig_dir + coreinfoJ['cruise'] + '_' + coreinfoJ['core'] + '_raw.pdf'

## plssible colors...
#JCcolors = ['#5578ad','#ad6255','#56b851']

## Plot parameters:
vmin = 1280
vmax = 1500
rhomin = 0.5
rhomax = 1.55
msmin = 0
msmax = 50
plot_xlims = {'pvel':[vmin,vmax],'rho':[rhomin,rhomax],'msu':[msmin,msmax]}

#
### Plot GC alone
mst.pltMST(proc_outfile,figpath,endcal='Yes',plotvals=['pvel','rho','msu'],xlims=plot_xlims,clean_caps=False,cleanPwave=False)

plt.close('all')
