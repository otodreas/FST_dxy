#!/usr/bin/env bash

# Define directory variable
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Define filename variables
VCF_Z="$SCRIPT_DIR/../data/ProjTaxa.vcf.gz"
VCF_TEST="$SCRIPT_DIR/ProjTaxa.vcf"

# Sample VCF (this is really slow for some reason)
bcftools view $VCF_Z | vcfrandomsample -r 0.01 > $VCF_TEST

# Zip
bgzip -k $VCF_TEST