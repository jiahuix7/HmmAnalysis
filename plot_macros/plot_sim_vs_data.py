from utils.sim_vs_data import draw_data_and_simul_and_ratio


# ordered from bottom to top in the plot, so order it from lower to bigger cross section
# background_sources = ["TT", "DY120-200", "DY50-120"]
background_sources = [
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
    "diMuon_mass",
    "diMuon_mass_full_range",
    "diMuon_rapidity",
    "diMuon_eta",
    "diMuon_pt",
    "diMuon_phi",
    # "n_jet",
    # "jet_pt",
    # "jet_eta",
    # "jet_phi",
    # "jet_mass",
    # "diJet_pt",
    # "diJet_eta",
    # "diJet_phi",
    # "diJet_mass",
    # "diJet_mass_mo",
    # "diJet_DeltaEta",
    "mu1_pt_mass_ratio",
    "mu2_pt_mass_ratio",
    "mu1_eta",
    "mu2_eta",
    "phi_CS",
    "cos_theta_CS",
]
eras = ["2022", "2022EE"]

for era in eras:
    for variable in variables:
        draw_data_and_simul_and_ratio(variable, era, background_sources, signal_sources)
