#HELLO DIEGO#
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
            print line
            seg=line.split(' ')[1]
            if seg not in segname:
                segname=segname+''+seg
                print segname
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
    
    XY=np.c_[x,y]
    np.savetxt(xyfile,XY,fmt,header=header)
                
