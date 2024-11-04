from utils.sig_vs_bg import draw_sig_and_bg_from_tuple

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
# era = "2022EE"
# eras = ["2022", "2022EE"]
eras = ["2023", "2023BPix"]

for variable in variables:
    for era in eras:
        draw_sig_and_bg_from_tuple(variable, era)
