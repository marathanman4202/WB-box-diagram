
def get_pop_scenario(scenario):
    # Cameron Barrie, June 2015
    """Returns population scenario needed for scenario
    """
    if scenario == '_HighPop_':
        return '_HighPop_'
    elif scenario == '_NoGrow_' or scenario == '_HistoricRef_' or scenario == 'HistoricHadGEM':
        return '_NoGrow_'
    else:
        return '_Ref_'

def get_population(data):
    import numpy as np
    num_yrs = np.shape(data)[0]
    population =[data[i,1] for i in range(num_yrs)]
    return population
    
