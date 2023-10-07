from pathlib import Path
from dash import dcc
from dash import html

import dash_bootstrap_components as dbc

from app import app

from references import cite
from genome import descriptions as product_descriptions


def make_button(file):
    href = app.get_asset_url(file.as_posix().replace('assets/', ''))
    return dbc.Row(dbc.Col(dbc.Button(file.name, href=href, download=file.name, target='_blank', color='primary', outline=False, external_link=True, size='md'), className="d-grid gap-2"), class_name="mb-4")


def make_card_link(file, name=None, link_width=12):
    href = app.get_asset_url(file.as_posix().replace('assets/', ''))

    body = []
    if name:
        body.append(html.H4(name, className="card-title"))
    body.append(dbc.CardLink(file.name, href=href, target='_blank'))

    return dbc.Col(dbc.Card( dbc.CardBody( body ), color='light', outline=True), width=link_width, class_name="mb-4")


def make_accordion_item(title, description=None, pattern=None, buttons=None, names_dict={}, link_width=12):
    public = Path('assets/public-data')

    body = []

    if description:
        body.append(dcc.Markdown(description))

    if buttons is not None:
        files = list(public.glob(buttons))

        for file in files:
            body.append(make_button(file))

    if pattern is not None:
        files = list(public.rglob(pattern))
        files.sort()

        card_blocks = []
        for file in files:
            name = names_dict.get(file.stem)
            if not name:
                name = file.stem
            card_blocks.append(make_card_link(file, name=name, link_width=link_width))

        body.append(dbc.Row(card_blocks))
    return dbc.AccordionItem(body, title=title)
    

def make_accordion():
    gene_names = product_descriptions.set_index('ID')['Name'].to_dict()
    return dbc.Accordion([
        make_accordion_item('Preprocessed Data', 'This is the `description`.'),
        make_accordion_item('Protein Structures by AlphaFold', pattern='alphafold/*.pdb', buttons='structures/alphafold_pdbs.zip', link_width=4, names_dict=gene_names),
        make_accordion_item('Protein Structures from Uniprot', pattern='uniprot/*.pdb', buttons='structures/unipro_pdbs.zip', link_width=4, names_dict=gene_names),
    ],
    start_collapsed=True,)

menu = None

body = [
    dbc.Row(dbc.Col([html.H1("Downloadable Data")]), class_name='mb-4'),
    dbc.Row(dbc.Col(make_accordion())),
]

