#!/bin/bash
# Extract chromosome statistics from VCF using bcftools
# Usage: bash vcf_chrom_stats.sh input.vcf.gz

VCF="$1"

if [ -z "$VCF" ]; then
    echo "Usage: bash vcf_chrom_stats.sh <input.vcf.gz>"
    exit 1
fi

echo "Chromosome    Sites    Min_Pos    Max_Pos    Span"
echo "---------------------------------------------------"

# Use bcftools query to extract chrom and position, then awk to process
bcftools query -f '%CHROM\t%POS\n' "$VCF" | \
awk '{
    chrom = $1
    pos = $2
    
    # Count sites
    count[chrom]++
    
    # Track min position
    if (chrom in min_pos) {
        if (pos < min_pos[chrom]) min_pos[chrom] = pos
    } else {
        min_pos[chrom] = pos
    }
    
    # Track max position
    if (chrom in max_pos) {
        if (pos > max_pos[chrom]) max_pos[chrom] = pos
    } else {
        max_pos[chrom] = pos
    }
}
END {
    # Print results for each chromosome
    for (chrom in count) {
        span = max_pos[chrom] - min_pos[chrom] + 1
        printf "%-12s %8d %10d %10d %12d\n", chrom, count[chrom], min_pos[chrom], max_pos[chrom], span
    }
}' | sort -V  # Sort chromosomes naturally (1, 2, 10 not 1, 10, 2)