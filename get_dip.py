import numpy as np
#from obspy.core.util.geodetics import gps2DistAzimuth
from glob import glob
from pyproj import Proj

#OUtput file name:
outfile='/Users/vjsahakian/Software/GMT/SONGS/NIRCdips.txt'

#Input files:
#Import bottom.  Glob files.
topUTM=glob('/Users/vjsahakian/SONGS/Data/FM_Data/RC_NI/dips/topUTM_dmap/*.xyz')
botUTM=glob('/Users/vjsahakian/SONGS/Data/FM_Data/RC_NI/dips/bottomUTM_dmap/*.xyz')

tx=np.array([])
ty=np.array([])
tz=np.array([])

bx=np.array([])
by=np.array([])
bz=np.array([])

k=0
for i in range(len(topUTM)):
    print topUTM[i]
    print botUTM[i]
    if i==0:
        dat=np.loadtxt(topUTM[i],skiprows=1)
        if np.size(dat)<=3:
            tx=dat[0]
            ty=dat[1]
            tz=dat[2]
        else:
            tx=dat[:,0]
            ty=dat[:,1]
            tz=dat[:,2]
            
        bdat=np.loadtxt(botUTM[i],skiprows=1)
        if np.size(bdat)<=3:
            bx=bdat[0]
            by=bdat[1]
            bz=bdat[2]
        else:
            bx=bdat[:,0]
            by=bdat[:,1]
            bz=bdat[:,2]
            
        #Get dip, etc.
        
    else:
        dat=np.loadtxt(topUTM[i],skiprows=1)
        if np.size(dat)<=3:
            tx=np.append(tx,dat[0])
            ty=np.append(ty,dat[1])
            tz=np.append(tz,dat[2])
        else:
            tx=np.append(tx,dat[:,0])
            ty=np.append(ty,dat[:,1])
            tz=np.append(tz,dat[:,2])
            
        bdat=np.loadtxt(botUTM[i],skiprows=1)
        if np.size(bdat)<=3:
            bx=np.append(bx,bdat[0])
            by=np.append(by,bdat[1])
            bz=np.append(bz,bdat[2])
        else:
            bx=np.append(bx,bdat[:,0])
            by=np.append(by,bdat[:,1])
            bz=np.append(bz,bdat[:,2])

#for i in range(len(topUTM)):
#    print topUTM[i]
#    print botUTM[i]
#    dat=np.loadtxt(topUTM[i],skiprows=1)
#    if np.size(dat)<=3:
#        tx=dat[0]
#        ty=dat[1]
#        tz=dat[2]
#    else:
#        tx=dat[:,0]
#        ty=dat[:,1]
#        tz=dat[:,2]
#        
#    bdat=np.loadtxt(botUTM[i],skiprows=1)
#    if np.size(bdat)<=3:
#        bx=bdat[0]
#        by=bdat[1]
#        bz=bdat[2]
#    else:
#        bx=bdat[:,0]
#        by=bdat[:,1]
#        bz=bdat[:,2]
#        
    #Get dip, etc.
    

  #Get x and y directions, so that dip will be in correct direction.  if bottom is
  #to east of top, vx will be positive.  if bottom is north of top, vy will be positve.          
vx=bx-tx
vy=by-ty

#get distance and depth difference
dist=np.sqrt((vx**2) + (vy**2))
dz=bz-tz

#get dip for each point
dip=np.rad2deg(np.arctan(dz/dist))

#
vx_n=(vx/dist)
vy_n=(vy/dist)

vx_d=(90-dip)*vx_n
vy_d=(90-dip)*vy_n


#Reproject x and y to get start points:
utmzone='11S'
p=Proj(proj='utm',zone=utmzone,ellps='WGS84')
lon,lat=p(tx,ty,inverse='True')

#Make uncertainties 0
sigx=np.zeros(tx.shape)
sigy=np.zeros(ty.shape)

#Concatenate to write out:
out=np.c_[lon,lat,vx_d,vy_d,sigx,sigy]
format='%.8f\t%.8f\t%.8f\t%.8f\t%d\t%d'
np.savetxt(outfile,out,fmt=format)
