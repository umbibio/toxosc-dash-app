CREATE TABLE scATAC_expr_all_genes (
    `GeneID` VARCHAR (13), 
    `Sample` VARCHAR (18), 
    `expr` FLOAT );

CREATE TABLE scATAC_meta_data (
    `Sample` VARCHAR (18), 
    `spp` VARCHAR (6), 
    `phase` VARCHAR (4), 
    `pt.shifted.scaled` FLOAT, 
    `cell.ord` INT, 
    `sc1` FLOAT, 
    `sc2` FLOAT, 
    `transition.atac` VARCHAR (2), 
    `PC_1` FLOAT, 
    `PC_2` FLOAT, 
    `PC_3` FLOAT, 
    `UMAP_1` FLOAT, 
    `UMAP_2` FLOAT );

CREATE TABLE scATAC_meta_gene_all_genes (
    `GeneID` VARCHAR (13) );

CREATE TABLE scATAC_scRNA_peak_expression_chromosome_location (
    `GeneID` VARCHAR (13), 
    `peak.ord.atac` FLOAT, 
    `peak.ord.rna` FLOAT, 
    `chromosome` VARCHAR (7), 
    `start` INT, 
    `end` INT );

CREATE TABLE scATAC_spline_fit_all_genes (
    `x` FLOAT, 
    `GeneID` VARCHAR (13), 
    `expr` FLOAT );

CREATE TABLE scATAC_spline_fit_distance_matrix (
    `GeneID.1` VARCHAR (13), 
    `GeneID.2` VARCHAR (13), 
    `distance` INT );

CREATE TABLE scATAC_spline_fit_distance_quantiles (
    `GeneID` VARCHAR (13), 
    `q0.001` INT, 
    `q0.002` INT, 
    `q0.003` INT, 
    `q0.004` INT, 
    `q0.005` INT, 
    `q0.006` INT, 
    `q0.007` INT, 
    `q0.008` INT, 
    `q0.009` INT, 
    `q0.010` INT, 
    `q0.011` INT, 
    `q0.012` INT, 
    `q0.013` INT, 
    `q0.014` INT, 
    `q0.015` INT, 
    `q0.016` INT, 
    `q0.017` INT, 
    `q0.018` INT, 
    `q0.019` INT, 
    `q0.020` INT, 
    `q0.021` INT, 
    `q0.022` INT, 
    `q0.023` INT, 
    `q0.024` INT, 
    `q0.025` INT );

CREATE TABLE scRNA_expr_all_genes (
    `GeneID` VARCHAR (13), 
    `Sample` VARCHAR (18), 
    `expr` FLOAT );

CREATE TABLE scRNA_meta_data (
    `Sample` VARCHAR (18), 
    `spp` VARCHAR (5), 
    `phase` VARCHAR (4), 
    `pt.shifted.scaled` FLOAT, 
    `cell.ord` INT, 
    `sc1` FLOAT, 
    `sc2` FLOAT, 
    `transition.rna` VARCHAR (2), 
    `PC_1` FLOAT, 
    `PC_2` FLOAT, 
    `PC_3` FLOAT, 
    `UMAP_1` FLOAT, 
    `UMAP_2` FLOAT );

CREATE TABLE scRNA_meta_gene_all_genes (
    `GeneID` VARCHAR (13) );

CREATE TABLE scRNA_spline_fit_all_genes (
    `x` FLOAT, 
    `GeneID` VARCHAR (13), 
    `expr` FLOAT );

CREATE TABLE scRNA_spline_fit_distance_matrix (
    `GeneID.1` VARCHAR (13), 
    `GeneID.2` VARCHAR (13), 
    `distance` INT );

CREATE TABLE scRNA_spline_fit_distance_quantiles (
    `GeneID` VARCHAR (13), 
    `q0.001` INT, 
    `q0.002` INT, 
    `q0.003` INT, 
    `q0.004` INT, 
    `q0.005` INT, 
    `q0.006` INT, 
    `q0.007` INT, 
    `q0.008` INT, 
    `q0.009` INT, 
    `q0.010` INT, 
    `q0.011` INT, 
    `q0.012` INT, 
    `q0.013` INT, 
    `q0.014` INT, 
    `q0.015` INT, 
    `q0.016` INT, 
    `q0.017` INT, 
    `q0.018` INT, 
    `q0.019` INT, 
    `q0.020` INT, 
    `q0.021` INT, 
    `q0.022` INT, 
    `q0.023` INT, 
    `q0.024` INT, 
    `q0.025` INT );

