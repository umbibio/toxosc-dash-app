from datetime import datetime

import re
import pandas as pd
from dash.exceptions import PreventUpdate

from dash import callback_context as ctx
from dash.dependencies import Input, Output, State, MATCH
import plotly.express as px
import plotly.graph_objects as go
from plotly.colors import sample_colorscale, get_colorscale

from app import app, db

from .layouts import scRNA_config, scATAC_config, available_periodic_genes, example_list_of_genes


# @app.callback(
#     Output('peak-expression-circos-plot', 'tracks'),
#     Input('peak-expression-gene-dropdown', 'value') )
def update_circos_plot(selected_genes):
    if not selected_genes:
        return []

    df = db.select('scATAC_scRNA', 'peak_expression_chromosome_location', where={'GeneID': selected_genes})
    df['block_id'] = df['chromosome']
    df['position'] = (df['start'] + df['end']) / 2
    scRNA_data = df.rename(columns={'peak.ord.rna': 'value'}).loc[:,['block_id', 'position', 'value']].to_dict('records')
    scATAC_data = df.rename(columns={'peak.ord.atac': 'value'}).loc[:,['block_id', 'position', 'value']].to_dict('records')

    return [
        {
            "id": "scRNA",
            "type": "SCATTER",
            "data": scRNA_data,
            "config": scRNA_config,
        },
        {
            "id": "scATAC",
            "type": "SCATTER",
            "data": scATAC_data,
            "config": scATAC_config,
        },
    ]


@app.callback(
    Output('peak-expression-scatter-plot', 'figure'),
    Input('peak-expression-gene-dropdown', 'value') )
def update_graph(selected_genes):
    if not selected_genes:
        fig = go.Figure(layout={"xaxis": { "visible": False }, "yaxis": { "visible": False }})
        fig.update_layout({"annotations": [
            {
                "text": "Select genes to visualize their expression peak times.",
                "xref": "paper",
                "yref": "paper",
                "showarrow": False,
                "font": {
                    "size": 16
                }
            }
        ]})

    else:
        df = db.select('scATAC_scRNA', 'peak_expression_chromosome_location', where={'GeneID': selected_genes})
        df = df.rename(columns={'peak.ord.atac': 'ATAC', 'peak.ord.rna': 'RNA', 'dclass': 'Data Class'})
        dff = df.melt(id_vars=['GeneID'], value_vars=['ATAC', 'RNA'], var_name='Data Class', value_name='time')

        fig = px.bar(dff, base='time', x=[.1] * len(dff), y='GeneID', color='Data Class', orientation='h', barmode='group', )
        fig.update_traces(hovertemplate="<br>".join([ "GeneID: %{y}", "peak time: %{base:.2f} hr", ]))
        fig.layout.xaxis.range = [0, 6.2]
        fig.layout.xaxis.title = 'peak time (hr)'
        fig.update_layout({"height": max(500, 200 + 7 * len(dff))})

    return fig


@app.callback(
    Output('peak-expression-gene-dropdown', 'value'),
    Output('peak-expression-gene-loader-modal-text-area', 'value'),
    Input("peak-expression-gene-loader-modal-close-button", "n_clicks"),
    Input("gene-list-clear-button", "n_clicks"),
    Input("peak-expression-gene-example-button", "n_clicks"),
    State('peak-expression-gene-loader-modal-text-area', 'value'),
    State('peak-expression-gene-dropdown', 'value'), )
def load_list_of_genes(n_clicks_modal, n_clicks_clear, n_clicks_example, textarea_content, selected_genes):

    trigger = ctx.triggered[0]['prop_id'].split('.')[0]
    match trigger:
        case 'gene-list-clear-button':
            return [], None
        case 'peak-expression-gene-example-button':
            return example_list_of_genes, None
        case _:
            pass

    if not selected_genes:
        selected_genes = []
    if not textarea_content:
        textarea_content = ''
    loaded_genes = re.sub('[,; \n]', ' ', textarea_content).split()

    return list(set(selected_genes + loaded_genes).intersection(available_periodic_genes)), None


@app.callback(
    Output("peak-expression-gene-loader-modal", "is_open"),
    Input ("peak-expression-gene-loader-button", "n_clicks"),
    Input ("peak-expression-gene-loader-modal-close-button", "n_clicks"),
    State ("peak-expression-gene-loader-modal", "is_open"), )
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open
