import constants as cst

def get_EFrules():
    """ Write rules for each location
    For each location, provide rules.
    Return rules.
    """
    shft = 365 - cst.day_of_year_oct1
    shftB = cst.day_of_year_oct1
                                   ##      rule_type    start_day             end_day              discharge            pct_time_met  weight
    EFrules = {
            'Salem':              (1, (  ['minQ7day', cst.day_of_year_apr1 + shft,  cst.day_of_year_apr30 + shft,  17800.*cst.cfs_to_m3,    100.,    1., 'Ref #5'],
                                         ['minQ7day', cst.day_of_year_may1 + shft,  cst.day_of_year_may31 + shft,  15000.*cst.cfs_to_m3,    100.,    1., 'Ref #5'],
                                         ['minQ7day', cst.day_of_year_jun1 + shft,  cst.day_of_year_jun15 + shft,  13000.*cst.cfs_to_m3,    100.,    1., 'Ref #5'],
                                         ['minQ7day', cst.day_of_year_jun16 + shft, cst.day_of_year_jun30 + shft,   8000.*cst.cfs_to_m3,    100.,    1., 'Ref #5'],
                                         ['minQ',     cst.day_of_year_apr1 + shft,  cst.day_of_year_apr30 + shft,  14300.*cst.cfs_to_m3,    100.,    1., 'Ref #5'],
                                         ['minQ',     cst.day_of_year_may1 + shft,  cst.day_of_year_may31 + shft,  12000.*cst.cfs_to_m3,    100.,    1., 'Ref #5'],
                                         ['minQ',     cst.day_of_year_jun1 + shft,  cst.day_of_year_jun15 + shft,  10500.*cst.cfs_to_m3,    100.,    1., 'Ref #5'],
                                         ['minQ',     cst.day_of_year_jun16 + shft, cst.day_of_year_jun30 + shft,   7000.*cst.cfs_to_m3,    100.,    1., 'Ref #5'],
                                         ['minQ',     cst.day_of_year_jul1 + shft,  cst.day_of_year_jul31 + shft,   6000.*cst.cfs_to_m3,    100.,    1., 'Ref #5'],
                                         ['minQ',     cst.day_of_year_aug1 + shft,  cst.day_of_year_aug15 + shft,   6000.*cst.cfs_to_m3,    100.,    1., 'Ref #5'],
                                         ['minQ',     cst.day_of_year_aug16 + shft, cst.day_of_year_aug31 + shft,   6500.*cst.cfs_to_m3,    100.,    1., 'Ref #5'],
                                         ['minQ',     cst.day_of_year_sep1 + shft,  cst.day_of_year_sep30 + shft,   7000.*cst.cfs_to_m3,    100.,    1., 'Ref #5'],
                                         ['minQ',     cst.day_of_year_oct1 - shftB, cst.day_of_year_oct31 - shftB,  7000.*cst.cfs_to_m3,    100.,    1., 'Ref #5']
                                         )), 
                                         
            'Hills Creek':        (2, (
                                         ['minQ',     cst.day_of_year_sep1 + shft,  cst.day_of_year_sep30 + shft,    400.*cst.cfs_to_m3,    99.9,    1., 'Ref #1'],
                                         ['minQ',     cst.day_of_year_oct1 - shftB, cst.day_of_year_jan31 + shft,    400.*cst.cfs_to_m3,    99.9,    1., 'Ref #1'],
                                         ['minQ',     cst.day_of_year_feb1 + shft,  cst.day_of_year_aug31 + shft,    400.*cst.cfs_to_m3,    99.9,    1., 'Ref #1']
                                        )),
                                        
            'Fall Creek':         (3, ( 
                                         ['minQ',     cst.day_of_year_sep1 + shft,  cst.day_of_year_sep30 + shft,    200.*cst.cfs_to_m3,    95.,     1., 'Ref #1'],
                                         ['minQ',     cst.day_of_year_oct1 - shftB, cst.day_of_year_oct15 - shftB,   200.*cst.cfs_to_m3,    95.,     1., 'Ref #1'],
                                         ['maxQ',     cst.day_of_year_sep1 + shft,  cst.day_of_year_sep30 + shft,    400.*cst.cfs_to_m3,    25.,     1., 'Ref #1'],
                                         ['maxQ',     cst.day_of_year_oct1 - shftB, cst.day_of_year_oct15 - shftB,   400.*cst.cfs_to_m3,    25.,     1., 'Ref #1'],
                                         ['minQ',     cst.day_of_year_oct16 - shftB,cst.day_of_year_mar31 + shft,     50.*cst.cfs_to_m3,    99.9,    1., 'Ref #1'],
                                         ['minQ',     cst.day_of_year_apr1 + shft,  cst.day_of_year_jun30 + shft,     80.*cst.cfs_to_m3,    99.9,    1., 'Ref #1'],
                                         ['minQ',     cst.day_of_year_jul1 + shft,  cst.day_of_year_aug31 + shft,     80.*cst.cfs_to_m3,    95.,     1., 'Ref #1']
                                        )),
                                        
            'Dexter':             (4, ( 
                                         ['minQ',     cst.day_of_year_sep1 + shft,  cst.day_of_year_sep30 + shft,   1200.*cst.cfs_to_m3,    99.9,    1., 'Ref #1'],
                                         ['minQ',     cst.day_of_year_oct1 - shftB, cst.day_of_year_oct15 - shftB,  1200.*cst.cfs_to_m3,    99.9,    1., 'Ref #1'],
                                         ['maxQ',     cst.day_of_year_sep1 + shft,  cst.day_of_year_sep30 + shft,   3500.*cst.cfs_to_m3,    25.,     1., 'Ref #1'],
                                         ['maxQ',     cst.day_of_year_oct1 - shftB, cst.day_of_year_oct15 - shftB,  3500.*cst.cfs_to_m3,    25.,     1., 'Ref #1'],
                                         ['minQ',     cst.day_of_year_oct16 - shftB,cst.day_of_year_aug31 + shft,   1200.*cst.cfs_to_m3,    99.9,    1., 'Ref #1']
                                        )),
                                        
            'Big Cliff':          (5, ( 
                                         ['minQ',     cst.day_of_year_sep1 + shft,  cst.day_of_year_sep30 + shft,   1500.*cst.cfs_to_m3,    95.,     1., 'Ref #1'],
                                         ['minQ',     cst.day_of_year_oct1 - shftB, cst.day_of_year_oct15 - shftB,  1500.*cst.cfs_to_m3,    95.,     1., 'Ref #1'],
                                         ['maxQ',     cst.day_of_year_sep1 + shft,  cst.day_of_year_sep30 + shft,   3000.*cst.cfs_to_m3,     5.,     1., 'Ref #1'],
                                         ['maxQ',     cst.day_of_year_oct1 - shftB, cst.day_of_year_oct15 - shftB,  3000.*cst.cfs_to_m3,     5.,     1., 'Ref #1'],
                                         ['minQ',     cst.day_of_year_oct16 - shftB,cst.day_of_year_jan31 + shft,   1200.*cst.cfs_to_m3,    98.,     1., 'Ref #1'],
                                         ['minQ',     cst.day_of_year_feb1 + shft,  cst.day_of_year_mar15 + shft,   1000.*cst.cfs_to_m3,    99.9,    1., 'Ref #1'],
                                         ['minQ',     cst.day_of_year_mar16 + shft, cst.day_of_year_may31 + shft,   1500.*cst.cfs_to_m3,    99.9,    1., 'Ref #1'],
                                         ['maxQ',     cst.day_of_year_mar16 + shft, cst.day_of_year_may31 + shft,   3000.*cst.cfs_to_m3,    25.,     1., 'Ref #1'],
                                         ['minQ',     cst.day_of_year_jun1 + shft,  cst.day_of_year_jul15 + shft,   1200.*cst.cfs_to_m3,    99.9,    1., 'Ref #1'],
                                         ['minQ',     cst.day_of_year_jul16 + shft, cst.day_of_year_aug31 + shft,   1000.*cst.cfs_to_m3,    99.9,    1., 'Ref #1']
                                        )),
                                        
            'Foster':             (6, ( 
                                         ['minQ',     cst.day_of_year_sep1 + shft,  cst.day_of_year_sep30 + shft,   1500.*cst.cfs_to_m3,    75.,     1., 'Ref #1'],
                                         ['minQ',     cst.day_of_year_oct1 - shftB, cst.day_of_year_oct15 - shftB,  1500.*cst.cfs_to_m3,    75.,     1., 'Ref #1'],
                                         ['maxQ',     cst.day_of_year_sep1 + shft,  cst.day_of_year_sep30 + shft,   3000.*cst.cfs_to_m3,     1.,     1., 'Ref #1'],
                                         ['maxQ',     cst.day_of_year_oct1 - shftB, cst.day_of_year_oct15 - shftB,  3000.*cst.cfs_to_m3,     1.,     1., 'Ref #1'],
                                         ['minQ',     cst.day_of_year_oct16 - shftB,cst.day_of_year_jan31 + shft,   1100.*cst.cfs_to_m3,    80.,     1., 'Ref #1'],
                                         ['minQ',     cst.day_of_year_feb1 + shft,  cst.day_of_year_mar15 + shft,    800.*cst.cfs_to_m3,    95.,     1., 'Ref #1'],
                                         ['minQ',     cst.day_of_year_mar1 + shft,  cst.day_of_year_may15 + shft,   1500.*cst.cfs_to_m3,    80.,     1., 'Ref #1'],
                                         ['maxQ',     cst.day_of_year_mar16 + shft, cst.day_of_year_may15 + shft,   3000.*cst.cfs_to_m3,    30.,     1., 'Ref #1'],
                                         ['minQ',     cst.day_of_year_may16 + shft, cst.day_of_year_jun30 + shft,   1100.*cst.cfs_to_m3,    95.,     1., 'Ref #1'],
                                         ['minQ',     cst.day_of_year_jul1 + shft,  cst.day_of_year_aug31 + shft,    800.*cst.cfs_to_m3,    99.,     1., 'Ref #1']
                                        )),
                                        
            'Blue River':        (7,  ( 
                                         ['minQ',     cst.day_of_year_sep1 + shft,  cst.day_of_year_sep30 + shft,     50.*cst.cfs_to_m3,    99.9,    1., 'Ref #1'],
                                         ['minQ',     cst.day_of_year_oct1 - shftB, cst.day_of_year_oct15 - shftB,    50.*cst.cfs_to_m3,    99.9,    1., 'Ref #1'],
                                         ['minQ',     cst.day_of_year_oct16 - shftB,cst.day_of_year_aug31 + shft,     50.*cst.cfs_to_m3,    99.9,    1., 'Ref #1']
                                        )),
                                        
            'Cougar':            (8,  ( 
                                         ['minQ',     cst.day_of_year_sep1 + shft,  cst.day_of_year_sep30 + shft,    300.*cst.cfs_to_m3,    99.9,    1., 'Ref #1'],
                                         ['minQ',     cst.day_of_year_oct1 - shftB, cst.day_of_year_oct15 - shftB,   300.*cst.cfs_to_m3,    99.9,    1., 'Ref #1'],
                                         ['maxQ',     cst.day_of_year_sep1 + shft,  cst.day_of_year_sep30 + shft,    580.*cst.cfs_to_m3,    60.,     1., 'Ref #1'],
                                         ['maxQ',     cst.day_of_year_oct1 - shftB, cst.day_of_year_oct15 - shftB,   580.*cst.cfs_to_m3,    60.,     1., 'Ref #1'],
                                         ['minQ',     cst.day_of_year_oct16 - shftB,cst.day_of_year_may31 + shft,    300.*cst.cfs_to_m3,    99.9,    1., 'Ref #1'],
                                         ['minQ',     cst.day_of_year_jun1 + shft,  cst.day_of_year_jun30 + shft,    400.*cst.cfs_to_m3,    99.9,    1., 'Ref #1'],
                                         ['minQ',     cst.day_of_year_jul1 + shft,  cst.day_of_year_aug31 + shft,    300.*cst.cfs_to_m3,    99.9,    1., 'Ref #1']
                                        )),
            }
    

    return EFrules