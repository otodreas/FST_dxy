#!/usr/bin/env bash

# Define directory variable
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Define filename variables
VCF="$SCRIPT_DIR/../data/ProjTaxa.vcf"
VCF_TEST="$SCRIPT_DIR/ProjTaxa.vcf"

# Create test file
head -n 2393 $VCF > $VCF_TEST
tail -n 50 $VCF >> $VCF_TEST

# Zip
bgzip -k $VCF_TEST