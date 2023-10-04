import dash_bio as dashbio
from dash import dcc, html, Input, Output, callback
from dash.exceptions import PreventUpdate
import dash_bio.utils.ngl_parser as ngl_parser
from pathlib import Path
from dash_bio.utils import PdbParser, create_mol3d_style


data_path = Path("assets/public-data/structures/")


@callback(
    Output("molecule3d-viewer", 'modelData'),
    Output("molecule3d-viewer", 'styles'),
    Input("molecule-viewer-dropdown", "value")
)
def return_molecule(value):

    if (value is None):
        raise PreventUpdate

    pdb_path = data_path.joinpath(value).as_posix()
    parser = PdbParser(pdb_path)
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
