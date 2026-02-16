#!/usr/bin/env bash

# Define directory variable
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Define filename variables
VCF_Z="$SCRIPT_DIR/../data/ProjTaxa.vcf.gz"
VCF_TEST="$SCRIPT_DIR/ProjTaxa.vcf"

# Drop outgroup and sample VCF (this is really slow)
vcftools --gzvcf "$VCF_Z" \
  --remove-indv Naxos2 \
  --recode --recode-INFO-all --stdout | \
bcftools view | vcfrandomsample -r 0.005 > "$VCF_TEST"

# Zip
bgzip "$VCF_TEST"
# bcftools index "$VCF_TEST".gz