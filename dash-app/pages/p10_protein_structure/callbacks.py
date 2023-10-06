from pathlib import Path
import dash_bio as dashbio
from dash import dcc, html, Input, Output, callback
from dash.exceptions import PreventUpdate
import dash_bio.utils.ngl_parser as ngl_parser
import dash_bootstrap_components as dbc
from dash_bio.utils import PdbParser, create_mol3d_style

from app import app

from genome import descriptions as product_descriptions
product_descriptions = product_descriptions.set_index('ID')

data_path = Path("assets/public-data/structures/")


@callback(
    Output('protein-structure-info-table-container', 'children'),
    Input('molecule-viewer-dropdown', 'value'),
)
def populate_protein_info_table(value):

    if (value is None):
        raise PreventUpdate

    pdb_path = data_path.joinpath(value)
    pdb_href = app.get_asset_url(f"public-data/structures/{value}")
    
    gene_id = pdb_path.stem
    description = product_descriptions.loc[gene_id] if gene_id in product_descriptions.index else {}

    table_content = [
        ("Gene ID", gene_id),
        ("Gene Symbol", description.get('Name')),
        ("Description", description.get('description')),
        ("Download link", html.A(pdb_href, href=pdb_href, target="_blank")),
    ]

    table_body = [
        html.Tbody([html.Tr([html.Td(v[0]), html.Td(v[1])])
        for v in table_content])
    ]

    return dbc.Table(table_body, bordered=True, dark=False, hover=False, responsive=True, striped=True, size='sm')


@callback(
    Output("molecule3d-viewer", 'modelData'),
    Output("molecule3d-viewer", 'styles'),
    Input("molecule-viewer-dropdown", "value")
)
def return_molecule(value):

    if (value is None):
        raise PreventUpdate

    pdb_path = data_path.joinpath(value)
    parser = PdbParser(pdb_path.as_posix())
    data = parser.mol3d_data()
    styles = create_mol3d_style( data['atoms'], visualization_type='cartoon' )

    return data, styles


# @callback(
#     Output("ngl-molecule-viewer", 'data'),
#     Output("ngl-molecule-viewer", "molStyles"),
#     Input("molecule-viewer-dropdown", "value")
# )
# def return_molecule(value):

#     if (value is None):
#         raise PreventUpdate

#     molstyles_dict = {
#         "representations": ["cartoon", "axes+box"],
#         "chosenAtomsColor": "white",
#         "chosenAtomsRadius": 1,
#         "molSpacingXaxis": 100,
#     }

#     src, pdb_id = value.split("/")
#     data_list = [ngl_parser.get_data(data_path=data_path + src + '/', pdb_id=pdb_id, color='red',reset_view=True)]
#     print(data_list)

#     return data_list, molstyles_dict
