#Convert core locations from UTM to decimal degrees
#VJS 1/2016

import numpy as np
from pyproj import Proj 

#Import core utm file (format: UTM x, UTm y)
#dat=np.genfromtxt('/Users/vjsahakian/Documents/Cruise/Jan2016_core/core_loc_utm.txt')
dat=np.genfromtxt('/Users/vjsahakian/Documents/Cruise/TN336/core_loc_utm_jan23.txt')


#Set values:
UTMx=dat[:,0]
UTMy=dat[:,1]

#Set up projection:
p=Proj(proj='utm',zone='11S',ellps='WGS84')

#Project:
lon,lat=p(UTMx,UTMy,inverse='True')

#Get in Degree, decimal minutes (**Note!!!  This is for negative longitudes!!):
dlon=np.ceil(lon)
dlat=np.floor(lat)

mlon=(dlon-lon)*60
mlat=(lat-dlat)*60

#Write to file:
#ofile='/Users/vjsahakian/Documents/Cruise/Jan2016_core/core_loc_ll.txt'
ofile='/Users/vjsahakian/Documents/Cruise/TN336/core_loc_ll_jan23.txt'
out=np.c_[lon,lat]
np.savetxt(ofile,out,fmt='%10.6f\t%8.6f')

#Also write degree/dec min:
#ofile='/Users/vjsahakian/Documents/Cruise/Jan2016_core/core_loc_dmll.txt'
ofile='/Users/vjsahakian/Documents/Cruise/TN336/core_loc_dmll_jan23.txt'
out=np.c_[dlon,mlon,dlat,mlat]
np.savetxt(ofile,out,fmt='%4i\t%8.6f\t%2i\t%8.6f')