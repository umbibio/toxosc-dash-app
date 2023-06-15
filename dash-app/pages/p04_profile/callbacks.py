from datetime import datetime

import pandas as pd
from dash.exceptions import PreventUpdate

from dash import callback_context as ctx
from dash.dependencies import Input, Output, State, MATCH
import plotly.express as px
import plotly.graph_objects as go
from plotly.colors import sample_colorscale, get_colorscale

from app import app, db


@app.callback(
    Output('similar-profiles-similar-genes-list-store', 'data'),
    Output('similar-profiles-similar-genes-list-textarea', 'value'),
    Input('similar-profiles-gene-dropdown', 'value'),
    Input('similar-profiles-filter-by-selector', 'value'),
    Input('similar-profiles-distance-quantile', 'value'), )
def update_similar_genes_list(gene_id, filter_by, quantile_pct):
    if filter_by and gene_id:
        quantile = quantile_pct / 100
        quantile_col = f"q{quantile:.3f}"

        similar_genes = set()
        for dclass in ['scRNA', 'scATAC']:
            if not filter_by in dclass and not filter_by == 'Both':
                continue

            # TODO: Fix gene names in database. Should have '_' instead of '-'

            quantile_thr = db.select(
                dclass=dclass,
                table='spline_fit_distance_quantiles_v2',
                cols=[quantile_col],
                where=dict(GeneID=gene_id.replace('_', '-'))).iloc[0, 0]
            

            dclass_similar_genes = db.select(
                dclass=dclass,
                table='spline_fit_distance_matrix_v2',
                cols=['GeneID.2'],
                where=[
                    {
                        'GeneID.1': gene_id.replace('_', '-'),
                        'distance': {quantile_thr: '<'},
                    },
                ],
                verbose=False)['GeneID.2'].str.replace('-', '_')

            if similar_genes:
                similar_genes.intersection(dclass_similar_genes)
            else:
                similar_genes = set(dclass_similar_genes)

        return list(similar_genes), '\n'.join(list(similar_genes))

    else:
        raise PreventUpdate


@app.callback(
    Output({'type': 'similar-profiles-expr-time-curve', 'key': MATCH}, 'figure'),
    Input('similar-profiles-similar-genes-list-store', 'data'),
    State({'type': 'similar-profiles-expr-time-curve', 'key': MATCH}, 'id'), )
def update_time_curve_plots(similar_genes, id):
    dclass = 'scRNA' if id['key'].startswith('RNA') else 'scATAC'

    fig = go.Figure(layout={'height': 450, "xaxis": { "visible": False }, "yaxis": { "visible": False }, 'margin': {'l':20, 'r':20, 't':60, 'b':60}})

    if dclass and similar_genes:

        df = db.select(
            dclass=dclass,
            table='spline_fit_all_genes',
            cols=['GeneID', 'x', 'expr'],
            # cols=['GeneID', 'x', 'expr', 'lb', 'ub'],
            where={ 'GeneID': similar_genes },
            verbose=False)

        for similar_gene_id in similar_genes:
            dff = df.query("GeneID == @similar_gene_id")


            fig.add_trace( go.Scatter(x=dff['x'], y=dff['expr'], mode='lines', name=similar_gene_id))
            # fig.add_trace( go.Scatter(x=dff['t'], y=dff['ub'], mode='lines', line=dict(color='black', dash='dash'), name='High'))
            # fig.add_trace( go.Scatter(x=dff['t'], y=dff['lb'], mode='lines', line=dict(color='black', dash='dash'), name='Low'))

        fig.update_layout({ "xaxis": { "visible": True }, "yaxis": { "visible": True }, })
        fig.update_layout( showlegend=False, xaxis_title = 'Time', yaxis_title = 'Expression', )
    else:
        fig.update_layout({"annotations": [
            {
                "text": "Select a gene to see expression profile.",
                "xref": "paper",
                "yref": "paper",
                "showarrow": False,
                "font": {
                    "size": 16
                }
            }
        ]})

    return fig


@app.callback(
    Output('similar-profiles-gene-dropdown', 'value'),
    Input('similar-profiles-gene-example-button', 'n_clicks'),
)
def update_gene_dropdown_value(n_clicks):
    try:
        if ctx.triggered_id == 'similar-profiles-gene-example-button':
            return 'TGME49_250800'
    except:
        PreventUpdate
