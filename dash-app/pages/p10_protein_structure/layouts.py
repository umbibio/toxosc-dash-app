import dash_bio as dashbio
from dash_bio.utils import PdbParser, create_mol3d_style

from dash import dcc
from dash import html
from glob import glob
from pathlib import Path

import dash_bootstrap_components as dbc

data_path = Path("assets/public-data/structures")

pdb_paths = list(data_path.rglob("*.pdb"))
pdb_paths.sort()

src_pdb_pairs = [f"{p.parent.name}/{p.name}" for p in pdb_paths]

initial_protein = pdb_paths[0]
parser = PdbParser(initial_protein.as_posix())

data = parser.mol3d_data()
styles = create_mol3d_style( data['atoms'], visualization_type='cartoon' )

menu = [
    html.Br(),
    dbc.Label([
        "Select PDB:",
    ], html_for='molecule-viewer-dropdown'),
    dcc.Dropdown(id='molecule-viewer-dropdown', options=[{'label': v, 'value': v} for v in src_pdb_pairs], value=src_pdb_pairs[0] ),
]

body = [
    dbc.Row(dbc.Col([html.H1("Protein Structure Visualization")])),
    dbc.Row(dbc.Col(dbc.Card([
        dbc.CardHeader(html.H4(id='molecule-viewer-card-header', children=initial_protein.name)),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([], id='protein-structure-info-table-container', width=12),
                dbc.Col([
                    dbc.Spinner([
                        dashbio.Molecule3dViewer( id='molecule3d-viewer', modelData=data, styles=styles, style={'width': '100%', 'height': '600'}),
                    ], id=f'loading-protein-structure-visualization', type='border', fullscreen=False, color='primary', delay_hide=100,),
                ], width=12),
            ]),
        ]),
    ])), class_name="mb-4 mt-4"),

    # dbc.Row(dbc.Col([dashbio.Molecule3dViewer( id='molecule3d-viewer', modelData=data, styles=styles, style={'width': '100%', 'height': '800px'}),])),
    # dashbio.NglMoleculeViewer(id="ngl-molecule-viewer", stageParameters={"backgroundColor": "lightgray"}),
    
]

