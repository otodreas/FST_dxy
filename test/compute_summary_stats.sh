#!/usr/bin/env bash

# Workflow adapted from https://speciationgenomics.github.io/filtering_vcfs/

# Define directory variable
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Assign variables
SUBSET_VCF="$SCRIPT_DIR/ProjTaxa.vcf.gz"
OUT="$SCRIPT_DIR/Summary_Stats/ProjTaxa_Stats"

# Allele frequency
vcftools --gzvcf $SUBSET_VCF --freq2 --out $OUT --max-alleles 2

# Mean depth per individual
vcftools --gzvcf $SUBSET_VCF --depth --out $OUT

# Mean depth per site
vcftools --gzvcf $SUBSET_VCF --site-mean-depth --out $OUT

# Site quality
vcftools --gzvcf $SUBSET_VCF --site-quality --out $OUT

# Proportion of missing data per individual
vcftools --gzvcf $SUBSET_VCF --missing-indv --out $OUT

# Poportion of missing data per site
vcftools --gzvcf $SUBSET_VCF --missing-site --out $OUT

# Heterozygosity and inbreeding coefficient per individual
vcftools --gzvcf $SUBSET_VCF --het --out $OUT