# import uproot as ur
import mplhep as hep
import numpy as np
import matplotlib.pyplot as plt
import uproot as ur

from .labels import x_labels, n_bins, x_range, variables_type
from .helper import (
    get_canvas,
    save_figure,
    clean_null_values,
    get_output_directory,
)

def draw_sig_and_bg_from_tuple(variable, era):
    plt.style.use(hep.style.CMS)

    with ur.open(
        "../root_io/skim/background_"
        + era
        + "_skimNO50120.root:tree_output"
    ) as file:
        background_branches = file.arrays([variable, "weight_no_lumi"], library="np")
    with ur.open(
        "../root_io/skim/signal_"
        + era
        + "_skim.root:tree_output"
    ) as file:
        signal_branches = file.arrays([variable, "weight_no_lumi"], library="np")

    clean_null_values(signal_branches, [variable, "weight_no_lumi"], variables_type)
    clean_null_values(background_branches, [variable, "weight_no_lumi"], variables_type)

    if "delta_phi" in variable:
        signal_branches[variable] = np.absolute(signal_branches[variable])
        background_branches[variable] = np.absolute(background_branches[variable])

    bkg_histogram, bins = np.histogram(
        background_branches[variable],
        bins=n_bins[variable],
        range=x_range[variable],
        weights=background_branches["weight_no_lumi"],
    )
    signal_histogram, _ = np.histogram(
        signal_branches[variable],
        bins=n_bins[variable],
        range=x_range[variable],
        weights=signal_branches["weight_no_lumi"],
    )

    fig, ax = get_canvas()

    hep.histplot(
        signal_histogram / np.sum(signal_histogram),
        bins,
        yerr=False,
        histtype="fill",
        label=" signal",
        ax=ax,
        color="blue",
        alpha=0.4,
    )

    hep.histplot(
        signal_histogram / np.sum(signal_histogram),
        bins,
        yerr=False,
        ax=ax,
        color="blue",
        linewidth=2,
    )

    hep.histplot(
        bkg_histogram / np.sum(bkg_histogram),
        bins,
        yerr=False,
        histtype="fill",
        label="background",
        ax=ax,
        color="red",
        alpha=0.4,
    )

    hep.histplot(
        bkg_histogram / np.sum(bkg_histogram),
        bins,
        yerr=False,
        ax=ax,
        color="red",
    )
    hep.cms.label(data="True", label="", year=era, com="13.6", ax=ax)

    plot_log_variables = [
        "leading_jet_pt",
        "subleading_jet_pt",
        "n_jet",
        "delta_eta_diJet",
        "z_zeppenfeld",
        "min_delta_phi_dimuon_jet",
        "min_delta_eta_dimuon_jet",
    ]

    ax.set_ylabel("Events / Total Events")
    ax.set_xlabel(x_labels[variable])
    ax.set_ylim(0.0, 1.3 * np.max(bkg_histogram / np.sum(bkg_histogram)))
    if variable in plot_log_variables:
        ax.set_ylim(0.001, 1.1)
        ax.set_yscale("log")
    ax.set_xlim(bins[0], bins[-1])
    ax.legend(frameon=False, loc="upper right", ncols=1)

    output_directory = "../plots/sig_vs_bkg/" + era + "/"
    output_directory = get_output_directory(variable, output_directory, variables_type)

    save_figure(fig, output_directory, variable + "_" + era + "_sig_vs_bkg")
