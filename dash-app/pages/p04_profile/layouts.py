from dash import dcc
from dash import html

import plotly.graph_objects as go
import dash_bootstrap_components as dbc

from app import db

scRNA_genes = db.select(dclass='scRNA', table='meta_gene_all_genes', cols=['GeneID']).GeneID
scATAC_genes = db.select(dclass='scATAC', table='meta_gene_all_genes', cols=['GeneID']).GeneID

gene_list = scRNA_genes.loc[scRNA_genes.isin(scATAC_genes)]

menu = [
    dcc.Store('similar-profiles-similar-genes-list-store'),
    html.Br(),
    dbc.Label([
        "Select Gene:",
        dbc.Button("Example", id='similar-profiles-gene-example-button', size='sm', color='primary', outline=True),
    ], html_for='similar-profiles-gene-dropdown', style={'display': 'flex', 'justify-content': 'space-between'}),
    dcc.Dropdown(id='similar-profiles-gene-dropdown', options=[
        {'label': gene, 'value': gene}
        for gene in gene_list
    ], placeholder='Search...'),
    html.Br(),
    dbc.Label([
        "Filter By:",
    ], html_for='similar-profiles-filter-by-selector'),
    dbc.RadioItems(
        options=[{'label': k, 'value': k} for k in ['RNA', 'ATAC', 'Both']],
        value='Both',
        inline=False,
        id='similar-profiles-filter-by-selector'),
    html.Br(),
    dbc.Label([
        "Closest Percentile:",
    ], html_for='similar-profiles-distance-quantile'),
    dcc.Slider(1, 25, 1, value=1,
               marks={v: f"{v}%" for v in [1, 5, 10, 15, 20, 25]},
               id='similar-profiles-distance-quantile'),
]

body = [
    html.H3('Similar Expression Profiles'),
    dbc.Row([
            dbc.Col(
            dbc.Card([ dbc.CardHeader(html.H4(key.replace('_', ' '))),
            dbc.CardBody(dbc.Row([
                dbc.Col([
                    dbc.Spinner([
                        dcc.Graph(
                            id={'type': 'similar-profiles-expr-time-curve', 'key': key},
                            figure={'layout': { 'height': 450, "xaxis": { "visible": 'false' }, "yaxis": { "visible": 'false' }, } },),
                    ], id=f'loading-similar-profiles-expr-time-curve-{key}', type='border', fullscreen=False, color='primary', delay_hide=100,),
                ]),
            ])),
        ]))
        for key in ['RNA_Profile', 'ATAC_Profile']
    ], class_name="mb-4"),
    dcc.Textarea(
        id="similar-profiles-similar-genes-list-textarea",
        value="",
        style={"height": 100},
    ),
    dcc.Clipboard(
        target_id="similar-profiles-similar-genes-list-textarea",
        title="Copy list of genes",
        style={
            "display": "inline-block",
            "fontSize": 20,
            "verticalAlign": "top",
        },
    ),
]

