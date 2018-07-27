import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import itertools
import ipdb
import plotly.graph_objs as go
from functools import partial

def getSelectedRunsFromDatatable(rows,selected_row_indices):
    if selected_row_indices==[]:
        selected_runs= rows
    else:
        selected_runs = [rows[i] for i in selected_row_indices]
    return [run_dict['Time'] for run_dict in selected_runs]

def getPlotNames(dict_of_plot_dicts):
    list_of_plot_names =[]
    for time,plot_dict in dict_of_plot_dicts.items():
        list_of_plot_names.append(plot_dict.keys())
    plot_names = sorted(set(list(itertools.chain(*list_of_plot_names))))
    return plot_names

def getHistogramNames(dict_of_histograms):
    list_of_histogram_names = []
    for histogram_dict in dict_of_histograms.values():
        list_of_histogram_names.append(histogram_dict.keys())
    histogram_names = sorted(set(list(itertools.chain(*list_of_histogram_names))))
    return histogram_names


def getLegendNames(dict_of_param_dicts):
    list_of_param_names = []
    for time,plot_dict in dict_of_param_dicts.items():
        list_of_param_names.append(plot_dict.keys())
    legend_names = sorted(set(list(itertools.chain(*list_of_param_names))))
    return legend_names

def getRunTitle(time):
    return html.Div(html.Button(time,id=time+'button',className='active'),className='row')

def getPlotlyFigureDict(histo_name,histo_values):
    histo_data = [go.Histogram(x=histo_values,histnorm='probability')]
    histo_layout = go.Layout(title=histo_name)
    figure_obj = go.Figure(data=histo_data,layout=histo_layout)
    ## Or 
    # figure_obj = {'data':go.Figure(data=histo_data,layout=histo_layout)}
    return figure_obj

def getHistogramComponentsForThisName(histo_name,dict_of_histograms_dicts):
        histogram_list = []
        for time,histograms_dict in dict_of_histograms_dicts.items():
            histo_values = histograms_dict[histo_name]
            figure_obj = getPlotlyFigureDict(time,histo_values)
            histo_component = html.Div(dcc.Graph(figure=figure_obj,id=time+':'+histo_name),className='col-md-4')
            histogram_list.append(histo_component)
        return histogram_list


def partial_decomaker(partial_name):
    def decorator(func):
        partial_func = partial(func,partial_name=partial_name)
        return partial_func
    return decorator

from inspect import getsource
def code(function):
    print(getsource(function))

class BaseTab():
    def __init__(self,title,nameObjects_for_each_run,paramObject_for_each_run):
        self.title = title
        self.nameObjects_for_each_run = nameObjects_for_each_run
        self.paramObject_for_each_run = paramObject_for_each_run
        self.figure_names = self.getFigureNames(self.nameObjects_for_each_run)

    @staticmethod
    def getFigureNames(nameObjects_for_each_run):
        list_of_names = []
        for time, one_run_dict in nameObjects_for_each_run.items():
            list_of_names.append(one_run_dict.keys())
        names = sorted(set(list(itertools.chain(*list_of_names))))
        return names
    #########################################
    def createHTMLStructure(self):
        html_row_list = []
        for figure_name in self.figure_names:
            button_row = html.Div(html.Button(name,id=figure_name+'button'),className='row')
            html_row_list.append(button)

            figure_row = html.Div(id=figure_name+'content')
            html_row_list.append(figure_row)
        return html.Div(html_row_list,id=self.title)
    def assignCallbacks(self,app):
        for figure_name in self.figure_names:
            self.assignShowCallback(figure_name,app)
            self.assignFigureCallback()
    ############################################# 
    @staticmethod
    def assignShowCallback(figure_name,app):
        @app.callback(
                ## Still Need to define this html structure
                Output(figure_name+'content','style'),
                [Input(figure_name+'button','n_clicks')]
                )
        def show_figure(n_clicks):
            if n_clicks!=None:
                if n_clicks%2==0:
                    return {'display':'inline'}
                else:
                    return {'display':'None'}
            ##inital display
            return {'display':'inline'}
    def assignFigureCallback(self,figure_name,app):
        @app.callback(
                Output(figure_name+'content','children'),
                [Input('buffer','children'),
                ## can change due to user interaction
                 Input('legend','value'),
                ## can change due to filter
                 Input('datatable', 'rows'),
                ## can change based on user interaction
                 Input('datatable', 'selected_row_indices')],
                )
        def update_figure_and_data_structure(children,legend_value,rows,selected_row_indices)
            ################ **Updating Data Structures** ##################
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

class PlotTab(BaseTab):
    def __init__(self,nameObjects_for_each_run,paramObject_for_each_run):
        super().__init__('Plots',nameObjects_for_each_run,paramObject_for_each_run)
    def getFigureContentForThisName(self,figure_name,times_of_each_run,legend_value):
        plot_for_each_run = []
        for time in times_of_each_run:
            one_run_plots = self.nameObjects_for_each_run[time]
            one_run_params = g_dict_of_param_dicts[time]
            # run_dict = {'y':list(filtered_df[plot_name])}
            scatter_obj = self.createScatterObject(figure_name,one_run_plots,one_run_params,legend_value)
            plot_for_each_run.append(scatter_obj)

        data_dict= {'data':plot_for_each_run}
        figure_object = dcc.Graph(id=figure_name+'plot',figure=data_dict)
        return html.Div(html.Div(figure_object,className='col-md-12'),className='row')
    @staticmethod
    def createScatterObject(name,one_run_plots,one_run_params,legend_value):
        label = legend_value+':'+str(one_run_params[legend_value])
        return go.Scatter(
                y = list(one_run_plots[name]),
                mode = 'lines',
                name = label,
                text = label,
                hoverinfo='text'
                )

class HistogramTab(BaseTab):
    def __init__(self,nameObjects_for_each_run,paramObject_for_each_run):
        super().__init__('Histograms',nameObjects_for_each_run,paramObject_for_each_run)
    def getFigureContentForThisName(self,figure_name,times_of_each_run,legend_value):
        histo_component_list = []
        for time in times_of_each_run:
            one_run_histogram = self.nameObjects_for_each_run[time]
            one_run_params = g_dict_of_param_dicts[time]

            histo_component = createHistogramComponent(figure_name,one_run_histogram,one_run_params,legend_value)
            histo_component_list.append(histo_component)

        return html.Div(histo_component_list,className='row')
    @staticmethod
    def createHistogramComponent(figure_name,one_run_histogram,one_run_params,legend_value):
        ################ **Creating Data Object** ##################
        one_run_values = one_run_histogram[figure_name]
        histo_data = [go.Histogram(x=one_run_values,histnorm='probability')]
        label = legend_value+':'+str(one_run_params[legend_value])
        histo_layout = go.Layout(title=label)
        data_obj = go.Figure(data=histo_data,layout=histo_layout)
        ##################################################

        figure_object = dcc.Graph(id=time+'_'+figure_name+' Histogram',figure= data_dict)
        return html.Div(figure_object,className='col-md-4')
        

class ImageTab(BaseTab):
    def __init__(self,nameObjects_for_each_run,paramObject_for_each_run):
        super().__init__('Images',nameObjects_for_each_run,paramObject_for_each_run)
    def getFigureContentForThisName(self,figure_name,times_of_each_run,legend_value):
        html_row_objects = []
        ################ **Creating the Components** ##################
        title_component_list =[]
        image_component_list = []
        for time in times_of_each_run:
            one_run_images = self.nameObjects_for_each_run[time]
            one_run_params = g_dict_of_param_dicts[time]

            image_component = createImageComponent(figure_name,one_run_images)
            image_component_list.append(image_component)
            title_component = createTitleComponent(one_run_params,legend_value)
            title_component_list.append(title_component)
        ################ **Creating the two Row Objects** ##################
        image_title_row = html.Div(image_title_components,className='row')
        html_row_objects.append(image_title_row)
        image_component_row = html.Div(image_content_components,className='row')
        html_row_objects.append(image_component_row)
        return html_row_objects
    @staticmethod
    def createImageComponent(figure_name,one_run_image):
        base64_image = one_run_image[figure_name]
        figure_object = html.Img(src='data:image/png;base64,{}'.format(base64_image),className='center-block')
        return html.Div(figure_object,className='col-md-6')
    @staticmethod
    def createTitleComponent(one_run_params,legend_value):
        label = legend_value+':'+str(one_run_params[legend_value])
        image_title = html.H4(label,className='text-center')
        return html.Div(image_title,'col-md-6')

