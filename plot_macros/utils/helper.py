import matplotlib.pyplot as plt
import numpy as np
import uproot as ur
import os


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


def get_histograms(variable, sources, era):
    histograms = []
    for source in sources:
        with ur.open("../root_io/" + source + "_" + era + "_histograms.root") as file:
            # with ur.open(
            # "../root_io/no_dimuon_mass_cut/" + source + "_" + era + "_histograms.root"
            # ) as file:
            histograms.append(file[variable])

    return histograms


def get_histograms_ratio(numerator_histogram, denominator_histogram):

    ratio = np.divide(
        numerator_histogram, denominator_histogram, where=(denominator_histogram != 0)
    )
    error = np.divide(
        numerator_histogram * np.sqrt(denominator_histogram)
        + denominator_histogram * np.sqrt(numerator_histogram),
        np.power(denominator_histogram, 2),
        where=(denominator_histogram != 0),
    )
    if (len(error[error < 0.0])):
        msg = "Unexpected negative ratio-error values found."\
            "Setting them to zero.\n > Re-run. If the value changes, "\
            "it might have to do with the minimum subnormal number bug!"
        print(msg)
        print("Error; length")
        print(error[error < 0.0], len(error[error < 0.0]))
        print("Ratio values")
        print(ratio[np.where(error < 0.0)])
        error[error < 0.0] = 0.0
   
    return ratio, error
