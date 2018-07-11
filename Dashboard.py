import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
from dash.dependencies import Input, Output, State
from DataLoader import getRunDicts
import ipdb
# import logging
# logging.basicConfig(level=logging.DEBUG)
# import plotly.graph_objs as go
from DashboardUtils import *
import sys
import plotly.graph_objs as go


################ **App Startup** ##################
app = dash.Dash(__name__)
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

################ **Global Variables** ##################
database_name='software_testing'
folder_name='lunarlander'
g_dict_of_param_dicts,g_dict_of_plot_dicts,g_dict_of_images,g_dict_of_histograms = getRunDicts(database_name,folder_name)
g_plot_names = getPlotNames(g_dict_of_plot_dicts)
g_legend_names = getLegendNames(g_dict_of_param_dicts)
g_inital_legend_name = g_legend_names[0]

################ **Layout Helper Functions** ##################
def createListOfButtonGraph(plot_names, legend_value):
    html_div_list=[]
    for plot in plot_names:
        button = html.Div([html.Div(html.Button(plot,id=plot+'button',className='active'),className='col-md-12')],className="row")
        html_div_list.append(button)

        graph = html.Div([html.Div(dcc.Graph(id=plot+'plot',figure=getInitialFigure(plot,legend_value)),className="col-md-12")],className="row",id=plot+'plotrow')
        html_div_list.append(graph)
    return html_div_list

def getInitialFigure(plot_name,legend_value):
    '''
    Gets the data for all the runs with the input plotiable name and plots them on one graph
    '''
    plot_for_each_run=[]
    for one_run_plots,one_run_params in zip(g_dict_of_plot_dicts.values(),g_dict_of_param_dicts.values()):
        # run_dict = {'y':one_run_plots[plot_name]}
        # plot_for_each_run.append(run_dict)

        scatter_obj = go.Scatter(
                y = list(one_run_plots[plot_name]),
                mode = 'lines',
                name = legend_value+":"+str(one_run_params[legend_value]),
                text = legend_value+":"+str(one_run_params[legend_value]),
                hoverinfo='text'
                )
        plot_for_each_run.append(scatter_obj)
    figure_dict= {'data':plot_for_each_run}
    return figure_dict

################ **Layout** ##################
app.layout = html.Div(
    [html.Div(
        [html.H1("Machine Learning Dashboard", className="text-center")]
    ,className="row")]+
    [html.Div(
        [html.Div(
            dcc.Checklist(
                id='autoupdateToggle',
                options=[{'label':'AutoUpdate','values':'On'}],
                values=[])
        ,className ='col-md-2'),
        html.Div(
             dcc.Interval(
                 id='interval',
                 interval=1*10_000,
                 n_intervals=0)
        ,className="col-md-1"),
        html.Div(
             html.Div(
                 "inital value",
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
        ,className="row",style={'display':'none'})]+
    [html.Div(
        [html.P("Debug Value",id='debug2',className="text-center")]
        ,className="row",style={'display':'none'})]+

    createListOfButtonGraph(g_plot_names,g_inital_legend_name)
, className="container-fluid")


################ **Assigning Callbacks** ##################
for plot_name in g_plot_names:
    # Display of Graphs
    @app.callback(
        Output(plot_name+'plotrow','style'),
        [Input(plot_name+'button', 'n_clicks')])
    def show_figure(n_clicks):
        if n_clicks!=None:
            if n_clicks%2==0:
                return {'display':'inline'}
            else:
                return {'display':'None'}
        ##inital display
        return {'display':'inline'}

    ## Graph data
    @app.callback(
    Output(plot_name+'plot', 'figure'),
    ## changes every n seconds if autoupdateToggle is checked
    [Input('buffer','children'),
    ## can change due to user interaction
     Input('legend','value'),
    ## can change due to filter
     Input('datatable', 'rows'),
    ## can change based on user interaction
     Input('datatable', 'selected_row_indices')],
    )
    def update_figure_and_python_dicts(children, legend_value, rows, selected_row_indices):
        ################ **Updating Global Variables** ##################
        global g_dict_of_param_dicts
        global g_dict_of_histograms
        global g_dict_of_images
        global g_dict_of_plot_dicts
        global g_legend_names
        global g_plot_names
        g_dict_of_param_dicts, g_dict_of_plot_dicts, g_dict_of_images, g_dict_of_histograms = getRunDicts(database_name,folder_name)
        g_plot_names = getPlotNames(g_dict_of_plot_dicts)
        g_legend_names = getLegendNames(g_dict_of_param_dicts)
       
        ################ **Interacting with DataTable to get Selected Runs** ##################
        times_of_each_run = getSelectedRunsFromDatatable(rows,selected_row_indices)
        ################ **Using DataFrame to Plot** ##################
        plot_for_each_run=[]
        ## creating the data dictionary for each run
        for time in times_of_each_run:
            one_run_plots = g_dict_of_plot_dicts[time]
            one_run_params = g_dict_of_param_dicts[time]
            # run_dict = {'y':list(filtered_df[plot_name])}
            scatter_obj = go.Scatter(
                    y = list(one_run_plots[plot_name]),
                    mode = 'lines',
                    name = legend_value+":"+str(one_run_params[legend_value]),
                    text = legend_value+":"+str(one_run_params[legend_value]),
                    hoverinfo='text'
                    )
            plot_for_each_run.append(scatter_obj)

        figure_dict= {'data':plot_for_each_run}
        return figure_dict

# Time toggle buffer
@app.callback(
        Output("buffer","children"),
        [Input("interval","n_intervals")],
        [State("autoupdateToggle","values")]
        )
def add_more_datapoints(n_intervals,values):
    if None in values:
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
        [Input("buffer",'children')]
        )
def printer(children):
    return "Debug Value 1:"+str(children)
@app.callback(
        Output('debug2','children'),
        [Input("datatable",'rows')],
        )
def printer(rows):
    # return str(children)+str(rows[14:])
    return "Debug Value 2:"+str(rows)
 
if __name__=='__main__':
    app.run_server(port=8000,debug=True)
    # div_list=createListOfButtonGraph(plot_name)
    # getFigure('Loss')
