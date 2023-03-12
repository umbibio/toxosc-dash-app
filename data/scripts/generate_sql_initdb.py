#!/usr/bin/env python

import os
import re
from glob import glob
import numpy as np
import pandas as pd
import argparse


def get_sql_datatype(series):
    print(series.name, flush=True, end=', ')

    if series.name.lower() == 'phase':
        # force str for phase. If first element is 'NA' then we wrongly infer float
        dtype = str
    else:
        # infer type from first element value
        dtype = type(series.iat[0])

    if dtype == str:
        max_length = series.str.len().max()
        return f'VARCHAR ({int(max_length)})'
    elif dtype in [int, np.int64]:
        return 'INT'
    elif dtype in [float, np.float64]:
        if (series == series.round()).all():
            return 'INT'
        else:
            return 'FLOAT'
    else:
        raise ValueError(f"Don't know how to translate dtype {dtype}")


def generate_create_tables(tsv_files, outdir):
    print('Generating sql files for table creation...')
    CREATE_TABLE_TEMPLATE = "CREATE TABLE {table_name} (\n    {columns_specs} );\n\n"
    OUTPUT_FILE = os.path.join(outdir, '01_create_tables.sql')

    with open(OUTPUT_FILE, 'w') as file:

        for table_path in tsv_files:
            print(f'\tProcessing {table_path} with columns:', flush=True, end=' ')
            table_filename = os.path.basename(table_path)
            table_name = os.path.splitext(table_filename)[0]
            
            df = pd.read_csv(table_path, sep='\t')
            columns_specs = ', \n    '.join([' '.join([f"`{cn}`", get_sql_datatype(df[cn])]) for cn in df.columns])
            line = CREATE_TABLE_TEMPLATE.format(table_name=table_name, columns_specs=columns_specs)
            file.write(line)
            print(flush=True)


def generate_create_indices(tsv_files, outdir):

    print('Generating sql files for index creation...')

    CREATE_INDEX_TEMPLATE = "CREATE INDEX {index_name} ON {table_name} ( {columns} );\n"
    CREATE_UNIQUE_INDEX_TEMPLATE = "CREATE UNIQUE INDEX {index_name} ON {table_name} ( {columns} );\n"
    OUTPUT_FILE = os.path.join(outdir, '04_create_indices.sql')

    with open(OUTPUT_FILE, 'w') as file:

        for table_path in tsv_files:
            print(f'\tProcessing {table_path}...')

            table_filename = os.path.basename(table_path)
            table_name = os.path.splitext(table_filename)[0]
            
            df = pd.read_csv(table_path, sep='\t', nrows=5)

            column_list = [cn for cn in df.columns if cn in ['GeneID', 'Sample', 't', 'x', 'GeneID.1', 'GeneID.2']]
            if column_list:
                assert len(column_list) <=2

                TEMPLATE = CREATE_INDEX_TEMPLATE if len(column_list) == 2 else CREATE_UNIQUE_INDEX_TEMPLATE

                for column in column_list:
                    if column in ['t', 'x', 'GeneID.2']:
                        continue
                    index_name = f"index_{table_name}_{column}".replace('.', '_')
                    line = TEMPLATE.format(index_name=index_name, table_name=table_name, columns=f"`{column}`")
                    file.write(line)
            else:
                column_list = [cn for cn in df.columns if cn in ['src', 'trg']]
                if len(column_list) == 2:
                    index_name = f"index_{table_name}_" + '_'.join(column_list)
                    line = CREATE_UNIQUE_INDEX_TEMPLATE.format(index_name=index_name, table_name=table_name, columns=', '.join(column_list))
                    file.write(line)
                    column = column_list[1]
                    index_name = f"index_{table_name}_{column}"
                    line = CREATE_INDEX_TEMPLATE.format(index_name=index_name, table_name=table_name, columns=column)
                    file.write(line)
                else:
                    print(table_path)
                    print(column_list)
                    raise NotImplementedError


def generate_insert_data(tsv_files, outdir):
    print('Generating sql files for data loading...')
    INSERT_DATA_TEMPLATE = "LOAD DATA INFILE '{table_path}' INTO TABLE {table_name} FIELDS TERMINATED BY '\\t' IGNORE 1 LINES;\n"
    OUTPUT_FILE_TEMPLATE = os.path.join(outdir, '03_insert_data_into_{table_name}.sql')

    for input_table_path in tsv_files:
        input_table_dirpath = os.path.dirname(input_table_path)
        input_table_filename = os.path.basename(input_table_path)
        container_table_filepath = os.path.join('/opt', 'data', 'tsv_files', input_table_filename)

        if input_table_filename.startswith('split_'):
            continue

        table_name = os.path.splitext(input_table_filename)[0]

        print(f'\tProcessing {input_table_path}...')

        with open(OUTPUT_FILE_TEMPLATE.format(table_name=table_name), 'w') as file:
            file.write('SET autocommit=0;\n')
            line = INSERT_DATA_TEMPLATE.format(table_path=container_table_filepath, table_name=table_name)
            file.write(line)
            file.write('COMMIT;\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('tsvfolder')
    parser.add_argument('--outdir', type=str, default='')
    parser.add_argument('--generate-create-tables', action='store_true')
    parser.add_argument('--generate-create-indices', action='store_true')
    parser.add_argument('--generate-insert-data', action='store_true')
    args = parser.parse_args()

    tsv_files = glob(os.path.join(args.tsvfolder, '*.tsv'))
    tsv_files.sort()

    if args.outdir:
        outdir = args.outdir
    else:
        outdir = os.path.join(args.tsvfolder, '..', 'initdb.d')

    os.makedirs(outdir, exist_ok=True)

    do_all = not args.generate_create_tables and not args.generate_create_indices and not args.generate_insert_data

    if args.generate_create_tables or do_all:
        generate_create_tables(tsv_files, outdir)
    if args.generate_create_indices or do_all:
        generate_create_indices(tsv_files, outdir)
    if args.generate_insert_data or do_all:
        generate_insert_data(tsv_files, outdir)

