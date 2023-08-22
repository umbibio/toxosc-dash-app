from datetime import datetime

import pandas as pd
from dash.exceptions import PreventUpdate

from dash import callback_context as ctx
from dash.dependencies import Input, Output, State, MATCH
import plotly.express as px
import plotly.graph_objects as go
from plotly.colors import sample_colorscale, get_colorscale

from app import app, db
from .common import dclass_data, make_sc_plot


@app.callback(
    Output({'type': 'pstime-expr-graph', 'key': MATCH}, 'figure'),
    Input('pstime-gene-dropdown', 'value'),
    State({'type': 'pstime-expr-graph', 'key': MATCH}, 'id'),
    Input('p03-colorscale-dropdown', 'value'),
    )
def update_expression_plots(gene_id, id, colorscale):
    return make_sc_plot(id['key'], gene_id, colorscale, alpha=0.1)


@app.callback(
    Output({'type': 'pstime-expr-time-curve', 'key': MATCH}, 'figure'),
    Input('pstime-gene-dropdown', 'value'),
    State({'type': 'pstime-expr-time-curve', 'key': MATCH}, 'id'), )
def update_time_curve_plots(gene_id, id):
    dclass = id['key']

    fig = go.Figure(layout={'height': 450, "xaxis": { "visible": False }, "yaxis": { "visible": False }, 'margin': {'l':20, 'r':20, 't':60, 'b':60}})

    if dclass and gene_id:
        df = db.select(
            dclass=dclass,
            table='meta_data',
            right_table='expr_all_genes',
            right_cols=['expr'],
            right_on='Sample',
            right_where=dict(GeneID=gene_id),
            verbose=False,
        )

        marker_color = '#2a3f5f'.strip('#')
        # marker_color = px.colors.qualitative.Plotly[0].strip('#')
        marker_rgb = tuple(int(marker_color[i:i+2], 16) for i in (0, 2, 4))
        marker_rgba = marker_rgb + (0.2,)
        line_rgba = marker_rgb + (0.4,)

        fig.add_trace(go.Scatter(
            x=df['pt.shifted.scaled'],
            y=df['expr'],
            mode='markers',
            marker=dict(
                color=f'rgba{marker_rgba}',
                line=dict(width=1, color=line_rgba),
            ),
            name='Expression',
        ))
        
        df = db.select(
            dclass=dclass,
            table='spline_fit_all_genes',
            cols=['GeneID', 'x', 'expr'],
            # cols=['GeneID', 'x', 'expr', 'lb', 'ub'],
            where=dict(GeneID=gene_id))

        fig.add_trace( go.Scatter(x=df['x'], y=df['expr'], mode='lines', name='Fit'))
        # fig.add_trace( go.Scatter(x=df['t'], y=df['ub'], mode='lines', line=dict(color='black', dash='dash'), name='High'))
        # fig.add_trace( go.Scatter(x=df['t'], y=df['lb'], mode='lines', line=dict(color='black', dash='dash'), name='Low'))
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
    Output('pstime-gene-dropdown', 'value'),
    Input('pstime-gene-example-button', 'n_clicks'),
)
def update_gene_dropdown_value(n_clicks):
    try:
        if ctx.triggered_id == 'pstime-gene-example-button':
            return 'TGME49_250800'
    except:
        PreventUpdate


# app.clientside_callback(
#     """
#     function update_pstime_gene_dropdown_value(n_clicks) {
#         if(dash_clientside.callback_context.triggered.length == 0) return;
#         prop_id = dash_clientside.callback_context.triggered[0].prop_id

#         if(prop_id !== 'pstime-gene-example-button.n_clicks') return;

#         return 'TGME49_250800';
#     }
#     """,
#     Output("pstime-gene-dropdown", 'value'),
#     Input("pstime-gene-example-button", "n_clicks"),
# )

