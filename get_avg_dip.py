#Get dip of each mapped fault segment
#VJS 4/2015


import kingdomTools as kt
import numpy as np
from glob import glob
from os import path
import math as m

#Coordinate system:
csys=1

#Conglomerate the files for top and bottom segments...
topd=glob('/Users/vjsahakian/SONGS/Data/FM_Data/RC_NI/dips/topK/*.dat')
botd=glob('/Users/vjsahakian/SONGS/Data/FM_Data/RC_NI/dips/bottomK/*.dat')

for i in range(len(topd)):
    print i
    #Get file/segment names and path one directory above
    topkname=path.split(topd[i])[1].split('.')[0]
    topkpath=path.split(topd[i])[0].split('top')[0]
    
    #Now for the bottom dip files
    botkname=path.split(botd[i])[1].split('.')[0]
    botkpath=path.split(botd[i])[0].split('bottom')[0]
    
    #Get the new directories for the xyz files
    toppath=topkpath+'topUTM/'+topkname+'.xyz'
    botpath=botkpath+'bottomUTM/'+botkname+'.xyz'
    
    #Convert from kingdom photon xy to xyz ascii
    kt.kFault2xyz(topd[i],toppath,csys)
    kt.kFault2xyz(botd[i],botpath,csys)
    
    #Convert the dip...
    tdat=np.genfromtxt(toppath)
    bdat=np.genfromtxt(botpath)
    
    if len(tdat)!=len(bdat):
        print 'Your files do not have the same number of mappings for'+topkname+'.  Go back to kingdom and try again'
    else:
        print i
        
#Get strike and dip for coulomb
#Read in unsorted segment files:
#For AGU...
#lj2tp=np.loadtxt('/Users/sahakian/SONGS/Data/FM_Data/RC_NI/xy/RCNI_lj2tp.xy',skiprows=1)
#tp2cc_u=np.loadtxt('/Users/sahakian/SONGS/Data/FM_Data/RC_NI/xy/RCNI_tp2cc.xy',skiprows=1)
#cc2lp_u=np.loadtxt('/Users/sahakian/SONGS/Data/FM_Data/RC_NI/xy/RCNI_cc2lp.xy',skiprows=1)
#wlp2_u=np.loadtxt('/Users/sahakian/SONGS/Data/FM_Data/RC_NI/xy/RCNI_Wlp2.xy',skiprows=1)
#dp2_u=np.loadtxt('/Users/sahakian/SONGS/Data/FM_Data/RC_NI/xy/RCNI_2dp.xy',skiprows=1)

lj2tp=np.loadtxt('/Users/vjsahakian/SONGS/Data/FM_Data/RC_NI/dips/topUTM/RCNI_lj2tp.xyz',skiprows=1)
tp2cc_u=np.loadtxt('/Users/vjsahakian/SONGS/Data/FM_Data/RC_NI/dips/topUTM/RCNI_tp2cc.xyz',skiprows=1)
cc2lp_u=np.loadtxt('/Users/vjsahakian/SONGS/Data/FM_Data/RC_NI/dips/topUTM/RCNI_cc2lp.xyz',skiprows=1)
wlp2_u=np.loadtxt('/Users/vjsahakian/SONGS/Data/FM_Data/RC_NI/dips/topUTM/RCNI_Wlp2.xyz',skiprows=1)
dp2_u=np.loadtxt('/Users/vjsahakian/SONGS/Data/FM_Data/RC_NI/dips/topUTM/RCNI_2dp.xyz',skiprows=1)

#Sort them
#Find indices
tpind=np.argsort(tp2cc_u[:,1])
ccind=np.argsort(cc2lp_u[:,1])
wlind=np.argsort(wlp2_u[:,1])
dpind=np.argsort(dp2_u[:,1])
#Sort
tp2cc=tp2cc_u[tpind,:]
cc2lp=cc2lp_u[ccind,:]
wlp2=wlp2_u[wlind,:]
dp2=dp2_u[dpind,:]


#Set origin, in La Jolla Canyon
x_or=474716.5
y_or=3635624.6

#Concatenate origin and lj2tp, since they're always rupturing together
x_or=np.r_[x_or,lj2tp[0]]
y_or=np.r_[y_or,lj2tp[1]]
z_or=np.r_[lj2tp[2],lj2tp[2]]

#Get strike/dip for each segment - with first and last point.  
lj2tp_beg=np.r_[x_or[0],y_or[0],z_or[0]]
lj2tp_end=np.r_[x_or[1],y_or[1],z_or[1]]

tp2cc_beg=tp2cc[0]
tp2cc_end=tp2cc[-1]

cc2lp_beg=cc2lp[0]
cc2lp_end=cc2lp[-1]

wlp2_beg=wlp2[0]
wlp2_end=wlp2[-1]

dp2_beg=dp2[0]
dp2_end=dp2[-1]

#Get strike:
lj2tp_s=m.degrees(m.atan((lj2tp_end[0]-lj2tp_beg[0])/(lj2tp_end[1]-lj2tp_beg[1])))
tp2cc_s=m.degrees(m.atan((tp2cc_end[0]-tp2cc_beg[0])/(tp2cc_end[1]-tp2cc_beg[1])))
cc2lp_s=m.degrees(m.atan((cc2lp_end[0]-cc2lp_beg[0])/(cc2lp_end[1]-cc2lp_beg[1])))
wlp2_s=m.degrees(m.atan((wlp2_end[0]-wlp2_beg[0])/(wlp2_end[1]-wlp2_beg[1])))
dp2_s=m.degrees(m.atan((dp2_end[0]-dp2_beg[0])/(dp2_end[1]-dp2_beg[1])))

#Get dip:
lj2tp_ddat=np.genfromtxt('/Users/vjsahakian/SONGS/Data/FM_Data/RC_NI/dips/lj2tp_d.dat')
lj2tp_d=90-(m.degrees(m.atan(np.abs((lj2tp_ddat[1,0]-lj2tp_ddat[0,0]))/(lj2tp_ddat[1,2]-lj2tp_ddat[0,2]))))

tp2cc_ddat=np.genfromtxt('/Users/vjsahakian/SONGS/Data/FM_Data/RC_NI/dips/tp2cc_d.dat')
tp2cc_d=90-(m.degrees(m.atan(np.abs((tp2cc_ddat[1,0]-tp2cc_ddat[0,0]))/(tp2cc_ddat[1,2]-tp2cc_ddat[0,2]))))

cc2lp_ddat=np.genfromtxt('/Users/vjsahakian/SONGS/Data/FM_Data/RC_NI/dips/cc2lp_d.dat')
cc2lp_d=90-(m.degrees(m.atan(np.abs((cc2lp_ddat[1,0]-cc2lp_ddat[0,0]))/(cc2lp_ddat[1,2]-cc2lp_ddat[0,2]))))

wlp2_ddat=np.genfromtxt('/Users/vjsahakian/SONGS/Data/FM_Data/RC_NI/dips/wlp2_d.dat')
wlp2_d=90-(m.degrees(m.atan(np.abs((wlp2_ddat[1,0]-wlp2_ddat[0,0]))/(wlp2_ddat[1,2]-wlp2_ddat[0,2]))))

dp2_ddat=np.genfromtxt('/Users/vjsahakian/SONGS/Data/FM_Data/RC_NI/dips/_2dp_d.dat')
dp2_d=90-(m.degrees(m.atan(np.abs((dp2_ddat[1,0]-dp2_ddat[0,0]))/(dp2_ddat[1,2]-dp2_ddat[0,2]))))

#Set origin:
Cor=np.array([448269.5,3683086])

#Get beginning/end with respect to origin:
lj2tp_b=(lj2tp_beg[0:2]-Cor)/1000
lj2tp_e=(lj2tp_end[0:2]-Cor)/1000

tp2cc_b=(tp2cc_beg[0:2]-Cor)/1000
tp2cc_e=(tp2cc_end[0:2]-Cor)/1000

cc2lp_b=(cc2lp_beg[0:2]-Cor)/1000
cc2lp_e=(cc2lp_end[0:2]-Cor)/1000

wlp2_b=(wlp2_beg[0:2]-Cor)/1000
wlp2_e=(wlp2_end[0:2]-Cor)/1000

dp2_b=(dp2_beg[0:2]-Cor)/1000
dp2_e=(dp2_end[0:2]-Cor)/1000

#Print out beginning point (x,y), end point(x,y), strike, and dip:
lj2tp_out=np.r_[np.c_[lj2tp_b[0],lj2tp_b[1],lj2tp_s,lj2tp_d],np.c_[lj2tp_e[0],lj2tp_e[1],lj2tp_s,lj2tp_d]]
tp2cc_out=np.r_[np.c_[tp2cc_b[0],tp2cc_b[1],tp2cc_s,tp2cc_d],np.c_[tp2cc_e[0],tp2cc_e[1],tp2cc_s,tp2cc_d]]
cc2lp_out=np.r_[np.c_[cc2lp_b[0],cc2lp_b[1],cc2lp_s,cc2lp_d],np.c_[cc2lp_e[0],cc2lp_e[1],cc2lp_s,cc2lp_d]]
wlp2_out=np.r_[np.c_[wlp2_b[0],wlp2_b[1],wlp2_s,wlp2_d],np.c_[wlp2_e[0],wlp2_e[1],wlp2_s,wlp2_d]]
dp2_out=np.r_[np.c_[dp2_b[0],dp2_b[1],dp2_s,dp2_d],np.c_[dp2_e[0],dp2_e[1],dp2_s,dp2_d]]

#Print to file:
np.savetxt('/Users/vjsahakian/SONGS/Data/FM_Data/RC_NI/dips/c.in/lj2tp.in',lj2tp_out,fmt='%8.5f\t%8.5f\t%3.0f\t%3.0f',header='X(m)    Y(m)    Strike(deg)  Dip(deg)')
np.savetxt('/Users/vjsahakian/SONGS/Data/FM_Data/RC_NI/dips/c.in/tp2cc.in',tp2cc_out,fmt='%8.5f\t%8.5f\t%3.0f\t%3.0f',header='X(m)    Y(m)    Strike(deg)  Dip(deg)')
np.savetxt('/Users/vjsahakian/SONGS/Data/FM_Data/RC_NI/dips/c.in/cc2lp.in',cc2lp_out,fmt='%8.5f\t%8.5f\t%3.0f\t%3.0f',header='X(m)    Y(m)    Strike(deg)  Dip(deg)')
np.savetxt('/Users/vjsahakian/SONGS/Data/FM_Data/RC_NI/dips/c.in/wlp2.in',wlp2_out,fmt='%8.5f\t%8.5f\t%3.0f\t%3.0f',header='X(m)    Y(m)    Strike(deg)  Dip(deg)')
np.savetxt('/Users/vjsahakian/SONGS/Data/FM_Data/RC_NI/dips/c.in/dp2.in',dp2_out,fmt='%8.5f\t%8.5f\t%3.0f\t%3.0f',header='X(m)    Y(m)    Strike(deg)  Dip(deg)')