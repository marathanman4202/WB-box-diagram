# -*- coding: utf-8 -*-
"""
Created on Fri Sep 26 12:37:07 2014

@author: haggertr
"""

import numpy as np
import constants as cst   # constants.py contains constants used here

np.set_printoptions(precision=3)

file_model_csv = "Willamette_at_Portland_(m3_s)_Ref_Run0.csv"
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
time = np.array(data_v[:,0])
Value_Ref = np.mean((np.array(data_v[:,1]))[:(cst.days_in_15_yrs-1)])*cst.seconds_in_yr/cst.Willamette_Basin_area_at_PDX*100.

file_model_csv = file_model_csv.replace("Ref", "HighClim")
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
Value_HC = np.mean((np.array(data_v[:,1]))[:(cst.days_in_15_yrs-1)])*cst.seconds_in_yr/cst.Willamette_Basin_area_at_PDX*100.

file_model_csv = file_model_csv.replace("HighClim", "LowClim")
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
Value_LC = np.mean((np.array(data_v[:,1]))[:(cst.days_in_15_yrs-1)])*cst.seconds_in_yr/cst.Willamette_Basin_area_at_PDX*100.

Value = np.mean(np.array([Value_Ref, Value_HC, Value_LC]))
print "Willamette at Portland = ", Value," cm"


file_model_csv = "Climate_Ref_Run0.csv"
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
Value_Ref = np.mean((np.array(data_v[:,2]))[:(cst.days_in_15_yrs-1)])*365/10.

file_model_csv = file_model_csv.replace("Ref", "HighClim")
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
Value_HC = np.mean((np.array(data_v[:,2]))[:(cst.days_in_15_yrs-1)])*365/10.

file_model_csv = file_model_csv.replace("HighClim", "LowClim")
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
Value_LC = np.mean((np.array(data_v[:,2]))[:(cst.days_in_15_yrs-1)])*365/10.

Value = np.mean(np.array([Value_Ref, Value_HC, Value_LC]))
print "Basin-wide avg Precip = ", Value," cm"


file_model_csv = "Snow_(mm)_Ref_Run0.csv"
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
Value_Ref = np.mean([np.max(np.array(data_v[i*365:(i+1)*365,1])) for i in range(15)])/10. #avg over max of each of 15 yrs

file_model_csv = file_model_csv.replace("Ref", "HighClim")
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
Value_HC = np.mean([np.max(np.array(data_v[i*365:(i+1)*365,1])) for i in range(15)])/10. #avg over max of each of 15 yrs

file_model_csv = file_model_csv.replace("HighClim", "LowClim")
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
Value_LC = np.mean([np.max(np.array(data_v[i*365:(i+1)*365,1])) for i in range(15)])/10. #avg over max of each of 15 yrs

Value = np.mean(np.array([Value_Ref, Value_HC, Value_LC]))
print "Basin-wide max SWE = ", Value," cm"


file_model_csv = "ET_by_Elevation_(mm)_Ref_Run0.csv"
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
Value_Ref = np.mean((np.array(data_v[:,1]))[1460:(cst.days_in_15_yrs-1)])*365/10.

file_model_csv = file_model_csv.replace("Ref", "HighClim")
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
Value_HC = np.mean((np.array(data_v[:,1]))[:(cst.days_in_15_yrs-1)])*365/10.

file_model_csv = file_model_csv.replace("HighClim", "LowClim")
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
Value_LC = np.mean((np.array(data_v[:,1]))[:(cst.days_in_15_yrs-1)])*365/10.
Value = np.mean(np.array([Value_Ref, Value_HC, Value_LC]))
print "Basin-wide avg AET = ", Value," cm"


# http://www.oregon.gov/owrd/docs/1998_04_Willamette_Brochure.pdf
WVP_Vol_summer = (93900+28700+281600+65000+194600+24800+249900+324200+78800+143900+108200)*cst.acft_to_m3/cst.Willamette_Basin_area*100.
WVP_Vol_full_pool = (116800+32900+455100+77600+355500+60700+281000+45800+89500+219000+125000)*cst.acft_to_m3/cst.Willamette_Basin_area*100.
print "Reservoirs Full Pool Storage = ",WVP_Vol_summer, " cm"


file_model_csv = "Daily_WaterMaster_Metrics_Ref_Run0.csv"
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
Value_Ref = np.mean((np.array(data_v[:,1]))[:(cst.days_in_15_yrs-1)])*cst.seconds_in_yr/cst.Willamette_Basin_area_at_PDX*100.

file_model_csv = file_model_csv.replace("Ref", "HighClim")
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
Value_HC = np.mean((np.array(data_v[:,1]))[:(cst.days_in_15_yrs-1)])*cst.seconds_in_yr/cst.Willamette_Basin_area_at_PDX*100.

file_model_csv = file_model_csv.replace("HighClim", "LowClim")
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
Value_LC = np.mean((np.array(data_v[:,1]))[:(cst.days_in_15_yrs-1)])*cst.seconds_in_yr/cst.Willamette_Basin_area_at_PDX*100.

Value = np.mean(np.array([Value_Ref, Value_HC, Value_LC]))
print "Instream regulatory use = ", Value," cm"


file_model_csv = "Daily_WaterMaster_Metrics_Ref_Run0.csv"
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
Value_Ref = (np.mean((np.array(data_v[:,2]))[:(cst.days_in_15_yrs-1)]) +\
             np.mean((np.array(data_v[:,3]))[:(cst.days_in_15_yrs-1)]))*cst.seconds_in_yr/cst.Willamette_Basin_area*100.

file_model_csv = file_model_csv.replace("Ref", "HighClim")
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
Value_HC = (np.mean((np.array(data_v[:,2]))[0:5474]) +\
             np.mean((np.array(data_v[:,3]))[0:5474]))*cst.seconds_in_yr/cst.Willamette_Basin_area*100.

file_model_csv = file_model_csv.replace("HighClim", "LowClim")
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
Value_LC = (np.mean((np.array(data_v[:,2]))[:(cst.days_in_15_yrs-1)]) +\
             np.mean((np.array(data_v[:,3]))[:(cst.days_in_15_yrs-1)]))*cst.seconds_in_yr/cst.Willamette_Basin_area*100.

Value = np.mean(np.array([Value_Ref, Value_HC, Value_LC]))
print "Irrigation water diverted = ", Value," cm"


#file_model_csv = "Daily_WaterMaster_Metrics_Ref_Run0.csv"
#file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
#data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
#Value_Ref = (np.mean((np.array(data_v[:,4]))[:(cst.days_in_15_yrs-1)]) +\
#             np.mean((np.array(data_v[:,5]))[:(cst.days_in_15_yrs-1)]))*cst.seconds_in_yr/cst.Willamette_Basin_area*100.
#
#file_model_csv = file_model_csv.replace("Ref", "HighClim")
#file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
#Value_HC = (np.mean((np.array(data_v[:,4]))[:(cst.days_in_15_yrs-1)]) +\
#             np.mean((np.array(data_v[:,5]))[:(cst.days_in_15_yrs-1)]))*cst.seconds_in_yr/cst.Willamette_Basin_area*100.
#
#file_model_csv = file_model_csv.replace("HighClim", "LowClim")
#file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
#Value_LC = (np.mean((np.array(data_v[:,4]))[:(cst.days_in_15_yrs-1)]) +\
#             np.mean((np.array(data_v[:,5]))[:(cst.days_in_15_yrs-1)]))*cst.seconds_in_yr/cst.Willamette_Basin_area*100.
#
#Value = np.mean(np.array([Value_Ref, Value_HC, Value_LC]))
#print "Municipal water diverted = ", Value," cm"


file_model_csv = "Urban_Population_Ref_Run0.csv"
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
UrbPop = np.mean(np.sum(np.array(data_v[1:,1:][:15]),1))
Metro_Pop = np.mean(np.array(data_v[1:16,1]))

file_model_csv = "Rural_Residential_Population_Ref_Run0.csv"
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
RurPop = np.mean(np.sum(np.array(data_v[1:,1:][:15]),1))

Basin_Pop = UrbPop + RurPop
print "Population = ", Basin_Pop

file_model_csv = "UrbanWaterDemand(_ccf_per_day_)_Ref_Run0.csv"
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
Value_Ref = np.mean(np.sum(np.column_stack((np.array(data_v[1:16,1]),np.array(data_v[1:16,9]))),1))*100*365*cst.cfs_to_m3/cst.Willamette_Basin_area*100.
Value_Ref = Value_Ref*Basin_Pop/Metro_Pop

file_model_csv = file_model_csv.replace("Ref", "HighClim")
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
Value_HC = np.mean(np.sum(np.column_stack((np.array(data_v[1:16,1]),np.array(data_v[1:16,9]))),1))*100*365*cst.cfs_to_m3/cst.Willamette_Basin_area*100.
Value_HC = Value_HC*Basin_Pop/Metro_Pop

file_model_csv = file_model_csv.replace("HighClim", "LowClim")
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
Value_LC = np.mean(np.sum(np.column_stack((np.array(data_v[1:16,1]),np.array(data_v[1:16,9]))),1))*100*365*cst.cfs_to_m3/cst.Willamette_Basin_area*100.
Value_LC = Value_LC*Basin_Pop/Metro_Pop

Value = np.mean(np.array([Value_Ref, Value_HC, Value_LC]))
print "Municipal & domestic water diverted = ", Value," cm"

print "Water use per person = ", Value*cst.Willamette_Basin_area/100*1000/3.785/365.25/Basin_Pop, " gal/day/person"
