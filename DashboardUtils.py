import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

def createListOfButtonGraph(df,var_names):
    html_div_list=[]
    for var in var_names:
        button = html.Div([html.Div(html.Button(var,id=var+'button'),className='col-md-8')],className="row")
        html_div_list.append(button)

        graph = html.Div([html.Div(dcc.Graph(id=var+'plot',figure=getFigure(df,var)),className="col-md-8")],className="row")
        html_div_list.append(graph)
    return html_div_list
def getFigure(df,var):
    '''
    Gets the data for all the runs with the input variable name and plots them on one graph
    '''
    run_names = df['Time'].unique()
    plot_for_each_run=[]
    for run in run_names:
        ##create dictionary
        filtered_df=df[df.Time==run]
        run_dict = {'y':list(filtered_df[var])}
        plot_for_each_run.append(run_dict)
    figure_dict= {'data':plot_for_each_run}
    return figure_dict

def createButtonCallbacks(app,var_names):
    for var in var_names:
        @app.callback(
            Output(var+'plot', 'figure'),
            [Input(var+'button', 'n_clicks')])
        def update_figure(selected_year):
            return figure_dictionary

from inspect import getsource
def code(function):
    print(getsource(function))
