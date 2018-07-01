import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from DataLoader import getTable
import ipdb
# import logging
# logging.basicConfig(level=logging.DEBUG)
# import plotly.graph_objs as go


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
df,var_names = getTable('lunarlander')

def createListOfButtonGraph(var_names):
    html_div_list=[]
    for var in var_names:
        button = html.Div([html.Div(html.Button(var,id=var+'button'),className='col-md-8')],className="row")
        html_div_list.append(button)

        graph = html.Div([html.Div(dcc.Graph(id=var+'plot',figure=getFigure(var)),className="col-md-8")],className="row")
        html_div_list.append(graph)
    return html_div_list

def getFigure(var):
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


app.layout = html.Div([
    html.Div(
        [html.H1("Machine Learning Dashboard", className="text-center")]
    ,className="row")]+
    createListOfButtonGraph(var_names)
    # +[html.Div([html.Div(html.Div(dcc.Graph(id=i)),className="col-md-8")])],className="row") for i in range(num_graphs)]
, className="container-fluid")


 
if __name__=='__main__':
    app.run_server(debug=True)
    # div_list=createListOfButtonGraph(var_names)
    # getFigure('Loss')
