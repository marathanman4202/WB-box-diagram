# -*- coding: utf-8 -*-
"""
Created on Fri Sep 26 12:37:07 2014

@author: haggertr
"""

import numpy as np
import constants as cst   # constants.py contains constants used here

np.set_printoptions(precision=3)

file_model_csv = "Willamette_at_Portland_(m3_s)_Historic_Run0.csv"
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
time = np.array(data_v[:,0])
Value_Ref = np.mean((np.array(data_v[:,1]))[:(cst.days_in_60_yrs-1)])*cst.seconds_in_yr/cst.Willamette_Basin_area_at_PDX*100.


Value = np.mean(np.array([Value_Ref]))
print "Willamette at Portland = ", Value," cm"


file_model_csv = "Climate_Historic_Run0.csv"
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
Value_Ref = np.mean((np.array(data_v[:,2]))[:(cst.days_in_60_yrs-1)])*365/10.


Value = np.mean(np.array([Value_Ref]))
print "Basin-wide avg Precip = ", Value," cm"


file_model_csv = "Snow_(mm)_Historic_Run0.csv"
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
Value_Ref = np.mean([np.max(np.array(data_v[i*365:(i+1)*365,1])) for i in range(60)])/10. #avg over max of each of 60 yrs


Value = np.mean(np.array([Value_Ref]))
print "Basin-wide max SWE = ", Value," cm"

# Calculate storage in soil water content as follows
# Since there is no simulated historical file as of 1/17/2015, use first 15 yrs of Ref, HighClim, LowClim 
# Sum the soil water in the 4 categories of forest soil.  Do the same (further below) for ag
# Take the difference between the max and the min as the storage

file_model_csv = "Forest_Water_Content_Ref_Run0.csv"
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
Value_Ref = np.max([np.array(np.sum([data_v[i*365:(i+1)*365,j] for j in range(1,5)],0)) for i in range(15)])/10. -\
            np.min([np.array(np.sum([data_v[i*365:(i+1)*365,j] for j in range(1,5)],0)) for i in range(1,15)])/10. #max of 15 yrs 

file_model_csv = file_model_csv.replace("Ref", "HighClim")
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
Value_HC = np.max([np.array(np.sum([data_v[i*365:(i+1)*365,j] for j in range(1,5)],0)) for i in range(15)])/10. -\
           np.min([np.array(np.sum([data_v[i*365:(i+1)*365,j] for j in range(1,5)],0)) for i in range(1,15)])/10. #max of 15 yrs 

file_model_csv = file_model_csv.replace("HighClim", "LowClim")
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
Value_LC = np.max([np.array(np.sum([data_v[i*365:(i+1)*365,j] for j in range(1,5)],0)) for i in range(15)])/10. -\
           np.min([np.array(np.sum([data_v[i*365:(i+1)*365,j] for j in range(1,5)],0)) for i in range(1,15)])/10. #max of 15 yrs 

Value_for = np.mean(np.array([Value_Ref,Value_HC,Value_LC]))*0.727  #Fraction of soil to be treated like forest for calc
print "Basin-wide stored soil water in forest = ", Value_for," cm"

file_model_csv = "Ag_Water_Content_Ref_Run0.csv"
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
Value_Ref = np.max([np.array(np.sum([data_v[i*365:(i+1)*365,j] for j in range(1,5)],0)) for i in range(15)])/10. -\
            np.min([np.array(np.sum([data_v[i*365:(i+1)*365,j] for j in range(1,5)],0)) for i in range(1,15)])/10. #max of 15 yrs 

file_model_csv = file_model_csv.replace("Ref", "HighClim")
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
Value_HC = np.max([np.array(np.sum([data_v[i*365:(i+1)*365,j] for j in range(1,5)],0)) for i in range(15)])/10. -\
           np.min([np.array(np.sum([data_v[i*365:(i+1)*365,j] for j in range(1,5)],0)) for i in range(1,15)])/10. #max of 15 yrs 

file_model_csv = file_model_csv.replace("HighClim", "LowClim")
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
Value_LC = np.max([np.array(np.sum([data_v[i*365:(i+1)*365,j] for j in range(1,5)],0)) for i in range(15)])/10. -\
           np.min([np.array(np.sum([data_v[i*365:(i+1)*365,j] for j in range(1,5)],0)) for i in range(1,15)])/10. #max of 15 yrs 

Value_ag = np.mean(np.array([Value_Ref,Value_HC,Value_LC]))*0.273   #Fraction of soil to be treated like ag for calc

print "Basin-wide stored soil water in ag = ", Value_ag," cm"
print "Basin-wide stored soil water total = ", Value_ag + Value_for, " cm"

file_model_csv = "ET_by_Elevation_(mm)_Historic_Run0.csv"
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
Value_Ref = np.mean((np.array(data_v[:,1]))[1460:(cst.days_in_60_yrs-1)])*365/10.

Value = np.mean(np.array([Value_Ref]))
print "Basin-wide avg AET = ", Value," cm"

file_model_csv = "ET_by_LandCover_(mm)_Historic_Run0.csv"
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
Value_Ref = np.mean((np.array(data_v[:,1]))[1460:(cst.days_in_60_yrs-1)])*365/10.
Value = np.mean(np.array([Value_Ref]))*0.727  #Frac forest area
print "Basin-wide avg Forest AET = ", Value," cm"

data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
Value_Ref = np.mean((np.array(data_v[:,3]))[1460:(cst.days_in_60_yrs-1)])*365/10.
Value = np.mean(np.array([Value_Ref]))*0.273  #Frac ag area
print "Basin-wide avg Ag AET = ", Value," cm"


# http://www.oregon.gov/owrd/docs/1998_04_Willamette_Brochure.pdf
WVP_Vol_summer = (93900+28700+281600+65000+194600+24800+249900+324200+78800+143900+108200)*cst.acft_to_m3/cst.Willamette_Basin_area*100.
WVP_Vol_full_pool = (116800+32900+455100+77600+355500+60700+281000+45800+89500+219000+125000)*cst.acft_to_m3/cst.Willamette_Basin_area*100.
print "Reservoirs Full Pool Storage = ",WVP_Vol_summer, " cm"


file_model_csv = "Daily_WaterMaster_Metrics_Historic_Run0.csv"
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
Value_Ref = np.mean((np.array(data_v[:,1]))[:(cst.days_in_60_yrs-1)])*cst.seconds_in_yr/cst.Willamette_Basin_area_at_PDX*100.

Value = np.mean(np.array([Value_Ref]))
print "Instream regulatory use = ", Value," cm"


file_model_csv = "Daily_WaterMaster_Metrics_Historic_Run0.csv"
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
Value_Ref = (np.mean((np.array(data_v[:,2]))[:(cst.days_in_60_yrs-1)]) +\
             np.mean((np.array(data_v[:,3]))[:(cst.days_in_60_yrs-1)]))*cst.seconds_in_yr/cst.Willamette_Basin_area*100.

Value = np.mean(np.array([Value_Ref]))
print "Irrigation water diverted = ", Value," cm"


file_model_csv = "Urban_Population_Historic_Run0.csv"
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
UrbPop = np.mean(np.sum(np.array(data_v[1:,1:][:60]),1))
Metro_Pop = np.mean(np.array(data_v[1:16,1]))

file_model_csv = "Rural_Residential_Population_Historic_Run0.csv"
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
RurPop = np.mean(np.sum(np.array(data_v[1:,1:][:60]),1))

Basin_Pop = UrbPop + RurPop
print "Population = ", Basin_Pop

#file_model_csv = "UrbanWaterDemand(_ccf_per_day_)_Historic_Run0.csv"
#file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
#data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
#Value_Ref = np.mean(np.sum(np.column_stack((np.array(data_v[1:16,1]),np.array(data_v[1:16,9]))),1))*100*365*cst.cfs_to_m3/cst.Willamette_Basin_area*100.
#Value_Ref = Value_Ref*Basin_Pop/Metro_Pop
#
#Value = np.mean(np.array([Value_Ref]))
#print "Municipal & domestic water diverted = ", Value," cm"
#
#print "Water use per person = ", Value*cst.Willamette_Basin_area/100*1000/3.785/365/Basin_Pop, " gal/day/person"
