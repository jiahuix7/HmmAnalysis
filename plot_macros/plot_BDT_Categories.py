import uproot as ur
import mplhep as hep
import numpy as np
import math
import matplotlib.pyplot as plt
import sys

from utils.labels import luminosity, x_range, n_bins, x_labels
from utils.helper import get_canvas, save_figure, get_histograms_ratio

eras = []
if len(sys.argv) == 1:
    eras = ["2022", "2022EE", "2022Combined"]
elif len(sys.argv) == 2:
    eras = [sys.argv[1]]
else:
    print("Use 0 arguments for run over the all the eras or use the eras as argument.")
    exit()


plt.style.use(hep.style.CMS)

bdt_categories = [0, 0.2, 0.4, 1]

for era in eras:
    with ur.open(
        "../root_io/skim/background_" + era + "_skim_ggH.root:tree_output"
    ) as file:
        bkg_branches = file.arrays(
            ["BDT_ggH", "weight_no_lumi", "diMuon_mass"], library="np"
        )
        bkg_hist, bkg_bins = np.histogram(
            bkg_branches["BDT_ggH"],
            bins=n_bins["BDT_ggH"],
            range=x_range["BDT_ggH"],
            weights=float(luminosity[era]) * bkg_branches["weight_no_lumi"],
        )

    with ur.open("../root_io/skim/ggH_" + era + "_skim_ggH.root:tree_output") as file:
        signal_branches = file.arrays(
            ["BDT_ggH", "weight_no_lumi", "diMuon_mass"], library="np"
        )
        signal_hist, signal_bins = np.histogram(
            signal_branches["BDT_ggH"],
            bins=n_bins["BDT_ggH"],
            range=x_range["BDT_ggH"],
            weights=float(luminosity[era]) * signal_branches["weight_no_lumi"],
        )
    fig, axs = get_canvas(True)

    hep.histplot(
        bkg_hist / np.sum(bkg_hist),
        bkg_bins,
        label="Background",
        ax=axs[0],
        stack=True,
        linewidth=2,
        color="red",
    )

    hep.histplot(
        signal_hist / np.sum(signal_hist),
        signal_bins,
        label="Signal (ggH)",
        color="blue",
        linewidth=2,
        ax=axs[0],
    )

    hep.cms.label(
        data="True",
        label="",
        year=era,
        com="13,6",
        lumi=luminosity[era],
        ax=axs[0],
    )

    max_height = max(
        np.max(signal_hist / np.sum(signal_hist)), np.max(bkg_hist / np.sum(bkg_hist))
    )

    axs[0].set_yscale("log")
    axs[0].set_ylim(
        0.001,
        10 * max_height,
    )
    # axs[0].set_ylim(
    # 0.0,
    # 1.3
    # * max(
    # np.max(signal_hist / np.sum(signal_hist)),
    # np.max(bkg_hist / np.sum(bkg_hist)),
    # ),
    # )
    axs[0].set_xlim(signal_bins[0], signal_bins[-1])
    axs[0].set_ylabel(r"Events/ Total events", loc="center")
    axs[0].legend(frameon=False, loc="upper right")

    signal = []
    bkg_sqrt = []

    for category in range(len(bdt_categories) - 1):
        if category != 0:
            axs[0].axvline(
                x=bdt_categories[category],
                ymin=0.001,
                ymax=max_height,
                color="grey",
                linestyle="--",
                alpha=0.5,
            )
        bkg_bool_list = (
            (bkg_branches["diMuon_mass"] > 121)
            & (bkg_branches["diMuon_mass"] < 129)
            & (bkg_branches["BDT_ggH"] > bdt_categories[category])
            & (bkg_branches["BDT_ggH"] < bdt_categories[category + 1])
        )
        signal_bool_list = (
            (signal_branches["diMuon_mass"] > 121)
            & (signal_branches["diMuon_mass"] < 129)
            & (signal_branches["BDT_ggH"] > bdt_categories[category])
            & (signal_branches["BDT_ggH"] < bdt_categories[category + 1])
        )

        signal_events = np.sum(
            float(luminosity[era]) * signal_branches["weight_no_lumi"][signal_bool_list]
        )
        bkg_events = np.sum(
            float(luminosity[era]) * bkg_branches["weight_no_lumi"][bkg_bool_list]
        )
        signal.append(signal_events)
        bkg_sqrt.append(math.sqrt(bkg_events))

    ratio_hist, ratio_error = get_histograms_ratio(np.array(signal), np.array(bkg_sqrt))

    hep.histplot(
        ratio_hist,
        bdt_categories,
        yerr=ratio_error,
        xerr=True,
        histtype="errorbar",
        color="black",
        ax=axs[1],
    )

    axs[1].set_ylabel(r"S/$\sqrt{B}$", loc="center")
    axs[1].set_ylim(0.0, 1.5)
    axs[1].set_xlim(signal_bins[0], signal_bins[-1])
    axs[1].set_xlabel(x_labels["BDT_ggH"])

    output_directory = "../plots/ggH_category/ggH/"
    save_figure(fig, output_directory, "BDT_output_" + era)
