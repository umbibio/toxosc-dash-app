from dash import dcc
from dash import html

import plotly.graph_objects as go
import dash_bootstrap_components as dbc

from app import db

from .table_component import MyTable

scRNA_genes = db.select(dclass='scRNA', table='meta_gene_all_genes', cols=['GeneID']).GeneID
scATAC_genes = db.select(dclass='scATAC', table='meta_gene_all_genes', cols=['GeneID']).GeneID

gene_list = scRNA_genes.loc[scRNA_genes.isin(scATAC_genes)]

menu = [
    html.Br(),
    dbc.Label([
        "Select Gene A:",
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
    dcc.Slider(0.1, 1.5, .1, value=.1,
               marks={v: f"{v}%" for v in [.1, .5, 1.0, 1.5]},
               id='similar-profiles-distance-quantile'),
    html.Br(),
    dcc.Textarea(
        id="similar-profiles-similar-genes-list-textarea",
        value="",
        style={"height": 100, "display": "none"},
    ),
    dcc.Textarea(
        id="debug_info_textarea",
        value="",
        style={"height": 300, "width": "100%", "display": "none"},
    ),
]

genes_table = MyTable('similar-profiles-table',
    table_columns=[
        # {'name':           'Gene A ID', 'type':    'alpha', 'header_style': {'width': '10%', 'minWidth': '140px'}, 'style': {'width': '10%', 'minWidth': '140px'}},
        {'name':           'Gene B ID', 'type':    'alpha', 'header_style': {'width': '10%', 'minWidth': '140px'}, 'style': {'width': '10%', 'minWidth': '140px'}},
        {'name':            'RNA Dist', 'type':  'numeric', 'header_style': {'width': '10%', 'minWidth': '140px'}, 'style': {'width': '10%', 'minWidth': '140px', 'textAlign': 'right'}},
        {'name':           'ATAC Dist', 'type':  'numeric', 'header_style': {'width': '10%', 'minWidth': '140px'}, 'style': {'width': '10%', 'minWidth': '140px', 'textAlign': 'right'}},
        {'name':              'Symbol', 'type':    'alpha', 'header_style': {'width': '10%', 'minWidth': '140px'}, 'style': {'width': '10%', 'minWidth': '140px'}},
        {'name': 'Product Description', 'type':    'alpha', 'header_style': {}, 'style': {}},
    ]
)

body = [
    dcc.Store('similar-profiles-similar-genes-store'),
    dcc.Store('hovered_trace_gene_id', data={'hovering': None, 'curveNumber': None}),
    dcc.Store(id=f'{genes_table.id_tag}-sort-column-values-state', data=[0 for _ in genes_table.table_columns]),
    html.H3('Similar Expression Profiles'),
    dbc.Row([
            dbc.Col(
            dbc.Card([ dbc.CardHeader(html.H4(key.replace('_', ' '))),
            dbc.CardBody(dbc.Row([
                dbc.Col([
                    dbc.Spinner([
                        dcc.Graph(
                            id={'key': key, 'type': 'similar-profiles-expr-time-curve'},
                            figure={'layout': { 'height': 450, "xaxis": { "visible": 'true' }, "yaxis": { "visible": 'true' }, } },
                            clear_on_unhover=True, 
                        ),
                    ], id=f'loading-similar-profiles-expr-time-curve-{key}', type='border', fullscreen=False, color='primary', delay_hide=100,),
                ]),
            ])),
        ]))
        for key in ['RNA_Profile', 'ATAC_Profile']
    ], class_name="mb-4"),
    dbc.Row([dbc.Col([
        dbc.Card([
            dbc.CardHeader([
                html.H4('Genes with similar profiles'),

                html.Small([
                    'click the icon to copy the list of genes',
                    ' ',
                    dcc.Clipboard( target_id="similar-profiles-similar-genes-list-textarea", title="Copy list of genes", className='hover-cursor-pointer', style={ "display": "inline-block", "fontSize": 20, "verticalAlign": "bottom", "color": "var(--bs-primary)"}, ),
                ]),
            ]),
            dbc.CardBody(genes_table.get_layout(),),
        ]),
    ],)], class_name='mb-4'),
]

