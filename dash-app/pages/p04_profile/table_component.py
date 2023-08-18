from dash import dcc
from dash import html

import plotly.graph_objects as go
import dash_bootstrap_components as dbc

table_columns=[
    {'name':             'Gene ID', 'type':    'alpha', 'header_style': {'width': '10%', 'minWidth': '140px'}, 'style': {'width': '10%', 'minWidth': '140px'}},
    {'name':                 'Deg', 'type':  'numeric', 'header_style': {'width':  '8%', 'minWidth':  '92px'}, 'style': {'width':  '8%', 'minWidth':  '92px', 'textAlign': 'right'}},
    {'name':                'ZVal', 'type':  'numeric', 'header_style': {'width':  '8%', 'minWidth':  '92px'}, 'style': {'width':  '8%', 'minWidth':  '92px', 'textAlign': 'right'}},
    {'name': 'Product Description', 'type':    'alpha', 'header_style': {}, 'style': {}},
    {'name':               'Phase', 'type':    'alpha', 'header_style': {'width': '10%', 'minWidth':  '90px'}, 'style': {'width': '10%', 'minWidth':  '90px'}},
]

def make_filter_popover(id_tag, name, input_component, delay_show=0, delay_hide=0, **kvargs):
    return html.Div([
        dbc.Button('Filter', id=f'{id_tag}-filter-{name}-toggle-button', color='primary', size='sm'),
        dbc.Popover(
            [
                dbc.PopoverBody([
                    html.P(id=f'{id_tag}-filter-{name}-form-message'),
                    input_component(id={'key': f'{id_tag}-filter', 'name': name}, **kvargs),
                ]),
            ],
            id=f'{id_tag}-filter-{name}-popover',
            target=f'{id_tag}-filter-{name}-toggle-button',
            trigger='legacy',
            delay={'show': delay_show, 'hide': delay_hide},
        ),
    ]),

# filter_inputs = {
#     'GeneID': dbc.Input(id='network-nodes-table-filter-GeneID', placeholder='Filter ...', size='sm'),
#     'degree':  make_filter_popover('', 'degree', dcc.RangeSlider, 10000, pushable=True, step=1),
#     'z.score': make_filter_popover('', 'zscore', dcc.RangeSlider, 10000, pushable=True, step=0.01),
#     'ProductDescription': dbc.Input(id='network-nodes-table-filter-ProductDescription', placeholder='Filter ...', size='sm'),
#     'phase': make_filter_popover('', 'phase', dbc.Checklist, 3000),
# }

class MyTable:
    def __init__(self, id_tag, table_columns, filter_inputs={}):
        self.id_tag = id_tag
        self.table_columns = table_columns

        self.table_header = [
            html.Tr([
                html.Th([
                    col['name'].replace('_', ' '), ' ',
                    html.Span([html.I(className="bi bi-sort-alpha-down sort-icon", id={'type': f'{self.id_tag}-sort-column-values', 'id': col['name']})])
                ], style=col['header_style'])
                for col in table_columns
            ]),
        ]

        filter_inputs = []
        for col in table_columns:
            match col['type']:
                case 'alpha':
                    filter_input = dbc.Input(id={'key': f'{id_tag}-filter', 'name': col['name']}, placeholder='Filter ...', size='sm')
                case 'numeric':
                    filter_input = make_filter_popover(self.id_tag, col['name'], dcc.RangeSlider, pushable=True, min=0, max=1, step=.1)
                case 'category':
                    filter_input = make_filter_popover(self.id_tag, col['name'], dbc.Checklist)
                case _:
                    filter_input = None
            filter_inputs.append(filter_input)

        self.table_header.append(html.Tr([ html.Th( filter_input ) for filter_input in filter_inputs ]))

    def get_layout(self):
        return [
                    dbc.Row(dbc.Col( dbc.Table([ html.Thead(self.table_header) ], id=f'{self.id_tag}-header', class_name='mb-0'))),
                    dbc.Row(dbc.Col(
                        dbc.Spinner([

                        dbc.Table(id=f'{self.id_tag}', hover=True),

                        ], id=f'loading-{self.id_tag}', type='border', fullscreen=False, color='primary', delay_hide=0,),
                    )),
                    dbc.Row([
                        dbc.Col([
                            dbc.Pagination(id=f'{self.id_tag}-pagination', active_page=1, max_value=2, first_last=True, previous_next=True, fully_expanded=False, size='sm', class_name='primary outline'),
                        ], width={'offset': 6, 'size': 4}, ),
                        dbc.Col([
                            html.Div(dbc.RadioItems(
                                id=f'{self.id_tag}-page-size-radio',
                                class_name="btn-group",
                                inputClassName="btn-check",
                                labelClassName="btn btn-sm btn-outline-primary",
                                labelCheckedClassName="active",
                                options=[
                                    {"label": " 5", "value": 5},
                                    {"label": "10", "value": 10},
                                    {"label": "20", "value": 20},
                                    {"label": "50", "value": 50},
                                ],
                                value=5,
                            ), className='radio-group'),
                        ], width={'size': 2}, ),
                    ]),
                ]
