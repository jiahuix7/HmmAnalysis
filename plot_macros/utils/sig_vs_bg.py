# import uproot as ur
import mplhep as hep
import numpy as np
import matplotlib.pyplot as plt
import uproot as ur
from matplotlib import colors as mplcolors

from .labels import x_labels, n_bins, x_range
from .helper import get_canvas, save_figure, get_histograms

y_axis_max_range = {
    "diMuon_rapidity": 0.04,
    "diMuon_pt": 0.16,
    "mu1_pt_mass_ratio": 0.2,
    "mu2_pt_mass_ratio": 0.2,
    "mu1_eta": 0.04,
    "mu2_eta": 0.04,
    "phi_CS": 0.03,
    "cos_theta_CS": 0.03,
}


def draw_sig_and_bg(variable, era, background_sources, signal_sources):
    plt.style.use(hep.style.CMS)

    background_histograms = get_histograms(variable, background_sources, era)
    signal_histograms = get_histograms(variable, signal_sources, era)

    total_bg_np_histogram = np.array([])
    total_sig_np_histogram = np.array([])
    bins = np.array([])

    for i, hist in enumerate(background_histograms):
        if i == 0:
            total_bg_np_histogram, bins = hist.to_numpy()
        else:
            total_bg_np_histogram = total_bg_np_histogram + hist.to_numpy()[0]

    for i, hist in enumerate(signal_histograms):
        if i == 0:
            total_sig_np_histogram = hist.to_numpy()[0]
        else:
            total_sig_np_histogram = total_sig_np_histogram + hist.to_numpy()[0]

    fig, ax = get_canvas()

    hep.histplot(
        total_bg_np_histogram / np.sum(total_bg_np_histogram),
        bins,
        yerr=True,
        histtype="fill",
        label="background",
        ax=ax,
        stack=True,
        color="blue",
        alpha=0.5,
    )

    hep.histplot(
        total_sig_np_histogram / np.sum(total_sig_np_histogram),
        bins,
        yerr=True,
        histtype="fill",
        label=" signal",
        ax=ax,
        stack=True,
        color="red",
        alpha=0.5,
    )

    hep.cms.label(data="True", label="Test", year="2022", com="13,6", ax=ax)

    ax.set_ylabel("Events / Total Events")
    ax.set_xlabel(x_labels[variable])
    ax.set_ylim(0, y_axis_max_range[variable])
    ax.set_xlim(bins[0], bins[-1])
    # ax.set_yscale("log")
    ax.legend(frameon=False, loc="upper right", ncols=2)

    save_figure(fig, "../plots/sig_vs_bkg/", variable + "_" + era + "_MCData_ratio")


def clean_null_values(branches, variable):

    if variable == "delta_phi_diJet":
        branches["weight"] = branches["weight"][branches[variable] != -1]
        branches[variable] = branches[variable][branches[variable] != -1]

    elif variable != "n_jet":
        branches["weight"] = branches["weight"][branches[variable] != 0]
        branches[variable] = branches[variable][branches[variable] != 0]


def draw_sig_and_bg_from_tuple(variable, era):
    plt.style.use(hep.style.CMS)

    with ur.open(
        "../root_io/skim/background_"
        + era
        + "_skim.root:tree_skim"
        # "../root_io/skim/no_diMuon_mass_cut/background_skim.root:tree_skim"
    ) as file:
        background_branches = file.arrays([variable, "weight"], library="np")
    with ur.open(
        "../root_io/skim/signal_"
        + era
        + "_skim.root:tree_skim"
        # "../root_io/skim/no_diMuon_mass_cut/signal_skim.root:tree_skim"
    ) as file:
        signal_branches = file.arrays([variable, "weight"], library="np")

    clean_null_values(signal_branches, variable)
    clean_null_values(background_branches, variable)

    if variable == "delta_eta_diJet" or variable == "delta_phi_diJet":
        signal_branches[variable] = np.absolute(signal_branches[variable])
        background_branches[variable] = np.absolute(background_branches[variable])

    bkg_histogram, bins = np.histogram(
        background_branches[variable],
        bins=n_bins[variable],
        range=x_range[variable],
        weights=background_branches["weight"],
    )
    signal_histogram, _ = np.histogram(
        signal_branches[variable],
        bins=n_bins[variable],
        range=x_range[variable],
        weights=signal_branches["weight"],
    )

    fig, ax = get_canvas()

    hep.histplot(
        signal_histogram / np.sum(signal_histogram),
        bins,
        yerr=False,
        histtype="fill",
        label=" signal",
        ax=ax,
        # facecolor = (blue[0], blue[1], blue[2], .3),
        color="blue",
        alpha=0.4,
        # color = (blue[0], blue[1], blue[2], .3),
        # edgecolor = "blue",
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
        # facecolor = (red[0], red[1], red[2], 0.5),
        # edgecolor = "red",
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
    hep.cms.label(data="True", label="Test", year="2022", com="13.6", ax=ax)

    plot_log_variables = ["leading_jet_pt", "subleading_jet_pt", "n_jet", "delta_eta_diJet", "z_zeppenfeld", "min_delta_phi_dimuon_jet", "min_delta_eta_dimuon_jet"]
    ax.set_ylabel("Events / Total Events")
    ax.set_xlabel(x_labels[variable])
    # ax.set_ylim(0, y_axis_max_range[variable])
    ax.set_ylim(0.0, 1.3 * np.max(bkg_histogram / np.sum(bkg_histogram)))
    if variable in plot_log_variables:
        ax.set_ylim(0.01, 1.1)
        ax.set_yscale("log")
    ax.set_xlim(bins[0], bins[-1])
    ax.legend(frameon=False, loc="upper right", ncols=1)

    save_figure(
        fig, "../plots/sig_vs_bkg/" + era + "/", variable + "_" + era + "_sig_vs_bkg"
    )
