# Roy Haggerty
# Sep 2014 - Jul 2015
# Help from Owen Haggerty Mar 2015
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

save_results_to_csv_file_named = 'Willamette_water_budget_test'

#******************************************************************************
#  ****** Choose period to aggregate  *******    
#  Currently works with months or seasons
#  shifting is needed because we want Oct 1 start for water year
period = 'months'
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
        

#******************************************************************************
#  ****** Set up the simulations that are to be read & processed  *******    

#  ****** Choose which simulations to read  *******    
ensemble = [0,1,2,3]  # Each simulation corresponds to a number here
table_save = len(ensemble)*[None]  # set up a table of the right size to save to

simulation_num = -1
for simulation in ensemble:
    simulation_num += 1
    if simulation == 0:
        era = 'past'
        scenario = 'HistoricRef'
        title = 'Simulated Historical (1950 - 2010) Reference scenario'
    elif simulation == 1:
        era = 'future'
        scenario = 'Ref'
        title = '2070 - 2100 Reference scenario'
    elif simulation == 2:
        era = 'future'
        scenario = 'HighClim'
        title = '2070 - 2100 HighClim scenario'
    elif simulation == 3:
        era = 'future'
        scenario = 'Extreme'
        title = '2070 - 2100 Extreme scenario'
    else:
        print 'no simulation chosen that is yet coded'
        assert False      
    
    if era == 'future':
        postscript = scenario + '_2070-2100' + '_' + period
        total_days_in_calculation = cst.days_in_30_yrs
        data_yr_start = 59
        data_yr_end = 89
    elif era == 'past':
        postscript = scenario + '1950-2010' + '_' + period
        total_days_in_calculation = cst.days_in_60_yrs
        data_yr_start = 0
        data_yr_end = 59
           
    table = []
    
    header = []
    row = ['Order', 'Month','Ann']   # Order is only used to re-order rows for output.  Numbers in Order are relative to each other only. 
    row.extend([period_name[i] for i in range(num_periods)])
    row_1 = ["","Scenario",]
    for i in range(num_periods+1):
        row_1.append(title)
    header.append(row)

#  ****** Willamette River Outflow *******    
    Col_num = 1
    file_model_csv = "Willamette_at_Portland_(m3_s)_" + scenario + "_Run0.csv"
    file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
    data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
    Value_Ref = np.mean((np.array(data_v[:,Col_num]))[:(total_days_in_calculation-1)])*cst.seconds_in_yr/cst.Willamette_Basin_area_at_PDX*100.
    data_v1 = mfx(file_model_csv_w_path, column=Col_num, skip=cst.day_of_year_oct1) # Read csv file into matrix
    Value_Ref = [nrc(data_v1,[data_yr_start, period_start[i]],[data_yr_end,period_end[i]])*period_secs[i]/cst.Willamette_Basin_area_at_PDX*100. for i in range(num_periods)]
    
    Value = nrc(data_v1,[data_yr_start, 1],[data_yr_end,365])*cst.seconds_in_yr/cst.Willamette_Basin_area_at_PDX*100.
    print "Willamette at Portland (Annual) = ", Value," cm"
    for i in range(num_periods):
        print "Willamette at Portland (", period_name[i], ") = ", Value_Ref[i]," cm"
    
    row = [100, 'Outflow Willamette']  # Number is Order, which is only used to re-order rows for output.  Numbers in Order are relative to each other only.
    row.append(Value)
    row.extend([Value_Ref[i] for i in range(num_periods)])
    table.append(row)
    Willamette_Outflow = Value_Ref
    
#  ****** Precipitation *******    
    Col_num = 2
    file_model_csv = "HBV_Climate_by_elev_0-200-1200_" + scenario + "_Run0.csv"
    file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
    data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
    Value_Ref = np.mean((np.array(data_v[:,Col_num]))[:(total_days_in_calculation-1)])*365/10.
    data_v1 = mfx(file_model_csv_w_path, column=Col_num, skip=cst.day_of_year_oct1) # Read csv file into matrix
    Value_Ref = [nrc(data_v1,[data_yr_start, period_start[i]],[data_yr_end,period_end[i]])*period_days[i]/10. for i in range(num_periods)]
    
    Value = nrc(data_v1,[data_yr_start, 1],[data_yr_end,365])*365./10.
    print "Basin-wide avg Precip (Annual) = ", Value," cm"
    for i in range(num_periods):
        print "Basin-wide avg Precip (", period_name[i], ") = ", Value_Ref[i]," cm"
    row = [1, 'Precip']   # Number is Order, which is only used to re-order rows for output.  Numbers in Order are relative to each other only.
    row.append(Value)
    row.extend([Value_Ref[i] for i in range(num_periods)])
    table.append(row)
    Precip = Value_Ref
    
#  ****** Snow (as SWE) *******    
    Col_num = 1
    file_model_csv = "HBV_Snow_(mm)_by_elev_0-500-1200_" + scenario + "_Run0.csv"
    file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
    data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
    Value_Ref = np.mean([np.max(np.array(data_v[i*365:(i+1)*365,Col_num])) for i in range(data_yr_start,data_yr_end+1)])/10. #avg over max of each of 30 yrs
    data_v1 = mfx(file_model_csv_w_path, column=Col_num, skip=cst.day_of_year_oct1) # Read csv file into matrix
    Value_Ref_Max = [nrc(data_v1,[data_yr_start, period_start[i]],[data_yr_end,period_end[i]],oper='AverageMaximum')/10. for i in range(num_periods)]
    Value_Ref_Min = [nrc(data_v1,[data_yr_start, period_start[i]],[data_yr_end,period_end[i]],oper='AverageMinimum')/10. for i in range(num_periods)]
    
    Value = nrc(data_v1,[data_yr_start, 1],[data_yr_end,365],'AverageMaximum')/10.
    print "Basin-wide max SWE (Annual) = ", Value," cm"
    for i in range(num_periods):
        print "Basin-wide max SWE (", period_name[i], ") = ", Value_Ref_Max[i]," cm"
        print "Basin-wide min SWE (", period_name[i], ") = ", Value_Ref_Min[i]," cm"
    row = [2, 'Basin-wide Max SWE']  # Number is Order, which is only used to re-order rows for output.  Numbers in Order are relative to each other only.
    row.append(Value)
    row.extend([Value_Ref_Max[i] for i in range(num_periods)])
    #table.append(row)
    row = [3, 'Basin-wide Min SWE']
    row.append(0.)
    row.extend([Value_Ref_Min[i] for i in range(num_periods)])
    #table.append(row)
    
#  ****** Change in Snow -- SnowDelta *******    
    row = [3.1,'SnowDelta']   # Number is Order, which is only used to re-order rows for output.  Numbers in Order are relative to each other only.
    SnowDelta = num_periods*[0.]
    SnowDelta[0] = Value_Ref_Min[0] - Value_Ref_Min[-1]
    for i in range(1,num_periods):
        SnowDelta[i] = Value_Ref_Min[i] - Value_Ref_Min[i-1]
    row.append(sum(SnowDelta))
    row.extend([SnowDelta[i] for i in range(num_periods)])
    table.append(row)
    
    fraction_of_landscape = [0.727, 0.273]   # division of landscape between ag and forest, approx

#  ****** Former code for soil water content *******    
#  Necessary output for it no longer available from Envision as
#  of this code mod, Mar. 16, 2015.
#  ******************************************
    # Calculate storage in soil water content as follows
    # Sum the soil water in the 4 categories of forest soil.  Do the same (further below) for ag
    # Take the difference between the max and the min as the storage
    
    #Col_num = range(1,5)
    #sum_Value = 0.
    #sum_Value_max =   [0.]*num_periods
    #sum_Value_min =   [0.]*num_periods
    #sum_Value_delta = [0.]*num_periods
    #
    #i_place = -1
    #
    #for place in ['Forest','Ag']:
    #    i_place += 1  # counter for Forest, Ag
    #    file_model_csv = place + "_Water_Content_" + scenario + "_Run0.csv"
    #    file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
    #    print file_model_csv_w_path
    #    data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
    #    Value_Ref = np.max([np.array(np.sum([data_v[i*365:(i+1)*365,j] for j in Col_num],0)) for i in range(data_yr_start,data_yr_end+1)])/10. -\
    #                np.min([np.array(np.sum([data_v[i*365:(i+1)*365,j] for j in Col_num],0)) for i in range(data_yr_start,data_yr_end+1)])/10. #max of 30 yrs 
    #          
    #    data_v1 = np.sum([mfx(file_model_csv_w_path, column=j, skip=cst.day_of_year_oct1) for j in Col_num],0)/10. # Read csv file cols into matrices and sum the matrices
    #    Value_Ref_max = [nrc(data_v1,[data_yr_start, period_start[i]],[data_yr_end,period_end[i]],oper='AverageMax') for i in range(num_periods)]
    #    Value_Ref_min = [nrc(data_v1,[data_yr_start, period_start[i]],[data_yr_end,period_end[i]],oper='AverageMin') for i in range(num_periods)]
    #    Value_Ref_delta = [Value_Ref_max[i] - Value_Ref_min[i] for i in range(num_periods)]
    #    
    #    file_model_csv = file_model_csv.replace(scenario, "HighClim")
    #    file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
    #    data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
    #    Value_HC = np.max([np.array(np.sum([data_v[i*365:(i+1)*365,j] for j in Col_num],0)) for i in range(data_yr_start,data_yr_end+1)])/10. -\
    #               np.min([np.array(np.sum([data_v[i*365:(i+1)*365,j] for j in Col_num],0)) for i in range(data_yr_start,data_yr_end+1)])/10. #max of 30 yrs 
    #    
    #    data_v1 = np.sum([mfx(file_model_csv_w_path, column=j, skip=cst.day_of_year_oct1) for j in Col_num],0)/10. # Read csv file cols into matrices and sum the matrices
    #    Value_HC_max = [nrc(data_v1,[data_yr_start, period_start[i]],[data_yr_end,period_end[i]],oper='AverageMax') for i in range(num_periods)]
    #    Value_HC_min = [nrc(data_v1,[data_yr_start, period_start[i]],[data_yr_end,period_end[i]],oper='AverageMin') for i in range(num_periods)]
    #    Value_HC_delta = [Value_Ref_max[i] - Value_Ref_min[i] for i in range(num_periods)]
    #    
    #    file_model_csv = file_model_csv.replace("HighClim", "LowClim")
    #    file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
    #    data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
    #    Value_LC = np.max([np.array(np.sum([data_v[i*365:(i+1)*365,j] for j in Col_num],0)) for i in range(data_yr_start,data_yr_end+1)])/10. -\
    #               np.min([np.array(np.sum([data_v[i*365:(i+1)*365,j] for j in Col_num],0)) for i in range(data_yr_start,data_yr_end+1)])/10. #max of 30 yrs 
    #    
    #    data_v1 = np.sum([mfx(file_model_csv_w_path, column=j, skip=cst.day_of_year_oct1) for j in Col_num],0)/10. # Read csv file cols into matrices and sum the matrices
    #    Value_LC_max = [nrc(data_v1,[data_yr_start, period_start[i]],[data_yr_end,period_end[i]],oper='AverageMax') for i in range(num_periods)]
    #    Value_LC_min = [nrc(data_v1,[data_yr_start, period_start[i]],[data_yr_end,period_end[i]],oper='AverageMin') for i in range(num_periods)]
    #    Value_LC_delta = [Value_Ref_max[i] - Value_Ref_min[i] for i in range(num_periods)]
    #    
    #    Value = np.mean(np.array([Value_Ref]))*fraction_of_landscape[i_place] #Fraction of soil to be treated like forest for calc
    #    Value_max = [np.mean(np.array([Value_Ref_max[i]]))*fraction_of_landscape[i_place] for i in range(num_periods)] #Fraction of soil to be treated like forest for calc
    #    Value_min = [np.mean(np.array([Value_Ref_min[i]]))*fraction_of_landscape[i_place] for i in range(num_periods)] #Fraction of soil to be treated like forest for calc
    #    Value_delta = [np.mean(np.array([Value_Ref_delta[i]]))*fraction_of_landscape[i_place] for i in range(num_periods)] #Fraction of soil to be treated like forest for calc
    #
    #    sum_Value += Value
    #    sum_Value_max =   [sum_Value_max[i] +   Value_max[i]   for i in range(num_periods)]
    #    sum_Value_min =   [sum_Value_min[i] +   Value_min[i]   for i in range(num_periods)]
    #    sum_Value_delta = [sum_Value_delta[i] + Value_delta[i] for i in range(num_periods)]
    #    print "Maximum Basin-wide stored soil water in", place, "(Annual) = ", Value," cm"
    #    for i in range(num_periods):
    #        print "Basin-wide stored soil water in", place, "(", period_name[i], "avg max) = ", Value_max[i]," cm"
    #        print "Basin-wide stored soil water in", place, "(", period_name[i], "avg min) = ", Value_min[i]," cm"
    #        print "Basin-wide stored soil water in", place, "(", period_name[i], "avg delta) = ", Value_delta[i]," cm"
    #
    #print "Maximum Basin-wide stored soil water whole WB (Annual) = ", sum_Value, " cm"
    #for i in range(num_periods):
    #    print "Basin-wide stored soil water whole WB (", period_name[i], " avg max) = ", sum_Value_max[i]," cm"
    #    print "Basin-wide stored soil water whole WB (", period_name[i], " avg min) = ", sum_Value_min[i]," cm"
    #    print "Basin-wide stored soil water whole WB (", period_name[i], " avg delta) = ", sum_Value_delta[i]," cm"
    #row = [4, 'Basin-wide Max soil water']
    #row.append(sum_Value)
    #row.extend([Value_Ref_max[i] for i in range(num_periods)])
    #table.append(row)
    #row = [5, 'Basin-wide Min soil water']
    #row.append(' ')
    #row.extend([Value_Ref_min[i] for i in range(num_periods)])
    #table.append(row)
    #row = [6, 'Basin-wide Delta soil water']
    #row.append(' ')
    #row.extend([Value_Ref_delta[i] for i in range(num_periods)])
    #table.append(row)
    
    
#  ****** Actual Evapotranspiration *******    
    Col_num = 1
    file_model_csv = "HBV_ET_(mm)_by_elev_0-200-1200_" + scenario + "_Run0.csv"
    file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
    data_v1 = mfx(file_model_csv_w_path, column=Col_num, skip=cst.day_of_year_oct1) # Read csv file into matrix
    Value_Ref = [nrc(data_v1,[data_yr_start, period_start[i]],[data_yr_end,period_end[i]])*period_days[i]/10. for i in range(num_periods)]
    
    Value = nrc(data_v1,[data_yr_start, 1],[data_yr_end,365])*365./10.
    print "Basin-wide avg AET (Annual) = ", Value," cm"
    for i in range(num_periods):
        print "Basin-wide avg AET (", period_name[i], ") = ", Value_Ref[i]," cm"
    row = [7, 'Act EvapoTrans']
    row.append(Value)
    row.extend([Value_Ref[i] for i in range(num_periods)])
    table.append(row)
    AET = Value_Ref
    
#  ****** ET for Ag & Forest *******    
##    Col_num = [1,3]
##    file_model_csv = "ET_by_LandCover_(mm)_" + scenario + "_Run0.csv"
##    file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
##    data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
##    i_place = -1
##    for place in ['Forest','Ag']:
##        i_place += 1
##        data_v1 = mfx(file_model_csv_w_path, column=Col_num[i_place], skip=cst.day_of_year_oct1) # Read csv file into matrix
##        Value_Ref = [nrc(data_v1,[data_yr_start, period_start[i]],[data_yr_end,period_end[i]])*period_days[i]/10.*fraction_of_landscape[i_place] for i in range(num_periods)]
##    
##        Value = nrc(data_v1,[data_yr_start, 1],[data_yr_end,365])*365./10.*fraction_of_landscape[i_place]
##        print "Basin-wide avg", place, "AET (Annual) = ", Value," cm"
##        for i in range(num_periods):
##            print "Basin-wide avg", place, "AET (", period_name[i], ") = ", Value_Ref[i]," cm"
    
#  ****** Reservoir calcs *******    
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
    #Value_Ref =      [nrc(data_v1,[data_yr_start, period_start[i]],[data_yr_end,period_end[i]])*period_days[i]/10. for i in range(num_periods)]
    Value_Ref_in    = [nrc(data_v_in,[data_yr_start, period_start[i]],[data_yr_end,period_end[i]])*period_days[i]*86400./cst.Willamette_Basin_area*100. for i in range(num_periods)]
    Value_Ref_out   = [nrc(data_v_out,[data_yr_start, period_start[i]],[data_yr_end,period_end[i]])*period_days[i]*86400./cst.Willamette_Basin_area*100. for i in range(num_periods)]
    Value_Ref_delta = [nrc(data_v_delta, [data_yr_start, period_start[i]],[data_yr_end,period_end[i]])*period_days[i]*86400./cst.Willamette_Basin_area*100. for i in range(num_periods)]
    Value_Ref_min   = [nrc(data_v_cumsum,[data_yr_start, period_start[i]],[data_yr_end,period_end[i]],oper='AverageMin')/cst.Willamette_Basin_area*100. for i in range(num_periods)]
    Value_Ref_max   = [nrc(data_v_cumsum,[data_yr_start, period_start[i]],[data_yr_end,period_end[i]],oper='AverageMax')/cst.Willamette_Basin_area*100. for i in range(num_periods)]
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
        
#  ****** Change in Reservoir storage (ResDelta) *******    
    row = [3.5, 'ResDelta']
    row.append(sum(Value_Ref_delta))
    row.extend([Value_Ref_delta[i] for i in range(num_periods)])
    table.append(row)
    ResDelta = Value_Ref_delta
    
#  ****** Reservoir max minus min for period *******    
    row = [3.7, 'All reservoirs max - min']
    row.append(sum(Value_Ref_delta))
    row.extend([Value_Ref_maxmin[i] for i in range(num_periods)])
    #table.append(row)
    
#  ****** Instream regulatory use *******    
    Col_num = 1
    file_model_csv = "AltWaterMaster_Daily_Metrics_" + scenario + "_Run0.csv"
    file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
    data_v = np.array(np.genfromtxt(file_model_csv_w_path, delimiter=',',skip_header=1)) # Read csv file
    data_v1 = mfx(file_model_csv_w_path, column=Col_num, skip=cst.day_of_year_oct1) # Read csv file into matrix
    Value_Ref = [nrc(data_v1,[data_yr_start, period_start[i]],[data_yr_end,period_end[i]])*period_secs[i]/cst.Willamette_Basin_area_at_PDX*100. for i in range(num_periods)]
    
    Value = nrc(data_v1,[data_yr_start, 1],[data_yr_end,365])*cst.seconds_in_yr/cst.Willamette_Basin_area_at_PDX*100.
    print "Instream regulatory use (Annual) = ", Value," cm"
    for i in range(num_periods):
        print "Instream regulatory use (", period_name[i], ") = ", Value_Ref[i]," cm"
     
#  ****** Irrigation *******    
    Col_num = [2,3]
    data_v1 = np.sum([mfx(file_model_csv_w_path, column=j, skip=cst.day_of_year_oct1) for j in Col_num],0)  # Read csv file cols into matrices and sum the matrices
    Value_Ref = [nrc(data_v1,[data_yr_start, period_start[i]],[data_yr_end,period_end[i]])*period_secs[i]/cst.Willamette_Basin_area*100. for i in range(num_periods)]
    
    Value = nrc(data_v1,[data_yr_start, 1],[data_yr_end,365])*cst.seconds_in_yr/cst.Willamette_Basin_area*100.
    print "Irrigation water diverted (Annual) = ", Value," cm"
    for i in range(num_periods):
        print "Irrigation water diverted (", period_name[i], ") = ", Value_Ref[i]," cm"
    row = [9, 'Ag Irrigation']
    row.append(Value)
    row.extend([Value_Ref[i] for i in range(num_periods)])
    table.append(row)
    
#  ****** Irrigation water lost to ET *******    
    # Agricultural water consumed  PLACEHOLDER. This will need work once we have a way of calculating from Envision output or other
    Ag_AET_fraction = 0.75
    row = [109, 'Ag Irrig Consumed']
    for i in range(num_periods):
        Value_Ref[i] = Ag_AET_fraction * Value_Ref[i]
    row.append(sum(Value_Ref))
    row.extend([Value_Ref[i] for i in range(num_periods)])
    table.append(row)
    #************************
    
#  ****** Municipal water use *******    
    Col_num = range(1,9)
    file_model_csv = "Daily_Urban_Water_Demand_Summary_" + scenario + "_Run0.csv"
    file_model_csv_w_path = cst.path_data + file_model_csv       # Add path to data & stats files
    data_v1 = np.sum([mfx(file_model_csv_w_path, column=j, skip=cst.day_of_year_oct1) for j in Col_num],0)  # Read csv file cols into matrices and sum the matrices
    Value_Ref = [nrc(data_v1,[data_yr_start, period_start[i]],[data_yr_end,period_end[i]])*100*period_days[i]*cst.cfs_to_m3/cst.Willamette_Basin_area*100.*1.11386 for i in range(num_periods)]
    
    if era != 'future':
        print "Municipal & domestic water diverted (Annual) = ", sum(Value_Ref)," cm"    
    else:
        print "Municipal & domestic water diverted (Annual) = ", Value*100/cst.Willamette_Basin_area," cm"
    for i in range(num_periods):
        print "Municipal & domestic water diverted (", period_name[i], ") = ", Value_Ref[i]," cm"
    row = [10, 'Muni & Domest']
    if era != 'future':
        row.append(sum(Value_Ref))
    else:
        row.append(Value*100/cst.Willamette_Basin_area)
    row.extend([Value_Ref[i] for i in range(num_periods)])
    table.append(row)
    
#  ****** Municipal water ET estimate *******    
    ##********************************* urban water demand/disposition code 3-14-15, pi day
    uwd_file = "seasonal_water_distribution_urban_demand.csv"  # let's simplify name to uwd
    urban_irrigation_efficiency = 0.80  # Based on email from W Jaeger 03/06/2015 01:52:31 PM PDT.  Fraction of urban water applied to landscape that is evapotranspired.
    data_uwd = mfx(uwd_file,column=5,filetype='csv')
    data_uwd = data_uwd.astype(np.float) 
    data_uwd = np.roll(data_uwd,(365-cst.day_of_year_oct1)) # Re-order numbers so that first number is on Oct. 1
    data_v2 = np.subtract(data_v1,data_v1 * data_uwd)
    data_v2= data_v2 * urban_irrigation_efficiency
    Value_Ref = [nrc(data_v2,[data_yr_start, period_start[i]],[data_yr_end,period_end[i]])*100*period_days[i]*cst.cfs_to_m3/cst.Willamette_Basin_area*100.*1.11386 for i in range(num_periods)]
    
    if era != 'future':
        print "Municipal & domestic water Consumed (Annual) = ", sum(Value_Ref)," cm"    
    else:
        print "Municipal & domestic water Consumed (Annual) = ", Value*100/cst.Willamette_Basin_area," cm"
    for i in range(num_periods):
        print "Municipal & domestic water Consumed (", period_name[i], ") = ", Value_Ref[i]," cm"
    row = [110, 'Muni & Domest Consumed']
    row.append(sum(Value_Ref))
    row.extend([Value_Ref[i] for i in range(num_periods)])
    table.append(row)
    
#  ****** Environmental Flows *******    
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
    row = [11, 'Environmental Flows']
    row.append(specific_minQ*100)
    
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
        minflows.append(specific_minQ*100.)
        print "Minimum flows at Salem (", period_name[i_period], ") = ", specific_minQ*100.," cm"
        vol = 0.
    row.extend([minflows[i] for i in range(num_periods)])
    table.append(row)
    row = [11.5, 'Willamette minus min flows at Salem']
    row.extend([table[1][i] - table[-1][i] for i in range(2,num_periods+3)])
    #table.append(row)
    
#  ****** Change in soil moisture (SoilDelta) *******    
#     Calculated as a residual
    row = [6.1, 'SoilDelta']
    SoilDelta = num_periods*[0.]
    pos_SoilDelta = 0.  # Needed for precip evaporation problem
    for i in range(num_periods):
        SoilDelta[i] = Precip[i] - Willamette_Outflow[i] - AET[i] - ResDelta[i] - SnowDelta[i]
        if SoilDelta[i] > 0: pos_SoilDelta += SoilDelta[i] # Needed for precip evaporation problem
            
    totalSoilDelta = sum(SoilDelta)
    SoilDelta_beforeCorrection = [totalSoilDelta] # Needed for precip evaporation problem
    SoilDelta_beforeCorrection.extend(SoilDelta) # Needed for precip evaporation problem
    ET_correction = [totalSoilDelta] # Needed for precip evaporation problem
#    row.append(totalSoilDelta)
    row.append(0.)  # Needed for precip evaporation problem  UNCOMMENT PREVIOUS LINE
    for i in range(num_periods):  # This whole loop Needed for precip evaporation problem
        if SoilDelta[i] > 0. and totalSoilDelta > 0: 
            ET_correction.append(SoilDelta[i] - SoilDelta[i]*(pos_SoilDelta-totalSoilDelta)/pos_SoilDelta) # Needed for precip evaporation problem
            SoilDelta[i] = SoilDelta[i]*(pos_SoilDelta-totalSoilDelta)/pos_SoilDelta  # Needed for precip evaporation problem
        else:  # Needed for precip evaporation problem
            ET_correction.append(0.)  # Needed for precip evaporation problem
    row.extend(SoilDelta)
    table.append(row)
    
    ActET_row = table[3]  # Needed for precip evaporation problem
    ActET_row [2:] = np.add(ActET_row [2:], ET_correction)  # Needed for precip evaporation problem
    table[3] = ActET_row  # Needed for precip evaporation problem

#******************************************************************************
#  ****** Prep and save information to table *******    
    table.sort(key=lambda x: x[0])  # sort by first (zeroth) element, which is the Order number that we have been recording
    
    table = np.insert(table, 0, header, 0)  # insert row (axis = 0, the 2nd 0) into table above 0th row (the first 0)
    table = np.insert(table, 0, row_1, 0)
    table_transposed = np.transpose(table)  # We want to print each process as a column rather than a row, so transpose
    final_header = table_transposed[1]
    if simulation_num == 0:
        table_save[simulation_num]=table_transposed[1:]
    else:
        table_save[simulation_num]=table_transposed[2:]



#******************************************************************************
#******************************************************************************
#******************************************************************************
#  ****** Print to csv file *******    
import csv
with open(save_results_to_csv_file_named + ".csv", "wb") as file_:
    writer = csv.writer(file_)
    for simulation_num in range(len(ensemble)):
        writer.writerows(table_save[simulation_num])
