SET autocommit=0;
LOAD DATA INFILE '/opt/data/tsv_files/scRNA_meta_data.tsv' INTO TABLE scRNA_meta_data FIELDS TERMINATED BY '\t' IGNORE 1 LINES;
COMMIT;
