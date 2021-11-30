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
    XY_u=np.c_[x,y]
    
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
                ## Reset the segment name so it will write for multiple segments
                segname = ''
        if line=='':
            print('breaking')
            break
    
    #Output and save to file
    fmt='%.8f\t%.8f\t%.2f'
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
             
###############################################################################
def kFault2xyz_multiseg(ffile,csys=1):
    '''
    Converts a kingdom Photon XY ASCII output fault file into
    a python dictionary file to use for fault planes, etc..
    To print out this file:
    -Go to Faults -> Export -> Fault Surfaces
    -Data Format to Output: Photon XY ASCII 
    -Select all lines to print, and select which faults to print
    -Right justified
    
    This script converts that format, and produces  
    
    Input:
        ffile:                  Path of kingdom output fault file (# Photo Systems etc.)
        csys:                   Coordinate system of input kingdom file.  0=lat/lon,1=utm (1 is default)
    Output:
        masterlist_dict:        A list with dictionaries, one per line. Each 
                                    dict contains: linename, faultnames (string and list each)
                                    X, Y, Z, and DIST (list of lists, one per fault segment)
                                    If csys is lat/lon (0), dist will be emtpy.
       all_ lines:              A list with the lines that have a dictionary in masterlist.
       masterfault_list:        A list with all faults in the dataset.
        
    '''
    #:: V. Sahakian, December 3 2014 ::#
    
    import numpy as np
    
    #Read in kingdom fault file, each line as a string into an array
    with open(ffile) as f:
        king_content = f.readlines()
    
    ## Strip newlines:
    king_content = [x.strip() for x in king_content]
    
    #### First, get all lines that there are faults for.
    ## Loop through the lines, and pull out the segment beginnings, get the line 
    ##   name:
    all_lines = []
    for i in range(len(king_content)):
        i_firstthree = king_content[i][0:3]
        ## If the first three is "Seg", then grab the line name (next part)
        if i_firstthree == 'Seg':
            i_line = king_content[i].split(' ')[1].split('"')[1]
            if i_line not in all_lines:
                all_lines.append(i_line)
                
    ## Make a master list for the line dictionaries:
    masterlist_linedicts = []
    ## And one for all faults in the dataset:
    masterfault_list = []
    
    ### Then, loop through the lines in all_lines. Make a dict for each one.
    for i_line_ind in range(len(all_lines)):
        i_line_dict = {}
        
        ## get the name of the line that this is, and add it to the dictionary:
        i_line = all_lines[i_line_ind]
        i_line_dict['linename'] = i_line
                
        ## get the fault names per segment:
        i_faultnames = []
        
        ## list for the x, y , z, and alongtrack dist. values for each segment
        i_x = []
        i_y = []
        i_z = []
        
        ## Loop through every line in king_content. If it has i_line in it,
        ##    start to pull out the data.
        ## Start a counter:
        segment_counter = 0
        for j_entry in king_content:
            ## If the line name is in this line, start pulling out on the next line:
            if i_line in j_entry:
                ## add to the segment counter to indicate to start counting on next line
                ## and make x, y, distance, and z arrays:
                segment_counter +=1
                j_x = []
                j_y = []
                j_z = []
                ## And get the fualt name for the list:
                j_faultname = j_entry.split(' ')[2].split('"')[1]
                i_faultnames.append(j_faultname)
                
                ## If this fault is not in the masterfault name list, add it.
                if j_faultname not in masterfault_list:
                    masterfault_list.append(j_faultname)
                    
            ## if the line has "Seg" but not this line, then restart the counter:
            elif ('Seg' in j_entry) and (i_line not in j_entry):
                segment_counter = 0
            ## If it's a '}' then it's the end of the segment, reset the counter:
            elif (j_entry == '}') and (segment_counter == 1):
                segment_counter = 0
                ## and also append the new list to the larger dict:
                i_x.append(j_x)
                i_y.append(j_y)
                i_z.append(j_z)
            ## All other cases, if the counter is still 1, then collect the data
            elif segment_counter == 1:
                ij_x = np.float64(j_entry.split(' ')[0])
                ij_y = np.float64(j_entry.split(' ')[1])
                ij_z = np.float64(j_entry.split(' ')[2]) 
                
                ## append to arrays:
                j_x.append(ij_x)
                j_y.append(ij_y)
                j_z.append(ij_z)
            elif j_entry == '':
                segment_counter = 0
                
        ## then, finalize the dictionary:
        i_line_dict['faultnames'] = i_faultnames
        i_line_dict['X'] = i_x
        i_line_dict['Y'] = i_y
        i_line_dict['Z'] = i_z
                
        ## And add it to the master list:
        masterlist_linedicts.append(i_line_dict)
                
    ## Return the list:
    return masterlist_linedicts, all_lines, masterfault_list

             
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
        
        
###############################################################################
    
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
    
    
    
###############################################################################
def parse_allhorizons_photonxy(horizon_path):
    '''
    Read a Kingdom Photon XY ASCII horizons file into a pandas dataframe
        to use in plotting in plchirp.py.
    Input:
        horizon_path:           String with the full path to Photon XY file
    Output:
        horizon_dict_list:      List of dictionaries, each with horizons for a line.
        unique_lines:           Array with the unique lines (there should be a dict for each)
        horizon_list:           A list with all horizons in the dataset.
    '''
    
    import pandas as pd
    from numpy import int,float64,unique,where,diff,arange,r_,sqrt
    
    ## get first row, dictates how many horizons there are:
    first_row_df = pd.read_csv(horizon_path,nrows=1)
    first_row = list(first_row_df)[0]
    ## number of horizons is the first number of the column name, and null value:
    num_horizons = int(first_row.split(' ')[0])
    null_value = float64(first_row.split(' ')[1])
    
    ## import the column names first:
    horizon_names_df = pd.read_csv(horizon_path,nrows=num_horizons)
    horizon_names = horizon_names_df[first_row].values
    
    column_names = ['Line','SP','X','Y'] + list(horizon_names)
    
    ## Then import the data, using these column names - skip an extra row when reading in,
    ##    because the first is the header:
    all_data = pd.read_csv(horizon_path,skiprows=(num_horizons+1),names=column_names,delim_whitespace=True)
    
    ## Get the unique lines:
    unique_lines = unique(all_data.Line)
    
    ## And the lines that have data on them:
    lines_with_horizons = []
    
    ## Make empty list to append df's do:
    horizon_dict_list = []
    
    ## Make empty list for the names of all horizons in the dataset:
    horizon_list = []
    
    ## Go through the unique lines, and for each one, pull out the dataframe and individual horizons:
    for i_line_ind in range(len(unique_lines)):
        i_line = unique_lines[i_line_ind]
        i_line_df = all_data.loc[all_data.Line == i_line].reset_index(drop=True)
        
        i_line_dict = {'line':i_line}
        
        ## Make an empty list for all horizons on this line:
        i_allhorizons = []
        
        ## wher ei sthere no null? Per horizon...
        for i_horizon_ind in range(len(horizon_names)):
            i_horizon = horizon_names[i_horizon_ind]
            i_horizon_df = i_line_df[i_horizon]
            i_horizon_nonull = i_horizon_df.loc[i_horizon_df != null_value]
            
            ## If there is something in here, grab the appropriate information for the dict:
            if len(i_horizon_nonull) > 0:
                
                ## For this horizon, make a dict:
                i_horizon_name = i_horizon.split(' ')[0] ## gets name without color
                i_horizon_dict = {'horizon':i_horizon_name}
                
                ## If it's not in there already, add the line this is on to
                ##   a list of lines that will have horizon dictionaries
                
                ## IF this horizon is not already in the list of horizons, append it:
                if i_horizon_name not in horizon_list:
                    horizon_list.append(i_horizon_name)
                
                i_horizon_X = []
                i_horizon_Y = []
                i_horizon_Z = []
                
                ## Add it to the horizons list:
                i_allhorizons.append(i_horizon_name)
                
                ## Get the indices where segment boundaries occur:
                for i_point in range(len(i_horizon_nonull)):
                    i_break_ind = where(diff(i_horizon_nonull.index) > 1)[0]
                    
                ## add 0 on the front of the break indices, and -1 to the end,
                ## for the purpose of the loop to split segments below:
                i_break_ind = r_[-1,i_break_ind,-1]
                
                ## Add the horizon name, X, Y, and depth, for each segment.
                ## i_break_ind is (n+1) - n, where n is the index of the last
                ##  portion of the prior segment. thus, take 0:n, n+1:... etc.
                for j_segment in range(1,len(i_break_ind),1):
                    j_segment_ind = arange(i_horizon_nonull.index[i_break_ind[j_segment-1]+1],i_horizon_nonull.index[i_break_ind[j_segment]]+1,1)
                    
                    ij_x = i_line_df.loc[j_segment_ind,'X'].values.astype('float64')
                    ij_y = i_line_df.loc[j_segment_ind,'Y'].values.astype('float64')
                    ij_z = i_line_df.loc[j_segment_ind,i_horizon].values.astype('float64')
                    
                    ## Append an individual list to this horizon's X, Y, and Z values:
                    i_horizon_X.append(list(ij_x))
                    i_horizon_Y.append(list(ij_y))
                    i_horizon_Z.append(list(ij_z))
                
                ## Then add these to the dict:
                i_horizon_dict['X'] = i_horizon_X
                i_horizon_dict['Y'] = i_horizon_Y
                i_horizon_dict['Z'] = i_horizon_Z
                
                ## and add this horizon dict to the main line dict:
                i_line_dict[i_horizon_name] = i_horizon_dict
                
        ## Then add each horizon to the line dictionary, if they contain data:
        if len(i_allhorizons) > 0:
            i_line_dict['horizons'] = i_allhorizons
        
            ## And add this line dict to the list of dicts:
            horizon_dict_list.append(i_line_dict)
            
            ## And add this to the list of lines that have data on them:
            lines_with_horizons.append(i_line)
                
    ## Return:
    return horizon_dict_list,lines_with_horizons, horizon_list        


                
                
                
    
    
    
#    kingf=open(ffile,'r')
#    
#    #Initialize x and y arrays
#    x=np.array([])
#    y=np.array([])
#    z=np.array([])
#    
#    segname=''
#    
#    #Read lines of file 
#    while True:
#        line=kingf.readline()
#        if 'Seg "' in line:
#            seg=line.split(' ')[1]
#            if seg not in segname:
#                segname=segname+''+seg
#                #Read the next line,
#                line=kingf.readline()
#                #Output the next line to x and y (first in tmp vars)...
#                XYout=line.split(' ')
#                xtmp=np.float32(XYout[0])
#                ytmp=np.float32(XYout[1])
#                ztmp=np.float32(XYout[2])
#                #Now to perm variables.
#                x=np.r_[x,xtmp]
#                y=np.r_[y,ytmp]
#                z=np.r_[z,ztmp]
#        if line=='':
#            break
#    
#    #Output and save to file
#    fmt='%.8f\t%.8f\t%.f'
#    if csys==0:
#        header='Lon   Lat	' + zheader
#    else:
#        header='X(m)   Y(m)	  ' + zheader
#    
#    #Unsorted values
#    XY_u=np.c_[x,y,z]
#    
#    #Sort by y (or lat)
#    xyind=np.argsort(XY_u[:,1])
#    XY=XY_u[xyind,:]
#    
#    print(xyzfile)
#    np.savetxt(xyzfile,XY,fmt,header=header)
            