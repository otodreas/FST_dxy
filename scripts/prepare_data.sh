#!/usr/bin/env bash


# This script takes bgzipped VCF files and cleans them up and turns them into
# Zarr directories in whatever directory you are in


# Set directory variables
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CWD="$(pwd)"

# Set filename variables
VCF_Z="$CWD/ProjTaxa.vcf.gz"
VCF_Z_CLEAN="$CWD/ProjTaxaClean.vcf.gz"

# Drop outgroup
bcftools view -s ^Naxos2 "$VCF_Z" -Oz -o "$VCF_Z_CLEAN"

# # Check that the data look sorted
# zcat $VCFZ | grep -v '^#' | head | awk '{print $2}'
# zcat $VCFZ | grep -v '^#' | tail | awk '{print $2}'

# Create index file
tabix -p vcf "$VCF_Z_CLEAN"

# Convert to Intermediate Columnar Format
vcf2zarr explode "$VCF_Z_CLEAN" "$CWD/ProjTaxa.icf"
# Convert Intermediate Columnar Format to Zarr
vcf2zarr encode "$CWD/ProjTaxa.icf" "$CWD/ProjTaxa.vcz"