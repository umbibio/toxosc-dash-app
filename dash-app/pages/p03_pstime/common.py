import numpy as np
import pandas as pd
import plotly.graph_objects as go

from plotly.colors import sample_colorscale, get_colorscale
import plotly.express as px

from app import db

from genome import descriptions


dclass_keys = ['scRNA', 'scATAC']
dclass_names = ['scRNA', 'scATAC']
dclass_names = dict(zip(dclass_keys, dclass_names))

dclass_data = { key: db.select( dclass=key, table='meta_data').to_dict() for key in dclass_keys}

phase_abbrv = ['G1.a', 'G1.b', 'S', 'M', 'C', 'NA']
phase_names = ['G1.a', 'G1.b', 'S', 'M', 'C', 'Not Available']

phase_colors = ["#1A5878", "#C44237", "#AD8941", "#E99093", "#D3D3D3", "#FFFFFF", "#50594B"]
phase_colors_rgb = ["rgb(26, 88, 120)", "rgb(196, 66, 55)", "rgb(173, 137, 65)", "rgb(233, 144, 147)", "rgb(211, 211, 211)", "rgb(255, 255, 255)", "rgb(80, 89, 75)"]
phase_color_dict = dict(zip(phase_abbrv, phase_colors))
phase_color_rgb_dict = dict(zip(phase_abbrv, phase_colors_rgb))

discrete_colors = [s for s in dir(px.colors.qualitative) if not s.startswith('_') and s != 'swatches']
discrete_colors_dict = {s: getattr(px.colors.qualitative, s) for s in discrete_colors}

discrete_colors.insert(0, 'Default')
discrete_colors_dict.update({'Default': phase_colors})

def _rgb_to_rgba(rgb, alpha=1):
    assert rgb.startswith('rgb('), 'Input color must be rgb'
    return rgb.replace('rgb(', 'rgba(').replace(')', f', {alpha})')

def _hex_to_rgba(hex, alpha=1):
    hex = hex.lstrip('#')
    assert len(hex) == 6, 'Hex color must be 6 digits long'
    r, g, b = int(hex[:2], 16), int(hex[2:4], 16), int(hex[4:], 16)
    return f'rgba({r}, {g}, {b}, {alpha})'

# phases_color_sequence = sample_colorscale('Rainbow', 7)
phases_color_sequence = [c.replace('(', 'a(').replace(')', ', 0.2)') for c in phase_colors_rgb]

def make_sc_plot(dclass, gene_id=None, palette=None, alpha=0.1, expression_colorscale='blues'):
    if palette is None:
        palette = 'Default'
    if expression_colorscale is None:
        expression_colorscale = 'blues'

    phase_visible='legendonly' if gene_id else True
    timeline_visible='legendonly' if gene_id else True
    fig = go.Figure(layout={ 'xaxis': {'title': 'PC_1'}, 'yaxis': {'title': 'PC_2', 'scaleanchor': 'x' }, 'height': 450, 'margin': {'l':10, 'r':10, 't':60, 'b':60}})
    

    df = pd.DataFrame(dclass_data[dclass])
    unique_phases = ['G1.a', 'G1.b', 'S', 'M', 'C']
    for phase, color in zip(unique_phases, discrete_colors_dict.get(palette)):
        if color.startswith('rgb('):
            color = _rgb_to_rgba(color, alpha=alpha)
        elif color.startswith('#'):
            color = _hex_to_rgba(color, alpha=alpha)
        else:
            raise ValueError(f'Unknown color format: {color}')

        x, y = df.loc[df['phase'] == phase, ['PC_1', 'PC_2']].values.T
        fig.add_trace(go.Scatter(
            x=x,
            y=y,
            mode='markers',
            marker=dict(
                color=color,
                line=None,
            ),
            name=phase,
            visible=phase_visible,
            legendgroup="phases_group",
            legendgrouptitle_text="Phases",
        ))

    dff = df.loc[df.sc1 != 0., ['pt.shifted.scaled', 'sc1', 'sc2']]
    dff['angle'] = np.arctan(dff.sc2 / dff.sc1)
    dff.loc[dff.sc1 < 0, 'angle'] += np.pi
    dff['angle'] -= dff.loc[dff['pt.shifted.scaled'] == dff['pt.shifted.scaled'].min(), 'angle'].iloc[0]
    dff['angle'] = dff.angle % (np.pi*2)
    dff = dff.sort_values('angle').reset_index(drop=True)

    n = 200
    i = len(dff) // n
    x, y = pd.concat([dff.iloc[::i], dff.iloc[[0]]]).loc[:, ['sc1', 'sc2']].values.T
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode='lines',
        line=dict(color='Black', width=1),
        name='Timeline',
        legendgroup="timeline_group",
        legendgrouptitle_text="Timeline",
    ))

    if gene_id is not None and gene_id in descriptions.ID.values:
        df = db.select(
            dclass=dclass,
            table='meta_data',
            right_table='expr_all_genes',
            right_cols=['expr'],
            right_on='Sample',
            right_where=dict(GeneID=gene_id),
        )

        expr_colorscale = get_colorscale(expression_colorscale)
        expr_colorscale_alpha = [[s, c.replace('(', 'a(').replace(')', f', {s/2})')] for s, c in expr_colorscale]
        expr_colorscale_const_alpha = [[s, c.replace('(', 'a(').replace(')', f', 0.1)')] for s, c in expr_colorscale]

        values = df['expr'] / df['expr'].max()
        values = values.fillna(0)
        marker_expr_colors = sample_colorscale(expr_colorscale, values)
        marker_expr_colors_alpha = [c.replace('(', 'a(').replace(')', f', {v/2})') for c, v in zip(marker_expr_colors, values)]

        unique_phases = df['phase'].sort_values().unique()
        colorbar_height_px = 250 - len(unique_phases) * 20
        fig.add_trace(go.Scatter(
            x=df['PC_1'],
            y=df['PC_2'],
            mode='markers',
            marker=dict(
                color=marker_expr_colors_alpha,
                cmin=df['expr'].min(),
                cmax=df['expr'].max(),
                line=dict(width=1.2, color='rgba(1.00, 1.00, 1.00, 0.05)'),
                # line=dict(width=1., color='rgba(0., 0., 0., 0.1)'),
                # line=dict(width=1., color=expr_colorscale_const_alpha[6][1]),
                colorbar=dict(
                    title="Counts",
                    len=colorbar_height_px,
                    lenmode='pixels',
                    x=1.1,
                    y=-0.1,
                    yanchor='bottom',
                ),
                colorscale=expr_colorscale_alpha,
            ),
            name='',
            legendgroup="expression_group",
            legendgrouptitle_text=gene_id,
        ))

        n = 200
        i = len(dff) // n
        x, y = pd.concat([dff.iloc[::i], dff.iloc[[0]]]).loc[:, ['sc1', 'sc2']].values.T
        fig.add_trace(go.Scatter(
            x=x,
            y=y,
            mode='lines',
            line=dict(color='Black', width=1),
            showlegend=False,
            legendgroup="timeline_group",
            legendgrouptitle_text="Timeline",
        ))

    x, y = dff.loc[[0], ['sc1', 'sc2']].values.T
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode='markers',
        marker=dict(color='Black', size=20),
        opacity=0.8,
        name='Time Start',
        legendgroup="timeline_group",
        legendgrouptitle_text="Timeline",
    ))

    fig.update_xaxes(showgrid=False, zeroline=False, showticklabels=False)
    fig.update_yaxes(showgrid=False, zeroline=False, showticklabels=False)
    return fig

