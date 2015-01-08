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
    
    cseg=0
    newSeg=''
    oldSeg=''
    
    #Read lines of file 
    while True:
        line=kingf.readline()
        #Once 'Seg "Line"' is encountered, read the next line, and...
        if 'Seg "' in line:
            #Define the components of the line, so you can pull out the line name
            oldline=line.split(' ')
            #If it's the first segment:
            if cseg==0:
                print 'in the first if, cseg=0'
                #Read the segment name as old segment, and the new segment as nothing
                oldSeg=oldline[1]
                newSeg=''
                #Read the next line,
                line=kingf.readline()
                #Output the next line to x and y (first in tmp vars)...
                XYout=line.split(' ')
                xtmp=np.float32(XYout[0])
                ytmp=np.float32(XYout[1])
                #Now to perm variables.
                x=np.r_[x,xtmp]
                y=np.r_[y,ytmp]
            #If it's not the first segment, then read the line name as newseg
            else:
                print 'in the first else, cseg ~= 0'
                newSeg=oldline[1]
            #IN this case, if the old segment (last line) and new segment are the same, 
            #go to the next line
            if oldSeg==newSeg:
                print 'in the second if, newseg==oldseg'
                line=kingf.readline()
            #If they're not the same, then this is a new segment so read it out 
            #to add to the xy file
            else:
                print 'in the second else, newseg ~=oldseg'
                line=kingf.readline()
                #Output the next line to x and y (first in tmp vars)...
                XYout=line.split(' ')
                xtmp=np.float32(XYout[0])
                ytmp=np.float32(XYout[1])
                #Now to perm variables.
                x=np.r_[x,xtmp]
                y=np.r_[y,ytmp]
        else:
            print 'no seg, go to next line'
            line=kingf.readline()
        #Now re-initialize so that this past segment will be the old segment;     
        oldSeg=newSeg
        #Add to the counter.
        cseg=cseg+1
        print 'added to counter'
        
        #Check to see if end of file has been reached
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
        
        
