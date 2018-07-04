import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

def createListOfButtonGraph(df,var_names):
    html_div_list=[]
    for var in var_names:
        button = html.Div([html.Div(html.Button(var,id=var+'button'),className='col-md-8')],className="row")
        html_div_list.append(button)

        graph = html.Div([html.Div(dcc.Graph(id=var+'plot',figure=getFigure(df,var)),className="col-md-8")],className="row",id=var+'plotrow')
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

def updateDataFrame(values):
    ## None will be in values if autoupdateToggle is on
    if None in values:
        # print("getting new df",file=sys.stdout)
        global df
        global var_names
        df,var_names = getTable(database_name,folder_name)

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
