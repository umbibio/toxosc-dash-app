from dash.exceptions import PreventUpdate

from dash import callback_context as ctx
from dash.dependencies import Input, Output, State, MATCH
import plotly.express as px
import plotly.graph_objects as go
from plotly.colors import sample_colorscale, get_colorscale

from app import app, db
from genome import descriptions


@app.callback(
    Output('2d3d-radio', 'style'),
    Input('dimred-radio', 'value'),)
def update_2d3d_visibility(dimred):

    if dimred == 'PCA':
        style = {'display': 'block'}
    else:
        style = {'display': 'none'}

    return style


@app.callback(
    Output({'type': 'expression-graph', 'dclass': MATCH}, 'figure'),
    Input({'type': 'expression-gene-dropdown-relay', 'dclass': MATCH}, 'id'),
    Input({'type': 'expression-gene-dropdown-relay', 'dclass': MATCH}, 'data'),
    Input('dimred-radio', 'value'),
    Input('2d3d-radio', 'value'),
    Input('p01-colorscale-dropdown', 'value'),
    )
def draw_expression_plot(dd_id, gene_id, dimred, pca_nd, colorscale):
    dclass = dd_id['dclass']

    if colorscale is None:
        colorscale = 'blues'

    params = dict()
    fig = go.Figure()
    scatter_function = go.Scatter

    if dclass is not None:
        df = db.select(
            dclass=dclass,
            table='meta_data')

        params.update(dict(mode='markers'))
        marker_dict = dict(
            color='rgba(0., 0., 0., 0.2)',
            line=dict(width=1.2, color='rgba(0.83, 0.83, 0.83, 0.)'),
            # line=dict(width=1.2, color=sample_colorscale('Blues', [1.])[0].replace('(', 'a(').replace(')', ', 0.2)')),
        )
        if gene_id is not None and gene_id in descriptions.ID.values:
            expression = db.select(
                dclass=dclass,
                table='expr_all_genes',
                cols=['GeneID', 'Sample', 'expr'],
                where=dict(GeneID=gene_id))

            df = df.merge(expression)

            expr_colorscale = get_colorscale(colorscale)

            values = df['expr'] / df['expr'].max()
            values = values.fillna(0.)
            marker_expr_colors = sample_colorscale(expr_colorscale, values)
            marker_expr_colors_alpha = [c.replace('(', 'a(').replace(')', f', {v})') for c, v in zip(marker_expr_colors, values)]

            expr_colorscale_alpha = [[s, c.replace('(', 'a(').replace(')', f', {s})')] for s, c in expr_colorscale]

            marker_line_color_alpha = sample_colorscale('Blues', [1.])[0].replace('(', 'a(').replace(')', ', 0.1)')
            marker_dict = dict(
                color=marker_expr_colors_alpha,
                cmin=df['expr'].min(),
                cmax=df['expr'].max(),
                # line=dict(width=1.2, color=marker_line_color_alpha),
                line=dict(width=1.2, color='rgba(0.83, 0.83, 0.83, 0.05)'),
                colorscale=expr_colorscale_alpha,
                colorbar=dict(
                    title='Expression'
                ),
            )

        axes_titles = dict()
        if dimred == 'PCA':
            x, y = df.loc[:, ['PC_1', 'PC_2']].values.T

            if pca_nd == '3D':
                z = df['PC_3']
                params.update(dict(z=z))
                scatter_function = go.Scatter3d
                axes_titles.update(
                    dict(scene=dict(
                        xaxis=dict(title='PC_1'),
                        yaxis=dict(title='PC_2'),
                        zaxis=dict(title='PC_3'),
                    )))
                if gene_id is not None:
                    marker_dict = dict(
                        color=marker_expr_colors_alpha,
                        size=3,
                        line=dict(width=1.2, color='rgba(1.0, 1.0, 1.0, 0.05)'),
                        # line=dict(width=1.2, color='rgba(0.83, 0.83, 0.83, 0.6)'),
                        # line=dict(width=1., color=sample_colorscale('Blues', [1.])[0].replace('(', 'a(').replace(')', ', 0.4)')),
                    )
                else:
                    marker_dict = dict(
                        color='rgba(0., 0., 0., 0.)',
                        size=3,
                        line=dict(width=1.2, color='rgba(1.0, 1.0, 1.0, 0.5)'),
                        # line=dict(width=1., color=sample_colorscale('Blues', [1.])[0].replace('(', 'a(').replace(')', ', 0.5)')),
                    )
            else:
                axes_titles.update(dict( xaxis_title = 'PC_1', yaxis_title = 'PC_2', ))

        elif dimred == 'UMAP':
            x, y = df.loc[:, ['UMAP_1', 'UMAP_2']].values.T
            axes_titles.update(dict( xaxis_title = 'UMAP_1', yaxis_title = 'UMAP_2', ))

        else:
            x = y = None

        params.update(dict(marker=marker_dict))
        params.update(dict(x=x, y=y))

        trace = scatter_function(**params)
        fig.add_trace(trace)
        fig.update_layout(axes_titles)

    fig.update_layout({ 
        'yaxis': { 'scaleanchor': 'x'},
        'height': 700 if pca_nd == '3D' else 500, },
    )
    fig.update_xaxes(showgrid=False, zeroline=False, showticklabels=False)
    fig.update_yaxes(showgrid=False, zeroline=False, showticklabels=False)
    return fig


app.clientside_callback(
    """
    function update_gene_dropdown_relay(gene_id) {
        if(gene_id === undefined) return '';
        if(gene_id.length === 0 || gene_id.length === 13) return gene_id;
        throw dash_clientside.PreventUpdate;
    }
    """,
    Output({'type': 'expression-gene-dropdown-relay', 'dclass': MATCH}, 'data'),
    Input({'type': 'expression-gene-dropdown', 'dclass': MATCH}, 'value'),
)


app.clientside_callback(
    """
    function update_gene_dropdown_value(n_clicks) {
        if(n_clicks === undefined) throw dash_clientside.PreventUpdate;
        return 'TGME49_250800';
    }
    """,
    Output({'type': 'expression-gene-dropdown', 'dclass': MATCH}, 'value'),
    Input({'type': 'expression-gene-example-button', 'dclass': MATCH}, 'n_clicks'),
)


app.clientside_callback(
    """
    function update_global_expression_colorscale(colorscale) {
        if(colorscale === undefined) throw dash_clientside.PreventUpdate;
        return colorscale;
    }
    """,
    Output('expression-color-scale-store', 'data'),
    Input('p01-colorscale-dropdown', 'value'),
)

# @app.callback(
#     Output("collapse", "is_open"),
#     [Input("collapse-button", "n_clicks")],
#     [State("collapse", "is_open")],
# )
# def toggle_collapse(n, is_open):
#     if n:
#         return not is_open
#     return is_open
