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

def getLegendNames(dict_of_param_dicts):
    list_of_param_names = []
    for time,plot_dict in dict_of_param_dicts.items():
        list_of_param_names.append(plot_dict.keys())
    legend_names = sorted(set(list(itertools.chain(*list_of_param_names))))
    return legend_names

def getRunTitle(time):
    return html.Div(html.Button(time,id=time+'button',className='active'),className='row')

def getPlotlyFigureDict(histo_name,histo_values):
    histo_data = go.Histogram(x=histo_values,histnorm='probability')
    histo_layout = go.Layout(title=histo_name)
    figure_obj = go.Figure(data=histo_data,layout=histo_layout)
    ## Or 
    # figure_obj = {'data':go.Figure(data=histo_data,layout=histo_layout)}
    return figure_obj


def partial_decomaker(partial_name):
    def decorator(func):
        partial_func = partial(func,partial_name=partial_name)
        return partial_func
    return decorator

from inspect import getsource
def code(function):
    print(getsource(function))
