from dash import dcc
from dash import html

import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import plotly.express as px

from app import db
from .common import make_sc_plot, dclass_keys, dclass_names, discrete_colors


# read gene ids for all dclass
ids_set_list = [
    set(db.select(key, 'meta_gene_all_genes', cols=['GeneID']).GeneID.to_list())
    for key in dclass_keys]

ids_intersection = list(set.intersection(*ids_set_list))
ids_intersection.sort()
del(ids_set_list)

menu = [
    html.Br(),
    dbc.Label([
        "Select Gene:",
        dbc.Button("Example", id='pstime-gene-example-button', size='sm', color='primary', outline=True),
    ], html_for='pstime-gene-dropdown', style={'display': 'flex', 'justify-content': 'space-between'}),
    dcc.Dropdown(
        id='pstime-gene-dropdown',
        options=[{'label': g, 'value': g} for g in ids_intersection],
        value=None,
        placeholder='Search...'),
    html.Br(),
    html.Hr(),
    dbc.Accordion(dbc.AccordionItem([
        dbc.Label([ "Select CC Phase Color Palette:", ], html_for='p03-colorscale-dropdown'),
        dcc.Dropdown( id='p03-colorscale-dropdown', options=discrete_colors, value='Default', persistence=True, ),
    ], title='Customize'), start_collapsed=True, flush=True, ),
]


body = [
    html.H3('Pseudo-time Expression'),
    html.Div(id='pstime-graphs-container', children=[
        dbc.Row(dbc.Col(dbc.Card([
            dbc.CardHeader(html.H4(dclass_names[key])),
            dbc.CardBody(dbc.Row([
                dbc.Col([
                    dbc.Spinner([
                        dcc.Graph(
                            id={'type': 'pstime-expr-graph', 'key': key},
                            figure=make_sc_plot(key),
                            animate=False),
                    ], id=f'loading-pstime-expr-graph-{key}', type='border', fullscreen=False, color='primary', delay_hide=100,),
                ], width=6),
                dbc.Col([
                    dbc.Spinner([
                        dcc.Graph(
                            id={'type': 'pstime-expr-time-curve', 'key': key},
                            figure={'layout': { 'height': 450, "xaxis": { "visible": 'false' }, "yaxis": { "visible": 'false' }, } },),
                    ], id=f'loading-pstime-expr-time-curve-{key}', type='border', fullscreen=False, color='primary', delay_hide=100,),
                ], width=6),
            ])),
        ])), class_name="mb-4")
        for key in dclass_keys if key != 'bmic'
    ], style={'display': 'block'}),
]

