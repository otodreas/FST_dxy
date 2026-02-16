#!/usr/bin/env bash

# Workflow adapted from https://speciationgenomics.github.io/filtering_vcfs/

# Define directory variable
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# TODO: take command line arguments, handle missing directory error (directory needs to exist in order to be populated with summary stats files)
# Assign variables
# VCF_Z="$SCRIPT_DIR/ProjTaxa.vcf.gz"
VCF_Z="$SCRIPT_DIR/ProjTaxaFilt.vcf.gz"
# OUT="$SCRIPT_DIR/Summary_Stats_PreFilter/ProjTaxa_Stats"
OUT="$SCRIPT_DIR/Summary_Stats_PostFilter/ProjTaxa_Stats"

# Allele frequency
vcftools --gzvcf $VCF_Z --freq2 --out $OUT --max-alleles 2

# Mean depth per individual
vcftools --gzvcf $VCF_Z --depth --out $OUT

# Mean depth per site
vcftools --gzvcf $VCF_Z --site-mean-depth --out $OUT

# Mean depth per site
vcftools --gzvcf $VCF_Z --geno-depth --out $OUT

# Site quality
vcftools --gzvcf $VCF_Z --site-quality --out $OUT

# Proportion of missing data per individual
vcftools --gzvcf $VCF_Z --missing-indv --out $OUT

# Poportion of missing data per site
vcftools --gzvcf $VCF_Z --missing-site --out $OUT

# Heterozygosity and inbreeding coefficient per individual
vcftools --gzvcf $VCF_Z --het --out $OUT