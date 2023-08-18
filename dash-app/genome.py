import pandas as pd

gff = pd.read_csv('assets/public-data/genome/ToxoDB-64_TgondiiME49_genes.gff', header=None, sep='\t')
gff.columns = ['seqname', 'source', 'feature', 'start', 'end', 'score', 'strand', 'frame', 'attribute']
descriptions = pd.DataFrame([dict([kv.split('=') for kv in s.replace('%2C', ',').split(';')]) for s in gff['attribute']])
descriptions.fillna('', inplace=True)
