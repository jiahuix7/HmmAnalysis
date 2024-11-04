from utils.sim_vs_data import draw_data_and_simul_and_ratio


# ordered from bottom to top in the plot, so order it from lower to bigger cross section
background_sources = [
    "EWK",
    "DiBoson",
    "TT",
    "DY",
]
# "ZZto2L2QNu",
# "WZto2L2QNu",
# "ZZto2L2Nu",
# "ZZto4L",
# "WWto2L2Nu",
# ]
signal_sources = [
    "ggH",
    "VBF",
    "ttH",
]
variables = [
    ## DiMuon variables
    "diMuon_mass",
    # "diMuon_mass_full_range",
    "diMuon_rapidity",
    "diMuon_eta",
    "diMuon_pt",
    "diMuon_phi",
    ## Muon variables
    "mu1_pt_mass_ratio",
    "mu2_pt_mass_ratio",
    "mu1_eta",
    "mu2_eta",
    "phi_CS",
    "cos_theta_CS",
    ## Jet variables
    "n_jet",
    "leading_jet_pt",
    "subleading_jet_pt",
    "leading_jet_eta",
    # diJet variables
    "diJet_mass",
    "delta_eta_diJet",
    "delta_phi_diJet",
    "z_zeppenfeld",
    "min_delta_eta_diMuon_jet",
    "min_delta_phi_diMuon_jet",
]
# eras = ["2022", "2022EE", "2023", "2023BPix"]
# eras = ["2022", "2022EE"]
# eras = ["2023", "2023BPix"]
eras = ["2023BPix"]
# eras = ["2022"]

for era in eras:
    for variable in variables:
        draw_data_and_simul_and_ratio(variable, era, background_sources, signal_sources)
    for variable in variables:
        draw_data_and_simul_and_ratio(
            variable, era, background_sources, signal_sources, use_ggH_category=True
        )

    draw_data_and_simul_and_ratio("PV", era, background_sources, signal_sources)
    draw_data_and_simul_and_ratio("rho", era, background_sources, signal_sources)
    draw_data_and_simul_and_ratio(
        "PV", era, background_sources, signal_sources, use_puweight=False
    )
    draw_data_and_simul_and_ratio(
        "rho", era, background_sources, signal_sources, use_puweight=False
    )
