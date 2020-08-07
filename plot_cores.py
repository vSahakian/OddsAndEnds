#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 15:40:58 2020

@author: vjs
"""

## Plotting of MST data
## VJS 7/2020 for OC2006A

import numpy as np
import MSTtools as mst
import matplotlib.pyplot as plt

fig_dir = '/Users/vjs/OC2006A/data/MSTfigs/'


# %% 2GC
####################  Core 2GC ####################
proc_outfile = '/Users/vjs/OC2006A/data/MST/outfiles/volume_normalized/OC2006A-2GC_vol_MS.out'

## Read Data:
data,units,coreinfoJ = mst.read_MSToutfile(proc_outfile)

## Make figure path:
figpath = fig_dir + coreinfoJ['cruise'] + '_' + coreinfoJ['core'] + '.pdf'

## plssible colors...
#JCcolors = ['#5578ad','#ad6255','#56b851']

## Plot parameters:
vmin = 1380
vmax = 1450
rhomin = 1.22
rhomax = 1.55
msmin = 0
msmax = 50
plot_xlims = {'pvel':[vmin,vmax],'rho':[rhomin,rhomax],'msu':[msmin,msmax]}

#
### Plot GC alone
mst.pltMST(proc_outfile,figpath,endcal='Yes',plotvals=['pvel','rho','msu'],xlims=plot_xlims)

plt.close('all')


# %% 3GC
####################  Core 3GC ####################
proc_outfile = '/Users/vjs/OC2006A/data/MST/outfiles/volume_normalized/OC2006A-3GC_vol_MS.out'

## Read Data:
data,units,coreinfoJ = mst.read_MSToutfile(proc_outfile)

## Make figure path:
figpath = fig_dir + coreinfoJ['cruise'] + '_' + coreinfoJ['core'] + '.pdf'

## plssible colors...
#JCcolors = ['#5578ad','#ad6255','#56b851']

## Plot parameters:

vmin = 1325
vmax = 1525
rhomin = 1.22
rhomax = 1.55
msmin = 0
msmax = 50

plot_xlims = {'pvel':[vmin,vmax],'rho':[rhomin,rhomax],'msu':[msmin,msmax]}

#
### Plot GC alone
mst.pltMST(proc_outfile,figpath,endcal='Yes',plotvals=['pvel','rho','msu'],xlims=plot_xlims)

plt.close('all')


# %% 9GC
####################  Core 9GC ####################
proc_outfile = '/Users/vjs/OC2006A/data/MST/outfiles/volume_normalized/OC2006A-9GC_vol_MS.out'

## Read Data:
data,units,coreinfoJ = mst.read_MSToutfile(proc_outfile)

## Make figure path:
figpath = fig_dir + coreinfoJ['cruise'] + '_' + coreinfoJ['core'] + '.pdf'

## plssible colors...
#JCcolors = ['#5578ad','#ad6255','#56b851']

## Plot parameters:

vmin = 1325
vmax = 1525
rhomin = 1.22
rhomax = 1.60
msmin = 0
msmax = 55

plot_xlims = {'pvel':[vmin,vmax],'rho':[rhomin,rhomax],'msu':[msmin,msmax]}

#
### Plot GC alone
mst.pltMST(proc_outfile,figpath,endcal='Yes',plotvals=['pvel','rho','msu'],xlims=plot_xlims)

plt.close('all')


# %% 10JC
####################  Core 10JC ####################
proc_outfileJC = '/Users/vjs/OC2006A/data/MST/outfiles/volume_normalized/OC2006A-10PC_vol_MS.out'
proc_outfileTC = '/Users/vjs/OC2006A/data/MST/outfiles/volume_normalized/OC2006A-10TC_vol_MS.out'

#sbdepth,section_num,section_depth,pvel,rho,msu,resistivity,fracporosity,units,coreinfo = mst.read_MSToutfile(proc_outfile)
dataJ,unitsJ,coreinfoJ = mst.read_MSToutfile(proc_outfileJC)
dataT,unitsT,coreinfoT = mst.read_MSToutfile(proc_outfileTC)

figpath_jc = fig_dir + coreinfoJ['cruise'] + '_' + coreinfoJ['core'] + '.pdf'
figpath_tc = fig_dir + coreinfoT['cruise'] + '_' + coreinfoT['core'] + '.pdf'
figpath_together = fig_dir + coreinfoT['cruise'] + '_' + coreinfoT['core'] + '_JC.pdf'

## plssible colors...
#JCcolors = ['#5578ad','#ad6255','#56b851']

## Shift the JC?
shift_10 = 65
## Plot parameters:

vmin = 1410
vmax = 1530
rhomin = 1.22
rhomax = 2.0
msmin = 0
msmax = 300

plot_xlims = {'pvel':[vmin,vmax],'rho':[rhomin,rhomax],'msu':[msmin,msmax]}

#
### Plot JC alone
#mst.pltMST(proc_outfileJC,figpath_jc,endcal='Yes',plotvals=['pvel','rho','msu'],xlims=plot_xlims)
#           
#           
## Plot together:
mst.pltJpcTc(proc_outfileJC,proc_outfileTC,figpath_together,endcal='Yes',plotvals=['pvel','rho','msu'],xlims=plot_xlims,jcshift=shift_10)
plt.close('all')

# %% 9GC and 10 together
##Plot 9GC and 10 JPC/TC together
proc_outfileJC = '/Users/vjs/OC2006A/data/MST/outfiles/volume_normalized/OC2006A-10PC_vol_MS.out'
proc_outfileTC = '/Users/vjs/OC2006A/data/MST/outfiles/volume_normalized/OC2006A-10TC_vol_MS.out'
proc_outfileGC = '/Users/vjs/OC2006A/data/MST/outfiles/volume_normalized/OC2006A-9GC_vol_MS.out'


#sbdepth,section_num,section_depth,pvel,rho,msu,resistivity,fracporosity,units,coreinfo = mst.read_MSToutfile(proc_outfile)
dataJ,unitsJ,coreinfoJ = mst.read_MSToutfile(proc_outfileJC)
dataT,unitsT,coreinfoT = mst.read_MSToutfile(proc_outfileTC)
dataG,unitsG,coreinfoG = mst.read_MSToutfile(proc_outfileGC)

figpath_together = fig_dir + coreinfoT['cruise'] + '_' + coreinfoT['core'] + '_JC_' + coreinfoG['core'] + '.pdf'


## Shift the JC?
shift_10jc = 65
## Shift the TC?
shift_10tc = 0
## Shift the GC?
shit_9gc = 0

## Plot parameters:

vmin = 1410
vmax = 1530
rhomin = 1.22
rhomax = 2.0
msmin = 0
msmax = 300

plot_xlims = {'pvel':[vmin,vmax],'rho':[rhomin,rhomax],'msu':[msmin,msmax]}

#
### Plot JC alone
#mst.pltMST(proc_outfileJC,figpath_jc,endcal='Yes',plotvals=['pvel','rho','msu'],xlims=plot_xlims)
#           
#           
## Plot together:
mst.pltJpcTcGc(proc_outfileJC,proc_outfileTC,proc_outfileGC,figpath_together,endcal='Yes',plotvals=['pvel','rho','msu'],xlims=plot_xlims,jcshift=shift_10jc)
plt.close('all')


# %% 11JC
####################  Core 11JC ####################
proc_outfileJC = '/Users/vjs/OC2006A/data/MST/outfiles/volume_normalized/OC2006A-11JC_vol_MS.out'
proc_outfileTC = '/Users/vjs/OC2006A/data/MST/outfiles/volume_normalized/OC2006A-11TC_vol_MS.out'

#sbdepth,section_num,section_depth,pvel,rho,msu,resistivity,fracporosity,units,coreinfo = mst.read_MSToutfile(proc_outfile)
dataJ,unitsJ,coreinfoJ = mst.read_MSToutfile(proc_outfileJC)
dataT,unitsT,coreinfoT = mst.read_MSToutfile(proc_outfileTC)

figpath_jc = fig_dir + coreinfoJ['cruise'] + '_' + coreinfoJ['core'] + '.pdf'
figpath_tc = fig_dir + coreinfoT['cruise'] + '_' + coreinfoT['core'] + '.pdf'
figpath_together = fig_dir + coreinfoT['cruise'] + '_' + coreinfoT['core'] + '_JC.pdf'

## plssible colors...
#JCcolors = ['#5578ad','#ad6255','#56b851']

## Shift the JC?
shift_11 = 148.5
## Plot parameters:

vmin = 1450
vmax = 1670
rhomin = 1.22
rhomax = 2.2
msmin = 0
msmax = 620

plot_xlims = {'pvel':[vmin,vmax],'rho':[rhomin,rhomax],'msu':[msmin,msmax]}

#
### Plot JC alone
#mst.pltMST(proc_outfileJC,figpath_jc,endcal='Yes',plotvals=['pvel','rho','msu'],xlims=plot_xlims)
#           
#           
## Plot together:
mst.pltJpcTc(proc_outfileJC,proc_outfileTC,figpath_together,endcal='Yes',plotvals=['pvel','rho','msu'],xlims=plot_xlims,jcshift=shift_11)
plt.close('all')


# %% 12JC
####################  Core 12JC ####################
proc_outfileJC = '/Users/vjs/OC2006A/data/MST/outfiles/volume_normalized/OC2006A-12JC_vol_MS.out'
proc_outfileTC = '/Users/vjs/OC2006A/data/MST/outfiles/volume_normalized/OC2006A-12TC_vol_MS.out'

#sbdepth,section_num,section_depth,pvel,rho,msu,resistivity,fracporosity,units,coreinfo = mst.read_MSToutfile(proc_outfile)
dataJ,unitsJ,coreinfoJ = mst.read_MSToutfile(proc_outfileJC)
dataT,unitsT,coreinfoT = mst.read_MSToutfile(proc_outfileTC)

figpath_jc = fig_dir + coreinfoJ['cruise'] + '_' + coreinfoJ['core'] + '.pdf'
figpath_tc = fig_dir + coreinfoT['cruise'] + '_' + coreinfoT['core'] + '.pdf'
figpath_together = fig_dir + coreinfoT['cruise'] + '_' + coreinfoT['core'] + '_JC.pdf'

## plssible colors...
#JCcolors = ['#5578ad','#ad6255','#56b851']

## Shift the JC?
shift_12 = 158
## Plot parameters:

vmin = 1380
vmax = 1645
rhomin = 1.22
rhomax = 2.4
msmin = 0
msmax = 670

plot_xlims = {'pvel':[vmin,vmax],'rho':[rhomin,rhomax],'msu':[msmin,msmax]}

#
### Plot JC alone
#mst.pltMST(proc_outfileJC,figpath_jc,endcal='Yes',plotvals=['pvel','rho','msu'],xlims=plot_xlims)
#           
#           
## Plot together:
mst.pltJpcTc(proc_outfileJC,proc_outfileTC,figpath_together,endcal='Yes',plotvals=['pvel','rho','msu'],xlims=plot_xlims,jcshift=shift_12)
plt.close('all')

# %% 15GC
####################  Core 15GC ####################
proc_outfile = '/Users/vjs/OC2006A/data/MST/outfiles/volume_normalized/OC2006A-15GC_vol_MS.out'

## Read Data:
data,units,coreinfoJ = mst.read_MSToutfile(proc_outfile)

## Make figure path:
figpath = fig_dir + coreinfoJ['cruise'] + '_' + coreinfoJ['core'] + '.pdf'

## plssible colors...
#JCcolors = ['#5578ad','#ad6255','#56b851']

## Plot parameters:

vmin = 1400
vmax = 1620
rhomin = 1.4
rhomax = 2.3
msmin = 0
msmax = 300

plot_xlims = {'pvel':[vmin,vmax],'rho':[rhomin,rhomax],'msu':[msmin,msmax]}

#
### Plot GC alone
mst.pltMST(proc_outfile,figpath,endcal='Yes',plotvals=['pvel','rho','msu'],xlims=plot_xlims)

plt.close('all')


# %% 16JC
####################  Core 16JC ####################
proc_outfileJC = '/Users/vjs/OC2006A/data/MST/outfiles/volume_normalized/OC2006A-16JC_vol_MS.out'
proc_outfileTC = '/Users/vjs/OC2006A/data/MST/outfiles/volume_normalized/OC2006A-16TC_vol_MS.out'

#sbdepth,section_num,section_depth,pvel,rho,msu,resistivity,fracporosity,units,coreinfo = mst.read_MSToutfile(proc_outfile)
dataJ,unitsJ,coreinfoJ = mst.read_MSToutfile(proc_outfileJC)
dataT,unitsT,coreinfoT = mst.read_MSToutfile(proc_outfileTC)

figpath_jc = fig_dir + coreinfoJ['cruise'] + '_' + coreinfoJ['core'] + '.pdf'
figpath_tc = fig_dir + coreinfoT['cruise'] + '_' + coreinfoT['core'] + '.pdf'
figpath_together = fig_dir + coreinfoT['cruise'] + '_' + coreinfoT['core'] + '_JC.pdf'

## plssible colors...
#JCcolors = ['#5578ad','#ad6255','#56b851']

## Shift the JC?
shift_16 = 222
## Plot parameters:

vmin = 1400
vmax = 1570
rhomin = 1.3
rhomax = 2.3
msmin = 10
msmax = 300

plot_xlims = {'pvel':[vmin,vmax],'rho':[rhomin,rhomax],'msu':[msmin,msmax]}

#
### Plot JC alone
#mst.pltMST(proc_outfileJC,figpath_jc,endcal='Yes',plotvals=['pvel','rho','msu'],xlims=plot_xlims)
#           
#           
## Plot together:
mst.pltJpcTc(proc_outfileJC,proc_outfileTC,figpath_together,endcal='Yes',plotvals=['pvel','rho','msu'],xlims=plot_xlims,jcshift=shift_16)
plt.close('all')


# %% 18JC
####################  Core 18JC ####################
proc_outfileJC = '/Users/vjs/OC2006A/data/MST/outfiles/volume_normalized/OC2006A-18JC_vol_MS.out'
proc_outfileTC = '/Users/vjs/OC2006A/data/MST/outfiles/volume_normalized/OC2006A-18TC_vol_MS.out'

#sbdepth,section_num,section_depth,pvel,rho,msu,resistivity,fracporosity,units,coreinfo = mst.read_MSToutfile(proc_outfile)
dataJ,unitsJ,coreinfoJ = mst.read_MSToutfile(proc_outfileJC)
dataT,unitsT,coreinfoT = mst.read_MSToutfile(proc_outfileTC)

figpath_jc = fig_dir + coreinfoJ['cruise'] + '_' + coreinfoJ['core'] + '.pdf'
figpath_tc = fig_dir + coreinfoT['cruise'] + '_' + coreinfoT['core'] + '.pdf'
figpath_together = fig_dir + coreinfoT['cruise'] + '_' + coreinfoT['core'] + '_JC.pdf'

## plssible colors...
#JCcolors = ['#5578ad','#ad6255','#56b851']

## Shift the JC?
shift_18 = 180
## Plot parameters:

vmin = 1350
vmax = 1630
rhomin = 1.1
rhomax = 2.15
msmin = 10
msmax = 300
plot_xlims = {'pvel':[vmin,vmax],'rho':[rhomin,rhomax],'msu':[msmin,msmax]}
         
## Plot together:
mst.pltJpcTc(proc_outfileJC,proc_outfileTC,figpath_together,endcal='Yes',plotvals=['pvel','rho','msu'],xlims=plot_xlims,jcshift=shift_18)
plt.close('all')



# %% 23JC
####################  Core 23JC ####################
proc_outfileJC = '/Users/vjs/OC2006A/data/MST/outfiles/volume_normalized/OC2006A-23JC_vol_MS.out'
proc_outfileTC = '/Users/vjs/OC2006A/data/MST/outfiles/volume_normalized/OC2006A-23TC_vol_MS.out'

#sbdepth,section_num,section_depth,pvel,rho,msu,resistivity,fracporosity,units,coreinfo = mst.read_MSToutfile(proc_outfile)
dataJ,unitsJ,coreinfoJ = mst.read_MSToutfile(proc_outfileJC)
dataT,unitsT,coreinfoT = mst.read_MSToutfile(proc_outfileTC)

figpath_jc = fig_dir + coreinfoJ['cruise'] + '_' + coreinfoJ['core'] + '.pdf'
figpath_tc = fig_dir + coreinfoT['cruise'] + '_' + coreinfoT['core'] + '.pdf'
figpath_together = fig_dir + coreinfoT['cruise'] + '_' + coreinfoT['core'] + '_JC.pdf'

## plssible colors...
#JCcolors = ['#5578ad','#ad6255','#56b851']

## Shift the JC?
shift_23 = 67
## Plot parameters:

vmin = 1400
vmax = 1530
rhomin = 1.35
rhomax = 2.15
msmin = 0
msmax = 120
plot_xlims = {'pvel':[vmin,vmax],'rho':[rhomin,rhomax],'msu':[msmin,msmax]}
         
## Plot together:
mst.pltJpcTc(proc_outfileJC,proc_outfileTC,figpath_together,endcal='Yes',plotvals=['pvel','rho','msu'],xlims=plot_xlims,jcshift=shift_23)
plt.close('all')


# %% 25GC
####################  Core 25GC ####################
proc_outfile = '/Users/vjs/OC2006A/data/MST/outfiles/volume_normalized/OC2006A-25GC_vol_MS.out'

## Read Data:
data,units,coreinfoJ = mst.read_MSToutfile(proc_outfile)

## Make figure path:
figpath = fig_dir + coreinfoJ['cruise'] + '_' + coreinfoJ['core'] + '.pdf'

## plssible colors...
#JCcolors = ['#5578ad','#ad6255','#56b851']

## Plot parameters:

vmin = 1300
vmax = 1575
rhomin = 1.3
rhomax = 2.0
msmin = 0
msmax = 360

plot_xlims = {'pvel':[vmin,vmax],'rho':[rhomin,rhomax],'msu':[msmin,msmax]}

#
### Plot GC alone
mst.pltMST(proc_outfile,figpath,endcal='Yes',plotvals=['pvel','rho','msu'],xlims=plot_xlims)

plt.close('all')

# %% 26GC
####################  Core 26GC ####################
proc_outfile = '/Users/vjs/OC2006A/data/MST/outfiles/volume_normalized/OC2006A-26GC_vol_MS.out'

## Read Data:
data,units,coreinfoJ = mst.read_MSToutfile(proc_outfile)

## Make figure path:
figpath = fig_dir + coreinfoJ['cruise'] + '_' + coreinfoJ['core'] + '.pdf'

## plssible colors...
#JCcolors = ['#5578ad','#ad6255','#56b851']

## Plot parameters:

vmin = 1400
vmax = 1485
rhomin = 1.3
rhomax = 1.8
msmin = 0
msmax = 150

plot_xlims = {'pvel':[vmin,vmax],'rho':[rhomin,rhomax],'msu':[msmin,msmax]}

#
### Plot GC alone
mst.pltMST(proc_outfile,figpath,endcal='Yes',plotvals=['pvel','rho','msu'],xlims=plot_xlims)

plt.close('all')


# %% 27JC/TC
####################  Core 27JC/TC ####################
proc_outfileJC = '/Users/vjs/OC2006A/data/MST/outfiles/volume_normalized/OC2006A-27JC_vol_MS.out'
proc_outfileTC = '/Users/vjs/OC2006A/data/MST/outfiles/volume_normalized/OC2006A-27TC_vol_MS.out'

#sbdepth,section_num,section_depth,pvel,rho,msu,resistivity,fracporosity,units,coreinfo = mst.read_MSToutfile(proc_outfile)
dataJ,unitsJ,coreinfoJ = mst.read_MSToutfile(proc_outfileJC)
dataT,unitsT,coreinfoT = mst.read_MSToutfile(proc_outfileTC)

figpath_jc = fig_dir + coreinfoJ['cruise'] + '_' + coreinfoJ['core'] + '.pdf'
figpath_tc = fig_dir + coreinfoT['cruise'] + '_' + coreinfoT['core'] + '.pdf'
figpath_together = fig_dir + coreinfoT['cruise'] + '_' + coreinfoT['core'] + '_JC.pdf'

## plssible colors...
#JCcolors = ['#5578ad','#ad6255','#56b851']

## Shift the JC?
shift_27 = 85
## Plot parameters:

vmin = 1350
vmax = 1600
rhomin = 1.25
rhomax = 2.3
msmin = 0
msmax = 220
plot_xlims = {'pvel':[vmin,vmax],'rho':[rhomin,rhomax],'msu':[msmin,msmax]}
         
## Plot together:
mst.pltJpcTc(proc_outfileJC,proc_outfileTC,figpath_together,endcal='Yes',plotvals=['pvel','rho','msu'],xlims=plot_xlims,jcshift=shift_27)
plt.close('all')




# %% 30JC/TC
####################  Core 30JC/TC ####################
proc_outfileJC = '/Users/vjs/OC2006A/data/MST/outfiles/volume_normalized/OC2006A-30JC_vol_MS.out'
proc_outfileTC = '/Users/vjs/OC2006A/data/MST/outfiles/volume_normalized/OC2006A-30TC_vol_MS.out'

#sbdepth,section_num,section_depth,pvel,rho,msu,resistivity,fracporosity,units,coreinfo = mst.read_MSToutfile(proc_outfile)
dataJ,unitsJ,coreinfoJ = mst.read_MSToutfile(proc_outfileJC)
dataT,unitsT,coreinfoT = mst.read_MSToutfile(proc_outfileTC)

figpath_jc = fig_dir + coreinfoJ['cruise'] + '_' + coreinfoJ['core'] + '.pdf'
figpath_tc = fig_dir + coreinfoT['cruise'] + '_' + coreinfoT['core'] + '.pdf'
figpath_together = fig_dir + coreinfoT['cruise'] + '_' + coreinfoT['core'] + '_JC.pdf'

## plssible colors...
#JCcolors = ['#5578ad','#ad6255','#56b851']

## Shift the JC?
shift_30 = 9
## Plot parameters:

vmin = 0
vmax = 1700
rhomin = 1.0
rhomax = 2.25
msmin = 15
msmax = 170
plot_xlims = {'pvel':[vmin,vmax],'rho':[rhomin,rhomax],'msu':[msmin,msmax]}
         
## Plot together:
mst.pltJpcTc(proc_outfileJC,proc_outfileTC,figpath_together,endcal='Yes',plotvals=['pvel','rho','msu'],xlims=plot_xlims,jcshift=shift_30)
plt.close('all')



# %% 31JC/TC
####################  Core 31JC/TC ####################
proc_outfileJC = '/Users/vjs/OC2006A/data/MST/outfiles/volume_normalized/OC2006A-31JC_vol_MS.out'
proc_outfileTC = '/Users/vjs/OC2006A/data/MST/outfiles/volume_normalized/OC2006A-31TC_vol_MS.out'

#sbdepth,section_num,section_depth,pvel,rho,msu,resistivity,fracporosity,units,coreinfo = mst.read_MSToutfile(proc_outfile)
dataJ,unitsJ,coreinfoJ = mst.read_MSToutfile(proc_outfileJC)
dataT,unitsT,coreinfoT = mst.read_MSToutfile(proc_outfileTC)

figpath_jc = fig_dir + coreinfoJ['cruise'] + '_' + coreinfoJ['core'] + '.pdf'
figpath_tc = fig_dir + coreinfoT['cruise'] + '_' + coreinfoT['core'] + '.pdf'
figpath_together = fig_dir + coreinfoT['cruise'] + '_' + coreinfoT['core'] + '_JC.pdf'

## plssible colors...
#JCcolors = ['#5578ad','#ad6255','#56b851']

## Shift the JC?
shift_31 = 2
## Plot parameters:

vmin = 10
vmax = 1750
rhomin = 1.1
rhomax = 2.2
msmin = 15
msmax = 190
plot_xlims = {'pvel':[vmin,vmax],'rho':[rhomin,rhomax],'msu':[msmin,msmax]}
         
## Plot together:
mst.pltJpcTc(proc_outfileJC,proc_outfileTC,figpath_together,endcal='Yes',plotvals=['pvel','rho','msu'],xlims=plot_xlims,jcshift=shift_31)
plt.close('all')