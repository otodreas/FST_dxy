#!/usr/bin/env bash

: '
This script takes bgzipped VCF files and cleans them up and turns them into
Zarr directories in whatever directory you are in

The program uses hard filters in vcftools as there is no truth set for the
data, bcftools to index, and vcf2zarr, which is recommended by the maintainers
of sgkit, which is used in the next script for analysis.
'

# Assign directory to variable
CWD="$(pwd)"

# Set filename variables
VCF_Z="$CWD/$1"
DATA_DIR=$(dirname "$VCF_Z")
VCF_Z_F="$DATA_DIR/Filtered.vcf.gz"

# Filter data with vcftools
  # Remove outgroup (Naxos2)
  # Keep biallelic SNPs only
  # Filter by quality by genotypes (GQ>20)
  # Filter by sample depth by genotypes (5<DP<70)
  # Filter by missingness by sites (missingness<=10%)
  # Recode output to VCF with all metadata
  # Pipe output into bcftools to encode in a bgzipped file
echo "1/2: Filtering bgzipped VCF file..."
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
echo "1/2: Indexing filtered bgzipped VCF file..."
bcftools index "$VCF_Z_F"

# Convert to Intermediate Columnar Format
echo "1/2: Converting filtered bgzipped VCF file to Intermediate Columnar Format..."
vcf2zarr explode "$VCF_Z_F" "$DATA_DIR/Filtered.icf"
echo "Intermediate data written to $DATA_DIR/Filtered.icf"
# Convert Intermediate Columnar Format to Zarr
echo "1/2: Converting Intermediate Columnar Format file to Zarr..."
vcf2zarr encode "$DATA_DIR/Filtered.icf" "$DATA_DIR/Filtered.vcz"
echo "Zarr data written to $DATA_DIR/Filtered.vcz"