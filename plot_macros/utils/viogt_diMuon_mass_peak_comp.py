import uproot as ur
import mplhep as hep
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.special import wofz


from .labels import (
    x_labels,
    background_labels,
    luminosity,
    x_range,
    n_bins,
    variables_type,
)  # , y_labels
from .helper import (
    get_canvas,
    save_figure,
    get_histograms_ratio,
    get_output_directory,
    clean_null_values,
)

y_axis_max_range = {
    "diMuon_mass_full_range": 10e8,
}

signal_sources = [
    "ggH",
    "VBF",
    "ttH",
]

signal_colors = {"ggH": "red", "VBF": "blue", "ttH": "lime"}

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

variables = ["diMuon_mass", "diMuon_bsConstrainedMass"]
Z_range = [80,100]
H_range = [115,135]
Z_fit_range = [89,93]
H_fit_range = [122.5,127.5]
Z_mass = 91
H_mass = 125
masses = {
    "Z":91,
    "H":125
}
natural_width={
    "Z":2.4952e-3, # in GeV
    "H":4.07e-3 # in GeV
}

def voigt(x, A, center, sigma, gamma):
    """
    Voigt function is a convolution of Gaussian and Lorentzian.
    In scipy, the viogt function can be computed using the real part of the Faddeeva function wofz.
    
    Parameters:
    - A: amplitude
    - center: peak center
    - sigma: Gaussian width parameter (detector resolution)
    - gamma: Lorentzian width parameter (natural width of the particle)
    """
    z = ((x - center) + 1j * gamma) / (sigma * np.sqrt(2))
    return A * np.real(wofz(z)) / (sigma * np.sqrt(2 * np.pi))

def gaussian(x, A, center, sigma):
    return A * np.exp(-0.5 * ((x - center) / sigma) ** 2)

def plot_diMuon_comp_and_fit(fit_range, mass_range, noBSC_hist, BSC_hist, particle, era, signal=None):
    if (particle == "H" and signal==None):
        print("Must provide a signal to plot")

    bin_centers = (noBSC_hist[1][:-1] + noBSC_hist[1][1:]) / 2
    minBin = np.where(noBSC_hist[1] >= fit_range[0])[0][0]
    maxBin = np.where(noBSC_hist[1] <= fit_range[1])[0][-1] + 1
    
    p0_noBSC = [np.max(noBSC_hist[0][minBin:maxBin]), masses[particle], 1, natural_width[particle]]
    p0_BSC =[np.max(BSC_hist[0][minBin:maxBin]), masses[particle], 1, natural_width[particle]]
    
    popt, pcov = curve_fit(
        voigt, 
        bin_centers[minBin:maxBin], 
        noBSC_hist[0][minBin:maxBin], 
        p0=p0_noBSC,
        maxfev=5000
    )
    
    poptBSC, pcovBSC = curve_fit(
        voigt, 
        bin_centers[minBin:maxBin],
        BSC_hist[0][minBin:maxBin], 
        p0=p0_BSC,
        maxfev=5000
    )

    perr = np.sqrt(np.diag(pcov))
    perrBSC = np.sqrt(np.diag(pcovBSC))
    
    amp, center, sigma, gamma = popt
    amp_err, center_err, sigma_err, gamma_err = perr
    
    BSC_amp, BSC_center, BSC_sigma, BSC_gamma = poptBSC
    BSC_amp_err, BSC_center_err, BSC_sigma_err, BSC_gamma_err = perrBSC
    
    effective_width = np.sqrt(sigma**2 + gamma**2)
    BSC_effective_width = np.sqrt(BSC_sigma**2 + BSC_gamma**2)
    
    effective_width_err = np.sqrt((sigma*sigma_err)**2 + (gamma*gamma_err)**2) / effective_width
    BSC_effective_width_err = np.sqrt((BSC_sigma*BSC_sigma_err)**2 + (BSC_gamma*BSC_gamma_err)**2) / BSC_effective_width
    
    noBSC_res = effective_width / center
    noBSC_res_err = noBSC_res * np.sqrt((center_err/center)**2 + (effective_width_err/effective_width)**2)
    
    BSC_res = BSC_effective_width / BSC_center
    BSC_res_err = BSC_res * np.sqrt((BSC_center_err/BSC_center)**2 + (BSC_effective_width_err/BSC_effective_width)**2)

    fig, axs = get_canvas(True)
    if (particle=="Z"): ifMCorData = "Data"
    else: ifMCorData = signal + " MC"

    hep.histplot(noBSC_hist[0], noBSC_hist[1], label = ifMCorData + " no BSC", ax=axs[0])
    hep.histplot(BSC_hist[0], BSC_hist[1], label = ifMCorData + " BSC", ax=axs[0])

    hep.cms.label(
    data="True",
    label="",
    year=era,
    com="13.6",
    lumi=luminosity[era],
    ax=axs[0],
    )

    axs[0].plot(bin_centers[minBin:maxBin], voigt(bin_centers[minBin:maxBin], *popt),
        label=
                r"$\mu={:.5f} \pm {:.3f}$".format(center, center_err)
                + "\n"
                + r"$\sigma={:.5f} \pm {:.3f}$".format(sigma, sigma_err)
                + "\n"
                + r"$\gamma={:.5f} \pm {:.3f}$".format(gamma, gamma_err)
                +"\n"
                + r"noBSC $\sigma_{{eff}} / \mu $: {:.6f} $\pm$ {:.6f}".format(noBSC_res, noBSC_res_err)
               )
    
    axs[0].plot(bin_centers[minBin:maxBin], voigt(bin_centers[minBin:maxBin], *poptBSC), 
        label=
                r"$\mu={:.5f} \pm {:.3f}$".format(BSC_center, BSC_center_err)
                + "\n"
                + r"$\sigma={:.5f} \pm {:.3f}$".format(BSC_sigma, BSC_sigma_err)
                + "\n"
                + r"$\gamma={:.5f} \pm {:.3f}$".format(BSC_gamma, BSC_gamma_err)
                +"\n"
                + r"BSC $\sigma_{{eff}} / \mu $: {:.6f} $\pm$ {:.6f}".format(BSC_res, BSC_res_err)
               )
    
    axs[0].set_ylabel("Events")
    axs[0].set_ylim(0, 1.6 * np.max(noBSC_hist[0]))
    axs[0].set_xlim(mass_range[0], mass_range[1])
    axs[0].legend(frameon=False, loc="upper right", ncols=2,fontsize=17)
    axs[0].tick_params(axis="x", which="both", bottom=True, top=True, labelbottom=False)

    axs[1].set_ylabel("BSC/noBSC", loc="center")
    axs[1].set_ylim(0.5, 1.5)
    axs[1].set_xlim(mass_range[0], mass_range[1])
    axs[1].set_xlabel("m$_{\mu\mu}$ [GeV]")

    ratio_hist, ratio_error = get_histograms_ratio(BSC_hist[0], noBSC_hist[0])
    hep.histplot(
        ratio_hist,
        noBSC_hist[1],
        yerr=ratio_error,
        histtype="errorbar",
        #label="data",
        color="black",
        ax=axs[1],
    )

    output_directory = f"../plots/viogt/resolution/{era}/"

    if particle == "H":
        save_figure(fig, output_directory, f"{particle}_{signal}_{era}_reso")
    else:
        save_figure(fig, output_directory, f"{particle}_{era}_reso")
    plt.close()

def plot_diMuon_comp_and_fit_gaussian_initial(fit_range, mass_range, noBSC_hist, BSC_hist, particle, era, signal=None):
    if (particle == "H" and signal==None):
        print("Must provide a signal to plot")

    bin_centers = (noBSC_hist[1][:-1] + noBSC_hist[1][1:]) / 2
    minBin = np.where(noBSC_hist[1] >= fit_range[0])[0][0]
    maxBin = np.where(noBSC_hist[1] <= fit_range[1])[0][-1] + 1
    
    gaussian_p0_noBSC = [np.max(noBSC_hist[0][minBin:maxBin]), masses[particle], 1]
    gaussian_p0_BSC = [np.max(BSC_hist[0][minBin:maxBin]), masses[particle], 1]
    
    gaussian_popt_noBSC, _ = curve_fit(
        gaussian, 
        bin_centers[minBin:maxBin], 
        noBSC_hist[0][minBin:maxBin], 
        p0=gaussian_p0_noBSC,
        maxfev=5000
    )
    
    gaussian_popt_BSC, _ = curve_fit(
        gaussian, 
        bin_centers[minBin:maxBin],
        BSC_hist[0][minBin:maxBin], 
        p0=gaussian_p0_BSC,
        maxfev=5000
    )
    
    p0_noBSC = [gaussian_popt_noBSC[0], gaussian_popt_noBSC[1], gaussian_popt_noBSC[2], natural_width[particle]]
    p0_BSC = [gaussian_popt_BSC[0], gaussian_popt_BSC[1], gaussian_popt_BSC[2], natural_width[particle]]
    
    popt, pcov = curve_fit(
        voigt, 
        bin_centers[minBin:maxBin], 
        noBSC_hist[0][minBin:maxBin], 
        p0=p0_noBSC,
        maxfev=5000
    )
    
    poptBSC, pcovBSC = curve_fit(
        voigt, 
        bin_centers[minBin:maxBin],
        BSC_hist[0][minBin:maxBin], 
        p0=p0_BSC,
        maxfev=5000
    )

    perr = np.sqrt(np.diag(pcov))
    perrBSC = np.sqrt(np.diag(pcovBSC))
    
    amp, center, sigma, gamma = popt
    amp_err, center_err, sigma_err, gamma_err = perr
    
    BSC_amp, BSC_center, BSC_sigma, BSC_gamma = poptBSC
    BSC_amp_err, BSC_center_err, BSC_sigma_err, BSC_gamma_err = perrBSC
    
    effective_width = np.sqrt(sigma**2 + gamma**2)
    BSC_effective_width = np.sqrt(BSC_sigma**2 + BSC_gamma**2)
    
    effective_width_err = np.sqrt((sigma*sigma_err)**2 + (gamma*gamma_err)**2) / effective_width
    BSC_effective_width_err = np.sqrt((BSC_sigma*BSC_sigma_err)**2 + (BSC_gamma*BSC_gamma_err)**2) / BSC_effective_width
    
    noBSC_res = effective_width / center
    noBSC_res_err = noBSC_res * np.sqrt((center_err/center)**2 + (effective_width_err/effective_width)**2)
    
    BSC_res = BSC_effective_width / BSC_center
    BSC_res_err = BSC_res * np.sqrt((BSC_center_err/BSC_center)**2 + (BSC_effective_width_err/BSC_effective_width)**2)

    fig, axs = get_canvas(True)
    if (particle=="Z"): ifMCorData = "Data"
    else: ifMCorData = signal + " MC"

    hep.histplot(noBSC_hist[0], noBSC_hist[1], label = ifMCorData + " no BSC", ax=axs[0])
    hep.histplot(BSC_hist[0], BSC_hist[1], label = ifMCorData + " BSC", ax=axs[0])

    hep.cms.label(
    data="True",
    label="", 
    year=era,
    com="13.6",
    lumi=luminosity[era],
    ax=axs[0],
    )

    axs[0].plot(bin_centers[minBin:maxBin], voigt(bin_centers[minBin:maxBin], *popt),
        label=
                r"$\mu={:.5f} \pm {:.3f}$".format(center, center_err)
                + "\n"
                + r"$\sigma={:.5f} \pm {:.3f}$".format(sigma, sigma_err)
                + "\n"
                + r"$\gamma={:.5f} \pm {:.3f}$".format(gamma, gamma_err)
                +"\n"
                + r"noBSC $\sigma_{{eff}} / \mu $: {:.6f} $\pm$ {:.6f}".format(noBSC_res, noBSC_res_err)
               )
    
    axs[0].plot(bin_centers[minBin:maxBin], voigt(bin_centers[minBin:maxBin], *poptBSC), 
        label=
                r"$\mu={:.5f} \pm {:.3f}$".format(BSC_center, BSC_center_err)
                + "\n"
                + r"$\sigma={:.5f} \pm {:.3f}$".format(BSC_sigma, BSC_sigma_err)
                + "\n"
                + r"$\gamma={:.5f} \pm {:.3f}$".format(BSC_gamma, BSC_gamma_err)
                +"\n"
                + r"BSC $\sigma_{{eff}} / \mu $: {:.6f} $\pm$ {:.6f}".format(BSC_res, BSC_res_err)
               )
    
    axs[0].set_ylabel("Events")
    axs[0].set_ylim(0, 1.6 * np.max(noBSC_hist[0]))
    axs[0].set_xlim(mass_range[0], mass_range[1])
    axs[0].legend(frameon=False, loc="upper right", ncols=2,fontsize=17)
    axs[0].tick_params(axis="x", which="both", bottom=True, top=True, labelbottom=False)

    axs[1].set_ylabel("BSC/noBSC", loc="center")
    axs[1].set_ylim(0.5, 1.5)
    axs[1].set_xlim(mass_range[0], mass_range[1])
    axs[1].set_xlabel("m$_{\mu\mu}$ [GeV]")

    ratio_hist, ratio_error = get_histograms_ratio(BSC_hist[0], noBSC_hist[0])
    hep.histplot(
        ratio_hist,
        noBSC_hist[1],
        yerr=ratio_error,
        histtype="errorbar",
        #label="data",
        color="black",
        ax=axs[1],
    )

    output_directory = f"../plots/viogt/gaussian_initial_guess/resolution/{era}/"

    if particle == "H":
        save_figure(fig, output_directory, f"{particle}_{signal}_{era}_reso")
    else:
        save_figure(fig, output_directory, f"{particle}_{era}_reso")
    plt.close()


def draw_diMuon_mass_peak_comp(particle, era, use_puweight=True):
    plt.style.use(hep.style.CMS)

    print("*" * len("****** PLOTTING " + particle + " peak for " + era + " *****"))
    print("****** PLOTTING " + particle + " peak for " + era + " *****")
    print("*" * len("****** PLOTTING " + particle + " peak for " + era + " *****"))

    era_reweight = 1
    if era == "2024":
        era_reweight = 106.45/9.45

    if particle == "Z":
        mass_range = Z_range
        fit_range = Z_fit_range
        histograms_list = []
        
        with ur.open("../root_io/tuples/Data_" + era + "_tuples.root:tree_output") as data_file:
            branches = data_file.arrays(variables, library="np")
            
        for var in variables:
            histogram, bins = np.histogram(
                branches[var],
                bins=160,
                range=Z_range,
            )
            histograms_list.append([histogram, bins])
        
        plot_diMuon_comp_and_fit_gaussian_initial(fit_range, mass_range, histograms_list[0], histograms_list[1], particle, era)

    if particle == "H":
        if era == "2024":
            print("There are no signal MC for 2024 yet")
            return
        mass_range = H_range
        fit_range = H_fit_range
        for signal in signal_sources:
            histograms_list = []
            
            with ur.open("../root_io/tuples/" + signal + "_" + era + "_tuples.root:tree_output") as data_file:
                branches = data_file.arrays(variables, library="np")
                
            for var in variables:
                histogram, bins = np.histogram(
                    branches[var],
                    bins=160,
                    range=H_range,
                )
                histograms_list.append([histogram, bins])
           
            plot_diMuon_comp_and_fit_gaussian_initial(fit_range, mass_range, histograms_list[0], histograms_list[1], particle, era, signal=signal)
