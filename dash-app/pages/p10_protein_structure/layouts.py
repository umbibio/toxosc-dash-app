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

parser = PdbParser(pdb_paths[0].as_posix())

data = parser.mol3d_data()
styles = create_mol3d_style( data['atoms'], visualization_type='cartoon' )

menu = [
    dcc.Dropdown(id='molecule-viewer-dropdown', options=[{'label': v, 'value': v} for v in src_pdb_pairs], value=src_pdb_pairs[0] ),
]

body = [
    dbc.Row(dbc.Col([html.H1("Protein Structure")])),
    dbc.Row(dbc.Col([dashbio.Molecule3dViewer( id='molecule3d-viewer', modelData=data, styles=styles, style={'width': '100%', 'height': '800px'}),])),
    # dashbio.NglMoleculeViewer(id="ngl-molecule-viewer", stageParameters={"backgroundColor": "lightgray"}),
    
]

