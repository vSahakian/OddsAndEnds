#Plot data from MST processed excel spreadsheet
#VJS 1/2016
    
######
#Plot from processed data
#VJS 1/2016

##############################
def read_MSToutfile(proc_outfile,endcal='Yes',clean=True):
    '''
    Input:
        proc_outfile:     String of path to .out Proc file 
        endcal:           'Yes'  or 'No' (Was a calibration section run at the end of the core?)
        clean:            Boolean for whether to clean the data at cap ends (Default: True - clean them)
    Output:  ** These will contain nans**:        Array with the core sub bottom depths 
        section_num:    Array with the core section number
        section_depth:  Array with the core section depth
        pvel:           Array with the p-wave velocity
        rho:            Array with the density
        msu:            Array with the magnetic susceptibility
        units:          Array with units for the respective output variables
        fileinfo:       String with information about datafile/core
    '''
    import numpy as np
    import pandas as pd
    
    print(clean)
    ## First get cruise and core info:
    cruise = proc_outfile.split('/')[-1].split('-')[0]
    core = proc_outfile.split('/')[-1].split('-')[1].split('.out')[0].split('_')[0]
    coreinfo = {'cruise':cruise, 'core':core}
    
    all_data_withunits = pd.read_csv(proc_outfile,skiprows=14,delimiter='\t')
    all_data = all_data_withunits.loc[1:]
    
    ## Get all units:
    all_units = all_data_withunits.loc[0]
    
    ## get units for p-wave vel, density, mag sus, resistivity, frac porosity
    ##   put them in a dictionary
    units = {'pvel':all_units['PWVel'],'rho':all_units['Den1'],'msu':all_units['MS1'],'resistivity':all_units['RES'],'fracporosity':all_units['FP']}
    
    ## want to plot p-wave velocity, density, magnetic susceptibility, resistivity, fractional porosity
    data_nocal = all_data.loc[((all_data['SECT NUM'] != 'cal sect') & (all_data['SECT NUM'] != 'before cal'))]
    if endcal == 'No':
        section_data = data_nocal.dropna()
    elif endcal == 'Yes':
        numsections_withcal = np.max(data_nocal['SECT NUM'].values.astype('float'))
        section_data = data_nocal.loc[data_nocal['SECT NUM'].values.astype('float') < numsections_withcal].dropna().reset_index()
        
    ## Finally, clean by removing 3cm at the beginning and end of each section.
    if clean == False:
        section_data_clean = section_data
    elif clean == True:
        indices2keep = []
        for i_measurement in range(len(section_data)):
            i_section_number =  np.float(section_data.loc[i_measurement]['SECT NUM'])
            
            ## Find all entries for this section:
            i_section_data = section_data.loc[section_data['SECT NUM'].astype('float') == i_section_number]
            
            ## Get the total length of the section:
            i_section_length = np.max(i_section_data['SECT DEPTH'].astype('float'))
            
            ## If the measurement is larger than 3cm or shorter than the section depth minus 3cm, keep it:
            if ((np.float(section_data.loc[i_measurement]['SECT DEPTH']) > 4) & (np.float(section_data.loc[i_measurement]['SECT DEPTH']) < (i_section_length - 4))):
                indices2keep.append(i_measurement)
                
        ## Keep "clean data" as a subset of section data with these indices:
        section_data_clean = section_data.loc[indices2keep]

        
    
        
    #Assign to variables:
    sbdepth = section_data_clean['SB DEPTH'].values.astype('float')
    section_num = section_data_clean['SECT NUM'].values.astype('float')
    section_depth = section_data_clean['SECT DEPTH'].values.astype('float')
    pvel = section_data_clean['PWVel'].values.astype('float')
    rho = section_data_clean['Den1'].values.astype('float')
    msu = section_data_clean['MS1'].values.astype('float')
    resistivity = section_data_clean['RES'].values.astype('float')
    fracporosity = section_data_clean['FP'].values.astype('float')
    
    ## Make it into a dataframe:
    clean_data_dict = {'sbdepth':sbdepth,'section_num':section_num,'section_depth':section_depth,'pvel':pvel,'rho':rho,'msu':msu,'resistivity':resistivity,'fracporosity':fracporosity}
    clean_data = pd.DataFrame(clean_data_dict)
    
    return clean_data,units,coreinfo


##############################
def rdax(axfile):
    #VJS 1/2016
    '''
    Read a text file with axis limits
    Input:
        axfile:     String to path of the input axfile.  
                    Format:
                        vmin=#
                        vmax=#
                        rmin=#
                        rmax=#
                        msmin=#
                        msmax=#
    Output:
        Returns pax: pax=np.array([[vmin,vmax],[rmin,rmax],[msmin,msmax]])
    '''
    
    import numpy as np
    
    #Open ax file
    ax=open(axfile,'r')
    
    #Read in vmin:
    vminl=ax.readline()
    vmaxl=ax.readline()
    rminl=ax.readline()
    rmaxl=ax.readline()
    msminl=ax.readline()
    msmaxl=ax.readline()
    #Close
    ax.close()
    
    #Convert:
    vmin=np.float(vminl.split('=')[1].split('\n')[0])
    vmax=np.float(vmaxl.split('=')[1].split('\n')[0])
    rmin=np.float(rminl.split('=')[1].split('\n')[0])
    rmax=np.float(rmaxl.split('=')[1].split('\n')[0])
    msmin=np.float(msminl.split('=')[1].split('\n')[0])
    msmax=np.float(msmaxl.split('=')[1].split('\n')[0])
    
    pax=np.array([[vmin,vmax],[rmin,rmax],[msmin,msmax]])
    
    return pax
    
    
##############################
def pltMST(mstfile,pdffile,endcal='Yes',plotvals=['pvel','rho','msu'],plotcolors=['midnightblue','firebrick','seagreen'],xlims=None,clean_caps=True,cleanPwave=True):
    '''
    ## VJS 7/2020
    Plot data from an output, processed, MST file 
    Data to plot: P-wave speed, magnetic susceptibility, and density
    Input:
        MSTfile:        String of path to csv Proc file (exported from excel)
        endcal:         'Yes' (default) or 'No' (Was a calibration section run at the end of the core?)
        pdffile:        String with output pdf file
        plotvals:       List of strings with values to plot. Default is ['pvel','rho','msu'], can also include 'resistivity' and 'fracporosity'
        plotcolors:     List with strings of colors. Must be the same length as plotvals. Default: ['blue','red','green']
        xliims:         Dictionary min/max for each value to plot, i.e.: {'pvel':[vmin,vmax],'rho':[rhomin,rhomax],'msu':[msmin,msmax]}
                            Default: None (use standard deviations)
        clean_caps:     Boolean for whether to clean the data at cap ends (Default: True - clean them)
        cleanPwave:     Boolean with whether or not to remove endcaps on Pwave data
    Output: 
        Prints a pdf to pdffile
    '''
    
    import numpy as np
    import matplotlib.pyplot as plt
    
    #Read data from MST file:
    data,units,coreinfo = read_MSToutfile(mstfile,endcal='Yes',clean=clean_caps)

    ## Remove more data points from the p-wave values ONLY
    if cleanPwave == True:
        pwave_data_clean = remove_extra_breakdata(data,break_length=8)
    else:
        pwave_data_clean = remove_extra_breakdata(data,break_length=0)
    
    #Get axes:
    #For y, always plot 0 to ymax:
    ymax=0
    ymin=np.max(data.sbdepth.values)
    yticks=np.arange(ymax,ymin,50)
    
    ## for each variable to plot, get the limits and ticks based on data:
    axis_dict = get_axis_dict(plotvals,data,units,ymin,ymax,pwave_data=pwave_data_clean,xlims=xlims)
        
    ## Get the depths of the core breaks - use less than 5 because the cleaned
    ##    data removes everything before 4 cm - then subtract 4:
    if clean_caps == True:
        core_break_depth = data.loc[data.section_depth < 5].sbdepth.values - 4
    elif clean_caps == False:
        core_break_depth = data.loc[data.section_depth < 1].sbdepth.values
    
    ####
    #INitiate Plotting!!
    f,axes = plt.subplots(nrows=1,ncols=len(plotvals),figsize=(4*len(plotvals),11),sharey=True)
    
    ## Set all yticks to none to start:
    for i in range(len(axes)):
        axes[i].set_yticks([])
        axes[i].tick_params(labelsize=14)
    
    ## Plot in a loop:
    for quantity in range(len(plotvals)):
        i_quantityname = plotvals[quantity]
        
        ## If it's p-wave data to plot, plot the cleaned one:
        if i_quantityname == 'pvel':
            plotdata = pwave_data_clean
        else:
            plotdata = data
        ## get plot color:
        i_color = plotcolors[quantity]
        ## get plot axes:
        i_axisinfo = axis_dict[i_quantityname]
        
        ## plot:
        ## get axis
        i_axis = axes[quantity]
        ## plot horizontal lines at break:
        i_axis.hlines(core_break_depth,i_axisinfo['axis'][0],i_axisinfo['axis'][1],linestyle='-.',linewidth=2,alpha=0.8,color='gray')
        i_axis.scatter(plotdata[i_quantityname].values,plotdata.sbdepth,color=i_color,s=5)
        i_axis.plot(plotdata[i_quantityname].values,plotdata.sbdepth,color=i_color,linewidth=1)
        
        
        ## axis and ticks:        
        i_axis.axis(i_axisinfo['axis'])
        ## turn off y ticks...
        if quantity == 0:
            ## if it's the first one, turn it back on
            i_axis.invert_yaxis()
            i_axis.set_yticks(yticks)
            i_axis.set_ylabel('Core depth (cm)',fontsize=20)
        
        

        i_axis.set_xticks(i_axisinfo['ticks'])
        i_axis.grid(b=True,which='major',axis='both')
#        i_axis.grid(b=True,which='minor',axis='both',linestyle='--',alpha=0.5)
        
        ## labels:
        i_axis.set_xlabel(i_axisinfo['xlabel'],fontsize=20)
    
    #Label
    if clean_caps == True:
        plt.suptitle(coreinfo['cruise'] + ', Core '+coreinfo['core'],fontsize=24)
    elif clean_caps == False:
        plt.suptitle(coreinfo['cruise'] + ', Core '+coreinfo['core'] + ' Raw',fontsize=24)
    
    ## adjust:
    plt.subplots_adjust(wspace=0.1)
    
    #Save figure
    plt.savefig(pdffile)
    plt.clf()    

#####################
#Plot trigger core and piston core together
#Vjs 1/2016
    ## modified 7/2020
def pltJpcTc(jpcfile,tcfile,pdffile,endcal='Yes',plotvals=['pvel','rho','msu'],JCplotcolors=['midnightblue','firebrick','seagreen'],TCplotcolors=['steelblue','lightcoral','mediumaquamarine'],lines=['-.','-'],xlims=None,jcshift=0):
    '''
    Plot a trigger core and piston core on the same plot
    Input:
        jpcfile:     String for path of jpc csv file
        tcfile:      String for path of tc csv file
        pdffile:     STring for path of output pdffile
        endcal:         'Yes' (default) or 'No' (Was a calibration section run at the end of the core?)
        pdffile:        String with output pdf file
        plotvals:       List of strings with values to plot. Default is ['pvel','rho','msu'], can also include 'resistivity' and 'fracporosity'
        JCplotcolors:   List with strings of JC colors. Must be the same length as plotvals. Default: ['blue','red','green']
        TCplotcolors:   List with strings of TC colors. Must be the same length as plotvals. Default: ['blue','red','green']
        lines:          List with strings of linestyles for TRIGGER and PISTON. Default: ['-.','-']
        xlims:          Dictionary min/max for each value to plot, i.e.: {'pvel':[vmin,vmax],'rho':[rhomin,rhomax],'msu':[msmin,msmax]}
                            Default: None (use standard deviations)
        jcshift:        Float with the number of centimeters to shift the JC record. - is up, + is down.
    Output:
        Prints to pdffile.
    '''
            
    import numpy as np
    import matplotlib.pyplot as plt
    import MSTtools as mst
    
    #Get data - trigger and piston:
    dataT,unitsT,coreinfoT = read_MSToutfile(tcfile,endcal='Yes')
    dataJ,unitsJ,coreinfoJ = read_MSToutfile(jpcfile,endcal='Yes')
    
    #Get cruise name and corename:
    cruisename=coreinfoJ['cruise']
    corename=coreinfoJ['core'] 

    ## Remove more data points from the p-wave values ONLY
    pwave_data_cleanT = remove_extra_breakdata(dataT,break_length=8)
    pwave_data_cleanJ = remove_extra_breakdata(dataJ,break_length=8)    

    ## SHIFT for JC shift:
    dataJ.sbdepth = dataJ.sbdepth + jcshift
    pwave_data_cleanJ.sbdepth = pwave_data_cleanJ.sbdepth + jcshift
      
        
    #Get axes for plotting:
    #For y, always plot 0 to ymax:
    ymax=0
    ymin=np.max(dataJ.sbdepth.values)
    yticks=np.arange(ymax,ymin,50)
    
    ## for each variable to plot, get the limits and ticks based on data:
    axis_dictT = get_axis_dict(plotvals,dataT,unitsT,ymin,ymax,pwave_data_cleanT,xlims=xlims)
    axis_dictJ = get_axis_dict(plotvals,dataJ,unitsJ,ymin,ymax,pwave_data_cleanJ,xlims=xlims)
    
    ## Get the depths of the core breaks - use less than 5 because the cleaned
    ##    data removes everything before 4 cm - then subtract 4:
    core_break_depthJ = dataJ.loc[dataJ.section_depth < 5].sbdepth.values - 4
    core_break_depthT = dataT.loc[dataT.section_depth < 5].sbdepth.values - 4
       
    
    #Plot:
    ####
    #INitiate Plotting!!
        ####
    #INitiate Plotting!!
    f,axes = plt.subplots(nrows=1,ncols=len(plotvals),figsize=(4*len(plotvals),11),sharey=True)
    
    ## Set all yticks to none to start:
    for i in range(len(axes)):
        axes[i].set_yticks([])
        axes[i].tick_params(labelsize=14)
    
    ## Plot in a loop:
    for quantity in range(len(plotvals)):
        i_quantityname = plotvals[quantity]
        
        ## If it's p-wave data to plot, plot the cleaned one:
        if i_quantityname == 'pvel':
            plotdataJ = pwave_data_cleanJ
            plotdataT = pwave_data_cleanT
        else:
            plotdataJ = dataJ
            plotdataT = dataT
        ## get plot color:
        i_color_JC = JCplotcolors[quantity]
        i_color_TC = TCplotcolors[quantity]
        ## get plot axes:
        i_axisinfo = axis_dictJ[i_quantityname]
        
        ## plot:
        ## get axis
        i_axis = axes[quantity]
        ## plot horizontal lines at break:
        i_axis.hlines(core_break_depthT,i_axisinfo['axis'][0],i_axisinfo['axis'][1],linestyle='-.',linewidth=1,alpha=0.5,color='gray',label='Trigger Breaks')
        i_axis.hlines(core_break_depthJ,i_axisinfo['axis'][0],i_axisinfo['axis'][1],linestyle='--',linewidth=1.5,alpha=0.7,color='gray',label='Piston Breaks')
        
        ## Plot piston:
        i_axis.scatter(plotdataJ[i_quantityname].values,plotdataJ.sbdepth,color=i_color_JC,s=3)
        i_axis.plot(plotdataJ[i_quantityname].values,plotdataJ.sbdepth,color=i_color_JC,linewidth=0.8,linestyle=lines[1],label='JC')
        
        ## Plot trigger:
        i_axis.scatter(plotdataT[i_quantityname].values,plotdataT.sbdepth,color=i_color_TC,s=3)
        i_axis.plot(plotdataT[i_quantityname].values,plotdataT.sbdepth,color=i_color_TC,linewidth=0.8,linestyle=lines[0],label='TC')
        
        
        ## axis and ticks:        
        i_axis.axis(i_axisinfo['axis'])
        ## turn off y ticks...
        if quantity == 0:
            ## if it's the first one, turn it back on
            i_axis.invert_yaxis()
            i_axis.set_yticks(yticks)
            i_axis.set_ylabel('Depth (cm)',fontsize=20)
        
        ## Add the JC shift as a title
        if jcshift > 0:
            jctext = 'down'
        elif jcshift < 0:
            jctext = 'up'
        else:
            jctext = ''
        i_axis.title.set_text('JC shift is ' + np.str(jcshift) + ' cm ' + jctext)
        
        i_axis.legend(framealpha=0.5)
        i_axis.set_xticks(i_axisinfo['ticks'])
        i_axis.grid(b=True,which='major',axis='both')
#        i_axis.grid(b=True,which='minor',axis='both',linestyle='--',alpha=0.5)
        
        ## labels:
        i_axis.set_xlabel(i_axisinfo['xlabel'],fontsize=20)
    
    #Label
    plt.suptitle(coreinfoJ['cruise'] + ', Core '+coreinfoJ['core'] + ' and ' + coreinfoT['core'],fontsize=24)

    
    ## adjust:
    plt.subplots_adjust(wspace=0.1)
    
    #Save figure
    plt.savefig(pdffile)
    plt.clf()    
    
    
    
    
#####################
#Plot trigger core and piston core together
#Vjs 1/2016
    ## modified 7/2020
def pltJpcTcGc(jpcfile,tcfile,gcfile,pdffile,endcal='Yes',plotvals=['pvel','rho','msu'],JCplotcolors=['midnightblue','firebrick','seagreen'],TCplotcolors=['steelblue','lightcoral','mediumaquamarine'],GCplotcolors=['skyblue','lightpink','aquamarine'],lines=[':','-.','-'],xlims=None,gcshift=0,tcshift=0,jcshift=0):
    '''
    Plot a trigger core and piston core on the same plot
    Input:
        jpcfile:        String for path of jpc csv file
        tcfile:         String for path of tc csv file
        gcfile:         String for path of gravity core csv file
        pdffile:        STring for path of output pdffile
        endcal:         'Yes' (default) or 'No' (Was a calibration section run at the end of the core?)
        pdffile:        String with output pdf file
        plotvals:       List of strings with values to plot. Default is ['pvel','rho','msu'], can also include 'resistivity' and 'fracporosity'
        JCplotcolors:   List with strings of JC colors. Must be the same length as plotvals. Default: ['midnightblue','firebrick','seagreen']
        TCplotcolors:   List with strings of TC colors. Must be the same length as plotvals. Default: ['steelblue','lightcoral','mediumaquamarine']
        GCplotcolors:   List with strings of TC colors. Must be the same length as plotvals. Default: ['skyblue','lightpink','aquamarine']
        lines:          List with strings of linestyles for GRAVITY, TRIGGER and PISTON. Default: ['.','-.','-']
        xlims:          Dictionary min/max for each value to plot, i.e.: {'pvel':[vmin,vmax],'rho':[rhomin,rhomax],'msu':[msmin,msmax]}
                            Default: None (use standard deviations)
        gcshift:        Float with the number of centimeters to shift the TG record. - is up, + is down.
        tcshift:        Float with the number of centimeters to shift the TC record. - is up, + is down.
        jcshift:        Float with the number of centimeters to shift the JC record. - is up, + is down.
    Output:
        Prints to pdffile.
    '''
            
    import numpy as np
    import matplotlib.pyplot as plt
    import MSTtools as mst
    
    #Get data - trigger and piston:
    dataT,unitsT,coreinfoT = read_MSToutfile(tcfile,endcal='Yes')
    dataJ,unitsJ,coreinfoJ = read_MSToutfile(jpcfile,endcal='Yes')
    dataG,unitsG,coreinfoG = read_MSToutfile(gcfile,endcal='Yes')
    
    #Get cruise name and corename:
    cruisename=coreinfoJ['cruise']
    corename=coreinfoJ['core'] 

    ## Remove more data points from the p-wave values ONLY
    pwave_data_cleanT = remove_extra_breakdata(dataT,break_length=8)
    pwave_data_cleanJ = remove_extra_breakdata(dataJ,break_length=8)
    pwave_data_cleanG = remove_extra_breakdata(dataG,break_length=8)    

    ## SHIFT for JC shift:
    dataJ.sbdepth = dataJ.sbdepth + jcshift
    pwave_data_cleanJ.sbdepth = pwave_data_cleanJ.sbdepth + jcshift
    
    ## SHIFT for TC shift:
    dataT.sbdepth = dataT.sbdepth + tcshift
    pwave_data_cleanT.sbdepth = pwave_data_cleanT.sbdepth + tcshift
    
    ## SHIFT for GC shift:
    dataG.sbdepth = dataG.sbdepth + gcshift
    pwave_data_cleanG.sbdepth = pwave_data_cleanG.sbdepth + gcshift
      
        
    #Get axes for plotting:
    #For y, always plot 0 to ymax:
    ymax=0
    ymin=np.max(dataJ.sbdepth.values)
    yticks=np.arange(ymax,ymin,50)
    
    ## for each variable to plot, get the limits and ticks based on data:
    axis_dictG = get_axis_dict(plotvals,dataG,unitsG,ymin,ymax,pwave_data_cleanG,xlims=xlims)
    axis_dictT = get_axis_dict(plotvals,dataT,unitsT,ymin,ymax,pwave_data_cleanT,xlims=xlims)
    axis_dictJ = get_axis_dict(plotvals,dataJ,unitsJ,ymin,ymax,pwave_data_cleanJ,xlims=xlims)
    
    ## Get the depths of the core breaks - use less than 5 because the cleaned
    ##    data removes everything before 4 cm - then subtract 4:
    core_break_depthJ = dataJ.loc[dataJ.section_depth < 5].sbdepth.values - 4
    core_break_depthT = dataT.loc[dataT.section_depth < 5].sbdepth.values - 4
    core_break_depthG = dataG.loc[dataG.section_depth < 5].sbdepth.values - 4
       
    
    #Plot:
    ####
    #INitiate Plotting!!
        ####
    #INitiate Plotting!!
    f,axes = plt.subplots(nrows=1,ncols=len(plotvals),figsize=(4*len(plotvals),11),sharey=True)
    
    ## Set all yticks to none to start:
    for i in range(len(axes)):
        axes[i].set_yticks([])
        axes[i].tick_params(labelsize=14)
    
    ## Plot in a loop:
    for quantity in range(len(plotvals)):
        i_quantityname = plotvals[quantity]
        
        ## If it's p-wave data to plot, plot the cleaned one:
        if i_quantityname == 'pvel':
            plotdataJ = pwave_data_cleanJ
            plotdataT = pwave_data_cleanT
            plotdataG = pwave_data_cleanG
        else:
            plotdataJ = dataJ
            plotdataT = dataT
            plotdataG = dataG
        ## get plot color:
        i_color_JC = JCplotcolors[quantity]
        i_color_TC = TCplotcolors[quantity]
        i_color_GC = GCplotcolors[quantity]
        ## get plot axes:
        i_axisinfo = axis_dictJ[i_quantityname]
        
        ## plot:
        ## get axis
        i_axis = axes[quantity]
        ## plot horizontal lines at break:
        i_axis.hlines(core_break_depthG,i_axisinfo['axis'][0],i_axisinfo['axis'][1],linestyle=':',linewidth=1,alpha=0.5,color='gray',label='Gravity Breaks')
        i_axis.hlines(core_break_depthT,i_axisinfo['axis'][0],i_axisinfo['axis'][1],linestyle='-.',linewidth=1,alpha=0.5,color='gray',label='Trigger Breaks')
        i_axis.hlines(core_break_depthJ,i_axisinfo['axis'][0],i_axisinfo['axis'][1],linestyle='--',linewidth=1.5,alpha=0.7,color='gray',label='Piston Breaks')
        
        ## Plot piston:
        i_axis.scatter(plotdataJ[i_quantityname].values,plotdataJ.sbdepth,color=i_color_JC,s=3)
        i_axis.plot(plotdataJ[i_quantityname].values,plotdataJ.sbdepth,color=i_color_JC,linewidth=0.8,linestyle=lines[2],label='JC')
        
        ## Plot trigger:
        i_axis.scatter(plotdataT[i_quantityname].values,plotdataT.sbdepth,color=i_color_TC,s=3)
        i_axis.plot(plotdataT[i_quantityname].values,plotdataT.sbdepth,color=i_color_TC,linewidth=0.8,linestyle=lines[1],label='TC')
        
        ## Plot gravity:
        i_axis.scatter(plotdataG[i_quantityname].values,plotdataG.sbdepth,color=i_color_GC,s=3)
        i_axis.plot(plotdataG[i_quantityname].values,plotdataG.sbdepth,color=i_color_GC,linewidth=0.8,linestyle=lines[0],label='GC')
        
        
        ## axis and ticks:        
        i_axis.axis(i_axisinfo['axis'])
        ## turn off y ticks...
        if quantity == 0:
            ## if it's the first one, turn it back on
            i_axis.invert_yaxis()
            i_axis.set_yticks(yticks)
            i_axis.set_ylabel('Depth (cm)',fontsize=20)
        
        ## Add the JC shift as a title
        if jcshift > 0:
            jctext = 'down'
        elif jcshift < 0:
            jctext = 'up'
        else:
            jctext = ''
            
        ## Add the TC shift as a title
        if tcshift > 0:
            tctext = 'down'
        elif tcshift < 0:
            tctext = 'up'
        else:
            tctext = ''
            
        ## Add the GC shift as a title
        if gcshift > 0:
            gctext = 'down'
        elif gcshift < 0:
            gctext = 'up'
        else:
            gctext = ''
            
        i_axis.title.set_text('Shifts - JC: ' + np.str(jcshift) + 'cm ' + jctext + '\n, TC: ' + np.str(tcshift) + 'cm ' + tctext + '\n, GC: ' + np.str(gcshift) + 'cm ' + gctext)
        
        i_axis.legend(framealpha=0.5)
        i_axis.set_xticks(i_axisinfo['ticks'])
        i_axis.grid(b=True,which='major',axis='both')
#        i_axis.grid(b=True,which='minor',axis='both',linestyle='--',alpha=0.5)
        
        ## labels:
        i_axis.set_xlabel(i_axisinfo['xlabel'],fontsize=20)
    
    #Label
    plt.suptitle(coreinfoJ['cruise'] + ', Core '+coreinfoJ['core'] + ', ' + coreinfoT['core'] + ', ' + coreinfoG['core'],fontsize=24)

    
    ## adjust:
    plt.subplots_adjust(wspace=0.1)
    
    #Save figure
    plt.savefig(pdffile)
    plt.clf()    
    
    

######################################################
def remove_extra_breakdata(data,break_length=8):
    '''
    Input:
        data:           Pandas dataframe with the original cleaned data
        break_length:   The added length at the breaks to remove (i.e., 
                            usually 4, maybe you want it to be 8). Default: 8
    Output:
        clean_data:     Pandas dataframe with removed data
    '''
    import numpy as np
    
    ## Remove more data points from the p-wave values ONLY
    indices2keep = []
    for i_measurement in range(len(data)):
        i_section_number =  np.float(data.loc[i_measurement]['section_num'])
        
        ## Find all entries for this section:
        i_section_data = data.loc[data['section_num'].astype('float') == i_section_number]
        
        ## Get the total length of the section:
        i_section_length = np.max(i_section_data['section_depth'].astype('float'))
        
        ## If the measurement is larger than 8cm or shorter than the section depth minus 8cm, keep it.
        ##  But recall that the section length ends at the original section length - 4 (from initial cleaning in file read)
        ##    so subtract 4 cm from the end.
        if ((np.float(data.loc[i_measurement]['section_depth']) > break_length) & (np.float(data.loc[i_measurement]['section_depth']) < (i_section_length - (break_length - 4)))):
            indices2keep.append(i_measurement)
            
    ## Keep "clean data" as a subset of section data with these indices:
    clean_data = data.loc[indices2keep]
    
    return clean_data

########################################################
def get_axis_dict(plotvals,data,units,ymin,ymax,pwave_data=None,xlims=None):
    '''
    Get an axis dictionary object based on the plot values and data
    Input:
        plotvals:      List of strings with values to plot. 
                            Default is ['pvel','rho','msu'], can also include 
                            'resistivity' and 'fracporosity'
        data:           Dictionary with all data (cleaned after reading)
        units:          Dictionary with units as comes out of reading MST file
        ymin:           Float with ymin for axis
        ymax:           Float with ymax for axis
        pwave_data:     Cleaned p-wave data with extra breaks removed (Default: None)
        xlims:          Dictionary min/max for each value to plot, 
                            i.e.: {'pvel':[vmin,vmax],'rho':[rhomin,rhomax],'msu':[msmin,msmax]}
                            Default: None (use standard deviations)         
    Output:
        axis_dict:      Axis dictionary with sub-dictionaries for each plot value (and same name).
                            Example sub-dictionary: {'axis':fpax,'ticks':fptick, 'xlabel':fpxlabel}
    
    '''
    import numpy as np
    ## for each variable to plot, get the limits and ticks based on data:
    axis_dict = {}
        
    if 'pvel' in plotvals:
        
        ## if not defined in function call, get std dev:
        if xlims == None:
            #For pwave velocity:
            vstd=np.std(pwave_data.pvel.values)
            ## for pwave get median instead of mean
            vm=np.median(pwave_data.pvel.values)
            vxmin=vm-2*vstd
            vxmax=vm+2*vstd
            
            #Get ticks:
            vtmin=vxmin-np.remainder(vxmin,100)
            vtmax=vxmax-np.remainder(vxmax,100)
            
            vax=[vtmin,vtmax,ymin,ymax]
            vtick=np.arange(vtmin,vtmax+100,np.round((vtmax-vtmin)/3,0))
            
        else:
            vxmin = xlims['pvel'][0]
            vxmax= xlims['pvel'][1]
            vax=[vxmin,vxmax,ymin,ymax]
            vtick=np.arange(vxmin,vxmax,np.floor((vxmax-vxmin)/3))
        
        vxlabel='P-Wave Vel.' + ' ('+units['pvel']+')'
        
        pveldict = {'axis':vax,'ticks':vtick,'xlabel':vxlabel}
        
        ## add to axis dict:
        axis_dict['pvel'] = pveldict
    
    if 'rho' in plotvals:
        if xlims == None:
            #Density:
            #Std dev:
            rstd=np.std(data.rho.values)
            rm=np.mean(data.rho.values)
            rxmin=np.round(rm-2.2*rstd,1)
            rxmax=np.round(rm+2.2*rstd,1)
            rax=[rxmin,rxmax,ymin,ymax]

        else:
            rxmin = xlims['rho'][0]
            rxmax= xlims['rho'][1]
            rax=[rxmin,rxmax,ymin,ymax]
        #Get ticks
        rtick=np.arange(rxmin,rxmax,np.floor((rxmax*100-rxmin*100)/4)/100)
        
        rxlabel='Density' + ' ('+units['rho']+')'
        
        rhodict = {'axis':rax, 'ticks':rtick,'xlabel':rxlabel}
        axis_dict['rho'] = rhodict

    if 'msu' in plotvals:
        if xlims == None:
            #Magnetic susceptibility:
            msstd=np.std(data.msu.values)
            msm=np.mean(data.msu.values)
            msxmin=np.round(msm-2.5*msstd,1)
            msxmax=np.round(msm+2.5*msstd,1)
            msax=[msxmin,msxmax,ymin,ymax]
        else:
            msxmin = xlims['msu'][0]
            msxmax= xlims['msu'][1]
            msax=[msxmin,msxmax,ymin,ymax]
        #Get ticks
        mtick=np.arange(msxmin,msxmax,np.floor((msxmax-msxmin)/4))
        
        mxlabel='Mag. Susc.' + '\n ('+units['msu']+')'
        
        msudict = {'axis':msax,'ticks':mtick, 'xlabel':mxlabel}
        axis_dict['msu'] = msudict
        
    if 'resistivity' in plotvals:
        if xlims == None:
            #resistivity:
            resstd=np.std(data.resistivity.values)
            resm=np.mean(data.resistivity.values)
            resxmin=np.round(resm-3.5*resstd,1)
            resxmax=np.round(msm+3.5*resstd,1)
            resax=[resxmin,resxmax,ymin,ymax]
        else:
            resxmin = xlims['resistivity'][0]
            resxmax= xlims['resistivity'][1]
            resax=[resxmin,resxmax,ymin,ymax]
            
        #Get ticks
        restick=np.arange(resxmin,resxmax,np.floor((resxmax-resxmin)/4))
        
        resxlabel='Resistivity' + ' ('+units['resistivity']+')'
        
        resdict = {'axis':resax,'ticks':restick, 'xlabel':resxlabel}
        axis_dict['resistivity'] = resdict
        
    if 'fracporosity' in plotvals:
        if xlims == None:
            #fractional porosity:
            fpstd=np.std(data.fracporosity.values)
            fpm=np.mean(data.fracporosity.values)
            fpxmin=np.round(fpm-3.5*fpstd,1)
            fpxmax=np.round(fpm+3.5*fpstd,1)
            fpax=[fpxmin,fpxmax,ymin,ymax]
        else:
            fpxmin = xlims['fracporosity'][0]
            fpxmax= xlims['fracporosity'][1]
            fpax=[fpxmin,fpxmax,ymin,ymax]
        #Get ticks
        fptick=np.arange(fpxmin,fpxmax,np.floor((fpxmax-fpxmin)/4))
        
        fpxlabel='Frac. Porosity' + ' ('+units['fracporosity']+')'
        
        fpdict = {'axis':fpax,'ticks':fptick, 'xlabel':fpxlabel}
        axis_dict['fracporosity'] = fpdict
        
    return axis_dict


#####################################################
def rdMSTpcsv(procfile):
    '''
    OBSOLETE NOW
    Read in data from an MST processed csv file, exported from excel 
    (first sheet only) - from Thompson cruise in January 2016. Obsolete now.
    Input:
        procfile:     String of path to csv Proc file (exported from excel)
    Output:  ** These will contain nans**
        sbdepth:      Array with the core sub bottom depths 
        pvel:         Array with the p-wave velocity
        rho:          Array with the density
        msu:          Array with the magnetic susceptibility
        units:        Array with units for the respective output variables
        fileinfo:     String with information about datafile
    '''
    
    import numpy as np
    
    #First, read in units:
    mstp=open(procfile,'r')
    #Read in information about file and date of creation
    mstpdat=mstp.readline()
    #It's all in one line if it's a csv, so split it:
    fileinfo=mstpdat.split('\r')[0].split(',')[0]
    udat=mstpdat.split('\r')[4].split(',')[11:23]    
    #Close file
    mstp.close()
    
    #Make units array:
    units=[udat[0],udat[5],udat[6],udat[8]]
    
    #Read in data:
    dat=np.genfromtxt(procfile,delimiter=',',skip_header=6)
    #Assign to variables:
    sbdepth=dat[:,11]
    pvel=dat[:,16]
    rho=dat[:,17]
    msu=dat[:,19]


    return sbdepth,pvel,rho,msu,units,fileinfo
    