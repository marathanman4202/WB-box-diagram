# Roy Haggerty
# Sep 2014 - Feb 2015
# Code to automatically calculate Willamette Basin water budget from
#   Envision output

import numpy as np
import constants as cst   # constants.py contains constants used here
from matrix_from_xls import matrix_from_xls as mfx
from Rectangle import np_rec_calc as nrc
from overlap import overlap

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

era = 'future'
period = 'seasons'

if era == 'future':
    scenario = 'HighClim'
    # scenario = 'Ref'
    postscript = scenario + '_2070-2100' + '_' + period
elif era == 'past':
    scenario = 'Historical'
    postscript = scenario + '1950-2010' + '_' + period

table = []

if period == 'months':
    num_periods = 12
    period_name = ['Oct','Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May',
                   'Jun', 'Jul', 'Aug', 'Sep']
    period_start = [cst.day_of_year_oct1 + shft - 365, cst.day_of_year_nov1 + shft - 365,
                    cst.day_of_year_dec1 + shft - 365, cst.day_of_year_jan1 + shft,
                    cst.day_of_year_feb1 + shft, cst.day_of_year_mar1 + shft,
                    cst.day_of_year_apr1 + shft, cst.day_of_year_may1 + shft,
                    cst.day_of_year_jun1 + shft, cst.day_of_year_jul1 + shft,
                    cst.day_of_year_aug1 + shft, cst.day_of_year_sep1 + shft]  
    period_end =   [cst.day_of_year_oct31 + shft - 365, cst.day_of_year_nov30 + shft - 365,
                    cst.day_of_year_dec31 + shft - 365, cst.day_of_year_jan31 + shft,
                    cst.day_of_year_feb28 + shft, cst.day_of_year_mar31 + shft,
                    cst.day_of_year_apr30 + shft, cst.day_of_year_may31 + shft,
                    cst.day_of_year_jun30 + shft, cst.day_of_year_jul31 + shft,
                    cst.day_of_year_aug31 + shft, cst.day_of_year_sep30 + shft]
    period_days = [period_end[i] - period_start[i] + 1 for i in range(num_periods)]
    period_secs = [period_days[i]*86400 for i in range(num_periods)]
elif period == 'seasons':  # [0] is summer; [1] is winter
    num_periods = 2
    period_name = ['Summer','Winter']
    period_start = [cst.day_of_year_jun1 + shft, 0]  
    period_end =   [cst.day_of_year_sep30 + shft, cst.day_of_year_may31 + shft]
    period_days = [period_end[i] - period_start[i] + 1 for i in range(num_periods)]
    period_secs = [period_days[i]*86400 for i in range(num_periods)]
    
header = []
row = ['Order', 'Flux','Annual (cm)']
row.extend([period_name[i] + ' (cm)' for i in range(num_periods)])
header.append(row)

Col_num = 1
file_model_csv = "Willamette_at_Portland_(m3_s)_" + scenario + "_Run0.csv"
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
Value_Ref = np.mean((np.array(data_v[:,Col_num]))[:(cst.days_in_30_yrs-1)])*cst.seconds_in_yr/cst.Willamette_Basin_area_at_PDX*100.
data_v1 = mfx(file_model_csv_w_path, column=Col_num, skip=cst.day_of_year_oct1) # Read csv file into matrix
Value_Ref = [nrc(data_v1,[59, period_start[i]],[89,period_end[i]])*period_secs[i]/cst.Willamette_Basin_area_at_PDX*100. for i in range(num_periods)]

Value = nrc(data_v1,[59, 1],[89,365])*cst.seconds_in_yr/cst.Willamette_Basin_area_at_PDX*100.
print "Willamette at Portland (Annual) = ", Value," cm"
for i in range(num_periods):
    print "Willamette at Portland (", period_name[i], ") = ", Value_Ref[i]," cm"

row = [100, 'Willamette at Portland']
row.append(Value)
row.extend([Value_Ref[i] for i in range(num_periods)])
table.append(row)

Col_num = 2
file_model_csv = "Climate_" + scenario + "_Run0.csv"
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
Value_Ref = np.mean((np.array(data_v[:,Col_num]))[:(cst.days_in_30_yrs-1)])*365/10.
data_v1 = mfx(file_model_csv_w_path, column=Col_num, skip=cst.day_of_year_oct1) # Read csv file into matrix
Value_Ref = [nrc(data_v1,[59, period_start[i]],[89,period_end[i]])*period_days[i]/10. for i in range(num_periods)]

Value = nrc(data_v1,[59, 1],[89,365])*365./10.
print "Basin-wide avg Precip (Annual) = ", Value," cm"
for i in range(num_periods):
    print "Basin-wide avg Precip (", period_name[i], ") = ", Value_Ref[i]," cm"
row = [1, 'Basin-wide avg Precip']
row.append(Value)
row.extend([Value_Ref[i] for i in range(num_periods)])
table.append(row)

Col_num = 1
file_model_csv = "Snow_(mm)_" + scenario + "_Run0.csv"
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
Value_Ref = np.mean([np.max(np.array(data_v[i*365:(i+1)*365,Col_num])) for i in range(59,90)])/10. #avg over max of each of 30 yrs
data_v1 = mfx(file_model_csv_w_path, column=Col_num, skip=cst.day_of_year_oct1) # Read csv file into matrix
Value_Ref_Max = [nrc(data_v1,[59, period_start[i]],[89,period_end[i]],oper='AverageMaximum')/10. for i in range(num_periods)]
Value_Ref_Min = [nrc(data_v1,[59, period_start[i]],[89,period_end[i]],oper='AverageMinimum')/10. for i in range(num_periods)]

#Value = np.mean(np.array([Value_Ref]))
Value = nrc(data_v1,[59, 1],[89,365],'AverageMaximum')/10.
print "Basin-wide max SWE (Annual) = ", Value," cm"
for i in range(num_periods):
    print "Basin-wide max SWE (", period_name[i], ") = ", Value_Ref_Max[i]," cm"
    print "Basin-wide min SWE (", period_name[i], ") = ", Value_Ref_Min[i]," cm"
row = [2, 'Basin-wide Max SWE']
row.append(Value)
row.extend([Value_Ref_Max[i] for i in range(num_periods)])
table.append(row)
row = [3, 'Basin-wide Min SWE']
row.append(0.)
row.extend([Value_Ref_Min[i] for i in range(num_periods)])
table.append(row)

# Calculate storage in soil water content as follows
# Sum the soil water in the 4 categories of forest soil.  Do the same (further below) for ag
# Take the difference between the max and the min as the storage

Col_num = range(1,5)
fraction_of_landscape = [0.727, 0.273]
sum_Value = 0.
sum_Value_max =   [0.]*num_periods
sum_Value_min =   [0.]*num_periods
sum_Value_delta = [0.]*num_periods

i_place = -1

for place in ['Forest','Ag']:
    i_place += 1  # counter for Forest, Ag
    file_model_csv = place + "_Water_Content_" + scenario + "_Run0.csv"
    file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
    data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
    Value_Ref = np.max([np.array(np.sum([data_v[i*365:(i+1)*365,j] for j in Col_num],0)) for i in range(59,90)])/10. -\
                np.min([np.array(np.sum([data_v[i*365:(i+1)*365,j] for j in Col_num],0)) for i in range(59,90)])/10. #max of 30 yrs 
          
    data_v1 = np.sum([mfx(file_model_csv_w_path, column=j, skip=cst.day_of_year_oct1) for j in Col_num],0)/10. # Read csv file cols into matrices and sum the matrices
    Value_Ref_max = [nrc(data_v1,[59, period_start[i]],[89,period_end[i]],oper='AverageMax') for i in range(num_periods)]
    Value_Ref_min = [nrc(data_v1,[59, period_start[i]],[89,period_end[i]],oper='AverageMin') for i in range(num_periods)]
    Value_Ref_delta = [Value_Ref_max[i] - Value_Ref_min[i] for i in range(num_periods)]
    
    file_model_csv = file_model_csv.replace(scenario, "HighClim")
    file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
    data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
    Value_HC = np.max([np.array(np.sum([data_v[i*365:(i+1)*365,j] for j in Col_num],0)) for i in range(59,90)])/10. -\
               np.min([np.array(np.sum([data_v[i*365:(i+1)*365,j] for j in Col_num],0)) for i in range(59,90)])/10. #max of 30 yrs 
    
    data_v1 = np.sum([mfx(file_model_csv_w_path, column=j, skip=cst.day_of_year_oct1) for j in Col_num],0)/10. # Read csv file cols into matrices and sum the matrices
    Value_HC_max = [nrc(data_v1,[59, period_start[i]],[89,period_end[i]],oper='AverageMax') for i in range(num_periods)]
    Value_HC_min = [nrc(data_v1,[59, period_start[i]],[89,period_end[i]],oper='AverageMin') for i in range(num_periods)]
    Value_HC_delta = [Value_Ref_max[i] - Value_Ref_min[i] for i in range(num_periods)]
    
    file_model_csv = file_model_csv.replace("HighClim", "LowClim")
    file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
    data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
    Value_LC = np.max([np.array(np.sum([data_v[i*365:(i+1)*365,j] for j in Col_num],0)) for i in range(59,90)])/10. -\
               np.min([np.array(np.sum([data_v[i*365:(i+1)*365,j] for j in Col_num],0)) for i in range(59,90)])/10. #max of 30 yrs 
    
    data_v1 = np.sum([mfx(file_model_csv_w_path, column=j, skip=cst.day_of_year_oct1) for j in Col_num],0)/10. # Read csv file cols into matrices and sum the matrices
    Value_LC_max = [nrc(data_v1,[59, period_start[i]],[89,period_end[i]],oper='AverageMax') for i in range(num_periods)]
    Value_LC_min = [nrc(data_v1,[59, period_start[i]],[89,period_end[i]],oper='AverageMin') for i in range(num_periods)]
    Value_LC_delta = [Value_Ref_max[i] - Value_Ref_min[i] for i in range(num_periods)]
    
    Value = np.mean(np.array([Value_Ref]))*fraction_of_landscape[i_place] #Fraction of soil to be treated like forest for calc
    Value_max = [np.mean(np.array([Value_Ref_max[i]]))*fraction_of_landscape[i_place] for i in range(num_periods)] #Fraction of soil to be treated like forest for calc
    Value_min = [np.mean(np.array([Value_Ref_min[i]]))*fraction_of_landscape[i_place] for i in range(num_periods)] #Fraction of soil to be treated like forest for calc
    Value_delta = [np.mean(np.array([Value_Ref_delta[i]]))*fraction_of_landscape[i_place] for i in range(num_periods)] #Fraction of soil to be treated like forest for calc

    sum_Value += Value
    sum_Value_max =   [sum_Value_max[i] +   Value_max[i]   for i in range(num_periods)]
    sum_Value_min =   [sum_Value_min[i] +   Value_min[i]   for i in range(num_periods)]
    sum_Value_delta = [sum_Value_delta[i] + Value_delta[i] for i in range(num_periods)]
    print "Maximum Basin-wide stored soil water in", place, "(Annual) = ", Value," cm"
    for i in range(num_periods):
        print "Basin-wide stored soil water in", place, "(", period_name[i], "avg max) = ", Value_max[i]," cm"
        print "Basin-wide stored soil water in", place, "(", period_name[i], "avg min) = ", Value_min[i]," cm"
        print "Basin-wide stored soil water in", place, "(", period_name[i], "avg delta) = ", Value_delta[i]," cm"

print "Maximum Basin-wide stored soil water whole WB (Annual) = ", sum_Value, " cm"
for i in range(num_periods):
    print "Basin-wide stored soil water whole WB (", period_name[i], " avg max) = ", sum_Value_max[i]," cm"
    print "Basin-wide stored soil water whole WB (", period_name[i], " avg min) = ", sum_Value_min[i]," cm"
    print "Basin-wide stored soil water whole WB (", period_name[i], " avg delta) = ", sum_Value_delta[i]," cm"
row = [4, 'Basin-wide Max soil water']
row.append(sum_Value)
row.extend([Value_Ref_max[i] for i in range(num_periods)])
table.append(row)
row = [5, 'Basin-wide Min soil water']
row.append(' ')
row.extend([Value_Ref_min[i] for i in range(num_periods)])
table.append(row)
row = [6, 'Basin-wide Delta soil water']
row.append(' ')
row.extend([Value_Ref_delta[i] for i in range(num_periods)])
table.append(row)


Col_num = 1
file_model_csv = "ET_by_Elevation_(mm)_" + scenario + "_Run0.csv"
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v1 = mfx(file_model_csv_w_path, column=Col_num, skip=cst.day_of_year_oct1) # Read csv file into matrix
Value_Ref = [nrc(data_v1,[59, period_start[i]],[89,period_end[i]])*period_days[i]/10. for i in range(num_periods)]

Value = nrc(data_v1,[59, 1],[89,365])*365./10.
print "Basin-wide avg AET (Annual) = ", Value," cm"
for i in range(num_periods):
    print "Basin-wide avg AET (", period_name[i], ") = ", Value_Ref[i]," cm"
row = [7, 'Basin-wide AET']
row.append(Value)
row.extend([Value_Ref[i] for i in range(num_periods)])
table.append(row)

Col_num = [1,3]
file_model_csv = "ET_by_LandCover_(mm)_" + scenario + "_Run0.csv"
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
i_place = -1
for place in ['Forest','Ag']:
    i_place += 1
    data_v1 = mfx(file_model_csv_w_path, column=Col_num[i_place], skip=cst.day_of_year_oct1) # Read csv file into matrix
    Value_Ref = [nrc(data_v1,[59, period_start[i]],[89,period_end[i]])*period_days[i]/10.*fraction_of_landscape[i_place] for i in range(num_periods)]

    Value = nrc(data_v1,[59, 1],[89,365])*365./10.*fraction_of_landscape[i_place]
    print "Basin-wide avg", place, "AET (Annual) = ", Value," cm"
    for i in range(num_periods):
        print "Basin-wide avg", place, "AET (", period_name[i], ") = ", Value_Ref[i]," cm"

# http://www.oregon.gov/owrd/docs/1998_04_Willamette_Brochure.pdf
WVP_Vol_summer = (93900+28700+281600+65000+194600+24800+249900+324200+78800+143900+108200)*cst.acft_to_m3/cst.Willamette_Basin_area*100.   #info from web on summer vol
WVP_Vol_full_pool = (116800+32900+455100+77600+355500+60700+281000+45800+89500+219000+125000)*cst.acft_to_m3/cst.Willamette_Basin_area*100. #info from web on full pool
print "Values from reservoir sizes: "
print "Reservoirs Full Pool Storage = ",WVP_Vol_full_pool, " cm"
print "Reservoirs Summer volume = ", WVP_Vol_summer, " cm"

Col_num1 = 3
Col_num2 = 4
file_list = [cst.path_data + 'Blue_River_Reservoir_(USACE)_Reservoir_' + scenario + '_Run0.csv',
             cst.path_data + 'Cottage_Grove_Reservoir_(USACE)_Reservoir_' + scenario + '_Run0.csv',
             cst.path_data + 'Cougar_Reservoir_(USACE)_Reservoir_' + scenario + '_Run0.csv',
             cst.path_data + 'Detroit_Reservoir_(USACE)_Reservoir_' + scenario + '_Run0.csv',
             cst.path_data + 'Dorena_Reservoir_(USACE)_Reservoir_' + scenario + '_Run0.csv',
             cst.path_data + 'Fall_Creek_Reservoir_(USACE)_Reservoir_' + scenario + '_Run0.csv',
             cst.path_data + 'Fern_Ridge_Reservoir_(USACE)_Reservoir_' + scenario + '_Run0.csv',
             cst.path_data + 'Foster_Reservoir_(USACE)_Reservoir_' + scenario + '_Run0.csv',
             cst.path_data + 'Green_Peter_Reservoir_(USACE)_Reservoir_' + scenario + '_Run0.csv',
             cst.path_data + 'Hills_Creek_Reservoir_(USACE)_Reservoir_' + scenario + '_Run0.csv',
             cst.path_data + 'Lookout_Point_Reservoir_(USACE)_Reservoir_' + scenario + '_Run0.csv']
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
#Value_Ref =      [nrc(data_v1,[59, period_start[i]],[89,period_end[i]])*period_days[i]/10. for i in range(num_periods)]
Value_Ref_in    = [nrc(data_v_in,[59, period_start[i]],[89,period_end[i]])*period_days[i]*86400./cst.Willamette_Basin_area*100. for i in range(num_periods)]
Value_Ref_out   = [nrc(data_v_out,[59, period_start[i]],[89,period_end[i]])*period_days[i]*86400./cst.Willamette_Basin_area*100. for i in range(num_periods)]
Value_Ref_delta = [nrc(data_v_delta, [59, period_start[i]],[89,period_end[i]])*period_days[i]*86400./cst.Willamette_Basin_area*100. for i in range(num_periods)]
Value_Ref_min   = [nrc(data_v_cumsum,[59, period_start[i]],[89,period_end[i]],oper='AverageMin')/cst.Willamette_Basin_area*100. for i in range(num_periods)]
Value_Ref_max   = [nrc(data_v_cumsum,[59, period_start[i]],[89,period_end[i]],oper='AverageMax')/cst.Willamette_Basin_area*100. for i in range(num_periods)]
Value_Ref_maxmin= [Value_Ref_max[i] - Value_Ref_min[i] for i in range(num_periods)]
print "Values from Envision calcs: "
print "All reservoirs annual input = ",  sum(Value_Ref_in),   " cm"
print "All reservoirs annual output = ", sum(Value_Ref_out),  " cm"
print "All reservoirs annual sum of deltas = ",  sum(Value_Ref_delta)," cm"
for i in range(num_periods):
    print "All reservoirs", period_name[i], "input = ",  Value_Ref_in[i],   " cm"
    print "All reservoirs", period_name[i], "output = ", Value_Ref_out[i],  " cm"
    print "All reservoirs", period_name[i], "delta = ",  Value_Ref_delta[i]," cm"
    print "All reservoirs", period_name[i], "min = ",    Value_Ref_min[i],  " cm"
    print "All reservoirs", period_name[i], "max = ",    Value_Ref_max[i],  " cm"
    print "All reservoirs", period_name[i], "max-min",   Value_Ref_maxmin[i], "cm"
row = [3.5, 'All reservoirs delta']
row.append(sum(Value_Ref_delta))
row.extend([Value_Ref_delta[i] for i in range(num_periods)])
table.append(row)
row = [3.7, 'All reservoirs max - min']
row.append(sum(Value_Ref_delta))
row.extend([Value_Ref_maxmin[i] for i in range(num_periods)])
table.append(row)

Col_num = 1
file_model_csv = "Daily_WaterMaster_Metrics_" + scenario + "_Run0.csv"
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
data_v1 = mfx(file_model_csv_w_path, column=Col_num, skip=cst.day_of_year_oct1) # Read csv file into matrix
Value_Ref = [nrc(data_v1,[59, period_start[i]],[89,period_end[i]])*period_secs[i]/cst.Willamette_Basin_area_at_PDX*100. for i in range(num_periods)]

Value = nrc(data_v1,[59, 1],[89,365])*cst.seconds_in_yr/cst.Willamette_Basin_area_at_PDX*100.
print "Instream regulatory use (Annual) = ", Value," cm"
for i in range(num_periods):
    print "Instream regulatory use (", period_name[i], ") = ", Value_Ref[i]," cm"
 
Col_num = [2,3]
data_v1 = np.sum([mfx(file_model_csv_w_path, column=j, skip=cst.day_of_year_oct1) for j in Col_num],0)  # Read csv file cols into matrices and sum the matrices
Value_Ref = [nrc(data_v1,[59, period_start[i]],[89,period_end[i]])*period_secs[i]/cst.Willamette_Basin_area*100. for i in range(num_periods)]

Value = nrc(data_v1,[59, 1],[89,365])*cst.seconds_in_yr/cst.Willamette_Basin_area*100.
print "Irrigation water diverted (Annual) = ", Value," cm"
for i in range(num_periods):
    print "Irrigation water diverted (", period_name[i], ") = ", Value_Ref[i]," cm"
row = [9, 'Irrigation']
row.append(Value)
row.extend([Value_Ref[i] for i in range(num_periods)])
table.append(row)

file_model_csv = "Urban_Population_" + scenario + "_Run0.csv"
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
UrbPop = np.mean(np.sum(np.array(data_v[1:,1:][59:90]),1))
Metro_Pop = np.mean(np.array(data_v[59:90,1]))

file_model_csv = "Rural_Residential_Population_" + scenario + "_Run0.csv"
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
RurPop = np.mean(np.sum(np.array(data_v[1:,1:][59:90]),1))

Basin_Pop = UrbPop + RurPop
print "Population = ", Basin_Pop

file_model_csv = "UrbanWaterDemand(_ccf_per_day_)_" + scenario + "_Run0.csv"
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
Value_Ref = np.mean(np.sum(np.column_stack((np.array(data_v[59:90,1]),np.array(data_v[59:90,9]))),1))*100*365*cst.cfs_to_m3 # in m3
Value_Ref = Value_Ref*Basin_Pop/Metro_Pop
Value = np.mean(np.array([Value_Ref]))
print "Water use per person = ", Value*1000/3.785/365/Basin_Pop, " gal/day/person"

Col_num = range(1,9)
file_model_csv = "Daily_Urban_Water_Demand_Summary_" + scenario + "_Run0.csv"
file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
data_v1 = np.sum([mfx(file_model_csv_w_path, column=j, skip=cst.day_of_year_oct1) for j in Col_num],0)  # Read csv file cols into matrices and sum the matrices
Value_Ref = [nrc(data_v1,[59, period_start[i]],[89,period_end[i]])*100*period_days[i]*cst.cfs_to_m3/cst.Willamette_Basin_area*100.*1.11386 for i in range(num_periods)]

print "Municipal & domestic water diverted (Annual) = ", Value*100/cst.Willamette_Basin_area," cm"
for i in range(num_periods):
    print "Municipal & domestic water diverted (", period_name[i], ") = ", Value_Ref[i]," cm"
row = [10, 'Municipal & domestic']
row.append(Value*100/cst.Willamette_Basin_area)
row.extend([Value_Ref[i] for i in range(num_periods)])
table.append(row)

import EF_rules as efr
EFrules = efr.get_EFrules()
keys = ['Salem']
EF_rules_list = [EFrules[key] for key in keys]
EF_rules_list = sorted(EF_rules_list, key=lambda x: x[0])  # order list by number
EF_rules_list = [EF_rules_list[i][1] for i in range(1)]
EF_rules = EF_rules_list[0]
num_rules = len(EF_rules)
rules = range(num_rules)
vol = 0.
for i in rules:
    num_days = EF_rules[i][2] - EF_rules[i][1]
    minQ = EF_rules[i][3]
    if EF_rules[i][0] == 'minQ': vol += num_days*86400.*minQ
specific_minQ = vol/cst.Willamette_Basin_area
print 'Minimum flows at Salem (Annual) = ', specific_minQ*100.,' cm'

i_period = -1
minflows = []
for period in period_name:
    i_period += 1
    vol = 0.    
    for i in rules:
        num_days = overlap(EF_rules[i][1], EF_rules[i][2], period_start[i_period], period_end[i_period]) # overlapping days between rule and period
        minQ = EF_rules[i][3]
        if EF_rules[i][0] == 'minQ': vol += num_days*86400.*minQ
    specific_minQ = vol/cst.Willamette_Basin_area
    minflows.append(specific_minQ)
    print "Minimum flows at Salem (", period_name[i_period], ") = ", specific_minQ*100.," cm"
    vol = 0.
row = [11, 'Minimum flows at Salem']
row.append(specific_minQ*100)
row.extend([minflows[i] for i in range(num_periods)])
table.append(row)

table.sort(key=lambda x: x[0])

import csv

with open("Willamette_water_budget_" + postscript + ".csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(header)
    writer.writerows(table)
