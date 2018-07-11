import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import itertools
import ipdb

def createListOfButtonGraph(dict_of_plot_dicts,plot_names):
    html_div_list=[]
    for plot in plot_names:
        button = html.Div([html.Div(html.Button(plot,id=plot+'button',className='active'),className='col-md-12')],className="row")
        html_div_list.append(button)

        graph = html.Div([html.Div(dcc.Graph(id=plot+'plot',figure=getInitialFigure(dict_of_plot_dicts,plot)),className="col-md-12")],className="row",id=plot+'plotrow')
        html_div_list.append(graph)
    return html_div_list

def getInitialFigure(dict_of_plot_dicts,plot):
    '''
    Gets the data for all the runs with the input plotiable name and plots them on one graph
    '''
    plot_for_each_run=[]
    for time,one_run_dict in dict_of_plot_dicts.items():
        run_dict = {'y':one_run_dict[plot]}
        plot_for_each_run.append(run_dict)
    figure_dict= {'data':plot_for_each_run}
    return figure_dict

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

def getLegendNames(dict_of_param_dicts):
    list_of_param_names = []
    for time,plot_dict in dict_of_param_dicts.items():
        list_of_param_names.append(plot_dict.keys())
    legend_names = sorted(set(list(itertools.chain(*list_of_param_names))))
    return legend_names
from inspect import getsource
def code(function):
    print(getsource(function))
