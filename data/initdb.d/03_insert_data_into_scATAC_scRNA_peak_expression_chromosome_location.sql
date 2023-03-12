SET autocommit=0;
LOAD DATA INFILE '/opt/data/tsv_files/scATAC_scRNA_peak_expression_chromosome_location.tsv' INTO TABLE scATAC_scRNA_peak_expression_chromosome_location FIELDS TERMINATED BY '\t' IGNORE 1 LINES;
COMMIT;
