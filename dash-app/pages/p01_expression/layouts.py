from dash import dcc
from dash import html

from plotly.colors import sample_colorscale, get_colorscale

import dash_bootstrap_components as dbc

from app import db



menu = [
    html.Br(),
    dbc.Label("Plot type", html_for='dimred-radio'),
    dbc.RadioItems(id='dimred-radio',
        options=[{'label': x, 'value': x} for x in ['PCA', 'UMAP']],
        value='PCA',
        inline=True),
    dbc.RadioItems(id='2d3d-radio',
        options=[{'label': x, 'value': x} for x in ['2D', '3D']],
        value='2D',
        inline=True),
    html.Br(),
    html.Div(id={'type': 'expression-gene-dropdown-container', 'dclass': 'scRNA'}, children=[
        dbc.Label([
            "Select Gene:",
            dbc.Button("Example", id={'type': 'expression-gene-example-button', 'dclass': 'scRNA'}, size='sm', color='primary', outline=True),
        ], html_for={'type': 'expression-gene-dropdown', 'dclass': 'scRNA'}, style={'display': 'flex', 'justify-content': 'space-between'}),
        dcc.Dropdown(id={'type': 'expression-gene-dropdown', 'dclass': 'scRNA'}, options=[
            {'label': gene, 'value': gene}
            for gene in db.select(dclass='scRNA', table='meta_gene_all_genes', cols=['GeneID']).GeneID
        ], placeholder='Search...'),
        
    ], style={'display': 'block'}),
    html.Br(),
    html.Div(id={'type': 'expression-gene-dropdown-container', 'dclass': 'scATAC'}, children=[
        dbc.Label([
            "Select Gene:",
            dbc.Button("Example", id={'type': 'expression-gene-example-button', 'dclass': 'scATAC'}, size='sm', color='primary', outline=True),
        ], html_for={'type': 'expression-gene-dropdown', 'dclass': 'scATAC'}, style={'display': 'flex', 'justify-content': 'space-between'}),
        dcc.Dropdown(id={'type': 'expression-gene-dropdown', 'dclass': 'scATAC'}, options=[
            {'label': gene, 'value': gene}
            for gene in db.select(dclass='scATAC', table='meta_gene_all_genes', cols=['GeneID']).GeneID
        ], placeholder='Search...'),
        
    ], style={'display': 'block'}),
]


body = [
    dbc.Row([
        dbc.Col([
            html.H3('scRNA'),
            dbc.Spinner([ dcc.Graph(
                id={'type': 'expression-graph', 'dclass': 'scRNA'}, 
                figure={'layout': { 'height': 700 } },
            )], type='border', fullscreen=False, color='primary', delay_hide=100, ),
   
        ], width=6),
        dbc.Col([
            html.H3('scATAC'),
            dbc.Spinner([ dcc.Graph(
                id={'type': 'expression-graph', 'dclass': 'scATAC'}, 
                figure={'layout': { 'height': 700 } },
            )], type='border', fullscreen=False, color='primary', delay_hide=100, ),
        ], width=6),
    ]),
]

