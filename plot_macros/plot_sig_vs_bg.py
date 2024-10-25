# from utils.sig_vs_bg import draw_sig_and_bg
from utils.sig_vs_bg import draw_sig_and_bg_from_tuple

background_sources = [
    "TT",
    "DiBoson",
    "DY",
]
signal_sources = ["ggH", "VBF", "ttH"]
variables = [
    ## DiMuon variables
    "diMuon_rapidity",
    "diMuon_pt",
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
    "leading_jet_eta",
    "delta_eta_dimuon_jet",
    "min_delta_eta_dimuon_jet",
    "min_delta_phi_dimuon_jet",
    # diJet variables
    "diJet_mass",
    "delta_eta_diJet",
    "delta_phi_diJet",
    "z_zeppenfeld",
    "min_delta_eta_dimuon_jet",
    "min_delta_phi_dimuon_jet",
]
era = "2022EE"

for variable in variables:
    # draw_sig_and_bg(variable, era, background_sources, signal_sources)
    draw_sig_and_bg_from_tuple(variable, era)
