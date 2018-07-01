from pymongo import MongoClient
from LoggerUtils import *
import pandas as pd
from datetime import datetime
import ipdb
import itertools

def getTable(run_name,folder_name='deep_learning'):
    '''
    returns a dataframe with the experiment parameters for each run in the folder
    '''
    mongo = Database()
    runs = mongo.client[folder_name][run_name]
    
    
    runs_iterator = runs.find()
    df_list =[]
    list_of_variable_names_for_each_run=[]
    for run_object in runs_iterator:
        min_array_length = getMinArrayLength(run_object)
        list_of_variable_names_for_each_run.append(getVariableNames(run_object))

        some_dict = {key: arrayLengthEqualizer(value,min_array_length) for key, value in run_object.items() if key != '_id'}
        some_df = pd.DataFrame(some_dict)
        ## This leaves NaNs, so not as optimal
        # some_df = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in some_dict.items() ]))
        df_list.append(some_df)
    final_df = pd.concat(df_list,ignore_index=False)
    final_df['Time']=final_df['Time'].apply(strToDatetime)

    return final_df,sorted(set(list(itertools.chain(*list_of_variable_names_for_each_run))))

def getVariableNames(dictionary):
    variable_list=[]
    for key,value in dictionary.items():
        if type(value)==list:
            variable_list.append(key)
    return variable_list
################################################################
def getMinArrayLength(dictionary):
    min_length_list=[]
    for key,value in dictionary.items():
        if type(value)==list:
            min_length_list.append(len(value))
    return min(min_length_list)
################################################################
def arrayLengthEqualizer(value,min_length):
    if type(value)==list:
        return restrictLength(value,min_length)
    else:
        return value
#########################
def restrictLength(a_list,min_length):
    a_length = len(a_list)
    if a_length==min_length:
        return a_list
    else:
        diff=min_length-a_length
        return a_list[:diff]
#########################
################################################################
def strToDatetime(string):
    if type(string)==float:
        return string
    else:
        return datetime.strptime(string,'%Y-%m-%d %H:%M:%S')
################################################################

if __name__ == '__main__':
    df,var_names = getTable('lunarlander')



