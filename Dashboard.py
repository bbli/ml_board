import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
from dash.dependencies import Input, Output
from DataLoader import getTable
import ipdb
# import logging
# logging.basicConfig(level=logging.DEBUG)
# import plotly.graph_objs as go
from DashboardUtils import *


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
temp_df = df.drop(var_names,axis=1)
table_df = temp_df.groupby('Time').apply(selectFirst)
# ipdb.set_trace()

app.layout = html.Div(
    [html.Div(
        [html.H1("Machine Learning Dashboard", className="text-center")]
    ,className="row")]+
    [html.Div(
        [dt.DataTable(
            rows=table_df.to_dict('records'),
            # optional - sets the order of columns
            columns=sorted(table_df.columns),

            row_selectable=True,
            filterable=True,
            sortable=True,
            selected_row_indices=[],
            id='datatable-gapminder'
            )]
    ,className="row")]+
    [html.Div(
        [html.H1("Debug Value",id='debug',className="text-center")]
    ,className="row")]+
    createListOfButtonGraph(df,var_names)
    # +[html.Div([html.Div(html.Div(dcc.Graph(id=i)),className="col-md-8")])],className="row") for i in range(num_graphs)]
, className="container-fluid")

createButtonCallbacks(app,var_names)

@app.callback(
        Output('debug','children'),
        [Input('Advantagebutton','n_clicks')]
        )
def printer(n_clicks):
    if n_clicks!=None:
        return "Debug Value: "+str(n_clicks)
    else:
        return "None"
 
if __name__=='__main__':
    app.run_server(port=8000,debug=True)
    # div_list=createListOfButtonGraph(var_names)
    # getFigure('Loss')
