SET autocommit=0;
LOAD DATA INFILE '/opt/data/tsv_files/scATAC_spline_fit_distance_quantiles.tsv' INTO TABLE scATAC_spline_fit_distance_quantiles FIELDS TERMINATED BY '\t' IGNORE 1 LINES;
COMMIT;
