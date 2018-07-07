import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from DataLoader import getTable

def createListOfButtonGraph(df,var_names):
    html_div_list=[]
    for var in var_names:
        button = html.Div([html.Div(html.Button(var,id=var+'button',className='active'),className='col-md-12')],className="row")
        html_div_list.append(button)

        graph = html.Div([html.Div(dcc.Graph(id=var+'plot',figure=getInitialFigure(df,var)),className="col-md-12")],className="row",id=var+'plotrow')
        html_div_list.append(graph)
    return html_div_list

def getInitialFigure(df,var):
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

def getSelectedRunsFromDatatable(rows,selected_row_indices):
    if selected_row_indices==[]:
        selected_runs= rows
    else:
        selected_runs = [rows[i] for i in selected_row_indices]
    return [run_dict['Time'] for run_dict in selected_runs]

def selectFirst(df_slice):
    return df_slice.iloc[0]

from inspect import getsource
def code(function):
    print(getsource(function))
