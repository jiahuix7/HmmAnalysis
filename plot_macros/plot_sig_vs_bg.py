from utils.sig_vs_bg import draw_sig_and_bg

background_sources = [
    "TT",
    "DiBoson",
    "DY",
]
signal_sources = ["ggH", "VBF", "ttH"]
variables = [
    "mu1_pt_mass_ratio",
    "mu2_pt_mass_ratio",
    "mu1_eta",
    "mu2_eta",
    "diMuon_rapidity",
    "diMuon_pt",
    "phi_CS",
    "cos_theta_CS",
    "n_jet",
    "jet_pt",
    "jet_mass",
    "jet_eta",
    "diJet_eta",
    "diJet_phi",
    "diJet_mass",
    "diJet_mass_mo",
    "diJet_DeltaEta",
]
era = "2022EE"

for variable in variables:
    draw_sig_and_bg(variable, era, background_sources, signal_sources)
