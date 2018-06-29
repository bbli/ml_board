from pymongo import MongoClient
from LoggerUtils import *
import pandas as pd
import ipdb

def getTable(run_name,folder_name='deep_learning'):
    '''
    returns a dataframe with the experiment parameters for each run in the folder
    '''
    mongo = Database()
    runs = mongo.client[folder_name][run_name]
    
    
    document_iterator = runs.find()
    # row_of_dicts=list(document_iterator)
    df_list =[]
    for json_object in document_iterator:
        some_dict = {key: value for key, value in json_object.items() if key != '_id'}
        some_df = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in some_dict.items() ]))
        print(len(some_df))
        df_list.append(some_df)
    final_df = pd.concat(df_list,ignore_index=False)
    ipdb.set_trace()
    return final_df
        

if __name__ == '__main__':
    ob = getTable('lunarlander')



