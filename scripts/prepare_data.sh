#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

VCF="$SCRIPT_DIR/../test/ProjTaxaTest.vcf"
VCF_CLEAN="$SCRIPT_DIR/../test/ProjTaxaTestClean.vcf"
DIR="$SCRIPT_DIR/../test/"

grep '^##' $VCF > $VCF_CLEAN
grep -v '^##' $VCF | awk '{NF--; print}' >> $VCF_CLEAN
bgzip -k $VCF_CLEAN

# zcat $VCFZ | grep -v '^#' | head | awk '{print $2}'
# zcat $VCFZ | grep -v '^#' | tail | awk '{print $2}'

zcat "$VCF_CLEAN.gz" | head

tabix -p vcf "$VCF_CLEAN.gz"
# 
# # Convert to Intermediate Columnar Format
# vcf2zarr explode $VCF $DIR/ProjTaxa.icf
# # Convert Intermediate Columnar Format to Zarr
# vcf2zarr encode data/ProjTaxa.icf data/ProjTaxa.vcz