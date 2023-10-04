from datetime import datetime
import json

import numpy as np
import pandas as pd
from dash.exceptions import PreventUpdate

from dash import callback_context as ctx, clientside_callback, html
from dash.dependencies import Input, Output, State, MATCH, ALL
import plotly.express as px
import plotly.graph_objects as go
from plotly.colors import sample_colorscale, get_colorscale

from app import app, db
from genome import descriptions as product_descriptions
from .layouts import genes_table


@app.callback(
    Output('similar-profiles-similar-genes-store', 'data'),
    Output('similar-profiles-similar-genes-list-textarea', 'value'),
    Input('similar-profiles-gene-dropdown', 'value'),
    Input('similar-profiles-filter-by-selector', 'value'),
    Input('similar-profiles-distance-quantile', 'value'), )
def update_similar_genes_list(gene_id, filter_by, quantile_pct):
    if filter_by and gene_id and quantile_pct:
        quantile = quantile_pct / 100
        quantile_col = f"q{quantile:.3f}"

        all_dclass = ['scRNA', 'scATAC']
        similar_genes = set()
        dfs = []
        quantile_thr_dict = {}
        for dclass in all_dclass:

            df = db.select(
                dclass=dclass,
                table='spline_fit_distance_matrix',
                cols=['GeneID.2', 'distance'],
                where=[
                    {
                        'GeneID.1': gene_id,
                    },
                ],
                verbose=False)
            if len(df) == 0:
                df = pd.DataFrame(columns=['GeneID.2', 'distance'])

            dfs.append(df.set_index('GeneID.2'))

            if not filter_by in dclass and not filter_by == 'Both':
                continue

            if len(df) == 0:
                quantile_thr_dict[dclass] = 0
                continue

            quantile_thr = db.select(
                dclass=dclass,
                table='spline_fit_distance_quantiles',
                cols=[quantile_col],
                where=dict(GeneID=gene_id))
            
            if len(quantile_thr) > 0:
                quantile_thr_dict[dclass] = quantile_thr.iloc[0, 0]

        df = pd.concat(dfs, axis=1, join='outer')
        df.columns = all_dclass
        df = df.fillna(np.inf)

        df['Score'] = df['scRNA'].clip(0, 1_000_000) + df['scATAC'].clip(0, 1_000_000)
        df = df.sort_values('Score').drop('Score', axis=1)

        for dclass, quantile_thr in quantile_thr_dict.items():
            df = df.loc[df[dclass] <= quantile_thr]

        df /= 1_000_000
        df = df.reset_index().iloc[:100]
        df = df.to_dict('list')

        return df, '\n'.join(df['GeneID.2'])

    else:
        return {}, ''


@app.callback(
    Output({'type': 'similar-profiles-expr-time-curve', 'key': MATCH}, 'figure'),
    Input('similar-profiles-similar-genes-store', 'data'),
    State({'type': 'similar-profiles-expr-time-curve', 'key': MATCH}, 'id'),
    State('similar-profiles-gene-dropdown', 'value'),
    Input('hovered_trace_gene_id', 'data'),
)
def update_time_curve_plots(similar_genes, id, gene_id, hovered_trace_gene_id):
    dclass = 'scRNA' if id['key'].startswith('RNA') else 'scATAC'

    layout = {'height': 350, "xaxis": { "visible": False }, "yaxis": { "visible": False },
              'margin': {'l':20, 'r':20, 't':60, 'b':60}}

    similar_genes = pd.DataFrame(similar_genes)
    if dclass and len(similar_genes) > 0:
        # similar_genes[f'{dclass}_color'] = sample_colorscale('viridis', similar_genes[dclass].clip(0, 0.5)/0.5)

        trigger = ctx.triggered[0]['prop_id'].split('.')[0]
        if trigger == 'hovered_trace_gene_id' and hovered_trace_gene_id['hovering']:
            if hovered_trace_gene_id['hovering'] == id['key']:
                raise PreventUpdate
            else:
                pass

        df = db.select(
            dclass=dclass,
            table='spline_fit_all_genes',
            cols=['GeneID', 'x', 'expr'],
            # cols=['GeneID', 'x', 'expr', 'lb', 'ub'],
            where={ 'GeneID': similar_genes['GeneID.2'].to_list() },
            verbose=False)

        data = []
        for i, row in similar_genes.iterrows():
            similar_gene_id = row['GeneID.2']
            # color = row[f'{dclass}_color']
            color = None

            dff = df.query("GeneID == @similar_gene_id")

            if similar_gene_id == gene_id:
                width = 4
            else:
                width = 2

            data.append(go.Scatter(x=dff['x'], y=dff['expr'], mode='lines', name='', line_color=color, line_width=width, hovertemplate=f'<b>{similar_gene_id}</b><br>Time: %{{x:.2f}}<br>Expression: %{{y:.2f}}'))
            # fig.add_trace( go.Scatter(x=dff['t'], y=dff['ub'], mode='lines', line=dict(color='black', dash='dash'), name='High'))
            # fig.add_trace( go.Scatter(x=dff['t'], y=dff['lb'], mode='lines', line=dict(color='black', dash='dash'), name='Low'))
        
        fig = go.Figure(layout=layout, data=data)
        fig.update_layout({ "xaxis": { "visible": True }, "yaxis": { "visible": True }, })
        fig.update_layout( showlegend=False, xaxis_title = 'Time (hrs)', yaxis_title = 'Expression', )
    else:
        fig = go.Figure(layout=layout)
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
    Output(f'{genes_table.id_tag}-sort-column-values-state', 'data'),
    Input({'type': f'{genes_table.id_tag}-sort-column-values', 'id': ALL}, 'n_clicks'), )
def update_sort_state(n_clicks):
    return [n % 3 if n else 0 for n in n_clicks]


@app.callback(
    Output({'type': f'{genes_table.id_tag}-sort-column-values', 'id': ALL}, 'className'),
    Input(f'{genes_table.id_tag}-sort-column-values-state', 'data'), )
def update_sort_icons_shape(sort_state):
    icons = [
        "bi bi-sort-{}-down sort-icon text-secondary",
        "bi bi-sort-{}-down sort-icon text-primary",
        "bi bi-sort-{}-up sort-icon text-primary",
    ]
    return [icons[s].format(c['type']) for s, c in zip(sort_state, genes_table.table_columns)]


@app.callback(
    Output(f'{genes_table.id_tag}-pagination', 'active_page'),
    Input('similar-profiles-gene-dropdown', 'value'),
    Input('similar-profiles-similar-genes-store', 'data'),
)
def reset_table_navigation(gene_id, similar_gene_ids):
    return 1


@app.callback(
    Output(f'{genes_table.id_tag}', 'children'),
    Output(f'{genes_table.id_tag}-pagination', 'max_value'),
    Output(f'{genes_table.id_tag}-filter-RNA Dist-form-message', 'children'),
    Output(f'{genes_table.id_tag}-filter-ATAC Dist-form-message', 'children'),
    Input('similar-profiles-gene-dropdown', 'value'),
    Input('similar-profiles-similar-genes-store', 'data'),
    Input(f'{genes_table.id_tag}-pagination', 'active_page'),
    Input(f'{genes_table.id_tag}-page-size-radio', 'value'),
    Input({'key': f'{genes_table.id_tag}-filter', 'name': ALL}, 'value'),
    Input({'key': f'{genes_table.id_tag}-filter', 'name': ALL}, 'id'),
    Input(f'{genes_table.id_tag}-sort-column-values-state', 'data'),
    # State('selected-network-nodes', 'data'),
)
def update_info_tables(gene_id, similar_gene_ids, page, page_size, all_filters, filter_ids, sort_state):
    selected_nodes = []

    if not gene_id or not similar_gene_ids:
        return [], 0, *['' for c in genes_table.table_columns if c['type'] == 'numeric']

    page = int(page) - 1

    df = pd.DataFrame( similar_gene_ids )
    df.columns = ['Gene B ID', 'RNA Dist', 'ATAC Dist']
    df['index'] = df['Gene B ID']

    numeric_form_messages = []

    for col, col_filter, filter_id in zip(genes_table.table_columns, all_filters, filter_ids):
        assert col['name'] == filter_id['name']

        match col['type']:
            case 'alpha':
                if col_filter:
                    df = df.loc[df[col['name']].str.lower().str.contains(col_filter.lower())]
            case 'numeric':
                if col_filter:
                    df = df.loc[(df[col['name']] >= col_filter[0])&(df[col['name']] <= col_filter[1])]
                    numeric_form_messages.append( f'Showing values between [{col_filter[0]:.2f}, {col_filter[1]:.2f}]')
                else:
                    numeric_form_messages.append('Showing values between [0.00, 1.00]')
            
            case 'category':
                if col_filter:
                    df = df.loc[df[col['name']].isin(col_filter)]
            case _:
                raise NotImplementedError

    by = [c['name'] for i, c in enumerate(genes_table.table_columns) if sort_state[i] > 0]
    ascending = [not bool(s-1) for s in sort_state if s > 0]
    df = df.sort_values(by, ascending=ascending)

    descriptions = product_descriptions.set_index('ID')
    descriptions = descriptions.loc[df['Gene B ID'].to_list(), ['Name', 'description']]
    df['Symbol'] = descriptions['Name'].to_list()
    df['Product Description'] = descriptions['description'].to_list()

    data_slice = [{'index': -1-i} for i in range(page_size)]
    for i, item in enumerate(df.iloc[page*page_size:(page+1)*page_size].to_dict('records')):
        data_slice[i] = item

    net_body = [
        html.Tbody([
            html.Tr([
                html.Td(item.get(c['name'], '-'), style=c['style'])
                for c in genes_table.table_columns],
            # draggable='false',
            id={'type': 'net-node-table-tr', 'index': item['index']},
            style={"fontWeight": 'bold'} if item['index'] in selected_nodes else {"fontWeight": 'normal'},
            className='table-active' if item['index'] in selected_nodes else '',)
            for item in data_slice
        ])
    ]

    filtered_data_nrows = len(df)

    return net_body, int(np.ceil(filtered_data_nrows / page_size)), *numeric_form_messages



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


# @app.callback(
#     Output('hovered_trace_gene_id', 'data'),
#     Input({'key': 'RNA_Profile', 'type': 'similar-profiles-expr-time-curve', }, 'hoverData'),
#     Input({'key': 'ATAC_Profile', 'type': 'similar-profiles-expr-time-curve', }, 'hoverData'),
#     State('hovered_trace_gene_id', 'data'),
# )
def update_hovered_trace_gene_id(data1, data2, current_data):

    if isinstance(ctx.triggered, dict):
        if ctx.triggered['prop_id'] == '.':
            raise PreventUpdate

    trigger = ctx.triggered[0]['prop_id'].split('.')[0]
    if not trigger:
        raise PreventUpdate

    trigger = json.loads(trigger)
    trigger_key = trigger['key']

    match trigger_key:
        case 'RNA_Profile':
            new_data = data1
        case 'ATAC_Profile':
            new_data = data2
        case _:
            raise PreventUpdate

    if current_data['hovering'] is None and new_data:
        current_data['hovering'] = trigger_key
        current_data['curveNumber'] = new_data['points'][0]['curveNumber']
    elif trigger_key != current_data['hovering']:
        raise PreventUpdate
    # elif trigger_key == current_data['hovering'] and not new_data:
    #     current_data['hovering'] = None
    #     current_data['curveNumber'] = None

    return current_data


@app.callback(
    Output('debug_info_textarea', 'value'),
    Input('hovered_trace_gene_id', 'data'),
)
def update_debug_info_textarea(data):
    return json.dumps(data, indent=4)


# clientside_callback(
#     """
#     function(e) {
#         console.log('event!', e);
#         graph = document.getElementById('{"key":"ATAC_Profile","type":"similar-profiles-expr-time-curve"}');
#         Plotly.Fx.hover(graph, {});
#         return String(e);
#     };
#     """,
#     Output('debug_info_textarea', 'value'),
#     Input({'key': 'RNA_Profile', 'type': 'similar-profiles-expr-time-curve', }, 'hoverData'),
# )

