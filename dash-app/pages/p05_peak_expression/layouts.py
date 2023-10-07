from dash import dcc
from dash import html

import dash_bootstrap_components as dbc

import sql_db as db
from references import cite


available_periodic_genes = db.select(dclass='scATAC_scRNA', table='peak_expression_chromosome_location', cols=['GeneID']).GeneID

menu = [
    html.Br(),
    dbc.Row([
        dbc.Col([ dbc.Button("Load List of Genes", id='peak-expression-gene-loader-button', size='sm', color='primary', outline=True),]),
        dbc.Col([ dbc.Button("Clear", id='gene-list-clear-button', size='sm', color='danger', outline=True),], class_name='text-end'),
    ]),
    dbc.Row([dbc.Col([
        dbc.Label([
            "Select Genes:",
            dbc.Button("Example", id='peak-expression-gene-example-button', size='sm', color='primary', outline=True),
        ], html_for='peak-expression-gene-dropdown', style={'display': 'flex', 'justify-content': 'space-between'}),
        dcc.Dropdown(id='peak-expression-gene-dropdown', options=[
            {'label': gene, 'value': gene}
            for gene in available_periodic_genes
        ], placeholder='Search...', multi=True),
    ])], class_name='mb-4 mt-4'),
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
