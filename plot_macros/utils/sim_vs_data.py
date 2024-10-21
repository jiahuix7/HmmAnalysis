import uproot as ur
import mplhep as hep
import numpy as np
import matplotlib.pyplot as plt

from .labels import x_labels, background_labels, luminosity  # , y_labels
from .helper import get_canvas, save_figure, get_histograms, get_histograms_ratio

y_axis_max_range = {
    "mu1_pt_mass_ratio": 10e6,
    "mu2_pt_mass_ratio": 10e6,
    "mu1_eta": 10e6,
    "mu2_eta": 10e6,
    "phi_CS": 10e6,
    "cos_theta_CS": 10e6,
    "diMuon_mass": 10e6,
    "diMuon_rapidity": 10e6,
    "diMuon_mass_full_range": 10e8,
    "diMuon_pt": 10e8,
    "diMuon_phi": 10e8,
    "diMuon_eta": 10e8,
    "n_jet": 10e8,
    "jet_pt": 10e8,
    "jet_eta": 10e8,
    "jet_phi": 10e8,
    "jet_mass": 10e8,
    "diJet_pt": 10e8,
    "diJet_eta": 10e8,
    "diJet_phi": 10e8,
    "diJet_mass": 10e8,
    "diJet_mass_mo": 10e8,
    "diJet_DeltaEta": 10e8,
}


def get_color_list(number_of_histograms):
    colors = [
        "#3f90da",
        "#ffa90e",
        "#bd1f01",
        "#94a4a2",
        "#832db6",
        "#a96b59",
        "#e76300",
        "#b9ac70",
        "#717581",
        "#92dadd",
    ]

    color_list = []
    for i in range(number_of_histograms):
        color_list.append(colors[i])

    return color_list


def get_background_label_list(background_sources):
    labels_list = []
    for source in background_sources:
        labels_list.append(background_labels[source])
    return labels_list


def draw_signal_sources(signal_sources, variable, era, ax):
    signal_colors = {"ggH": "red", "VBF": "blue", "ttH": "lime"}
    for source in signal_sources:
        with ur.open(
            "../root_io/" + source + "_" + era + "_histograms.root"
        ) as data_file:
            histogram = data_file[variable]

        numpy_histogram, bins = histogram.to_numpy()
        hep.histplot(
            numpy_histogram * 10,
            bins,
            yerr=False,
            # yerr=True,
            label=source,
            color=signal_colors[source],
            ax=ax,
        )


def draw_data_and_simul_and_ratio(variable, era, background_sources, signal_sources):
    plt.style.use(hep.style.CMS)  # or ATLAS/LHCb2
    background_histograms = get_histograms(variable, background_sources, era)

    with ur.open("../root_io/Data_" + era + "_histograms.root") as data_file:
        data_histogram = data_file[variable]

    data_numpy_histogram, data_bins = data_histogram.to_numpy()
    if "mass" in variable:
        data_numpy_histogram[data_numpy_histogram == 0] = -100.0
    # print(data_numpy_histogram)

    fig, axs = get_canvas(True)

    hep.histplot(
        background_histograms,
        yerr=True,
        histtype="fill",
        label=get_background_label_list(background_sources),
        ax=axs[0],
        stack=True,
        color=get_color_list(len(background_sources)),
    )

    hep.histplot(
        data_numpy_histogram,
        data_bins,
        yerr=True,
        histtype="errorbar",
        label="data",
        color="black",
        ax=axs[0],
    )

    draw_signal_sources(signal_sources, variable, era, axs[0])

    hep.cms.label(
        data="True",
        label="Test",
        year="2022",
        com="13,6",
        lumi=luminosity[era],
        ax=axs[0],
    )

    axs[0].set_ylabel(r"Events")
    # axs[0].set_ylim(-10000, y_axis_max_range[variable])
    axs[0].set_ylim(0.1, y_axis_max_range[variable])
    axs[0].set_xlim(data_bins[0], data_bins[-1])
    axs[0].set_yscale("log")
    axs[0].legend(frameon=False, loc="upper right", ncols=2)
    axs[0].tick_params(axis="x", which="both", bottom=True, top=True, labelbottom=False)

    plt.axhline(y=1, color="grey", linestyle="--", alpha=0.5)

    tot_bg_numpy_hist = np.array([])
    for i, bg_hist in enumerate(background_histograms):
        if i == 0:
            tot_bg_numpy_hist = bg_hist.to_numpy()[0]
        else:
            tot_bg_numpy_hist = tot_bg_numpy_hist + bg_hist.to_numpy()[0]

    ratio_hist, ratio_error = get_histograms_ratio(
        data_numpy_histogram, tot_bg_numpy_hist
    )

    hep.histplot(
        ratio_hist,
        data_bins,
        yerr=ratio_error,
        histtype="errorbar",
        label="data",
        color="black",
        ax=axs[1],
    )

    axs[1].set_ylabel("Data/MC", loc="center")
    axs[1].set_ylim(0.5, 1.5)
    axs[1].set_xlim(data_bins[0], data_bins[-1])
    axs[1].set_xlabel(x_labels[variable])

    output_directory = "../plots/ratio/" + era + "/"
    if "diMuon" in variable:
        output_directory = output_directory + "diMuon/"
    elif "diJet" in variable:
        output_directory = output_directory + "diJet/"
    elif "jet" in variable:
        output_directory = output_directory + "Jet/"
    else:
        output_directory = output_directory + "muon/"

    save_figure(fig, output_directory, variable + "_" + era + "_MCData_ratio"
