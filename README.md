# FST_dxy
Project for BINP28 comparing FST and dxy across the genome.

## Directory structure

The directory structure of this reproducible workflow is as follows

```
FST_dxy_analysis/
├── data/
├── scripts/
│   ├── gzVCF_toFilter_toZarr.sh
│   └── Zarr_toXArray_toResults.py
├── results/
├── environment.yaml
├── LICENSE
└── README.md
```

where `data/` and `results/` are empty directories that you will populate.

The scripts in `scripts/` are intended to be run sequentially, which is outlined in **Reproducible workflow: Run analyses**.

This project is available on [GitHub](https://github.com/otodreas/FST_dxy/tree/main). The GitHub repo also has docs (including written report), test data and test results.

## Reproducible workflow

Below are comprehensive steps to run the workflow. If you prefer, scroll to the bottom to find the entire, uninterrupted list of commands.

`cd` into the root directory for the **entirety of this workflow**.

```sh
cd ~/FST_dxy_analysis/
```

Note that it can take some time to build the environment and run the scripts.

### Import data

This workflow is rigidly built to work with the `ProjTaxa.vcf.gz` dataset. Please copy it into the `data` folder or make note of where else you might have it, as it will be passed as an argument to the first script. ***NOTE: if you choose to call the data file from another folder, intermediate data will be written to that destination.***

### Build environment

Build the conda environment from the project root and activate it:

```sh
conda env create -f environment.yml
conda activate Todreas_FST_dxy
```

The conda environment contains VCFTools, BCFTools, bio2zarr, pytz, Python, sgkit, matplotlib, and all dependencies (including Xarray, numpy, and SciPy).

### Change permissions

It will be helpful to update the script permissions so they can be run from anywhere as executables.

Update permissions:

```sh
chmod +x scripts/*
```

### Run analyses

Both scripts need to be run on their own, since `sgkit` (Statistical Genetics Toolkit) relies on `Zarr` directories, which cant be written to `stdout`.

Run analyses:

```sh
./scripts/gzVCF_toFilter_toZarr.sh data/ProjTaxa.vcf.gz
./scripts/Zarr_toXArray_toResults.py data/Filtered.vcz -o results/stats.csv -p plot.pdf
```

### Entire pipeline

Before proceeding, `cd` into the root.

```sh
conda env create -f environment.yml
conda activate FST_dxy
chmod +x scripts/*
./scripts/gzVCF_toFilter_toZarr.sh data/ProjTaxa.vcf.gz
./scripts/Zarr_toXArray_toResults.py data/Filtered.vcz -o results/stats.csv -p results/plot.pdf
```