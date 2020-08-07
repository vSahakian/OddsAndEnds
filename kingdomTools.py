def kFault2xy(ffile,xyfile,csys):
    '''
    Converts a kingdom Photon XY ASCII output fault file into
    an xy file to plot with GMT.
    To print out this file:
    -Go to Faults -> Export -> Fault Surfaces
    -Data Format to Output: Photon XY ASCII 
    -Select all lines to print, and select which fault to print
    -Right justified
    
    This script converts that format.  If on any given line, one fault is marked 
    more than once (i.e. more than one segment, such as a flower structure),
    this script will print only the first segment to the output file so that GMT
    will not connect multiple segments on one line.
    If this is not desired, assign only the main strand as the main segment, and 
    reassign the complimentary/smaller segments as "unassigned", or as another fault.   
    
    Input:
        ffile:      Path of kingdom output fault file (# Photo Systems etc.)
        xyfile:     Path of output xy file 
        csys:       Coordinate system of input kingdom file.  0=lat/lon,1=utm
        
    Output:
        xyfile will be in format:
            X  Y  
        for each point of the fault to be plotted.
    '''
    #:: V. Sahakian, December 3 2014 ::#
    
    import numpy as np
    
    #Read in kingdom fault file
    kingf=open(ffile,'r')
    
    #Initialize x and y arrays
    x=np.array([])
    y=np.array([])
    
    segname=''
    
    #Read lines of file 
    while True:
        line=kingf.readline()
        if 'Seg "' in line:
            print(line)
            seg=line.split(' ')[1]
            if seg not in segname:
                segname=segname+''+seg
                print(segname)
                #Read the next line,
                line=kingf.readline()
                #Output the next line to x and y (first in tmp vars)...
                XYout=line.split(' ')
                xtmp=np.float32(XYout[0])
                ytmp=np.float32(XYout[1])
                #Now to perm variables.
                x=np.r_[x,xtmp]
                y=np.r_[y,ytmp]
        if line=='':
            break
    
    #Output and save to file
    fmt='%.8f\t%.8f'
    if csys==0:
        header='Lon   Lat'
    else:
        header='X(m)   Y(m)'
    
    #Unsorted values
    XY_u=np.c_[x,y,z]
    
    #Sort by y (or lat)
    xyind=np.argsort(XY_u[:,1])
    XY=XY_u[xyind,:]
    
    np.savetxt(xyfile,XY,fmt,header=header)
                

############
def kFault2xyz(ffile,xyzfile,csys,zheader='Z'):
    '''
    Converts a kingdom Photon XY ASCII output fault file into
    an xyz file to use for fault planes, etc..
    To print out this file:
    -Go to Faults -> Export -> Fault Surfaces
    -Data Format to Output: Photon XY ASCII 
    -Select all lines to print, and select which fault to print
    -Right justified
    
    This script converts that format.  If on any given line, one fault is marked 
    more than once (i.e. more than one segment, such as a flower structure),
    this script will print only the first segment to the output file so that GMT
    will not connect multiple segments on one line.
    If this is not desired, assign only the main strand as the main segment, and 
    reassign the complimentary/smaller segments as "unassigned", or as another fault.   
    
    Input:
        ffile:      Path of kingdom output fault file (# Photo Systems etc.)
        xyzfile:     Path of output xy file 
        csys:       Coordinate system of input kingdom file.  0=lat/lon,1=utm
        zheader:    string with the z line info (default: Z) could be ms, or m
    Output:
        xyfile will be in format:
            X  Y  Z
        for each point of the fault to be plotted.
    '''
    #:: V. Sahakian, December 3 2014 ::#
    
    import numpy as np
    
    #Read in kingdom fault file
    kingf=open(ffile,'r')
    
    #Initialize x and y arrays
    x=np.array([])
    y=np.array([])
    z=np.array([])
    
    segname=''
    
    #Read lines of file 
    while True:
        line=kingf.readline()
        if 'Seg "' in line:
            seg=line.split(' ')[1]
            if seg not in segname:
                segname=segname+''+seg
                #Read the next line,
                line=kingf.readline()
                #Output the next line to x and y (first in tmp vars)...
                XYout=line.split(' ')
                xtmp=np.float32(XYout[0])
                ytmp=np.float32(XYout[1])
                ztmp=np.float32(XYout[2])
                #Now to perm variables.
                x=np.r_[x,xtmp]
                y=np.r_[y,ytmp]
                z=np.r_[z,ztmp]
        if line=='':
            break
    
    #Output and save to file
    fmt='%.8f\t%.8f\t%.f'
    if csys==0:
        header='Lon   Lat	' + zheader
    else:
        header='X(m)   Y(m)	  ' + zheader
    
    #Unsorted values
    XY_u=np.c_[x,y,z]
    
    #Sort by y (or lat)
    xyind=np.argsort(XY_u[:,1])
    XY=XY_u[xyind,:]
    
    print(xyzfile)
    np.savetxt(xyzfile,XY,fmt,header=header)
             
             
############             
def f_utm2ll(globfile_utm,lloutdir,utmzone,zheader='z'):
    '''
    Convert all files in a directory from UTM to lat/lon
    Input:
        globfile:   list with each row being the string of a file to convert.
        lloutdir:   string with path of output directory for lat/lon files
        utmzone:    string with utm zone to convert, i.e., '11S'
        zheader:    string with the z line (default: z) could be ms, or m
    '''
    from pyproj import Proj
    import numpy as np
    from os import path
    
    #Set up projection
    p=Proj(proj='utm',zone=utmzone,ellps='WGS84')
    
    #loop over files:
    for i in range(len(globfile_utm)):
        #Set output filename/path:
        fname=path.split(globfile_utm[i])[1].split('.')[0]
        outfile=lloutdir+'/'+fname+'_ll.txt'
        
        #Extract data:
        dat=np.genfromtxt(globfile_utm[i],skip_header=1)
        if (np.size(dat)) <= 3:
            x=dat[0]
            y=dat[1]
            z=dat[2]
        else:
            x=dat[:,0]
            y=dat[:,1]
            z=dat[:,2]
        
        #Project:
        lon,lat=p(x,y,inverse='True')
        
        #Save to file:
        out=np.c_[lon,lat,z]
        header_string='lon\tlat\t' + zheader
        np.savetxt(outfile,out,fmt='%12.8f\t%10.8f\t%3.2f',header=header_string)
        
        
############
def catFaults(globfile,outfile):
    '''
    Concatenate the fault files made by kFault2xy or kFault2xyz (or lat/lon) for
    GMT
    Input: 
        globfile:   list with each row as the string of a file.  glob these before
        outfile:     string with out file name
    '''
    import numpy as np
    
    #Open output file
    fid=open(outfile,'w')
    #Write first >
    fid.write('>\n')
    
    #Loop over xy/xyz files and open data
    for i in range(len(globfile)):
        dat=np.genfromtxt(globfile[i])
        #Loop over this data, write line by line:
        print(i)
        for j in range(len(dat)):
            if np.size(dat) <= 3:
                line='%12.8f\t%10.8f\n' % (dat[0],dat[1])
                fid.write(line)
            else:
                line='%12.8f\t%10.8f\n' % (dat[j,0],dat[j,1])
                fid.write(line)        
        #Write carrot out at the end:
        fid.write('>\n')
    #close file:
    fid.close()
        
        
    
def twtt2m(xytfile,xyzfile,vel,csys):
    '''
    Convert an xyt file (X, Y, T (twtt, ms)) to an xyz file (X,Y,Z (m))
    Input:
        xytfile:        Path to the input file with X, Y, TWTT (ms)
        xyzfile:        Path to the output file with X, Y, Z (m)
        vel:            Velocity to use in conversion (m/s)
        csys:           Coordinate system
    Output: 
        xyzfile
    '''
    
    import numpy as np
    
    #Read in data:
    dat=np.loadtxt(xytfile,skiprows=1)
    
    #Classify - x, y, twtt (ms):
    if len(dat)>3:
        x=dat[:,0]
        y=dat[:,1]
        twtt_ms=dat[:,2]
    else:
       x=dat[0]
       y=dat[1]
       twtt_ms=dat[2]
       
         
    #Put ms to s:
    twtt_s=twtt_ms/1000
    
    #Get single direction travel time, for one direction depth:
    swtt_s=twtt_s/2
    
    #Get depth in meters, z_m, d=vt:
    z_m=vel*swtt_s
    
    
    
    #Output and save to file
    fmt='%.8f\t%.8f\t%.f'
    if csys==0:
        header='Lon     Lat    Z(m)'
    else:
        header='X(m)   Y(m)	  Z(m)'
    
    #Unsorted values
    XY_u=np.c_[x,y,z_m]
    
    #Sort by y (or lat)
    xyind=np.argsort(XY_u[:,1])
    XY=XY_u[xyind,:]
    
    print(xyzfile)
    np.savetxt(xyzfile,XY,fmt,header=header)