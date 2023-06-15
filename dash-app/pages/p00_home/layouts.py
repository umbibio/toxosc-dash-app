from dash import dcc
from dash import html

import dash_bootstrap_components as dbc

from references import cite


description = f'''
'''
# Welcome!
# This portal is related to {cite('name2023', markdown=True)}
# '''

contact = '''
For questions or comments please contact:

[ArriojasMaldonado001@umb.edu](mailto:ArriojasMaldonado001@umb.edu?Subject=About%20your%20ToxoSC%20web%20app)
'''


menu = None

body = [
    dbc.Row(dbc.Col(
        dbc.Card([
            dbc.CardHeader(html.H2("Toxo Single Cell Atlas")),
            dbc.CardBody(
                dbc.Row([
                    dbc.Col(dcc.Markdown(description),
                    width={'size': '6', 'offset': '0'}),
                # dbc.Col(
                #     dbc.Carousel(items=[
                #         {"key": "1", "src": "/appname/assets/carousel/1.png"},
                #         {"key": "2", "src": "/appname/assets/carousel/2.png"},
                #         {"key": "3", "src": "/appname/assets/carousel/3.png"},
                #     ], interval=5000, className="carousel-fade", indicators=False)),
                ])
            ),
        ],),
    ), class_name="mb-4 mt-4"),
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader(html.H4("Citation")),
            dbc.CardBody([
                cite('lou2023mpm', full=True)
            ]),
        ],),),
        dbc.Col(dbc.Card([
            dbc.CardHeader(html.H4("Contact")),
            dbc.CardBody(dcc.Markdown(contact)),
        ],),),
    ]),
]

