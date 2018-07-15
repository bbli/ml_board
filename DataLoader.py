from pymongo import MongoClient
from logger_utils import Database
from board_utils import *
from datetime import datetime
import ipdb
import numpy as np
from io import BytesIO
from PIL import Image
import pickle
import base64

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
        dict_of_param_dicts[time]=Experimental_Parameters

        try:
            ## Graph Components need to index into a Time and then the variable
            Plots=run_object['Plots']
            dict_of_plot_dicts[time]=Plots
        except KeyError:
            pass
        try:
            Images = run_object['Images']
            # Images = {time:value[0] for key,value in Images.items()}
            Images = {image_name:getBase64Encoding(binary_image) for image_name,binary_image in Images.items()}
            ipdb.set_trace()
            dict_of_images[time]=Images
        except KeyError:
            pass
        try:
            Histograms = run_object['Histograms']
            dict_of_histograms[time]=Histograms
        except KeyError:
            pass

    return dict_of_param_dicts,dict_of_plot_dicts,dict_of_images,dict_of_histograms 

def getBase64Encoding(binary_image):
    numpy_matrix=pickle.loads(binary_image)
    img = Image.fromarray(np.uint8(numpy_matrix*255),'L')
    # base64_string= base64.b64encode(numpy_matrix)
    buff = BytesIO()
    img.save(buff, format="JPEG")
    base64_string = base64.b64encode(buff.getvalue())
    buff.close()
    return str(base64_string)[2:-1]


if __name__ == '__main__':
    import dash
    import dash_html_components as html
    dict_of_param_dicts,dict_of_plot_dicts,dict_of_images, dict_of_histograms = getRunDicts('software_testing','frozen_lake_image')
    plot_names = getPlotNames(dict_of_plot_dicts)
    legend_names = getLegendNames(dict_of_param_dicts)

    ## Testing Image
    app = dash.Dash()
    encoded_image = [image_dict['gradient'] for image_dict in dict_of_images.values()][0]

    app.layout = html.Div([
        html.Img(src='data:image/png;base64,{}'.format(encoded_image))
    ])
    app.run_server(debug=True)
