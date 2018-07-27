import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
from dash.dependencies import Input, Output, State
import ipdb
from utils import *
import plotly.graph_objs as go


################ **App Startup** ##################
app = dash.Dash(__name__)
app.title = "Machine Learning Dashboard"
# Boostrap CSS.
app.css.append_css({
    "external_url": "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
})

# Extra Dash styling.
app.css.append_css({
    "external_url": 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

# JQuery is required for Bootstrap.
app.scripts.append_script({
    "external_url": "https://code.jquery.com/jquery-3.2.1.min.js"
})

# Bootstrap Javascript.
app.scripts.append_script({
    "external_url": "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"
})

################ **Components** ##################
class PlotTab(BaseTab):
    def __init__(self,database_name,folder_name):
        title = 'Plots'
        f = None
        super().__init__(database_name,folder_name,title,f)
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
    def __init__(self,database_name,folder_name):
        title = 'Histograms'
        f = None
        super().__init__(database_name,folder_name,title,f)
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
    def __init__(self,database_name,folder_name):
        title = 'Images'
        f = getBase64Encoding
        super().__init__(database_name,folder_name,title,f)
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

################ **Global Variables** ##################
database_name='software_testing'
# folder_name='lunarlander'
folder_name = 'frozen_lake_thoughts'
plotTab_object = PlotTab(database_name,folder_name)
histoTab_object = HistogramTab(database_name,folder_name)
imageTab_object = ImageTab(database_name,folder_name)

g_dict_of_param_dicts = getParamDict(database_name,folder_name)
g_legend_names = getLegendNames(g_dict_of_param_dicts)
g_inital_legend_name = g_legend_names[0]

g_tab_names = [plotTab_object.title,histoTab_object.title,imageTab_object.title]

################ **Layout** ##################
app.layout = html.Div(
    [html.Div(
        [html.H1("Machine Learning Dashboard", className="text-center")]
    ,className="row")]+
    [html.Div(
        [html.Div(
            dcc.Checklist(
                id='autoupdateToggle',
                options=[{'label':'AutoUpdate','value':'On'}],
                values=['On'])
        ,className ='col-md-2'),
        html.Div(
             dcc.Interval(
                 id='interval',
                 interval=1*10_000,
                 n_intervals=0)
        ,className="col-md-1"),
        html.Div(
             html.Div(
                 style={'display':"none"},
                 id='buffer')
        ,className="col-md-5"),
         html.Div(
             dcc.Dropdown(
                 id='legend',
                 options=[{'label':param,'value':param} for param in g_legend_names],
                 # options=[{'label':"test","value":"test"}],
                 value = g_inital_legend_name,
                 # labelStyle={'display': 'inline-block'}
                 )
         ,className='col-md-4')
         ]
     ,className='row')]+
    [html.Div(
        [dt.DataTable(
            rows= [value for key,value in g_dict_of_param_dicts.items()],
            # optional - sets the order of columns
            columns= g_legend_names,

            row_selectable=True,
            filterable=True,
            sortable=True,
            editable=False,
            selected_row_indices=[],
            id='datatable'
            )]
    ,className="row")]+

    [html.Div(
        [html.P("Debug Value",id='debug',className="text-center")]
    ,className="row",)]+#style={'display':'none'})]+
    [html.Div(
        [html.P("Debug Value",id='debug2',className="text-center")]
    ,className="row",style={'display':'none'})]+
    [html.Div(
        dcc.Tabs(
            tabs=[{'label': '{}'.format(name), 'value': name} for name in g_tab_names],
            value=g_tab_names[0],
            id='tabs'
        )
    ,className="row")]
    +[plotTab_object.createHTMLStructure()]
    +[imageTab_object.createHTMLStructure()]
    +[histoTab_object.createHTMLStructure()]
, className="container-fluid")


################ **Assigning Callbacks** ##################
plotTab_object.assignCallbacks(app)
imageTab_object.assignCallbacks(app)
histoTab_object.assignCallbacks(app)

# Time toggle buffer
@app.callback(
        Output("buffer","children"),
        [Input("interval","n_intervals")],
        [State("autoupdateToggle","values")]
        )
def add_more_datapoints(n_intervals,values):
    if 'On' in values:
        return "changed"
    else:
        raise Exception

## Table data
@app.callback(
        Output("datatable","rows"),
        [Input('buffer','children')],
        )
def update_table(children):
    rows= [value for key,value in g_dict_of_param_dicts.items()]
    # print("line break")
    # print(type(rows))
    return rows
## Table columns
@app.callback(
        Output("datatable","columns"),
        [Input('buffer','children')],
        )
def update_table_columns(children):
    return g_legend_names

## Debug
@app.callback(
        Output('debug','children'),
        [Input('buffer','children')]
        )
def printer(children):
    return "Debug Value 1:"+str(children)
# @app.callback(
        # Output('debug2','children'),
        # [Input("datatable",'rows')],
        # )
# def printer(rows):
    # # return str(children)+str(rows[14:])
    # return "Debug Value 2:"+str(rows)
 
if __name__=='__main__':
    app.run_server(port=8000,debug=True)
    # div_list=createListOfButtonGraph(plot_name)
    # getFigure('Loss')
