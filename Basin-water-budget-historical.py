# -*- coding: utf-8 -*-
"""
Created on Fri Sep 26 12:37:07 2014

@author: haggertr
"""

import numpy as np
import constants as cst   # constants.py contains constants used here
from matrix_from_xls import matrix_from_xls as mfx
from Rectangle import np_rec_calc as nrc

shft = 365 - cst.day_of_year_oct1
summer_start = cst.day_of_year_jun1 + shft
summer_end = cst.day_of_year_sep30 + shft
summer_days = summer_end - summer_start + 1
summer_secs = summer_days*86400
winter_start = 0   # first day of October = 0
winter_end = cst.day_of_year_may31 + shft
winter_days = winter_end - winter_start + 1
winter_secs = winter_days*86400

np.set_printoptions(precision=3)


Col_num = 1
file_model_csv = "Willamette_at_Portland_(m3_s)_Historic_Run0.csv"
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
Value_Ref = np.mean((np.array(data_v[:,Col_num]))[:(cst.days_in_60_yrs-1)])*cst.seconds_in_yr/cst.Willamette_Basin_area_at_PDX*100.
data_v1 = mfx(file_model_csv_w_path, column=Col_num, skip=cst.day_of_year_oct1) # Read csv file into matrix
Value_Ref_Summer = nrc(data_v1,[1, summer_start],[59,summer_end])*summer_secs/cst.Willamette_Basin_area_at_PDX*100.
Value_Ref_Winter = nrc(data_v1,[1, winter_start],[59,winter_end])*winter_secs/cst.Willamette_Basin_area_at_PDX*100.

Value = np.mean(np.array([Value_Ref]))
print "Willamette at Portland (Annual) = ", Value," cm"
print "Willamette at Portland (Summer) = ", Value_Ref_Summer," cm"
print "Willamette at Portland (Winter) = ", Value_Ref_Winter," cm"


Col_num = 2
file_model_csv = "Climate_Historic_Run0.csv"
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
Value_Ref = np.mean((np.array(data_v[:,Col_num]))[:(cst.days_in_60_yrs-1)])*365/10.
data_v1 = mfx(file_model_csv_w_path, column=Col_num, skip=cst.day_of_year_oct1) # Read csv file into matrix
Value_Ref_Summer = nrc(data_v1,[1, summer_start],[59,summer_end])*summer_days/10.
Value_Ref_Winter = nrc(data_v1,[1, winter_start],[59,winter_end])*winter_days/10.

Value = np.mean(np.array([Value_Ref]))
print "Basin-wide avg Precip (Annual) = ", Value," cm"
print "Basin-wide avg Precip (Summer) = ", Value_Ref_Summer," cm"
print "Basin-wide avg Precip (Winter) = ", Value_Ref_Winter," cm"


Col_num = 1
file_model_csv = "Snow_(mm)_Historic_Run0.csv"
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
Value_Ref = np.mean([np.max(np.array(data_v[i*365:(i+1)*365,Col_num])) for i in range(60)])/10. #avg over max of each of 60 yrs
data_v1 = mfx(file_model_csv_w_path, column=Col_num, skip=cst.day_of_year_oct1) # Read csv file into matrix
Value_Ref_Max_Summer = nrc(data_v1,[1, summer_start],[59,summer_end],oper='AverageMaximum')/10.
Value_Ref_Min_Summer = nrc(data_v1,[1, summer_start],[59,summer_end],oper='AverageMinimum')/10.
Value_Ref_Max_Winter = nrc(data_v1,[1, winter_start],[59,winter_end],oper='AverageMaximum')/10.
Value_Ref_Min_Winter = nrc(data_v1,[1, winter_start],[59,winter_end],oper='AverageMinimum')/10.

Value = np.mean(np.array([Value_Ref]))
print "Basin-wide max SWE (Annual) = ", Value," cm"
print "Basin-wide max SWE (Summer) = ", Value_Ref_Max_Summer," cm"
print "Basin-wide min SWE (Summer) = ", Value_Ref_Min_Summer," cm"
print "Basin-wide max SWE (Winter) = ", Value_Ref_Max_Winter," cm"
print "Basin-wide min SWE (Winter) = ", Value_Ref_Min_Winter," cm"

# Calculate storage in soil water content as follows
# Since there is no simulated historical file as of 1/17/2015, use first 15 yrs of Ref, HighClim, LowClim 
# Sum the soil water in the 4 categories of forest soil.  Do the same (further below) for ag
# Take the difference between the max and the min as the storage

Col_num = range(1,5)
file_model_csv = "Forest_Water_Content_Ref_Run0.csv"
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
Value_Ref = np.max([np.array(np.sum([data_v[i*365:(i+1)*365,j] for j in Col_num],0)) for i in range(15)])/10. -\
            np.min([np.array(np.sum([data_v[i*365:(i+1)*365,j] for j in Col_num],0)) for i in range(1,15)])/10. #max of 15 yrs 
            
data_v1 = np.sum([mfx(file_model_csv_w_path, column=j, skip=cst.day_of_year_oct1) for j in Col_num],0)/10. # Read csv file cols into matrices and sum the matrices
Value_Ref_Summer_max = nrc(data_v1,[0, summer_start],[15,summer_end],oper='AverageMax') 
Value_Ref_Summer_min = nrc(data_v1,[0, summer_start],[15,summer_end],oper='AverageMin') 
Value_Ref_Summer_delta = Value_Ref_Summer_max - Value_Ref_Summer_min
Value_Ref_Winter_max = nrc(data_v1,[0, winter_start],[15,winter_end],oper='AverageMax')
Value_Ref_Winter_min = nrc(data_v1,[0, winter_start],[15,winter_end],oper='AverageMin')
Value_Ref_Winter_delta = Value_Ref_Winter_max - Value_Ref_Winter_min

file_model_csv = file_model_csv.replace("Ref", "HighClim")
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
Value_HC = np.max([np.array(np.sum([data_v[i*365:(i+1)*365,j] for j in Col_num],0)) for i in range(15)])/10. -\
           np.min([np.array(np.sum([data_v[i*365:(i+1)*365,j] for j in Col_num],0)) for i in range(1,15)])/10. #max of 15 yrs 

data_v1 = np.sum([mfx(file_model_csv_w_path, column=j, skip=cst.day_of_year_oct1) for j in Col_num],0)/10. # Read csv file cols into matrices and sum the matrices
Value_HC_Summer_max = nrc(data_v1,[0, summer_start],[15,summer_end],oper='AverageMax') 
Value_HC_Summer_min = nrc(data_v1,[0, summer_start],[15,summer_end],oper='AverageMin') 
Value_HC_Summer_delta = Value_HC_Summer_max - Value_HC_Summer_min
Value_HC_Winter_max = nrc(data_v1,[0, winter_start],[15,winter_end],oper='AverageMax')
Value_HC_Winter_min = nrc(data_v1,[0, winter_start],[15,winter_end],oper='AverageMin')
Value_HC_Winter_delta = Value_HC_Winter_max - Value_HC_Winter_min

file_model_csv = file_model_csv.replace("HighClim", "LowClim")
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
Value_LC = np.max([np.array(np.sum([data_v[i*365:(i+1)*365,j] for j in Col_num],0)) for i in range(15)])/10. -\
           np.min([np.array(np.sum([data_v[i*365:(i+1)*365,j] for j in Col_num],0)) for i in range(1,15)])/10. #max of 15 yrs 

data_v1 = np.sum([mfx(file_model_csv_w_path, column=j, skip=cst.day_of_year_oct1) for j in Col_num],0)/10. # Read csv file cols into matrices and sum the matrices
Value_LC_Summer_max = nrc(data_v1,[0, summer_start],[15,summer_end],oper='AverageMax') 
Value_LC_Summer_min = nrc(data_v1,[0, summer_start],[15,summer_end],oper='AverageMin') 
Value_LC_Summer_delta = Value_Ref_Summer_max - Value_Ref_Summer_min
Value_LC_Winter_max = nrc(data_v1,[0, winter_start],[15,winter_end],oper='AverageMax')
Value_LC_Winter_min = nrc(data_v1,[0, winter_start],[15,winter_end],oper='AverageMin')
Value_LC_Winter_delta = Value_Ref_Winter_max - Value_Ref_Winter_min

Value_for = np.mean(np.array([Value_Ref,Value_HC,Value_LC]))*0.727  #Fraction of soil to be treated like forest for calc
Value_for_Summer_max = np.mean(np.array([Value_Ref_Summer_max,Value_HC_Summer_max,Value_LC_Summer_max]))*0.727  #Fraction of soil to be treated like forest for calc
Value_for_Summer_min = np.mean(np.array([Value_Ref_Summer_min,Value_HC_Summer_min,Value_LC_Summer_min]))*0.727  #Fraction of soil to be treated like forest for calc
Value_for_Summer_delta = np.mean(np.array([Value_Ref_Summer_delta,Value_HC_Summer_delta,Value_LC_Summer_delta]))*0.727  #Fraction of soil to be treated like forest for calc
Value_for_Winter_max = np.mean(np.array([Value_Ref_Winter_max,Value_HC_Winter_max, Value_LC_Winter_max]))*0.727  #Fraction of soil to be treated like forest for calc
Value_for_Winter_min = np.mean(np.array([Value_Ref_Winter_min,Value_HC_Winter_min, Value_LC_Winter_min]))*0.727  #Fraction of soil to be treated like forest for calc
Value_for_Winter_delta = np.mean(np.array([Value_Ref_Winter_delta,Value_HC_Winter_delta, Value_LC_Winter_delta]))*0.727  #Fraction of soil to be treated like forest for calc
print "Maximum Basin-wide stored soil water in forest (Annual) = ", Value_for," cm"
print "Basin-wide stored soil water in forest (Summer avg max) = ", Value_for_Summer_max," cm"
print "Basin-wide stored soil water in forest (Summer avg min) = ", Value_for_Summer_min," cm"
print "Basin-wide stored soil water in forest (Summer avg delta) = ", Value_for_Summer_delta," cm"
print "Basin-wide stored soil water in forest (Winter avg max) = ", Value_for_Winter_max," cm"
print "Basin-wide stored soil water in forest (Winter avg min) = ", Value_for_Winter_min," cm"
print "Basin-wide stored soil water in forest (Winter avg delta) = ", Value_for_Winter_delta," cm"

Col_num = range(1,5)
file_model_csv = "Ag_Water_Content_Ref_Run0.csv"
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
Value_Ref = np.max([np.array(np.sum([data_v[i*365:(i+1)*365,j] for j in Col_num],0)) for i in range(15)])/10. -\
            np.min([np.array(np.sum([data_v[i*365:(i+1)*365,j] for j in Col_num],0)) for i in range(1,15)])/10. #max of 15 yrs 
            
data_v1 = np.sum([mfx(file_model_csv_w_path, column=j, skip=cst.day_of_year_oct1) for j in Col_num],0)/10. # Read csv file cols into matrices and sum the matrices
Value_Ref_Summer_max = nrc(data_v1,[0, summer_start],[15,summer_end],oper='AverageMax') 
Value_Ref_Summer_min = nrc(data_v1,[0, summer_start],[15,summer_end],oper='AverageMin') 
Value_Ref_Summer_delta = Value_Ref_Summer_max - Value_Ref_Summer_min
Value_Ref_Winter_max = nrc(data_v1,[0, winter_start],[15,winter_end],oper='AverageMax')
Value_Ref_Winter_min = nrc(data_v1,[0, winter_start],[15,winter_end],oper='AverageMin')
Value_Ref_Winter_delta = Value_Ref_Winter_max - Value_Ref_Winter_min

file_model_csv = file_model_csv.replace("Ref", "HighClim")
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
Value_HC = np.max([np.array(np.sum([data_v[i*365:(i+1)*365,j] for j in Col_num],0)) for i in range(15)])/10. -\
           np.min([np.array(np.sum([data_v[i*365:(i+1)*365,j] for j in Col_num],0)) for i in range(1,15)])/10. #max of 15 yrs 

data_v1 = np.sum([mfx(file_model_csv_w_path, column=j, skip=cst.day_of_year_oct1) for j in Col_num],0)/10. # Read csv file cols into matrices and sum the matrices
Value_HC_Summer_max = nrc(data_v1,[0, summer_start],[15,summer_end],oper='AverageMax') 
Value_HC_Summer_min = nrc(data_v1,[0, summer_start],[15,summer_end],oper='AverageMin') 
Value_HC_Summer_delta = Value_HC_Summer_max - Value_HC_Summer_min
Value_HC_Winter_max = nrc(data_v1,[0, winter_start],[15,winter_end],oper='AverageMax')
Value_HC_Winter_min = nrc(data_v1,[0, winter_start],[15,winter_end],oper='AverageMin')
Value_HC_Winter_delta = Value_HC_Winter_max - Value_HC_Winter_min

file_model_csv = file_model_csv.replace("HighClim", "LowClim")
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
Value_LC = np.max([np.array(np.sum([data_v[i*365:(i+1)*365,j] for j in Col_num],0)) for i in range(15)])/10. -\
           np.min([np.array(np.sum([data_v[i*365:(i+1)*365,j] for j in Col_num],0)) for i in range(1,15)])/10. #max of 15 yrs 

data_v1 = np.sum([mfx(file_model_csv_w_path, column=j, skip=cst.day_of_year_oct1) for j in Col_num],0)/10. # Read csv file cols into matrices and sum the matrices
Value_LC_Summer_max = nrc(data_v1,[0, summer_start],[15,summer_end],oper='AverageMax') 
Value_LC_Summer_min = nrc(data_v1,[0, summer_start],[15,summer_end],oper='AverageMin') 
Value_LC_Summer_delta = Value_Ref_Summer_max - Value_Ref_Summer_min
Value_LC_Winter_max = nrc(data_v1,[0, winter_start],[15,winter_end],oper='AverageMax')
Value_LC_Winter_min = nrc(data_v1,[0, winter_start],[15,winter_end],oper='AverageMin')
Value_LC_Winter_delta = Value_Ref_Winter_max - Value_Ref_Winter_min

Value_ag = np.mean(np.array([Value_Ref,Value_HC,Value_LC]))*0.727  #Fraction of soil to be treated like forest for calc
Value_ag_Summer_max = np.mean(np.array([Value_Ref_Summer_max,Value_HC_Summer_max,Value_LC_Summer_max]))*0.727  #Fraction of soil to be treated like forest for calc
Value_ag_Summer_min = np.mean(np.array([Value_Ref_Summer_min,Value_HC_Summer_min,Value_LC_Summer_min]))*0.727  #Fraction of soil to be treated like forest for calc
Value_ag_Summer_delta = np.mean(np.array([Value_Ref_Summer_delta,Value_HC_Summer_delta,Value_LC_Summer_delta]))*0.727  #Fraction of soil to be treated like forest for calc
Value_ag_Winter_max = np.mean(np.array([Value_Ref_Winter_max,Value_HC_Winter_max, Value_LC_Winter_max]))*0.727  #Fraction of soil to be treated like forest for calc
Value_ag_Winter_min = np.mean(np.array([Value_Ref_Winter_min,Value_HC_Winter_min, Value_LC_Winter_min]))*0.727  #Fraction of soil to be treated like forest for calc
Value_ag_Winter_delta = np.mean(np.array([Value_Ref_Winter_delta,Value_HC_Winter_delta, Value_LC_Winter_delta]))*0.727  #Fraction of soil to be treated like forest for calc
print "Maximum Basin-wide stored soil water in ag (Annual) = ", Value_ag," cm"
print "Basin-wide stored soil water in ag (Summer avg max) = ", Value_ag_Summer_max," cm"
print "Basin-wide stored soil water in ag (Summer avg min) = ", Value_ag_Summer_min," cm"
print "Basin-wide stored soil water in ag (Summer avg delta) = ", Value_ag_Summer_delta," cm"
print "Basin-wide stored soil water in ag (Winter avg max) = ", Value_ag_Winter_max," cm"
print "Basin-wide stored soil water in ag (Winter avg min) = ", Value_ag_Winter_min," cm"
print "Basin-wide stored soil water in ag (Winter avg delta) = ", Value_ag_Winter_delta," cm"

print "Maximum Basin-wide stored soil water whole WB (Annual) = ", Value_ag + Value_for," cm"
print "Basin-wide stored soil water whole WB (Summer avg max) = ", Value_ag_Summer_max + Value_for_Summer_max," cm"
print "Basin-wide stored soil water whole WB (Summer avg min) = ", Value_ag_Summer_min + Value_for_Summer_min," cm"
print "Basin-wide stored soil water whole WB (Summer avg delta) = ", Value_ag_Summer_delta + Value_for_Summer_delta," cm"
print "Basin-wide stored soil water whole WB (Winter avg max) = ", Value_ag_Winter_max + Value_for_Winter_max," cm"
print "Basin-wide stored soil water whole WB (Winter avg min) = ", Value_ag_Winter_min + Value_for_Winter_min," cm"
print "Basin-wide stored soil water whole WB (Winter avg delta) = ", Value_ag_Winter_delta + Value_for_Winter_delta," cm"


Col_num = 1
file_model_csv = "ET_by_Elevation_(mm)_Historic_Run0.csv"
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
Value_Ref = np.mean((np.array(data_v[:,Col_num]))[365:(cst.days_in_60_yrs-1)])*365/10.
data_v1 = mfx(file_model_csv_w_path, column=Col_num, skip=cst.day_of_year_oct1) # Read csv file into matrix
Value_Ref_Summer = nrc(data_v1,[1, summer_start],[59,summer_end])*summer_days/10.
Value_Ref_Winter = nrc(data_v1,[1, winter_start],[59,winter_end])*winter_days/10.

Value = np.mean(np.array([Value_Ref]))
print "Basin-wide avg AET (Annual) = ", Value," cm"
print "Basin-wide avg AET (Summer) = ", Value_Ref_Summer," cm"
print "Basin-wide avg AET (Winter) = ", Value_Ref_Winter," cm"


Col_num = 1
file_model_csv = "ET_by_LandCover_(mm)_Historic_Run0.csv"
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
Value_Ref = np.mean((np.array(data_v[:,Col_num]))[365:(cst.days_in_60_yrs-1)])*365/10.
data_v1 = mfx(file_model_csv_w_path, column=Col_num, skip=cst.day_of_year_oct1) # Read csv file into matrix
Value_Ref_Summer = nrc(data_v1,[1, summer_start],[59,summer_end])*summer_days/10.*0.727
Value_Ref_Winter = nrc(data_v1,[1, winter_start],[59,winter_end])*winter_days/10.*0.727

Value = np.mean(np.array([Value_Ref]))*0.727  #Frac forest area
print "Basin-wide avg Forest AET (Annual) = ", Value," cm"
print "Basin-wide avg Forest AET (Summer) = ", Value_Ref_Summer," cm"
print "Basin-wide avg Forest AET (Winter) = ", Value_Ref_Winter," cm"


Col_num = 3
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
Value_Ref = np.mean((np.array(data_v[:,Col_num]))[365:(cst.days_in_60_yrs-1)])*365/10.
data_v1 = mfx(file_model_csv_w_path, column=Col_num, skip=cst.day_of_year_oct1) # Read csv file into matrix
Value_Ref_Summer = nrc(data_v1,[1, summer_start],[59,summer_end])*summer_days/10.*0.273
Value_Ref_Winter = nrc(data_v1,[1, winter_start],[59,winter_end])*winter_days/10.*0.273

Value = np.mean(np.array([Value_Ref]))*0.273  #Frac ag area
print "Basin-wide avg Ag AET (Annual) = ", Value," cm"
print "Basin-wide avg Ag AET (Summer) = ", Value_Ref_Summer," cm"
print "Basin-wide avg Ag AET (Winter) = ", Value_Ref_Winter," cm"


# http://www.oregon.gov/owrd/docs/1998_04_Willamette_Brochure.pdf
WVP_Vol_summer = (93900+28700+281600+65000+194600+24800+249900+324200+78800+143900+108200)*cst.acft_to_m3/cst.Willamette_Basin_area*100.   #info from web on summer vol
WVP_Vol_full_pool = (116800+32900+455100+77600+355500+60700+281000+45800+89500+219000+125000)*cst.acft_to_m3/cst.Willamette_Basin_area*100. #info from web on full pool
print "Reservoirs Full Pool Storage = ",WVP_Vol_full_pool, " cm"
print "Reservoirs Summer volume = ", WVP_Vol_summer, " cm"

Col_num1 = 3
Col_num2 = 4
file_list = [cst.path_data + 'Blue_River_Reservoir_(USACE)_Reservoir_Historic_Run0.csv',
             cst.path_data + 'Cottage_Grove_Reservoir_(USACE)_Reservoir_Historic_Run0.csv',
             cst.path_data + 'Cougar_Reservoir_(USACE)_Reservoir_Historic_Run0.csv',
             cst.path_data + 'Detroit_Reservoir_(USACE)_Reservoir_Historic_Run0.csv',
             cst.path_data + 'Dorena_Reservoir_(USACE)_Reservoir_Historic_Run0.csv',
             cst.path_data + 'Fall_Creek_Reservoir_(USACE)_Reservoir_Historic_Run0.csv',
             cst.path_data + 'Fern_Ridge_Reservoir_(USACE)_Reservoir_Historic_Run0.csv',
             cst.path_data + 'Foster_Reservoir_(USACE)_Reservoir_Historic_Run0.csv',
             cst.path_data + 'Green_Peter_Reservoir_(USACE)_Reservoir_Historic_Run0.csv',
             cst.path_data + 'Hills_Creek_Reservoir_(USACE)_Reservoir_Historic_Run0.csv',
             cst.path_data + 'Lookout_Point_Reservoir_(USACE)_Reservoir_Historic_Run0.csv']
data_v_in    =  np.zeros_like(data_v1)
data_v_out   = np.zeros_like(data_v1)
data_v_delta = np.zeros_like(data_v1)
data_v_cumsum = np.zeros_like(data_v1)
for file_name in file_list:
    data_tmp = mfx(file_name, column=Col_num1, skip=cst.day_of_year_oct1)
    data_v_in  =   np.add(data_v_in, data_tmp)
    data_tmp = mfx(file_name, column=Col_num2, skip=cst.day_of_year_oct1)
    data_v_out =   np.add(data_v_out, data_tmp)
data_v_delta = np.subtract(data_v_in,data_v_out)
data_v_cumsum = np.cumsum(data_v_delta*86400,axis=1)
Value_Ref_Summer_in = nrc(data_v_in,[1, summer_start],[59,summer_end])*summer_days*86400./cst.Willamette_Basin_area*100.
Value_Ref_Winter_in = nrc(data_v_in,[1, winter_start],[59,winter_end])*winter_days*86400./cst.Willamette_Basin_area*100.
Value_Ref_Summer_out = nrc(data_v_out,[1, summer_start],[59,summer_end])*summer_days*86400./cst.Willamette_Basin_area*100.
Value_Ref_Winter_out = nrc(data_v_out,[1, winter_start],[59,winter_end])*winter_days*86400./cst.Willamette_Basin_area*100.
Value_Ref_Summer_delta = nrc(data_v_delta, [1, summer_start],[59,summer_end])*summer_days*86400./cst.Willamette_Basin_area*100.
Value_Ref_Winter_delta = nrc(data_v_delta, [1, winter_start],[59,winter_end])*winter_days*86400./cst.Willamette_Basin_area*100.
Value_Ref_Summer_min =   nrc(data_v_cumsum,[1, summer_start],[59,summer_end],oper='AverageMin')/cst.Willamette_Basin_area*100.
Value_Ref_Summer_max =   nrc(data_v_cumsum,[1, summer_start],[59,summer_end],oper='AverageMax')/cst.Willamette_Basin_area*100.
Value_Ref_Winter_min =   nrc(data_v_cumsum,[1, winter_start],[59,winter_end],oper='AverageMin')/cst.Willamette_Basin_area*100.
Value_Ref_Winter_max =   nrc(data_v_cumsum,[1, winter_start],[59,winter_end],oper='AverageMax')/cst.Willamette_Basin_area*100.
print "All reservoirs summer input = ", Value_Ref_Summer_in," cm"
print "All reservoirs winter input = ", Value_Ref_Winter_in," cm"
print "All reservoirs annual input = ", Value_Ref_Winter_in+Value_Ref_Summer_in," cm"
print "All reservoirs summer output = ", Value_Ref_Summer_out," cm"
print "All reservoirs winter output = ", Value_Ref_Winter_out," cm"
print "All reservoirs annual output = ", Value_Ref_Winter_out+Value_Ref_Summer_out," cm"
print "All reservoirs summer delta = ", Value_Ref_Summer_delta," cm"
print "All reservoirs winter delta = ", Value_Ref_Winter_delta," cm"
print "All reservoirs annual delta = ", Value_Ref_Winter_delta + Value_Ref_Summer_delta," cm"
print "All reservoirs summer min = ", Value_Ref_Summer_min," cm"
print "All reservoirs summer max = ", Value_Ref_Summer_max," cm"
print "All reservoirs winter min = ", Value_Ref_Winter_min," cm"
print "All reservoirs winter max = ", Value_Ref_Winter_max," cm"


Col_num = 1
file_model_csv = "Daily_WaterMaster_Metrics_Historic_Run0.csv"
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
Value_Ref = np.mean((np.array(data_v[:,Col_num]))[:(cst.days_in_60_yrs-1)])*cst.seconds_in_yr/cst.Willamette_Basin_area_at_PDX*100.
data_v1 = mfx(file_model_csv_w_path, column=Col_num, skip=cst.day_of_year_oct1) # Read csv file into matrix
Value_Ref_Summer = nrc(data_v1,[1, summer_start],[59,summer_end])*summer_secs/cst.Willamette_Basin_area_at_PDX*100.
Value_Ref_Winter = nrc(data_v1,[1, winter_start],[59,winter_end])*winter_secs/cst.Willamette_Basin_area_at_PDX*100.

Value = np.mean(np.array([Value_Ref]))
print "Instream regulatory use (Annual) = ", Value," cm"
print "Instream regulatory use (Summer) = ", Value_Ref_Summer," cm"
print "Instream regulatory use (Winter) = ", Value_Ref_Winter," cm"


Col_num = [2,3]
file_model_csv = "Daily_WaterMaster_Metrics_Historic_Run0.csv"
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
Value_Ref = (np.mean((np.array(data_v[:,Col_num[0]]))[:(cst.days_in_60_yrs-1)]) +\
             np.mean((np.array(data_v[:,Col_num[1]]))[:(cst.days_in_60_yrs-1)]))*cst.seconds_in_yr/cst.Willamette_Basin_area*100.
data_v1 = np.sum([mfx(file_model_csv_w_path, column=j, skip=cst.day_of_year_oct1) for j in Col_num],0)  # Read csv file cols into matrices and sum the matrices
Value_Ref_Summer = nrc(data_v1,[1, summer_start],[59,summer_end])*summer_secs/cst.Willamette_Basin_area*100.
Value_Ref_Winter = nrc(data_v1,[1, winter_start],[59,winter_end])*winter_secs/cst.Willamette_Basin_area*100.

Value = np.mean(np.array([Value_Ref]))
print "Irrigation water diverted (Annual) = ", Value," cm"
print "Irrigation water diverted (Summer) = ", Value_Ref_Summer," cm"
print "Irrigation water diverted (Winter) = ", Value_Ref_Winter," cm"

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

file_model_csv = "UrbanWaterDemand(_ccf_per_day_)_Ref_Run0.csv"
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
Value_Ref = np.mean(np.sum(np.column_stack((np.array(data_v[1:16,1]),np.array(data_v[1:16,9]))),1))*100*365*cst.cfs_to_m3/cst.Willamette_Basin_area*100.
Value_Ref = Value_Ref*Basin_Pop/Metro_Pop

Col_num = range(1,9)
file_model_csv = "Daily_Urban_Water_Demand_Summary_Historic_Run0.csv"
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v1 = np.sum([mfx(file_model_csv_w_path, column=j, skip=cst.day_of_year_oct1) for j in Col_num],0)  # Read csv file cols into matrices and sum the matrices
Value_Ref_Summer = nrc(data_v1,[1, summer_start],[59,summer_end])*100*summer_days*cst.cfs_to_m3/cst.Willamette_Basin_area*100.*1.11386
Value_Ref_Winter = nrc(data_v1,[1, winter_start],[59,winter_end])*100*winter_days*cst.cfs_to_m3/cst.Willamette_Basin_area*100.*1.11386

Value = np.mean(np.array([Value_Ref]))
print "Municipal & domestic water diverted (Annual) = ", Value," cm"
print "Municipal & domestic water diverted (Summer) = ", Value_Ref_Summer," cm"
print "Municipal & domestic water diverted (Winter) = ", Value_Ref_Winter," cm"

print "Water use per person = ", Value*cst.Willamette_Basin_area/100*1000/3.785/365/Basin_Pop, " gal/day/person"

import EF_rules as efr
EFrules = efr.get_EFrules()
keys = ['Salem']
EF_rules_list = [EFrules[key] for key in keys]
EF_rules_list = sorted(EF_rules_list, key=lambda x: x[0])  # order list by number
EF_rules_list = [EF_rules_list[i][1] for i in range(1)]
EF_rules = EF_rules_list[0]
num_rules = len(EF_rules)
vol = 0.
for i in range(num_rules):
    num_days = EF_rules[i][2] - EF_rules[i][1]
    minQ = EF_rules[i][3]
    if EF_rules[i][0] == 'minQ': vol += num_days*86400.*minQ
specific_minQ = vol/cst.Willamette_Basin_area
print 'Minimum flows at Salem (Annual) = ', specific_minQ*100.,' cm'

Winter_rules =[0,1,4,5,12]
Summer_rules =[2,3,6,7,8,9,10,11]
vol = 0.
for i in Summer_rules:
    num_days = EF_rules[i][2] - EF_rules[i][1]
    minQ = EF_rules[i][3]
    if EF_rules[i][0] == 'minQ': vol += num_days*86400.*minQ
specific_minQ = vol/cst.Willamette_Basin_area
print 'Minimum flows at Salem (Summer) = ', specific_minQ*100.,' cm'
vol = 0.
for i in Winter_rules:
    num_days = EF_rules[i][2] - EF_rules[i][1]
    minQ = EF_rules[i][3]
    if EF_rules[i][0] == 'minQ': vol += num_days*86400.*minQ
specific_minQ = vol/cst.Willamette_Basin_area
print 'Minimum flows at Salem (Winter) = ', specific_minQ*100.,' cm'
