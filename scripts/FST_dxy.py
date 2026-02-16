#!/usr/bin/env python

# Import libraries
import sys
import os
import csv
import argparse as ap
import sgkit as sg
import xarray as xr
import numpy as np
import scipy.stats as sp
import matplotlib.pyplot as plt


# Define functions
def parse_args() -> ap.Namespace:
    """
    Parse arguments passed at the command line

    :return: An object with the parsed arguments
    :rtype: argparse.Namespace
    """
    parser = ap.ArgumentParser(
        prog="FST_dxy",
        description=(
            "This program takes the ProjTaxa.vcz/ Zarr directory as input, "
            + "converts it to an xarray.Dataset object, computes pairwise "
            + "windowed FST and dxy, and generates scatterplots."
        ),
        epilog="Author: Oliver Todreas",
    )

    # Add arguments
    parser.add_argument("filename")
    parser.add_argument("-o", "--output", help="Name of csv with correlation statistics")
    parser.add_argument("-p", "--plot", help="Name of plot to be saved")

    # Assign parsed arguments to object
    args = parser.parse_args()

    # Handle bad inputs
    if not os.path.isdir(os.path.realpath(args.filename)):
        sys.exit("Input is invalid or does not exist")

    if not args.filename.endswith(".vcz"):
        sys.exit("Input must be .vcz")

    if not os.path.isdir(os.path.dirname(args.output)):
        sys.exit("Output directory does not exist")

    if not os.path.isdir(os.path.dirname(args.plot)):
        sys.exit("Plot directory does not exist")

    if not args.output.endswith(".csv"):
        sys.exit("Output summary must be .csv")

    if not args.plot.endswith((".png", ".pdf", ".jpeg", ".jpg", ".svg")):
        sys.exit("Invalid plot filetype")

    # Return parsed arguments
    return args


def load_data(args: ap.Namespace) -> list:
    """
    Load data from Zarr (vcz), assign cohorts (populations), chromosomes, split
    into 2 datasets and return list of two datasets

    :param args: Parsed arguments. Only uses the `filename` argument
    :type args: ap.Namespace
    :return: one xarray.Dataset per chromosome in a list
    :rtype: list
    """

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


def compute_new_dims(ds: list) -> list:
    """
    Merge windows, FST and dxy dimensions into each chromosomes dataset

    :param ds: a list of xarray.Datasets, one per chromosome
    :type ds: list
    :return: The same list, but each xarray.Dataset has window, FST, and dxy dimensions merged into it
    :rtype: list
    """

    # Loop over the index of each dataset by chromosome
    for i in range(len(ds)):
        # Merge windows into dataset
        ds[i] = sg.window_by_variant(ds[i], size=80)

        # Merge FST and dxy into dataset (both are computed with the `sg.Fst()` method)
        ds[i] = sg.Fst(ds[i])

    # Return the list of merged datasets
    return ds


def make_output(ds: list, args: ap.Namespace):
    """
    Create and save plot, save statistics as csv.

    :param ds: list of xarray.Datasets with window, FST, and dxy dimensions
    :type ds: list
    :param args: arguments from command line. All arguments but filename are used
    :type args: ap.Namespace
    """

    # Create tuples with cohort and chromosome names
    cohort_names = ("8N", "K", "Lesina")
    chrom_names = ("Chromosome 5", "Chromosome Z")

    # Create key for indices of statistics by population comparison
    x = np.array([(0, 1), (0, 2), (1, 2)])

    # Create subplots
    fig, ax = plt.subplots(
        nrows=2,
        ncols=3,
        sharex=True,
        sharey=True,
        figsize=(6, 3.5),
        constrained_layout=True,
    )

    # Create an array to store statistics in with header
    stats_out = [["rho", "p", "cohort_comparison", "chromosome"]]

    # Loop through subplot rows
    for i in range(ax.shape[0]):
        # Loop through subplot columns
        for j in range(ax.shape[1]):
            # Assign the two cohorts being compared to `comparison`
            comparison = f"{cohort_names[x[j, 0]]} vs {cohort_names[x[j, 1]]}"

            # Assign FST values for a give population comparison to array
            fst = ds[i].stat_Fst.values[:, x[j, 0], x[j, 1]]

            # Assign dxy values for a given population comparison to array
            dxy = ds[i].stat_divergence.values[:, x[j, 0], x[j, 1]]

            # Assign correlation stats to scipy SignificanceResult
            corr = sp.spearmanr(fst, dxy)

            # Extract rounded values to plot from correlation stats
            stats_row = []
            corr_round = []
            for stat in corr:
                # Append stat to row of output file
                stats_row.append(stat)

                # Use scientific notation if exceedingly small
                if stat < 0.005:
                    corr_round.append(f"{stat:.0e}")

                else:
                    corr_round.append(f"{stat:.2f}")

            # Append population comparison and chromosome to output row
            stats_row.extend([comparison, chrom_names[i]])
            stats_out.append(stats_row)

            # Draw a scatter plot
            scatter = ax[i, j].scatter(
                # Plot FST on x and dxy on y
                x=fst,
                y=dxy,
                # Color scale
                c=ds[i].window_start.values / ds[-1].window_stop.values[-1],
                cmap="managua",
                # Point aesthetics
                s=50,
                alpha=0.3,
            )

            # Place stats in subplots
            ax[i, j].text(
                # Top right
                x=0.05,
                y=0.95,
                # Latex-style and f-string style formatting
                s=(rf"$\rho = {corr_round[0]}$" + "\n" + rf"$p = {corr_round[1]}$"),
                # Assign coordinates to the axes-relative space rather than real x-y values
                transform=ax[i, j].transAxes,
                # Align left and top
                ha="left",
                va="top",
            )

            # Set population comparison labels on top plots
            if i == 0:
                # Assign twin axis to `t_lab` and remove ticks
                t_lab = ax[i, j].twiny()
                t_lab.set_xticks([])

                # Set text label
                t_lab.set_xlabel(
                    f"{cohort_names[x[j, 0]]} vs {cohort_names[x[j, 1]]}", labelpad=8
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
        label="Window order",
    )

    # Save stats
    if args.output:
        with open(args.output, "w") as f:
            csv.writer(f).writerows(stats_out)

    # Save plot
    if args.plot:
        plt.savefig(args.plot)


def main():
    """
    Parse command line arguments, load data into xarray.Datasets, merge new
    dimensions into xarray.Datasets, create and save plots and outputs in csv
    """
    args = parse_args()
    ds = load_data(args)
    ds = compute_new_dims(ds)
    make_output(ds, args)


# Run program
if __name__ == "__main__":
    main()
