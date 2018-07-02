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
df,var_names = getTable('deep_learning','lunarlander')
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
            editable=False,
            selected_row_indices=[],
            id='datatable'
            )]
    ,className="row")]+

    [html.Div(
        [html.P("Debug Value",id='debug',className="text-center")]
    ,className="row")]+
    [html.Div(
        [html.P("Debug Value",id='debug2',className="text-center")]
    ,className="row")]+

    createListOfButtonGraph(df,var_names)
    # +[html.Div([html.Div(html.Div(dcc.Graph(id=i)),className="col-md-8")])],className="row") for i in range(num_graphs)]
, className="container-fluid")

for var in var_names:
    ## Button Toggle
    @app.callback(
        Output(var+'plotrow','style'),
        [Input(var+'button', 'n_clicks')])
    def update_figure(n_clicks):
        if n_clicks!=None:
            if n_clicks%2==0:
                return {'display':'inline'}
            else:
                return {'display':'None'}
        return {'display':'inline'}
    ## Table to Graph callback
    @app.callback(
    Output(var+'plot', 'figure'),
    ##rows can change due to filter
    [Input('datatable', 'rows'),
     Input('datatable', 'selected_row_indices')])
    def update_figure(rows, selected_row_indices):
        plot_for_each_run=[]
        if selected_row_indices==[]:
            selected_rows= rows
        else:
            selected_rows = [rows[i] for i in selected_row_indices]
        for run_dict in selected_rows:
            run_name=run_dict['Time']
            ##create dictionary
            filtered_df=df[df.Time==run_name]
            run_dict = {'y':list(filtered_df[var])}
            plot_for_each_run.append(run_dict)

        figure_dict= {'data':plot_for_each_run}
        return figure_dict


@app.callback(
        Output('debug','children'),
        [Input('datatable','rows')]
        )
def printer(rows):
    return "Debug Value 1:\n"+str(rows)

@app.callback(
        Output('debug2','children'),
        [Input('datatable','selected_row_indices')]
        )
def printer(rows):
    return "Debug Value 2:\n"+str(rows)
 
if __name__=='__main__':
    app.run_server(port=8000,debug=True)
    # div_list=createListOfButtonGraph(var_names)
    # getFigure('Loss')
