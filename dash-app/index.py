from importlib import import_module
import re

from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State, MATCH

from app import app, server, url_base_pathname
import pages

import dash_bootstrap_components as dbc

from genome import descriptions


page_modules = [mod for mod in pages.__loader__.get_resource_reader().contents() if re.match('^p\d\d_', mod)]
page_modules.sort()
page_names = [re.sub('^p\d\d_', '', mod) for mod in page_modules]
page_hrefs = page_names.copy()
page_hrefs[0] = ''

page_info_list = [
    {
        'title': ' '.join([n.capitalize() for n in name.split('_')]),
        'module': module,
        'href': f'{url_base_pathname}{href}',
    }
    for name, module, href in zip(page_names, page_modules, page_hrefs)
]

for page in page_info_list:
    import_module(f"pages.{page['module']}")


nav = dbc.Nav([
    dbc.NavItem(dbc.NavLink(page['title'], href=page['href'], id={'type': 'navlink', 'page': page['module']}))
    for page in page_info_list ], pills=True)

logo = html.Img(src=app.get_asset_url('logo.png'), className="img-fluid")

app.layout = dbc.Container(
    dbc.Row([
        dcc.Location(id='url', refresh=False),
        html.Datalist(id='list-suggested-gene-ids', children=[html.Option(value=word) for word in descriptions.ID]),
        dcc.Store(id='expression-color-scale-store', storage_type='local'),
        dbc.Col([
            dbc.Row(dbc.Col(logo, width=10)),
            dbc.Row(dbc.Col(id='left-menu')),
        ], width=3),
        dbc.Col([
            dbc.Row(dbc.Col(nav), class_name="p-2"),
            dbc.Row(dbc.Col(id='page-content'), class_name='mt-4'),
        ], width=9),
    ], class_name="mt-4"),
    fluid=False
)


@app.callback(
    Output({'type': 'navlink', 'page': MATCH}, 'active'),
    Input('url', 'pathname'),
    State({'type': 'navlink', 'page': MATCH}, 'href'),)
def update_active_menu(pathname, page_href):
    return pathname == page_href


@app.callback(Output('left-menu', 'children'),
              Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    print(f"display page: {pathname}", flush=True)

    for page in page_info_list:
        if pathname == page['href']:

            page_app = getattr(pages, page['module'])
            menu = getattr(page_app, 'menu')
            body = getattr(page_app, 'body')

            return menu, body

    print(f"page not found: {pathname}", flush=True)
    return None, None


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='127.0.0.1')
    parser.add_argument('--port', type=int, default=8080)
    parser.add_argument('--debug', action='store_true')
    
    kvargs = vars(parser.parse_args())

    app.run_server(**kvargs)

