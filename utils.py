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

    def removeCollection(self,folder_name,run_name):
        self.client[folder_name][run_name].drop()

    def viewDataBase(self,folder_name):
        '''
        show all collections in a folder
        '''
        # include include_system_collections=False?
        for collection in self.client[folder_name].collection_names():
            print(collection)
    def viewCollection(self,folder_name,run_name):
        '''
        show all documents in a collection
        '''
        for doc in self.client[folder_name][run_name].find():
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
def getNameObjects(database_name,folder_name,name,f=None):
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

################ **Functions used During Callbacks** ##################
def getSelectedRunsFromDatatable(rows,selected_row_indices):
    if selected_row_indices==[]:
        selected_runs= rows
    else:
        selected_runs = [rows[i] for i in selected_row_indices]
    return [run_dict['Time'] for run_dict in selected_runs]
##############################################################


class BaseTab():
    def __init__(self,database_name,folder_name,title,f):
        self.title = title
        self.f = f
        self.nameObjects_for_each_run = getNameObjects(database_name,folder_name,self.title,self.f)
        self.figure_names = getFigureNames(self.nameObjects_for_each_run)
        self.database_name = database_name
        self.folder_name = folder_name

    #########################################
    def createHTMLStructure(self):
        html_row_list = []
        for figure_name in self.figure_names:
            button_row = html.Div(html.Button(figure_name,id=self.title+':'+figure_name+'button'),className='row')
            html_row_list.append(button_row)

            figure_row = html.Div(id=self.title+':'+figure_name+'content')
            html_row_list.append(figure_row)
        return html.Div(html_row_list,id=self.title)
    def assignCallbacks(self,app):
        for figure_name in self.figure_names:
            self.assignFigureShowCallback(figure_name,app)
            self.assignFigureCallback(figure_name,app)

        self.assignTabShowCallback(app)


    ############################################# 
    def assignFigureShowCallback(self,figure_name,app):
        @app.callback(
                ## Still Need to define this html structure
                Output(self.title+':'+figure_name+'content','style'),
                [Input(self.title+':'+figure_name+'button','n_clicks')]
                )
        def show_figure(n_clicks):
            if n_clicks!=None:
                if n_clicks%2==0:
                    return {'display':'inline'}
                else:
                    return {'display':'None'}
            ##inital display
            return {'display':'inline'}
    #########################
    def assignFigureCallback(self,figure_name,app):
        @app.callback(
                Output(self.title+':'+figure_name+'content','children'),
                [Input('buffer','children'),
                ## can change due to user interaction
                 Input('legend','value'),
                ## can change due to filter
                 Input('datatable', 'rows'),
                ## can change based on user interaction
                 Input('datatable', 'selected_row_indices')],
                )
        def update_figure_and_data_structure(children,legend_value,rows,selected_row_indices):
            ################ **Updating Data Structures** ##################
            global g_dict_of_param_dicts
            global g_legend_names
            g_dict_of_param_dicts = getParamDict(self.database_name,self.folder_name)
            g_legend_names = getLegendNames(g_dict_of_param_dicts)

            self.nameObjects_for_each_run = getNameObjects(self.title)
            self.figure_names = self.getFigureNames(self.nameObjects_for_each_run)
            ################ **Interacting with DataTable to get Selected Runs** ##################
            times_of_each_run = getSelectedRunsFromDatatable(rows,selected_row_indices)
            figure_content_for_this_name = self.getFigureContentForThisName(figure_name,times_of_each_run,legend_value)
            return figure_content

    def getFigureContentForThisName(self,figure_name,times_of_each_run,legend_value):
        '''
        figure_name is so we know figure info is pulled correctly
        times_of_each_run is so we know which runs to pull
        legend_value for formatting the figure
        '''
        raise NotImplementedError("Implement this function!")
    #########################
    def assignTabShowCallback(self,app):
        @app.callback(
                Output(self.title,'style'),
                [Input('tabs','value')]
                )
        def show_tab(value):
            if value == self.title:
                return {'display':'inline'}
            else:
                return {'display':'none'}

if __name__ == '__main__':
    database = Database()
    database.client['test_db']['test_collection'].insert_one({"Test":"test"})
    database.viewRun('test_db','test_collection')
    database.removeRun('test_db','test_collection')
    database.viewRun('test_db','test_collection')
