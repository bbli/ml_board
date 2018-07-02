import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

def createListOfButtonGraph(df,var_names):
    html_div_list=[]
    for var in var_names:
        button = html.Div([html.Div(html.Button(var,id=var+'button'),className='col-md-8')],className="row")
        html_div_list.append(button)

        graph = html.Div([html.Div(dcc.Graph(id=var+'plot'),className="col-md-8")],className="row",id=var+'plotrow')
        html_div_list.append(graph)
    return html_div_list

def selectFirst(df_slice):
    return df_slice.iloc[0]

from inspect import getsource
def code(function):
    print(getsource(function))
