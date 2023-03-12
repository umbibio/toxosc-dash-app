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
    `q0.01` INT, 
    `q0.02` INT, 
    `q0.03` INT, 
    `q0.04` INT, 
    `q0.05` INT, 
    `q0.06` INT, 
    `q0.07` INT, 
    `q0.08` INT, 
    `q0.09` INT, 
    `q0.10` INT, 
    `q0.11` INT, 
    `q0.12` INT, 
    `q0.13` INT, 
    `q0.14` INT, 
    `q0.15` INT, 
    `q0.16` INT, 
    `q0.17` INT, 
    `q0.18` INT, 
    `q0.19` INT, 
    `q0.20` INT, 
    `q0.21` INT, 
    `q0.22` INT, 
    `q0.23` INT, 
    `q0.24` INT, 
    `q0.25` INT );

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
    `q0.01` INT, 
    `q0.02` INT, 
    `q0.03` INT, 
    `q0.04` INT, 
    `q0.05` INT, 
    `q0.06` INT, 
    `q0.07` INT, 
    `q0.08` INT, 
    `q0.09` INT, 
    `q0.10` INT, 
    `q0.11` INT, 
    `q0.12` INT, 
    `q0.13` INT, 
    `q0.14` INT, 
    `q0.15` INT, 
    `q0.16` INT, 
    `q0.17` INT, 
    `q0.18` INT, 
    `q0.19` INT, 
    `q0.20` INT, 
    `q0.21` INT, 
    `q0.22` INT, 
    `q0.23` INT, 
    `q0.24` INT, 
    `q0.25` INT );

