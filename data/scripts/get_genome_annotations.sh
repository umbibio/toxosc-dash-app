#!/bin/bash

output_dir=${1-"."}

mkdir -p $output_dir
cd $output_dir

if [ ! -f "ToxoDB-64_TgondiiME49.gff" ];then
    echo "Downloading genome annotations from ToxoDB"
    wget https://toxodb.org/common/downloads/release-64/TgondiiME49/gff/data/ToxoDB-64_TgondiiME49.gff
fi

if [ ! -f "ToxoDB-64_TgondiiME49_genes.gff" ];then
    echo "Extracting gene annotations from genome annotations"
    grep 'protein_coding_gene' ToxoDB-64_TgondiiME49.gff > ToxoDB-64_TgondiiME49_genes.gff
fi
