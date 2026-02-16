#!/usr/bin/env python

# Import libraries
import argparse as ap
import sgkit as sg
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt


# Define functions
def parse_args() -> str:
    pass

def load_data(path: str) -> list:
    pass

def compute_stats(ds: list) -> list:
    pass

def make_plot(ds: list):
    pass

def main(path: str):
    path = parse_args()
    ds = load_data(path)
    ds = compute_stats(ds)
    make_plot(ds)


# Run program
if __name__ == "__main__":
    main()



# # Load data into an xarray.Dataset object
# ds = sg.load_dataset("../test/ProjTaxaFilt.vcz")
# # Map population structure onto the dimension `sample_cohort`
# ds["sample_cohort"] = xr.DataArray(
#     np.array([0] * 5 + [1] * 5 + [2] * 5), dims="samples"
# )

# # Create 1-D numpy.array equivalent to the `CHROM` column in the VCF
# chrom = ds.contig_id.values[ds.variant_contig.values]

# # Assign boolean masks for each chromosome to use to split the dataset by chromosome index
# mask_5 = chrom == "chr5"
# mask_Z = np.invert(mask_5)

# # Create two datasets that are subsets of the original by chromosome
# ds_chr5 = ds.isel(variants=mask_5)
# ds_chrZ = ds.isel(variants=mask_Z)

# # Reassign the `ds` variable to a list storing pointers to both datasets
# ds = [ds_chr5, ds_chrZ]

# # Loop over the index of each dataset by chromosome
# for i in range(len(ds)):

#     # Merge windows into dataset
#     ds[i] = sg.window_by_variant(ds[i], size=80)

#     # Merge FST and dxy into dataset (both are computed with the `sg.Fst()` method)
#     ds[i] = sg.Fst(ds[i])

# # Create tuples with cohort and chromosome names
# cohort_names = ("8N", "K", "Lesina")
# chrom_names = ("Chromosome 5", "Chromosome Z")

# # Create key for indices of statistics by population comparison
# x = np.array([(0, 1), (0, 2), (1, 2)])

# # Create subplots
# fig, ax = plt.subplots(2, 3, sharex=True, sharey=True, figsize=(6, 3))

# # Loop through subplot rows
# for i in range(ax.shape[0]):
#     # Loop through subplot columns
#     for j in range(ax.shape[1]):
#         # Draw a scatter plot
#         scatter = ax[i, j].scatter(
#             # FST values for a give population comparison
#             ds[i].stat_Fst.values[:, x[j, 0], x[j, 1]],

#             # dxy values for a given population comparison
#             ds[i].stat_divergence.values[:, x[j, 0], x[j, 1]],

#             # Color scale
#             c=ds[i].window_start.values / ds[-1].window_stop.values[-1] * 100,
#             cmap="managua",

#             # Point aesthetics
#             s=50,
#             alpha=1/3
#         )

#         # Set population comparison labels on top plots
#         if i == 0:
#             # Assign twin axis to `t_lab` and remove ticks
#             t_lab = ax[i, j].twiny()
#             t_lab.set_xticks([])

#             # Set text label
#             t_lab.set_xlabel(
#                 f"{cohort_names[x[j, 0]]} vs {cohort_names[x[j, 1]]}",
#                 labelpad=8
#             )

#         # Set x label on bottom plots
#         else:
#             ax[i, j].set_xlabel("FST")

#     # Set y label on left plots
#     ax[i, 0].set_ylabel("dxy")

#     # Assign twin axis to `r_lab` and remove ticks
#     r_lab = ax[i, -1].twinx()
#     r_lab.set_yticks([])
    
#     # Set chromosome labels on right plots
#     r_lab.set_ylabel(chrom_names[i], rotation=90, labelpad=8)

# # Create colorbar
# fig.colorbar(
#     # Use scatter plot data
#     mappable=scatter,
#     ax=ax,

#     # Aesthetics
#     location="right",
#     aspect=25, 
#     pad=0.09,
#     label='Window Start (% Chromosome Length)'
# )