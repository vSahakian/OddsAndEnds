def conv2xcalign(pkfile_2col,pkfile_xc,line):
    
    import numpy as np
    
    #Read in files:
    pk2=np.loadtxt(pkfile_2col)
    
    Inst=0
    Tr=1
    Ty='V1'
    Lat=0
    Lon=0
    Range=0
    Acc='a 0.001'
    Type='Sf'
    First='0'
    
    
    

