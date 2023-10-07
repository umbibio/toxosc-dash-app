from pathlib import Path
from dash import dcc
from dash import html

import dash_bootstrap_components as dbc

from app import app

from references import cite
from genome import descriptions as product_descriptions


def make_card_link(file, name=None, link_width=12):
    href = app.get_asset_url(file.as_posix().replace('assets/', ''))

    body = []
    if name:
        body.append(html.H4(name, className="card-title"))
    body.append(dbc.CardLink(file.name, href=href, target='_blank'))

    return dbc.Col(dbc.Card( dbc.CardBody( body ), color='light', outline=True), width=link_width, class_name="mb-4")


def make_accordion_item(pattern, title, description='', extra=[], names_dict={}, link_width=12):
    public = Path('assets/public-data')
    files = list(public.rglob(pattern))
    files.sort()

    body_content = []
    for file in files:
        name = names_dict.get(file.stem)
        if not name:
            name = file.stem
        body_content.append(make_card_link(file, name=name, link_width=link_width))

    return dbc.AccordionItem(dbc.Row(body_content), title=title)
    

def make_accordion():
    gene_names = product_descriptions.set_index('ID')['Name'].to_dict()
    return dbc.Accordion([
        make_accordion_item('alphafold/*.pdb', 'Protein Structures by AlphaFold', link_width=4, names_dict=gene_names),
        make_accordion_item('uniprot/*.pdb', 'Protein Structures from Uniprot', link_width=4, names_dict=gene_names),
    ],
    start_collapsed=True,)

menu = None

body = [
    dbc.Row(dbc.Col([html.H1("Downloadable Data")]), class_name='mb-4'),
    dbc.Row(dbc.Col(make_accordion())),
]

