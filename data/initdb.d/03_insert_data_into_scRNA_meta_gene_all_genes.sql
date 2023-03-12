SET autocommit=0;
LOAD DATA INFILE '/opt/data/tsv_files/scRNA_meta_gene_all_genes.tsv' INTO TABLE scRNA_meta_gene_all_genes FIELDS TERMINATED BY '\t' IGNORE 1 LINES;
COMMIT;
