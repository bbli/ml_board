from pymongo import MongoClient
from LoggerUtils import *
import pandas as pd

def getTable(folder_name):
    '''
    returns a dataframe with the experiment parameters for each run in the folder
    '''
    mongo = Database()
    folder = mongo.client[folder_name]
    
    
    for run in folder.collection_names():
        experiment_parameters_iterator = folder[run].find({"Name of Text":{"$exists":"true"}})
        variable_name_iterator = folder[run].find({"Variable name":{"$exists":"true"}})
        for json_object in experiment_parameters_iterator:
            print(json_object)
    return json_object
        

if __name__ == '__main__':
    ob = getTable('aql')



