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
################################################################

# num_graphs = len(df['Time'].unique())
database_name='software_testing'
folder_name='lunarlander'
dict_of_param_dicts,dict_of_plot_dicts,dict_of_images,dict_of_histograms,legend_values = getRunDicts(database_name,folder_name)
# ipdb.set_trace()

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
                 options=[{'label':param,'value':param} for param in legend_values],
                 # options=[{'label':"test","value":"test"}]
                 value=legend_values[0],
                 # labelStyle={'display': 'inline-block'}
                 )
         ,className='col-md-4')
         ]
     ,className='row')]+
    [html.Div(
        [dt.DataTable(
            rows= dict_of_param_dicts,
            # optional - sets the order of columns
            columns= legend_values,

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

    createListOfButtonGraph(df,var_names)
    # +[html.Div([html.Div(html.Div(dcc.Graph(id=i)),className="col-md-8")])],className="row") for i in range(num_graphs)]
, className="container-fluid")

################ **Assigning Callbacks** ##################
for var in var_names:
    ## Display of Graphs
    @app.callback(
        Output(var+'plotrow','style'),
        [Input(var+'button', 'n_clicks')])
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
    Output(var+'plot', 'figure'),
    ## changes every n seconds if autoupdateToggle is checked
    [Input('buffer','children'),
    ## can change due to user interaction
     Input('legend','value'),
    ## can change due to filter
     Input('datatable', 'rows'),
    ## can change based on user interaction
     Input('datatable', 'selected_row_indices')],
     [State(var+'plot','figure')]
    )
    def update_figure_and_python_dicts(children, legend_value, rows, selected_row_indices, figure):
        ################ **Updating DataFrame** ##################
        global dict_of_param_dicts
        global dict_of_histograms
        global dict_of_images
        global dict_of_plot_dicts
        global legend_values
        dict_of_param_dicts, dict_of_histograms, dict_of_images, dict_of_plot_dicts, legend_values = getRunDicts(database_name,folder_name)
       
        ################ **Interacting with DataTable to get Selected Runs** ##################
        times_of_each_run = getSelectedRunsFromDatatable(rows,selected_row_indices)
        ################ **Using DataFrame to Plot** ##################
        plot_for_each_run=[]
        ## creating the data dictionary for each run
        for time in times_of_each_run:
            one_run_plots = dict_of_plot_dicts[time]
            one_run_params = dict_of_param_dicts[time]
            # run_dict = {'y':list(filtered_df[var])}
            scatter_obj = go.Scatter(
                    y = list(one_run_plots[var]),
                    mode = 'lines',
                    name = legend_value+":"+str(one_run_params[legend_value]),
                    text = legend_value+":"+str(one_run_params[legend_value]),
                    hoverinfo='text'
                    )
            plot_for_each_run.append(scatter_obj)

        figure_dict= {'data':plot_for_each_run}
        return figure_dict

## Time toggle buffer
@app.callback(
        Output("buffer","children"),
        [Input("interval","n_intervals")],
        [State("autoupdateToggle","values")]
        )
def add_more_datapoints(n_intervals,values):
    if None in values:
        return "true"
    else:
        raise Exception

## Table data
@app.callback(
        Output("datatable","rows"),
        [Input('buffer','children')],
        )
def update_table(children):
    return dict_of_param_dicts
## Table columns
@app.callback(
        Output("datatable","columns"),
        [Input('buffer','children')],
        )
def update_table_columns(children):
    return legend_values


## Debug
@app.callback(
        Output('debug','children'),
        [Input("legend",'value')]
        )
def printer(rows):
    return "Debug Value 1:"+str(rows)

# @app.callback(
        # Output('debug2','children'),
        # [Input("debug",'children')],
        # [State("debug2","children")]
        # )
# def printer(rows,children):
    # return str(children)+str(rows[14:])
 
if __name__=='__main__':
    app.run_server(port=8000,debug=True)
    # div_list=createListOfButtonGraph(var_names)
    # getFigure('Loss')
