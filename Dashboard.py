import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from DataLoader import getTable
# import ipdb
# import logging
# logging.basicConfig(level=logging.DEBUG)

app = dash.Dash(__name__)
df,var_names = getTable('lunarlander')
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

app.layout = html.Div([
    html.Div(
        [html.H1("Machine Learning Dashboard", className="text-center")]
    ,className="row")]+
    [html.Div(
        [html.Div(
            [dcc.Graph(id='a'+str(i))]
        ,className="col-md-8")]
    ,className="row") for i in range(len(var_names))]
    # +[html.Div([html.Div(html.Div(dcc.Graph(id=i)),className="col-md-8")])],className="row") for i in range(num_graphs)]
, className="container-fluid")

# def table
 
if __name__=='__main__':
    app.run_server(debug=True)
