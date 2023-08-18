import pandas as pd
from dash import dcc
from dash import html

import plotly.express as px
import dash_bootstrap_components as dbc
import json
import urllib.request as urlreq
import dash_bio as dashbio

import sql_db as db
from references import cite

# import plotly.express as px
# annotations = pd.read_csv('./assets/ToxoDB-59_TgondiiME49.gtf', sep='\t', header=None, usecols=[0, 3, 4])
# annotations = annotations.loc[annotations[0].str.startswith('TGME49')]
# annotations[0] = annotations[0].str.replace('TGME49_', '')
# chr_end = annotations.groupby(0).max()[4]
# chr_ids = chr_end.index.to_list()
# chr_colors = px.colors.qualitative.Alphabet
# df = pd.DataFrame(zip(chr_ids, chr_ids, chr_colors, chr_end), columns=['id', 'label', 'color', 'len'], index=chr_ids)
# df = df.loc[[ 'chrIa', 'chrIb', 'chrII', 'chrIII', 'chrIV', 'chrV', 'chrVI', 'chrVIIa', 'chrVIIb', 'chrVIII', 'chrIX', 'chrX', 'chrXI', 'chrXII']]
# ToxoDB_59_TgondiiME49_chromosomes = df.to_dict('records')


ToxoDB_59_TgondiiME49_chromosomes = [
    {'id': 'chrIa',   'label': 'chrIa',   'color': '#FE00CE', 'len': 1858847},
    {'id': 'chrIb',   'label': 'chrIb',   'color': '#0DF9FF', 'len': 1916245},
    {'id': 'chrII',   'label': 'chrII',   'color': '#FD3216', 'len': 2300801},
    {'id': 'chrIII',  'label': 'chrIII',  'color': '#00FE35', 'len': 2456760},
    {'id': 'chrIV',   'label': 'chrIV',   'color': '#6A76FC', 'len': 2685352},
    {'id': 'chrV',    'label': 'chrV',    'color': '#F6F926', 'len': 3273806},
    {'id': 'chrVI',   'label': 'chrVI',   'color': '#FF9616', 'len': 3647018},
    {'id': 'chrVIIa', 'label': 'chrVIIa', 'color': '#EEA6FB', 'len': 4473859},
    {'id': 'chrVIIb', 'label': 'chrVIIb', 'color': '#DC587D', 'len': 5069556},
    {'id': 'chrVIII', 'label': 'chrVIII', 'color': '#479B55', 'len': 6917687},
    {'id': 'chrIX',   'label': 'chrIX',   'color': '#FED4C4', 'len': 6326364},
    {'id': 'chrX',    'label': 'chrX',    'color': '#D626FF', 'len': 7483912},
    {'id': 'chrXI',   'label': 'chrXI',   'color': '#6E899C', 'len': 6619062},
    {'id': 'chrXII',  'label': 'chrXII',  'color': '#00B5F7', 'len': 7071773},
]

layout_config = {"labels": {"display": True}, "ticks": {"display": False}}


scRNA_config = {
    "innerRadius": 0.5,
    "outerRadius": 0.95,
    "min": 0,
    "max": 6.5,
    "color": "red",
    "size": 20,
    "strokeWidth": 0,
    "axes": [{"spacing": 1, "thickness": 0.2, "color": "#666666"}],
    "backgrounds": [
        # {"start": 0, "end": 0.002, "color": "#f44336", "opacity": 0.5},
        # {"start": 0.006, "end": 0.015, "color": "#4caf50", "opacity": 0.5},
    ],
}

scATAC_config = {
    "innerRadius": 0.5,
    "outerRadius": 0.95,
    "min": 0,
    "max": 6.5,
    "color": "blue",
    "size": 20,
    "strokeWidth": 0,
}


circos_plot = dashbio.Circos(
    id='peak-expression-circos-plot',
    layout=ToxoDB_59_TgondiiME49_chromosomes,
    config=layout_config,
    tracks=[
        {
            "id": "scRNA",
            "type": "SCATTER",
            "data": [],
            "config": scRNA_config,
        },
        {
            "id": "scATAC",
            "type": "SCATTER",
            "data": [],
            "config": scATAC_config,
        },
    ],
)

available_periodic_genes = db.select(dclass='scATAC_scRNA', table='peak_expression_chromosome_location', cols=['GeneID']).GeneID

menu = [
    dbc.Row([dbc.Col([
        dbc.Label([
            "Select Genes:",
            dbc.Button("Example", id='peak-expression-gene-example-button', size='sm', color='primary', outline=True),
        ], html_for='peak-expression-gene-dropdown', style={'display': 'flex', 'justify-content': 'space-between'}),
        dcc.Dropdown(id='peak-expression-gene-dropdown', options=[
            {'label': gene, 'value': gene}
            for gene in available_periodic_genes
        ], placeholder='Search...', multi=True, style={ "overflow-y":"scroll", "height": "200px"}),
    ])], class_name='mb-4 mt-4'),
    dbc.Row([
        dbc.Col([ dbc.Button("Load List of Genes", id='peak-expression-gene-loader-button', size='sm', color='primary', outline=True),]),
        dbc.Col([ dbc.Button("Clear", id='gene-list-clear-button', size='sm', color='danger', outline=True),], class_name='text-end'),
    ]),
    dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Load list of genes")),
            dbc.ModalBody([
                dbc.Textarea(
                    id='peak-expression-gene-loader-modal-text-area',
                    rows=15,
                    size="sm",
                    className="mb-3",
                    placeholder="Paste a list of genes. Valid separators are spaces, commas, semicolons and line breaks.",
                ),
            ]),
            dbc.ModalFooter(
                dbc.Button(
                    "Load", id="peak-expression-gene-loader-modal-close-button", className="ms-auto", n_clicks=0
                )
            ),
        ],
        id="peak-expression-gene-loader-modal",
        is_open=False,
    ),
]

body = [
    dbc.Spinner([
        dcc.Graph(id='peak-expression-scatter-plot'),
    ], id=f'loading-peak-expression-scatter-plot', type='border', fullscreen=False, color='primary', delay_hide=100,),
]

example_list_of_genes = [
    'TGME49_235370',
    'TGME49_270200',
    'TGME49_226680',
    'TGME49_206710',
    'TGME49_226040',
    'TGME49_250690',
    'TGME49_243250',
    'TGME49_289880',
    'TGME49_281650',
    'TGME49_239800',
    'TGME49_315510',
    'TGME49_271270',
    'TGME49_313780',
    'TGME49_211280',
    'TGME49_298010',
    'TGME49_249440',
    'TGME49_251740',
    'TGME49_272640',
    'TGME49_235690',
    'TGME49_312580',
    'TGME49_257470',
    'TGME49_315220',
    'TGME49_314358',
    'TGME49_238420',
    'TGME49_268176',
    'TGME49_320030',
    'TGME49_203985',
    'TGME49_266630',
    'TGME49_254290',
    'TGME49_234260',
    'TGME49_254870',
    'TGME49_222100',
    'TGME49_221250',
    'TGME49_265080',
    'TGME49_209200',
    'TGME49_295125',
    'TGME49_293520',
    'TGME49_305590',
    'TGME49_204880',
    'TGME49_294560',
    'TGME49_245550',
    'TGME49_237190',
    'TGME49_268182',
    'TGME49_307020',
    'TGME49_276130',
    'TGME49_208910',
    'TGME49_312100',
    'TGME49_316290',
    'TGME49_310010',
    'TGME49_293440',
    'TGME49_224540',
    'TGME49_260580',
    'TGME49_314250',
    'TGME49_245475',
    'TGME49_209590',
    'TGME49_312300',
    'TGME49_282210',
    'TGME49_306350',
    'TGME49_231210',
    'TGME49_309150',
    'TGME49_245640',
    'TGME49_292300',
    'TGME49_272030',
    'TGME49_257370',
    'TGME49_239020',
    'TGME49_264420',
    'TGME49_201730',
    'TGME49_205662',
]
