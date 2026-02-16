#!/usr/bin/env bash


# This script takes bgzipped VCF files and cleans them up and turns them into
# Zarr directories in whatever directory you are in


# Assign directory to variable
CWD="$(pwd)"

# Set filename variables
VCF_Z="$CWD/ProjTaxa.vcf.gz"
VCF_Z_F="$CWD/ProjTaxaFilt.vcf.gz"

# Filter data with vcftools
  # Remove outgroup (Naxos2)
  # Keep biallelic SNPs only
  # Filter by quality by genotypes (GQ>20)
  # Filter by sample depth by genotypes (5<DP<70)
  # Filter by missingness by sites (missingness<=10%)
  # Recode output to VCF with all metadata
  # Pipe output into bcftools to encode in a bgzipped file
vcftools --gzvcf "$VCF_Z" \
  --remove-indv Naxos2 \
  --remove-indels --min-alleles 2 --max-alleles 2 \
  --minGQ 20 \
  --minDP 5 --maxDP 70 \
  --max-missing 0.9 \
  --recode --recode-INFO-all \
  --stdout | \
  bcftools view -O z -o "$VCF_Z_F"

# Index filtered VCF file
bcftools index "$VCF_Z_F"

# Convert to Intermediate Columnar Format
vcf2zarr explode "$VCF_Z_F" "$CWD/ProjTaxaFilt.icf"
# Convert Intermediate Columnar Format to Zarr
vcf2zarr encode "$CWD/ProjTaxaFilt.icf" "$CWD/ProjTaxaFilt.vcz"