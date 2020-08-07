#Convert kingdom depth of deformation mappings to file for GMT
#VJS 6/2016

import kingdomTools as kt
from glob import glob
from os import path
import numpy as np

#Which files to convert?
globfile=glob('/Users/vsahakian/songs/faultdata/DepthOfDeformation/dat/*.dat')

#What coord system are then in?  0=lat/lon, 1=utm
csys=1
#Velocity to migrate?  (m/s)
wvel=1500

for i in range(len(globfile)):
    #print globfile[i]
    #First convert to an xyz type format, with the z column as TWTT (ms)
    t_dirout=path.split(globfile[i])[0].split('/dat')[0]+'/xyt/'
    t_fnameout=path.split(globfile[i])[1].split('.')[0]+'.xyt'
    t_fpathout=t_dirout+t_fnameout
    kt.kFault2xyz(globfile[i],t_fpathout,csys)
    
    #Then put them into Z format, depth meters:
    z_dirout=path.split(globfile[i])[0].split('/dat')[0]+'/xyz/'
    z_fnameout=path.split(globfile[i])[1].split('.')[0]+'.xyz'
    z_fpathout=z_dirout+z_fnameout
    kt.twtt2m(t_fpathout,z_fpathout,wvel,csys)
    
    
#Then in batch, convert all xyz (utm) to LL:
#Which data to convert:
globfile_utm=glob('/Users/vsahakian/songs/faultdata/DepthOfDeformation/xyz/*.xyz')
#Which output direectory:
lloutdir='/Users/vsahakian/songs/faultdata/DepthOfDeformation/LL'
#what utm zone?
utmzone='11S'

kt.f_utm2ll(globfile_utm,lloutdir,utmzone)


###Then, run 
#/Users/vsahakian/songs/faultdata/DepthOfDeformation/get_seafloor_depth.sh
#to get the depth of the seafloor at each data point.  

#Now, compute the depth beneath the seafloorof the deformation:
globfile_sd=glob('/Users/vsahakian/songs/faultdata/DepthOfDeformation/sfd/*.sfd')

for j in range(len(globfile_sd)):
    #Get file names, etc...
    pbase=path.split(globfile_sd[j])[0].split('/sfd')[0]+'/dd/'
    fname=path.split(globfile_sd[j])[1].split('.')[0]+'.dd'
    ddfile=pbase+fname
    
    #Load in data....
    sfdat=np.loadtxt(globfile_sd[j])
    if len(sfdat)>4:
        lon=sfdat[:,0]
        lat=sfdat[:,1]
        defr=sfdat[:,2]
        sflr=sfdat[:,3]
    else:
        lon=sfdat[0]
        lat=sfdat[1]
        defr=sfdat[2]
        sflr=sfdat[3]
        
    #Get the depth of deformation, below the seafloor:
    ddep=defr+sflr
    
    #There is some discrepancy between the bathymetry and seismic data, so if 
    #there is a negative value, set it to some small value, like 2 meters:
    if type(ddep)==np.float64:
        if ddep<0:
            ddep=2
    else:
        for k in range(len(ddep)):
            if ddep[k]<0:
                ddep[k]=2
            
    #Save to file:
    XYS=np.c_[lon,lat,ddep]
    np.savetxt(ddfile,XYS,fmt='%12.8f\t%10.8f\t%3.2f')
            
            
###Outside python, concatenate them all together.....NIRCdeformatoin.txt