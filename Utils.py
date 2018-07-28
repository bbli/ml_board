from pymongo import MongoClient
from threading import Thread
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import itertools
from io import BytesIO
from PIL import Image
import pickle
import base64
import numpy as np

import ipdb

class Database():
    def __init__(self):
        self.client = MongoClient()
        self.checkConnection()
    ## Database utilities
    ## I do not want the user to accidently delete all their data
    # def removeDataBase(self,folder_name):
        # self.client.drop_database(folder_name)

    def removeFolder(self,database_name,folder_name):
        self.client[database_name][folder_name].drop()

    def viewDataBase(self,database_name):
        '''
        show all collections in a folder
        '''
        # include include_system_collections=False?
        for collection in self.client[database_name].list_collection_names():
            print(collection)
    def getAllFolderIteratorsFromDatabase(self,database_name):
        folder_iterators_list= []
        folder_names = self.client[database_name].list_collection_names()
        for folder_name in folder_names:
            iterator = self.client[database_name][folder_name].find()
            folder_iterators_list.append(iterator)

        return folder_iterators_list


    def viewFolder(self,database_name,folder_name):
        '''
        show all documents in a collection
        '''
        for doc in self.client[database_name][folder_name].find():
            print(doc)
    def close(self):
        self.client.close()

    ## Connection utilties, not meant to be used by user
    def checkConnection(self):
       t = Thread(target=self.testInsert) 
       t.start()
       t.join(2)
       if t.is_alive():
           raise Exception("Cannot connect to MongoDB")

    def testInsert(self):
        doc = self.client['test_db']['test_collection']
        doc.insert({"Test":1})
        doc.remove({"Test":1})
################ **Misc** ##################
from functools import partial
def partial_decomaker(partial_name):
    def decorator(func):
        partial_func = partial(func,partial_name=partial_name)
        return partial_func
    return decorator

from inspect import getsource
def code(function):
    print(getsource(function))

################ **Functions used to load Data in** ##################
def getParamDict(database_name,folder_name):
    mongo = Database()
    runs = mongo.client[database_name][folder_name]
    ## all the runs in the folder
    runs_iterator = runs.find()

    dict_of_dicts = {}
    for run_object in runs_iterator:
        Experimental_Parameters = run_object['Experimental Parameters']
        time = Experimental_Parameters['Time']
        dict_of_dicts[time] = Experimental_Parameters
    return dict_of_dicts
def getLegendNames(dict_of_param_dicts):
    list_of_param_names = []
    for time,plot_dict in dict_of_param_dicts.items():
        list_of_param_names.append(plot_dict.keys())
    legend_names = sorted(set(list(itertools.chain(*list_of_param_names))))
    return legend_names
## Object Related
def getDictOfNameObjects(database_name,folder_name,name,f=None):
    mongo = Database()
    runs = mongo.client[database_name][folder_name]
    ## all the runs in the folder
    runs_iterator = runs.find()

    nameObjects_for_each_run = {}
    # paramObjects_for_each_run = {}
    for run_object in runs_iterator:
        Experimental_Parameters = run_object['Experimental Parameters']
        time = Experimental_Parameters['Time']
        # param_objects_for_each_run[time] = Experimental_Parameters

        try:
            one_run_dict = run_object[name]
            if f:
                one_run_dict = f(one_run_dict)
            nameObjects_for_each_run[time] = one_run_dict
        except KeyError:
            print("Name does not exist in the run")
    mongo.close()
    # return nameObjects_for_each_run, paramObjects_for_each_run
    return nameObjects_for_each_run
def getBase64Encoding(one_run_dict):
    return {image_name:binaryToBase64(binary_image) for image_name,binary_image in one_run_dict.items()}
def binaryToBase64(binary_image):
    numpy_matrix=pickle.loads(binary_image)
    img = Image.fromarray(np.uint8(numpy_matrix*255),'L')
    # base64_string= base64.b64encode(numpy_matrix)
    buff = BytesIO()
    img.save(buff, format="JPEG")
    base64_string = base64.b64encode(buff.getvalue())
    buff.close()
    return str(base64_string)[2:-1]
def getFigureNames(nameObjects_for_each_run):
    list_of_names = []
    for time, one_run_dict in nameObjects_for_each_run.items():
        list_of_names.append(one_run_dict.keys())
    names = sorted(set(list(itertools.chain(*list_of_names))))
    return names

##############################################################
def getDictOfAllThoughtLists(database_name):
    mongo = Database()
    folder_iterators_list = mongo.getAllFolderIteratorsFromDatabase(database_name)
    database_dict = {}
    for folder_iterator in folder_iterators_list:
        dict_of_thoughtlists = getDictOfThoughtLists(folder_iterator)
        database_dict.update(dict_of_thoughtlists)
    mongo.close()
    return database_dict

#########################
def getDictOfThoughtLists(folder_iterator):
    dict_of_thoughtlists = {}
    for run_object in folder_iterator:
        Experimental_Parameters = run_object['Experimental Parameters']
        time = Experimental_Parameters['Time']
        try:
            thought_list = run_object['Thoughts']
            ## eliminating the extra self.folder_name logs
            dict_of_thoughtlists[time]=thought_list
        except KeyError:
            print("Run object does not have 'Thoughts' as a key")

    return dict_of_thoughtlists
#########################
def getOrderedKeys(dict_of_thoughtlists):
    return sorted(dict_of_thoughtlists.keys())

def createThoughts(list_of_thoughts):
    paragraph_list = []
    ## skipping the folder_names
    for thought in list_of_thoughts[1::2]:
        paragraph = html.P(thought)
        paragraph_list.append(paragraph)
    return paragraph_list

def createThoughtsTitle(list_of_thoughts,time):
    folder_name = list_of_thoughts[0]
    ## No need for year and seconds
    title_row = html.Div(html.B(time[5:-3]+': '+folder_name),className='row')
    return title_row

##############################################################

################ **Functions used During Callbacks** ##################
def getSelectedRunsFromDatatable(rows,selected_row_indices):
    if selected_row_indices==[]:
        selected_runs= rows
    else:
        selected_runs = [rows[i] for i in selected_row_indices]
    return [run_dict['Time'] for run_dict in selected_runs]
##############################################################



if __name__ == '__main__':
    database = Database()
    database.client['test_db']['test_collection'].insert_one({"Test":"test"})
    database.viewRun('test_db','test_collection')
    database.removeRun('test_db','test_collection')
    database.viewRun('test_db','test_collection')
