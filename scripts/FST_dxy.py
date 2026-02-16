#!/usr/bin/env python

# Import libraries
import argparse as ap
import sgkit as sg
import xarray as xr
import numpy as np
import scipy.stats as sp
import matplotlib.pyplot as plt
import matplotlib.transforms as trans


# Define functions
def parse_args() -> ap.Namespace:
    # Define parser
    parser = ap.ArgumentParser(
        prog="FST_dxy",
        description=(
            "This program takes the ProjTaxa.vcz/ Zarr directory as input, "
            + "converts it to an xarray.Dataset object, computes pairwise "
            + "windowed FST and dxy, and generates scatterplots."
        ),
        epilog="Author: Oliver Todreas"
    )

    # Add arguments
    parser.add_argument("filename")
    parser.add_argument("-o", "--output")

    # Return parsed arguments
    return parser.parse_args()

def load_data(args: ap.Namespace) -> list:
    # Load data into an xarray.Dataset object
    ds = sg.load_dataset(args.filename)

    # Map population structure onto the dimension `sample_cohort`
    ds["sample_cohort"] = xr.DataArray(
        np.array([0] * 5 + [1] * 5 + [2] * 5), dims="samples"
    )

    # Create 1-D numpy.array equivalent to the `CHROM` column in the VCF
    chrom = ds.contig_id.values[ds.variant_contig.values]

    # Assign boolean masks for each chromosome to use to split the dataset by chromosome index
    mask_5 = chrom == "chr5"
    mask_Z = np.invert(mask_5)

    # Return a list storing two datasets that are subsets of the original dataset
    return [ds.isel(variants=mask_5), ds.isel(variants=mask_Z)]

def compute_stats(ds: list) -> list:
    # Loop over the index of each dataset by chromosome
    for i in range(len(ds)):

        # Merge windows into dataset
        ds[i] = sg.window_by_variant(ds[i], size=80)

        # Merge FST and dxy into dataset (both are computed with the `sg.Fst()` method)
        ds[i] = sg.Fst(ds[i])
    
    ds
    # Return the list of merged datasets
    return ds

def make_plot(ds: list, args: ap.Namespace):
    # Create tuples with cohort and chromosome names
    cohort_names = ("8N", "K", "Lesina")
    chrom_names = ("Chromosome 5", "Chromosome Z")

    # Create key for indices of statistics by population comparison
    x = np.array([(0, 1), (0, 2), (1, 2)])

    # Create subplots
    fig, ax = plt.subplots(2, 3, sharex=True, sharey=True, figsize=(6, 3.5), constrained_layout=True)

    # Loop through subplot rows
    for i in range(ax.shape[0]):
        # Loop through subplot columns
        for j in range(ax.shape[1]):
            # Assign FST values for a give population comparison to array
            fst = ds[i].stat_Fst.values[:, x[j, 0], x[j, 1]]

            # Assign dxy values for a given population comparison to array
            dxy = ds[i].stat_divergence.values[:, x[j, 0], x[j, 1]]

            # Assign correlation stats to scipy SignificanceResult
            corr = sp.spearmanr(fst, dxy)

            # Extract rounded values to plot from correlation stats
            corr_round = []
            for stat in corr:
                # Use scientific notation if exceedingly small
                if stat < 0.005:
                    corr_round.append(f"{stat:.0e}")

                else:
                    corr_round.append(f"{stat:.2f}")

            # Draw a scatter plot
            scatter = ax[i, j].scatter(
                # Plot FST on x and dxy on y
                fst,
                dxy,

                # Color scale
                c=ds[i].window_start.values / ds[-1].window_stop.values[-1],
                cmap="managua",

                # Point aesthetics
                s=50,
                alpha=1/3
            )

            # Place stats in subplots
            ax[i, j].text(
                # Top right
                x=0.05,
                y=0.95,

                # Latex-style and f-string style formatting
                s=(
                    fr"$\rho = {corr_round[0]}$"
                    + "\n"
                    + fr"$p = {corr_round[1]}$"
                ),

                # Assign coordinates to the axes-relative space rather than real x-y values
                transform=ax[i, j].transAxes,

                # Align left and top
                ha='left',
                va='top'
            )

            # Set population comparison labels on top plots
            if i == 0:
                # Assign twin axis to `t_lab` and remove ticks
                t_lab = ax[i, j].twiny()
                t_lab.set_xticks([])

                # Set text label
                t_lab.set_xlabel(
                    f"{cohort_names[x[j, 0]]} vs {cohort_names[x[j, 1]]}",
                    labelpad=8
                )

            # Set x label on bottom plots
            else:
                ax[i, j].set_xlabel("FST")

        # Set y label on left plots
        ax[i, 0].set_ylabel("dxy")

        # Assign twin axis to `r_lab` and remove ticks
        r_lab = ax[i, -1].twinx()
        r_lab.set_yticks([])
        
        # Set chromosome labels on right plots
        r_lab.set_ylabel(chrom_names[i], rotation=90, labelpad=8)

    # Create colorbar
    fig.colorbar(
        # Use scatter plot data
        mappable=scatter,
        ax=ax,

        # Aesthetics
        location="right",
        aspect=25, 
        pad=0.035,
        label="Window order"
    )

    # Save plot
    if args.output:
        plt.savefig(args.output)#, bbox_inches=trans.Bbox([[0, 0], [0, 0.5]]))

def main():
    args = parse_args()
    ds = load_data(args)
    ds = compute_stats(ds)
    make_plot(ds, args)


# Run program
if __name__ == "__main__":
    main()