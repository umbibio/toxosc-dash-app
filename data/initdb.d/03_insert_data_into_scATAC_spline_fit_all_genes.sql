SET autocommit=0;
LOAD DATA INFILE '/opt/data/tsv_files/scATAC_spline_fit_all_genes.tsv' INTO TABLE scATAC_spline_fit_all_genes FIELDS TERMINATED BY '\t' IGNORE 1 LINES;
COMMIT;
