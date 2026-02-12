# FST_dxy
Project for BINP28 comparing FST and dxy across the genome.

## Workflow

### Prepare environment

The environment can be found in `environment.yaml`. It includes Jupyter (TODO: make yaml without Jupyter).

### Prepare data

First, we must index the VCF file for improved access to data in downstream computation.

This is done at the command line

First, we drop the final column because we don't need the out group.

```sh
zcat data/ProjTaxa.vcf.gz | awk '{NF--; print}' | bzip2 > data/ProjTaxa.vcf.gz
```

We check that the VCF file looks sorted:

```sh
zcat data/ProjTaxa.vcf.gz | grep -v '^#' | head | awk '{print $2}'
zcat data/ProjTaxa.vcf.gz | grep -v '^#' | tail | awk '{print $2}'
```

Now we can index it using samtools:

```sh
tabix -p vcf data/ProjTaxa.vcf.gz
```

And encode as Zarr file

```sh
# Convert to Intermediate Columnar Format
vcf2zarr data/explode ProjTaxa.vcf.gz data/ProjTaxa.icf
# Convert Intermediate Columnar Format to Zarr
vcf2zarr encode data/ProjTaxa.icf data/ProjTaxa.vcz
```

### Run analyses

