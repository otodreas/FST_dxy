# FST_dxy

Project for BINP28 at Lund University's masters in bioinformatics that compares FST and dxy across the genome.

## Requirements

With a Linux 64-bit platform, you can build my conda environment form `./environment.yml`, which is explained below.

If your system does not match or the environment build doesn't work, you can build the conda environment manually and install

- `vcftools=0.1`
- `bcftools=1.23`
- `bio2zarr=0.1`
- `python=3.12`
- `sgkit=0.10`
- `matplotlib=3.10`

## Directory structure

The directory structure of this reproducible workflow is as follows

```
FST_dxy/
├── docs/ # archived scripts, submitted files
├── environment.yml
├── LICENSE
├── README.md
├── results/
│   ├── plot.pdf
│   └── stats.csv
├── scripts/
│   ├── gzVCF_toFilter_toZarr.sh
│   └── Zarr_toXArray_toResults.py
└── test/
    ├── compute_summary_stats.sh
    ├── make_test_data.sh
    └── ProjTaxaSmall.vcf.gz
```

The scripts in `./scripts/` are intended to be run sequentially, which is outlined in **Reproducible workflow: Run analyses**.

## Test data

The scripts can be run on `./test/ProjTaxaSmall.vcf.gz`, but use a **window size of 20 variants**. Since window size is hard-coded for reproducibility, you will need to change it on line `295` of `./scripts/Zarr_toXArray_toResults.py`, inside the `main` function.

```py
def main():
    """
    Parse command line arguments, load data into xarray.Datasets, merge new
    dimensions into xarray.Datasets, create and save plots and outputs in csv
    """
    window_size = 1_250 # change to 20

    args = parse_args()
    ds = load_data(args)
    ds = compute_new_dims(ds, window_size)
    make_output(ds, args, window_size)
```

## Reproducible workflow

Below are comprehensive steps to run the workflow. If you prefer, scroll to the bottom to find the entire, uninterrupted list of commands.

### Clone repo

Clone the repo and `cd` into the root directory for the **entirety of this workflow**.

```sh
cd ~/FST_dxy/
```

Note that it can take some time to build the environment and run the scripts.

### Import data

This workflow is rigidly built to work with the `ProjTaxa.vcf.gz` dataset. Please copy it into the `data` folder from the Lund University bioinformatics server or make note of where else you might have it, as it will be passed as an argument to the first script. ***NOTE: if you choose to call the data file from another folder, intermediate data will be written to that destination.***

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
./scripts/Zarr_toXArray_toResults.py data/Filtered.vcz -o results/stats_reproduced.csv -p results/plot_reproduced.pdf
```

### Entire pipeline

Before proceeding, `cd` into the root.

```sh
conda env create -f environment.yml
conda activate Todreas_FST_dxy
chmod +x scripts/*
./scripts/gzVCF_toFilter_toZarr.sh data/ProjTaxa.vcf.gz
./scripts/Zarr_toXArray_toResults.py data/Filtered.vcz -o results/stats_reproduced.csv -p results/plot_reproduced.pdf
```

### Pipeline for test dataset

```sh
conda env create -f environment.yml
conda activate Todreas_FST_dxy
chmod +x scripts/*
./scripts/gzVCF_toFilter_toZarr.sh test/ProjTaxaSmall.vcf.gz
./scripts/Zarr_toXArray_toResults.py test/Filtered.vcz -o results/stats_reproduced_test.csv -p results/plot_reproduced_test.pdf
```