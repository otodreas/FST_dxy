The VCF file does not contain invariant sites.

```sh
grep -v '^#' $VCF | awk '{print $5}' | grep -c "\."
```

"." represents an invariant site according to the [VCF Manual](https://samtools.github.io/hts-specs/VCFv4.2.pdf) (page 4-5).

So using pixy is not possible.

The other options are
- VCFtools for FST
- scikit-allel or PopGenome (R) for dxy

Scikit-allel has moved to [sgkit](https://sgkit-dev.github.io/sgkit/latest/index.html).

`sgkit.Fst()` and `sgkit.divergence()` are methods I might want to use

TODO: understand cohorts in the context of sgkit

Claude suggestions for directory structure:

```
project/
├── README.md
├── .gitignore
├── LICENSE
├── environment.yml          # or requirements.txt for Python deps
├── config.yml              # parameters (window size, populations, etc.)
├── data/
│   ├── raw/               # original VCF, sample metadata
│   ├── processed/         # filtered VCF, population files
│   └── README.md          # data sources, preprocessing notes
├── scripts/
│   ├── 01_filter_vcf.py
│   ├── 02_calculate_fst.py
│   ├── 03_calculate_dxy.py
│   ├── 04_plot_results.py
│   └── utils.py           # shared functions
├── results/               # instead of "outputs"
│   ├── fst/
│   ├── dxy/
│   ├── figures/
│   └── tables/
├── notebooks/             # exploratory analysis (optional)
│   └── exploratory_analysis.ipynb
└── report/
    ├── manuscript.tex
    ├── references.bib
    └── figures/           # symlink to ../results/figures/
```

