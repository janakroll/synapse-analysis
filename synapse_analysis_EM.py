# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 14:54:12 2022

@author: krollj
"""

import os
import glob
import pandas as pd
import numpy as np
from scipy.spatial import distance

pi = np.pi

#Input pixel size as calculated from scale in imageJ as nm/pixel
pixel_size = 0.XYZ

#Creation of lists for all parameters that will be appended with every txt file 
#and saved as excel files in the end
az_length = []
N_docked = []
diameter_all = []
D_avg = []
N_ELV = []
A_ELV = []
SVsurface = []
AZ_counter = []

dist_to_AZ = pd.DataFrame()
binned_dist_to_AZ = pd.DataFrame()

#Directory containing txt files exported with imageJ
os.chdir('PATH-CONTAINING-YOUR-IMAGEJ-TXT-FILES')
print(os.getcwd())
filenames = (glob.glob('*.txt'))

for f in filenames:
    #Import of txt files generated with ImageJ, addition of headings in data frame
    test = pd.read_csv(f, delimiter='\t', names = ["#", "category", "value1", "value2", "value3"])
    test.set_index("category", inplace=True)
    
    AZ_number = (test.index == 'Active_zone').sum()

    #pre-check if exactly one active zone was labeled per txt file
    if AZ_number == 1: 
        AZ_counter.append(1)
    else:
        print ('Problem with active zone in file:', f)
        
        
if(len(filenames)) == len(AZ_counter):
    print ('Active zone check passed')
    
    #bins for the binning of distances
    bins = np.arange(0,1001,10,int)  
    binningvalues = bins.tolist() 
    

    for f in filenames:
        #Import of txt files generated with ImageJ, addition of headings in data frame
        test = pd.read_csv(f, delimiter='\t', names = ["#", "category", "value1", "value2", "value3"])
        test.set_index("category", inplace=True)
        
        """
        Part 1 - Active zone
        """
        
        #Addition of active zone length to the list az_length
        length = (test.loc['Active_zone','value1'])
        az_length.append(length*pixel_size)
        
        #Creation of array with coordinates of all active zone values (x and y)
        x_coord = (test.loc['Active_zone','value2'])
        x = (x_coord.split(','))
        y_coord = (test.loc['Active_zone','value3'])
        y = (y_coord.split(','))
        xy_coord = np.array((x,y),float)
        xy_coord = np.transpose(xy_coord)
    

        """
        Part 2 - Vesicles (SV)
        """

        #Creation of data frame with only SV values
        sv_values = (test.loc['SV'])
        
        #Addition of all radiuses to list radius_all_sv
        radius_all_sv = np.array(sv_values['value3'], float)
        radius_all_sv = radius_all_sv*pixel_size
        
        #Calculation surface area for all SVs in one image
        surfaces = 4 * pi * radius_all_sv ** 2
        SVsurface.append(surfaces.sum())
        
        #Creation of array with coordinates of all SVs 
        x_sv = (sv_values['value1'].astype(float))
        y_sv = (sv_values['value2'].astype(float))
        xy_sv = np.array((x_sv,y_sv))
        xy_sv = np.transpose(xy_sv)

        
        #Calculation of min. euclidean distance between each SV and active zone
        #thereby subtraction of radius of each SV to have the distance between membranes
        all_dist = (distance.cdist(xy_sv,xy_coord).min(axis=1))*pixel_size-radius_all_sv
        
        #binning of distances
        out = pd.cut(all_dist, bins=bins)
        distancebins = pd.value_counts(out, sort = False)
    
        
        """
        Part 3 - Docked vesicles
        """
  
      #test how many docked SVs are listed in txt file
        m = (test.index == 'docked_SV').sum()
        
        if m == 0:
            N_docked.append(0)
            D = radius_all_sv*2
            diameter_all.append(D)
            D_avg.append(D.mean())
            
        elif m == 1:
            N_docked.append(1)
            docked_values = (test.loc['docked_SV'])
            radius_all_docked = np.array(docked_values['value3'],float)
            radius_all_docked = radius_all_docked*pixel_size
            D = np.append(radius_all_sv,radius_all_docked)*2
            diameter_all.append(D)
            D_avg.append(D.mean())
            
        else:
            #Creation of data frame with only docked_SV values
            docked_values = (test.loc['docked_SV'])
            
            #Addition of all radiuses to list radius_all_docked
            radius_all_docked = np.array(docked_values['value3'], float)
            radius_all_docked = radius_all_docked*pixel_size
            
            #Count of docked SVs
            N_docked.append(len(radius_all_docked))
            
            #Addition of all SV diameters to list diameter_all, addition of avg. D to D_avg
            D = np.concatenate([radius_all_sv,radius_all_docked])*2
            diameter_all.append(D)
            D_avg.append(D.mean())
  
          
        """
        Part 4 - Endosome-like vacuoles (ELVs)
        
        """

        #test how many endosomes are listed in txt file
        n = (test.index == 'Endosome').sum()
        
        if n == 0:
            N_ELV.append(0)
            A_ELV.append(0)
            
        elif n == 1:
            N_ELV.append(1)
            ELV_values = (test.loc['Endosome'])
            ELV_area = (ELV_values['value1'])
            ELV_area = ELV_area*pixel_size*pixel_size
            A_ELV.append(ELV_area)
        
        else:
            
            #Creation of data frame with only endosome values
            ELV_values = (test.loc['Endosome'])
            
            #Creation of array with ELV areas
            ELV_area = np.array(ELV_values['value1'], float)
            ELV_area = ELV_area*pixel_size*pixel_size
            
            #Addition of ELV number to list N_ELV
            N_ELV.append(len(ELV_area))
            A_ELV.append(ELV_area.mean())

            
        """
        Part 5 - Export as Excel files
        """
        #Collection of distances and binned distances for each txt file 
        distseries = pd.Series(all_dist)        
        dist_to_AZ = pd.concat([dist_to_AZ,distseries], axis=1)
        binned_dist_to_AZ = pd.concat([binned_dist_to_AZ,distancebins], axis=1)

    dist_to_AZ.columns = filenames
    binned_dist_to_AZ.columns = filenames  
   
    alltogether = pd.DataFrame(list(zip(filenames, az_length, N_docked, D_avg, N_ELV, A_ELV,SVsurface)), columns =['File', 'Active zone length (nm)', 'N docked SVs', 'avg. SV diameter (nm)', 'N endosomal structures', 'avg. endosome area (nm²)', 'Summed SV surface area (nm²)']) 
    
    with pd.ExcelWriter('synapse_analysis.xlsx') as writer:  
        alltogether.to_excel(writer, sheet_name='Summary')
        dist_to_AZ.to_excel(writer, sheet_name='SV distances to AZ')
        binned_dist_to_AZ.to_excel(writer, sheet_name='Binned SV distances to AZ')

    print ('Analysis done')
    
else:
    print('Analysis could not be performed. Please correct indicated txt files.')
                   
        
