#!/usr/bin/env bash


# This script takes bgzipped VCF files and cleans them up and turns them into
# Zarr directories in whatever directory you are in


# Set directory variables
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CWD="$(pwd)"

# Set filename variables
VCF_Z="$CWD/ProjTaxa.vcf.gz"
VCF_Z_F="$CWD/ProjTaxaFilt.vcf.gz"

# Set filters
# MAF=0.1
MISS=0.5
# QUAL=30
MIN_DEPTH=2.5
MAX_DEPTH=50

# Drop outgroup
bcftools view -s ^Naxos2 "$VCF_Z" | \
# Drop indels
bcftools view -v snps | \
# Filter across all samples at a site
bcftools filter -i 'QUAL<6247 & INFO/DP>16320696 & INFO/DP<81603482' -O z -o "$VCF_Z_F" #| \
# Genotype-level filtering
# bcftools +setGT -O z -o "$VCF_Z_F" -- -t q -n . -i 'FMT/GQ<20 | FMT/DP<5 | FMT/DP>60'

# # Create index file
# tabix -p vcf "$VCF_Z_F"

# # Convert to Intermediate Columnar Format
# vcf2zarr explode "$VCF_Z_F" "$CWD/ProjTaxa.icf"
# # Convert Intermediate Columnar Format to Zarr
# vcf2zarr encode "$CWD/ProjTaxa.icf" "$CWD/ProjTaxa.vcz"