import uproot as ur
import mplhep as hep
import matplotlib.pyplot as plt
import numpy as np
import os

plt.style.use(hep.style.CMS)  # or ATLAS/LHCb2
# print(hep.style.CMS.keys())


def get_canvas(draw_ratio=False):
    if draw_ratio:
        fig, axs = plt.subplots(2, 1, height_ratios=[10, 2])
        fig.subplots_adjust(hspace=0.1)
        return fig, axs

    fig, axs = plt.subplots(1, 1)
    return fig, axs


def save_figure(fig, outputDirectory, name):
    os.makedirs(outputDirectory, exist_ok=True)
    fig.savefig(outputDirectory + name + ".pdf", bbox_inches="tight")
    fig.savefig(outputDirectory + name + ".png", bbox_inches="tight", dpi=300)
    fig.savefig(outputDirectory + name + ".pdf")
    fig.savefig(outputDirectory + name + ".png", dpi=300)
    print(outputDirectory + name + " Has been created")


x_labels = {
    "mass": r"$M_{\mu\mu}$ GeV",
    "pt": r"$Pt_{\mu\mu}$ GeV",
    "phi": r"$Phi_{\mu\mu}$ rad",
    "eta": r"$eta_{\mu\mu}$ ",
    "t_Mu_pt": r"$Pt_{\mu}$ GeV",
}

y_labels = {
    "mass": r"events/0.5gev",
    "pt": r"events/gev",
    "phi": r"events",
    "eta": r"events",
}

y_axis_max_range = {
    "mass": 10e6,
    "pt": 10e8,
    "phi": 10e8,
    "eta": 10e6,
}

background_lables = {
    "TT": "TT Background",
    "DY50-120": "DY MLL50-120 Bg",
    "DY120-200": "DY MLL120-200 Bg",
    "DY": "DY Background",
}

# ordered from bottom to top in the plot, so order it from lower to bigger cross section
# background_sources = ["TT", "DY120-200", "DY50-120"]
background_sources = ["TT", "DY"]


def get_background_histograms(variable):
    histograms = []
    for background in background_sources:
        with ur.open("../root_io/" + background + "hist.root") as file:
            histograms.append(file["diMuon_" + variable])

    return histograms


def get_color_list(number_of_histograms):
    colors = ["#5790fc", "#f89c20", "#e42536", "#964a8b", "#9c9ca1", "#7a21dd"]

    color_list = []
    for i in range(number_of_histograms):
        color_list.append(colors[i])

    return color_list


def get_background_label_list(background_sources):
    labels_list = []
    for source in background_sources:
        labels_list.append(background_lables[source])
    return labels_list


def draw_data_and_simul(variable, era):
    background_histograms = get_background_histograms(variable)

    with ur.open("../root_io/Datahist.root") as data_file:
        data_histogram = data_file["diMuon_" + variable]

    data_numpy_histogram, data_bins = data_histogram.to_numpy()
    if variable == "mass":
        data_numpy_histogram[data_numpy_histogram == 0] = -100.0

    fig, ax = get_canvas()

    hep.histplot(
        background_histograms,
        yerr=True,
        histtype="fill",
        label=get_background_label_list(background_sources),
        ax=ax,
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
        ax=ax,
    )

    hep.cms.label(data="True", label="Test", year="2022", com="13,6", lumi="17.4")

    ax.set_ylabel(y_labels[variable])
    ax.set_yscale("log")
    ax.set_ylim(0.1, y_axis_max_range[variable])
    ax.legend(frameon=False, loc="upper right")
    ax.set_xlabel(x_labels[variable])
    save_figure(fig, "../plots/", variable + "_" + era + "_MCData")


def draw_data_and_simul_and_ratio(variable, era):
    background_histograms = get_background_histograms(variable)

    with ur.open("../root_io/Datahist.root") as data_file:
        data_histogram = data_file["diMuon_" + variable]

    # with ur.open("../root_io/ggFhist.root") as data_file:
        # ggH_histogram = data_file["diMuon_" + variable]

    data_numpy_histogram, data_bins = data_histogram.to_numpy()
    if variable == "mass":
        data_numpy_histogram[data_numpy_histogram == 0] = -100.0

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

    # hep.histplot(
        # ggH_histogram,
        # yerr=True,
        # # histtype="errorbar",
        # label="ggF",
        # color="red",
        # ax=axs[0],
    # )

    hep.cms.label(
        data="True", label="Test", year="2022", com="13,6", lumi="17.4", ax=axs[0]
    )

    axs[0].set_ylabel(y_labels[variable])
    axs[0].set_ylim(0.1, y_axis_max_range[variable])
    axs[0].set_xlim(data_bins[0], data_bins[-1])
    axs[0].set_yscale("log")
    axs[0].legend(frameon=False, loc="upper right")
    axs[0].tick_params(axis="x", which="both", bottom=True, top=True, labelbottom=False)

    plt.axhline(y=1, color="grey", linestyle="--", alpha=0.5)

    ratio_hist, ratio_error = get_hitograms_ratio(
        data_numpy_histogram, background_histograms
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
    save_figure(fig, "../plots/ratio/", variable + "_" + era + "_MCData_ratio")


def get_hitograms_ratio(data_numpy_hist, background_histograms):
    bg_numpy_hist = []
    for bg_hist in background_histograms:
        bg_numpy_hist.append(bg_hist.to_numpy()[0])

    ratio = np.divide(data_numpy_hist, bg_numpy_hist, where=(bg_numpy_hist != 0))
    error = np.divide(
        data_numpy_hist * np.sqrt(bg_numpy_hist)
        + bg_numpy_hist * np.sqrt(data_numpy_hist),
        np.power(bg_numpy_hist, 2),
        where=(bg_numpy_hist != 0),
    )

    return ratio, error


# draw_data_and_simul("pt", "2022EE")
# draw_data_and_simul("mass", "2022EE")
# draw_data_and_simul("phi", "2022EE")
# draw_data_and_simul("eta", "2022EE")
draw_data_and_simul_and_ratio("pt", "2022EE")
draw_data_and_simul_and_ratio("mass", "2022EE")
draw_data_and_simul_and_ratio("phi", "2022EE")
draw_data_and_simul_and_ratio("eta", "2022EE")
