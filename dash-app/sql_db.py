from typing import List, Dict, Union
import atexit
import os
import pandas as pd
from mysql.connector.pooling import MySQLConnectionPool


class DBPool(object):
    def __init__(self) -> None:
        dbconfig = {n: os.environ.get(f'MARIADB_{n.upper()}') for n in ['host', 'user', 'password', 'database']}
        self.pool = MySQLConnectionPool(pool_name="bsc_pool", pool_size = 32, **dbconfig)

    def query(self, query, dictionary=False):
        cnx = self.pool.get_connection()
        cursor = cnx.cursor(dictionary=dictionary, buffered=True)
        cursor.execute(query)
        cursor.close()

        data = list(cursor)

        cnx.close()
        return data

    def get_table_from_query(self, query):
        data = self.query(query, dictionary=True)
        return pd.DataFrame(data)
    
    def close(self):
        print(f'closing db pool: {self.pool._remove_connections()} connections closed.', flush=True)


conn = DBPool()
atexit.register(conn.close)


def query(query):
    return conn.get_table_from_query(query)


def parse_comparison(table, column, val_comp):
    assert type(val_comp) in [dict, str, int, float], type(val_comp)
    if type(val_comp) == str:
        val_comp = {val_comp: '='}

    and_list = []
    for val, comp in val_comp.items():
        and_list.append(f"`{table}`.`{column}`{comp}'{val}'")

    return ' ( ' + ' AND '.join(and_list) + ' ) '


def parse_conditions(table, column, comparison_list):
    if type(comparison_list) != list:
        comparison_list = [comparison_list]

    or_list = []
    for comparison in comparison_list:
        or_list.append(parse_comparison(table, column, comparison))

    return ' ( ' + ' OR '.join(or_list) + ' ) '


def parse_where(table, where):
    if type(where) != list:
        where = [where]

    or_list = []
    for where_or in where:
        and_list = []
        for column, conditions in where_or.items():
            and_list.append(parse_conditions(table, column, conditions))

        or_list.append(' ( ' + ' AND '.join(and_list) + ' ) ')

    return ' ( ' + ' OR '.join(or_list) + ' ) '


def select(dclass:     str,
           table:       str,
           cols:        List[str]=[],
           where:       List[Dict]={},
           right_table: str='',
           right_cols:  List[str]=[],
           right_on:    str='',
           right_where: List[Dict]={},
           verbose:     bool=False) -> pd.DataFrame:

    table_name = f'{dclass}_{table}'
    cols = [f"`{table_name}`.`{c}`" for c in cols] if cols else [f"`{table_name}`.*"]

    if right_table:
        right_table_name = f'{dclass}_{right_table}'
        right_cols = [f"`{right_table_name}`.`{c}`" for c in right_cols] if right_cols else [f"`{right_table_name}`.*"]
        cols.extend(right_cols)

        assert right_on != ''
        table_str = f'`{table_name}` LEFT JOIN `{right_table_name}` ON `{table_name}`.`{right_on}` = `{right_table_name}`.`{right_on}`'
    else:
        table_str = f'`{table_name}`'

    columns_str = ', '.join(cols)
    if verbose:
        print(f'+++ start fetching {table_name} ...', flush=True)

    conditions = []

    if where:
        conditions.append(parse_where(table_name, where))

    if right_where:
        conditions.append(parse_where(right_table_name, right_where))

    
    combined_conditions = ' AND '.join(conditions)
    if combined_conditions:
        where_str = f"WHERE {combined_conditions}"
    else:
        where_str = ''

    query = f"SELECT {columns_str} FROM {table_str} {where_str};"
    if verbose:
        print(query, flush=True)

    df = conn.get_table_from_query(query)

    if verbose:
        print(f'--- done fetching {len(df)} rows from {table_name}', flush=True)
    return df

