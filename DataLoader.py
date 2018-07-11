from pymongo import MongoClient
from LoggerUtils import *
import pandas as pd
from datetime import datetime
import ipdb
import itertools

def getRunDicts(database_name,folder_name):
    '''
    returns a dataframe with the experiment parameters for each run in the folder
    '''
    mongo = Database()
    runs = mongo.client[database_name][folder_name]
    ## all the runs in the folder
    runs_iterator = runs.find()

    dict_of_param_dicts = {}
    dict_of_plot_dicts = {}
    dict_of_images={}
    dict_of_histograms={}
    for run_object in runs_iterator:
        ## Datatable and RadioItems Components needs all experiment parameters from each run in a list
        ## No need to use try-except block here because Logger will always create this key
        Experimental_Parameters = run_object['Experimental Parameters']
        time = Experimental_Parameters['Time']
        dict_of_plot_dicts[time]=Experimental_Parameters

        try:
            ## Graph Components need to index into a Time and then the variable
            Plots=run_object['Plots']
            dict_of_plot_dicts[time]=Plots
        except KeyError:
            pass
        try:
            Images = run_object['Images']
            dict_of_images[time]=Images
        except KeyError:
            pass
        try:
            Histograms = run_object['Histograms']
            dict_of_images[time]=Histograms
        except KeyError:
            pass

    return dict_of_param_dicts,dict_of_plot_dicts,dict_of_images,dict_of_histograms 


if __name__ == '__main__':
    dict_of_plot_dicts,dict_of_param_dicts,dict_of_histograms,dict_of_images = getRunDicts('software_testing','lunarlander')
    plot_names = getPlotNames(dict_of_plot_dicts)
    legend_names = getLegendNames(dict_of_param_dicts)



