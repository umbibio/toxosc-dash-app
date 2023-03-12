SET autocommit=0;
LOAD DATA INFILE '/opt/data/tsv_files/scRNA_spline_fit_distance_matrix.tsv' INTO TABLE scRNA_spline_fit_distance_matrix FIELDS TERMINATED BY '\t' IGNORE 1 LINES;
COMMIT;
