SET autocommit=0;
LOAD DATA INFILE '/opt/data/tsv_files/scRNA_expr_all_genes.tsv' INTO TABLE scRNA_expr_all_genes FIELDS TERMINATED BY '\t' IGNORE 1 LINES;
COMMIT;
