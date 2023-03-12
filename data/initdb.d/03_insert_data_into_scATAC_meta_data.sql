SET autocommit=0;
LOAD DATA INFILE '/opt/data/tsv_files/scATAC_meta_data.tsv' INTO TABLE scATAC_meta_data FIELDS TERMINATED BY '\t' IGNORE 1 LINES;
COMMIT;
