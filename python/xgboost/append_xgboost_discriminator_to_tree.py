#!/usr/bin/env python

import sys
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd

# import math
import pickle as pickle
import ROOT as root
import uproot as uproot


# USAGE
# python append_xgboost_discriminator_to_tree.py <folder_name> <input_file_name> <year> <bdt_type>

root.gROOT.Reset()

if len(sys.argv) != 3:
    print("Please use two arguments. channel era")
    exit()
channel = sys.argv[1]
era = sys.argv[2]

signals = "signals"

FileName = "../../root_io/skim/" + channel + "_" + era + "_skim_" + signals + ".root"

File = root.TFile(FileName, "update")
Tree = File.Get("tree_output")


test_name = "ReadingXgBoostModel"

_model_name = "./models/" + signals + "/model_mumu_vs_bkg_" + era + ".pkl"

variables = [
    ["diMuon_rapidity", "diMuon_rapidity", r"$y_{\mu\mu}$ (GeV)", 50, -2.5, 2.5],
    ["diMuon_pt", "diMuon_pt", r"$M_{\mu\mu}$ (GeV)", 100, 0, 250],
    [
        "mu1_pt_mass_ratio",
        "mu1_pt_mass_ratio",
        r"$p_T^{\mu 1}/m_{/mu/mu}$",
        50,
        0,
        1.4,
    ],
    [
        "mu2_pt_mass_ratio",
        "mu2_pt_mass_ratio",
        r"$p_T^{\mu 2}/m_{/mu/mu}$",
        50,
        0,
        1.4,
    ],
    ["mu1_eta", "mu1_eta", r"$\eta_\mu 1$", 50, -2.4, 2.4],
    ["mu2_eta", "mu2_eta", r"$\eta_\mu 2$", 50, -2.4, 2.4],
    ["phi_CS", "phi_CS", r"$\phi_{CS}$", 50, -3.14, 3.14],
    ["cos_theta_CS", "cos_theta_CS", r"$cos(\theta_CS)$", 50, -1, 1],
    #   Jet variables
    ["n_jet", "n_jet", r"n jets", 8, 0, 8],
    ["leading_jet_pt", "leading_jet_pt", r"$Pt_{j1}$ GeV", 50, 0, 400],
    ["leading_jet_eta", "leading_jet_eta", r"$\eta_{jet}$", 50, -5, 5],
    ["subleading_jet_pt", "subleading_jet_pt", r"$Pt_{j2}$", 50, 0, 400],
    ["diJet_mass", "diJet_mass", r"$m_{jj}$ GeV", 50, 0, 400],
    ["delta_eta_diJet", "delta_eta_diJet", r"$\Delta\eta_{jj}$", 50, -8, 8],
    ["delta_phi_diJet", "delta_phi_diJet", r"$\Delta\phi_{jj}$", 50, -3.14, 3.14],
    ["z_zeppenfeld", "z_zeppenfeld", r"Z Zeppendfeld", 50, -8, 8],
    [
        "min_delta_eta_diMuon_jet",
        "min_delta_eta_diMuon_jet",
        r"min$\Delta\eta_{\mu\mu,j}",
        50,
        -8,
        8,
    ],
    [
        "min_delta_phi_diMuon_jet",
        "min_delta_phi_diMuon_jet",
        r"min$\Delta\phi_{\mu\mu,j}",
        50,
        -3.14,
        3.14,
    ],
    # ["weight", "weight", "weight", 100, -1.0, 1.0],
]


print(len(variables))
my_variables = []
for var in variables:
    print(var[0])
    my_variables.append(var[0])

with uproot.open(FileName) as file:
    df = pd.DataFrame(
        file["tree_output"].arrays([row[0] for row in variables], library="np"),
        # flatten=False,
    )

# getting a numpy array from two pandas data frames
x_test = df.values
# creating numpy array for target variables
y_test = np.zeros(len(df))


############################
# get model from file
############################
with open(_model_name, "rb") as pkl_file:
    model = pickle.load(pkl_file)


# make predictions for test data
y_pred = model.predict_proba(x_test)[:, 1]
print("y_pred", y_pred)
predictions = [round(value) for value in y_pred]

# print y_pred
##########################################################
# make histogram of discriminator value for signal and bkg
##########################################################
y_frame = pd.DataFrame({"truth": y_test, "disc": y_pred})
print("y_frame", y_frame)
disc = y_frame[y_frame["truth"] == 0]["disc"].values
# disc    = y_frame[y_frame['truth'] == 1]['disc'].values
plt.figure()
plt.hist(disc, bins=50, alpha=0.3)
plt.savefig("mydiscriminator_" + era + ".png")
print("disc_bkg: ", disc)
# print y_pred

#############################################
##Creating a new TTree with the discriminator
#############################################

nEntries = Tree.GetEntries()
print("nEntries = ", nEntries)
_disc_var_name = "BDT_ggH"

root.gROOT.ProcessLine("struct MyStruct{float disc;};")

from ROOT import MyStruct

# Create branches in the tree
my_s = MyStruct()
print(my_s)
print(root.addressof(my_s))
print(root.addressof(my_s, "disc"))
root.addressof(my_s, "disc")
bpt = Tree.Branch(_disc_var_name, root.addressof(my_s, "disc"), _disc_var_name + "/F")

for i in range(nEntries):
    Tree.GetEntry(i)
    if i % 10000 == 0:
        print("Processing event nr. %i of %i" % (i, nEntries))
    my_s.disc = disc[i]
    bpt.Fill()

Tree.Print()
Tree.GetCurrentFile().Write()
Tree.GetCurrentFile().Close()
