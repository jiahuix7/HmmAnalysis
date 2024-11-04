#!/usr/bin/env python
# coding: utf-8
import matplotlib.pyplot as plt
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_curve, roc_auc_score
import numpy as np
import pandas as pd
import math
import pickle as pickle
import ROOT as root
import os
import shlex
import uproot
import sys

if len(sys.argv) > 1:
    era = sys.argv[1]
    print("Era :", era)
else:
    print("Provided era as input.")
    exit()

root.gROOT.SetBatch(True)
root.gStyle.SetOptStat(0)
root.gStyle.SetOptFit(111)
root.gStyle.SetPaintTextFormat("2.1f")

# plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["text.usetex"] = False
plt.rcParams["mathtext.fontset"] = "cm"

# era = "2022EE"
luminosity = {
    "2022": 7.9804,
    "2022EE": 26.6717,
    "2022Combined": 34.6521,
}

test_name = "mumu_vs_bkg_" + era
plotDir = "../../plots/xgboost/"
pwd = os.getcwd()
data_directory = "../../root_io/skim/"

os.system("mkdir -p " + plotDir)
os.system("mkdir -p " + plotDir + "training")
os.system("mkdir -p " + plotDir + "results")
os.system("mkdir -p " + plotDir + "scores")
os.system("mkdir -p " + plotDir + "variables")
os.system("mkdir -p models")
os.system("cp ../index.php " + plotDir)
os.system("cp ../index.php " + plotDir + "training/")
os.system("cp ../index.php " + plotDir + "results/")
os.system("cp ../index.php " + plotDir + "scores/")
os.system("cp ../index.php " + plotDir + "variables/")


# signal
signal_file_name = data_directory + "signal_" + era + "_skim.root"
signal_file = root.TFile(signal_file_name)
signal_tree = signal_file.Get("tree_output")
signal_tree.Draw("diMuon_pt>>tmp1", "weight_no_lumi")
signal_histogram = root.gDirectory.Get("tmp1")
signal_events = luminosity[era] * signal_histogram.Integral()

# bkg
bkg_file_name = data_directory + "background_" + era + "_skim.root"
bkg_file = root.TFile(bkg_file_name)
bkg_tree = bkg_file.Get("tree_output")
bkg_tree.Draw("diMuon_pt>>tmp2", "weight_no_lumi")
bkg_histogram = root.gDirectory.Get("tmp2")
bkg_events = luminosity[era] * bkg_histogram.Integral()

print(
    "[INFO]: S = "
    + str(signal_events)
    + "; B = "
    + str(bkg_events)
    + "; S/sqrt(B) = "
    + str(signal_events / math.sqrt(bkg_events))
)

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
    ["n_jet", "n_jet", r"n jet", 8, 0, 8],
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
    ["weight_no_lumi", "weight_no_lumi", "weight_no_lumi", 100, -1.0, 1.0],
]

print("number of variables", len(variables))

##Getting ROOT files into pandas

with uproot.open(signal_file_name) as file:
    df_signal = pd.DataFrame(
        file["tree_output"].arrays([row[0] for row in variables], library="np"),
        # flatten=False,
    )

print("Signal data frame created")
with uproot.open(bkg_file_name) as file:
    df_bkg = pd.DataFrame(
        file["tree_output"].arrays([row[0] for row in variables], library="np"),
        # flatten=False,
    )

print("Background data frame created")
##Getting a numpy array out of two pandas data frame

# getting a numpy array from two pandas data frames
x = np.concatenate([df_bkg.values, df_signal.values])
# creating numpy array for target variables
y = np.concatenate([np.zeros(len(df_bkg)), np.ones(len(df_signal))])

print("signal sample size: " + str(len(df_signal.values)))
print("bkg sample size: " + str(len(df_bkg.values)))

###plot correlation
file_sig = root.TFile(signal_file_name)
tree_sig = file_sig.Get("tree_output")
file_bkg = root.TFile(bkg_file_name)
tree_bkg = file_sig.Get("tree_output")
h2_corr_sig = root.TH2F(
    "h2_corr_sig",
    "h2_corr_sig",
    len(variables) - 1,
    0,
    len(variables) - 1,
    len(variables) - 1,
    0,
    len(variables) - 1,
)
h2_corr_bkg = root.TH2F(
    "h2_corr_bkg",
    "h2_corr_bkg",
    len(variables) - 1,
    0,
    len(variables) - 1,
    len(variables) - 1,
    0,
    len(variables) - 1,
)

for idx1 in range(len(variables) - 1):
    for idx2 in range(len(variables) - 1):
        tree_sig.Draw(variables[idx1][0] + ":" + variables[idx2][0] + ">>temp_sig")
        tree_bkg.Draw(variables[idx1][0] + ":" + variables[idx2][0] + ">>temp_bkg")
        sig_hist = root.gDirectory.Get("temp_sig")
        h2_corr_sig.SetBinContent(idx1 + 1, idx2 + 1, sig_hist.GetCorrelationFactor())
        bkg_hist = root.gDirectory.Get("temp_bkg")
        h2_corr_bkg.SetBinContent(idx1 + 1, idx2 + 1, bkg_hist.GetCorrelationFactor())
        root.gDirectory.Delete("temp_sig")
        root.gDirectory.Delete("temp_bkg")
h2_corr_sig.GetZaxis().SetRangeUser(-1.0, 1.0)
h2_corr_bkg.GetZaxis().SetRangeUser(-1.0, 1.0)
for idx in range(len(variables) - 1):
    h2_corr_sig.GetXaxis().SetBinLabel(idx + 1, variables[idx][1])
    h2_corr_sig.GetYaxis().SetBinLabel(idx + 1, variables[idx][1])
    h2_corr_bkg.GetXaxis().SetBinLabel(idx + 1, variables[idx][1])
    h2_corr_bkg.GetYaxis().SetBinLabel(idx + 1, variables[idx][1])

h2_corr_sig.LabelsOption("v", "X")
h2_corr_bkg.LabelsOption("v", "X")
my_canvas = root.TCanvas("my_canvas", "my_canvas", 200, 10, 900, 800)
my_canvas.SetHighLightColor(2)
my_canvas.SetFillColor(0)
my_canvas.SetBorderMode(0)
my_canvas.SetBorderSize(2)
my_canvas.SetLeftMargin(0.12)
my_canvas.SetRightMargin(0.12)
my_canvas.SetBottomMargin(0.12)
my_canvas.SetTopMargin(0.12)
my_canvas.SetFrameBorderMode(0)
my_canvas.SetFrameBorderMode(0)

stops = np.array([0.00, 0.34, 0.61, 0.84, 1.00])
red = np.array([0.50, 0.50, 1.00, 1.00, 1.00])
green = np.array([0.50, 1.00, 1.00, 0.60, 0.50])
blue = np.array([1.00, 1.00, 0.50, 0.40, 0.50])
root.TColor.CreateGradientColorTable(len(stops), stops, red, green, blue, 255)
root.gStyle.SetNumberContours(255)

h2_corr_sig.Draw("COLZTEXT")
h2_corr_sig.SetTitle("")
my_canvas.SaveAs(plotDir + "variables/" + test_name + "_correlation_matrix_sig.pdf")
my_canvas.SaveAs(plotDir + "variables/" + test_name + "_correlation_matrix_sig.png")
my_canvas.SaveAs(plotDir + "variables/" + test_name + "_correlation_matrix_sig.C")
h2_corr_bkg.Draw("COLZTEXT")
h2_corr_bkg.SetTitle("")
my_canvas.SaveAs(plotDir + "variables/" + test_name + "_correlation_matrix_bkg.pdf")
my_canvas.SaveAs(plotDir + "variables/" + test_name + "_correlation_matrix_bkg.png")
my_canvas.SaveAs(plotDir + "variables/" + test_name + "_correlation_matrix_bkg.C")


# split data into train and test sets
seed = 7
test_size = 0.4
sample_size = 1.0
x_train_p, x_test_p, y_train, y_test = train_test_split(
    x,
    y,
    train_size=sample_size * (1 - test_size),
    test_size=sample_size * test_size,
    random_state=seed,
)

x_train = x_train_p[:, :-1]
x_test = x_test_p[:, :-1]
sample_weights_train = x_train_p[:, -1]
sample_weights_test = x_test_p[:, -1]


for idx in range(len(sample_weights_train)):
    sample_weights_train[idx] = luminosity[era] * sample_weights_train[idx]
for idx in range(len(sample_weights_test)):
    sample_weights_test[idx] = luminosity[era] * sample_weights_test[idx]

# fit model no training data
model = xgb.XGBClassifier(
    max_depth=3,
    learning_rate=0.1,
    n_estimators=400,
    verbosity=2,
    n_jobs=4,
    reg_lambda=1.0,
)
model.fit(x_train, y_train)  # , sample_weights_train)

# print( dir(model) )
# print(model)
# make predictions for test data
y_pred = model.predict_proba(x_test)[:, 1]
y_pred_train = model.predict_proba(x_train)[:, 1]
predictions = [round(value) for value in y_pred]
# evaluate predictions
accuracy = accuracy_score(y_test, predictions)
print("Accuracy: %.2f%%" % (accuracy * 100.0))

AUC = roc_auc_score(y_test, y_pred)
print("AUC: " + str(AUC))
# get roc curve
# roc = roc_curve(y_test, y_pred)
fpr, tpr, thr = roc_curve(y_test, y_pred, sample_weight=sample_weights_test)


significance = []
effSignal = []
effBkg = []
thresholds = []

ctr = 0
f_roc = open(test_name + "_roc.txt", "w")

for i in range(len(fpr)):
    if fpr[i] > 1e-5 and tpr[i] > 1e-5:
        print(
            "thr = " + str(thr[i]) + ", fpr = " + str(fpr[i]) + ", tpr = " + str(tpr[i])
        )
        f_roc.write(
            "thr = "
            + str(thr[i])
            + ", fpr = "
            + str(fpr[i])
            + ", tpr = "
            + str(tpr[i])
            + " \n"
        )
        # print fpr[i], tpr[i]
        # significance.append(math.sqrt(luminosity[era])*4.8742592356*0.006431528796*tpr[i]/math.sqrt(fpr[i]*0.9935684712))
        significance.append(signal_events * tpr[i] / math.sqrt(fpr[i] * bkg_events))
        effSignal.append(tpr[i])
        effBkg.append(fpr[i])
        thresholds.append(thr[i])
        # print significance[ctr], ' ' , fpr[ctr], ' ', tpr[ctr]
        ctr = ctr + 1
f_roc.close()

max_significance = max(significance)
idx_max_significance = np.argmax(np.array(significance))
best_threshold = thresholds[idx_max_significance]
best_effSignal = effSignal[idx_max_significance]
best_effBkg = effBkg[idx_max_significance]

print("max_significance: " + str(max_significance))
print("best_threshold: " + str(best_threshold))
print("best_effSignal: " + str(best_effSignal))
print("best_effBkg: " + str(best_effBkg))

idx_WP90 = 0
minD0p9 = 999.0
for idx in range(len(effSignal)):
    if abs(effSignal[idx] - 0.90) < minD0p9:
        idx_WP90 = idx
        minD0p9 = abs(effSignal[idx] - 0.90)

WP90_significance = significance[idx_WP90]
WP90_threshold = thresholds[idx_WP90]
WP90_effSignal = effSignal[idx_WP90]
WP90_effBkg = effBkg[idx_WP90]

print("WP90_significance: " + str(WP90_significance))
print("WP90_threshold: " + str(WP90_threshold))
print("WP90_effSignal: " + str(WP90_effSignal))
print("WP90_effBkg: " + str(WP90_effBkg))

idx_WP80 = 0
minD0p8 = 999.0
for idx in range(len(effSignal)):
    if abs(effSignal[idx] - 0.80) < minD0p8:
        idx_WP80 = idx
        minD0p8 = abs(effSignal[idx] - 0.80)

WP80_significance = significance[idx_WP80]
WP80_threshold = thresholds[idx_WP80]
WP80_effSignal = effSignal[idx_WP80]
WP80_effBkg = effBkg[idx_WP80]

print("WP80_significance: " + str(WP80_significance))
print("WP80_threshold: " + str(WP80_threshold))
print("WP80_effSignal: " + str(WP80_effSignal))
print("WP80_effBkg: " + str(WP80_effBkg))

##########################################################
# make histogram of discriminator value for signal and bkg
##########################################################
# pd.DataFrame({'truth':y_test, 'disc':y_pred}).hist(column='disc', by='truth', bins=50)
y_frame = pd.DataFrame({"truth": y_test, "disc": y_pred, "weight": sample_weights_test})
y_frame_train = pd.DataFrame(
    {
        "truth": y_train,
        "disc": y_pred_train,
        "weight": sample_weights_train,
    }
)
disc_bkg = y_frame[y_frame["truth"] == 0]["disc"].values
disc_bkg_train = y_frame_train[y_frame_train["truth"] == 0]["disc"].values
disc_signal = y_frame[y_frame["truth"] == 1]["disc"].values
disc_signal_train = y_frame_train[y_frame_train["truth"] == 1]["disc"].values
weight_bkg = y_frame[y_frame["truth"] == 0]["weight"].values
weight_bkg_train = y_frame_train[y_frame_train["truth"] == 0]["weight"].values
weight_signal = y_frame[y_frame["truth"] == 1]["weight"].values
weight_signal_train = y_frame_train[y_frame_train["truth"] == 1]["weight"].values
f = plt.figure()
ax = f.add_subplot(111)
plt.subplots_adjust(top=0.9, bottom=0.15, left=0.15, right=0.95)
plt.hist(
    disc_signal,
    density=True,
    bins=100,
    alpha=1.0,
    histtype="step",
    lw=2,
    label="signal - test",
    weights=weight_signal,
)
plt.hist(
    disc_signal_train,
    density=True,
    bins=100,
    alpha=1.0,
    histtype="step",
    lw=2,
    label="signal  - train",
    weights=weight_signal_train,
)
plt.hist(
    disc_bkg,
    density=True,
    bins=100,
    alpha=1.0,
    histtype="step",
    lw=2,
    label="bkg - test",
    weights=weight_bkg,
)
plt.hist(
    disc_bkg_train,
    density=True,
    bins=100,
    alpha=1.0,
    histtype="step",
    lw=2,
    label="bkg - train",
    weights=weight_bkg_train,
)
plt.yscale("log")
plt.xlim([0.0, 1.0])
plt.ylim([0.001, 1000.0])
plt.legend(loc="upper center")
plt.xlabel("BDT response", horizontalalignment="right", x=1.0, fontsize=15)
plt.ylabel("Events", horizontalalignment="right", y=1.0, fontsize=14)
plt.xticks(fontsize=13)
plt.yticks(fontsize=13)
# plt.axvline(x=WP90_threshold, color="black", linestyle='--')
# plt.axvline(x=WP80_threshold, color="black")

# plt.text(0.5,0.7,'WP90: disc > %.4f'%WP90_threshold, fontsize=12, horizontalalignment='center', verticalalignment='center', transform=plt.gca().transAxes)
# plt.text(0.5,0.6,'WP80: disc > %.4f'%WP80_threshold, fontsize=12, horizontalalignment='center', verticalalignment='center', transform=plt.gca().transAxes)
plt.text(
    0.0,
    1.01,
    "CMS",
    ha="left",
    va="bottom",
    transform=ax.transAxes,
    weight="bold",
    fontsize=17,
)
plt.text(
    0.12,
    1.01,
    "Simulation Preliminary",
    ha="left",
    va="bottom",
    transform=ax.transAxes,
    style="italic",
    fontsize=16,
)
plt.text(
    1.0, 1.01, "13 TeV", ha="right", va="bottom", transform=ax.transAxes, fontsize=16
)
plt.savefig(plotDir + "training/mydiscriminator_" + test_name + "_logY.pdf")
plt.savefig(plotDir + "training/mydiscriminator_" + test_name + "_logY.png")


f = plt.figure()
ax = f.add_subplot(111)
plt.subplots_adjust(top=0.9, bottom=0.15, left=0.15, right=0.95)
plt.hist(
    disc_signal,
    density=True,
    bins=100,
    alpha=1.0,
    histtype="step",
    lw=2,
    label="signal - test",
    weights=weight_signal,
)
plt.hist(
    disc_signal_train,
    density=True,
    bins=100,
    alpha=1.0,
    histtype="step",
    lw=2,
    label="signal  - train",
    weights=weight_signal_train,
)
plt.hist(
    disc_bkg,
    density=True,
    bins=100,
    alpha=1.0,
    histtype="step",
    lw=2,
    label="bkg - test",
    weights=weight_bkg,
)
plt.hist(
    disc_bkg_train,
    density=True,
    bins=100,
    alpha=1.0,
    histtype="step",
    lw=2,
    label="bkg - train",
    weights=weight_bkg_train,
)
plt.yscale("linear")
plt.xlim([0.0, 1.0])
# plt.ylim([0.001, 100.0])
plt.legend(loc="upper center")
plt.xlabel("BDT response", horizontalalignment="right", x=1.0, fontsize=15)
plt.ylabel("Events", horizontalalignment="right", y=1.0, fontsize=14)
plt.xticks(fontsize=13)
plt.yticks(fontsize=13)
# plt.axvline(x=WP90_threshold, color="black", linestyle='--')
# plt.axvline(x=WP80_threshold, color="black")
# plt.text(0.5,0.7,'WP90: disc > %.4f'%WP90_threshold, fontsize=12, horizontalalignment='center', verticalalignment='center', transform=plt.gca().transAxes)
# plt.text(0.5,0.6,'WP80: disc > %.4f'%WP80_threshold, fontsize=12, horizontalalignment='center', verticalalignment='center', transform=plt.gca().transAxes)
plt.text(
    0.0,
    1.01,
    "CMS",
    ha="left",
    va="bottom",
    transform=ax.transAxes,
    weight="bold",
    fontsize=17,
)
plt.text(
    0.12,
    1.01,
    "Simulation Preliminary",
    ha="left",
    va="bottom",
    transform=ax.transAxes,
    style="italic",
    fontsize=16,
)
plt.text(
    1.0, 1.01, "13 TeV", ha="right", va="bottom", transform=ax.transAxes, fontsize=16
)
plt.savefig(plotDir + "training/mydiscriminator_" + test_name + "_linY.pdf")
plt.savefig(plotDir + "training/mydiscriminator_" + test_name + "_linY.png")


# plot roc curve
f = plt.figure()
ax = f.add_subplot(111)
plt.subplots_adjust(top=0.9, bottom=0.15, left=0.15, right=0.95)
lw = 2
plt.plot(fpr, tpr, color="darkorange", lw=lw, label="ROC curve")
plt.plot([0, 1], [0, 1], color="navy", lw=lw, linestyle="--")
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.ylabel("Signal Efficiency", horizontalalignment="right", y=1.0, fontsize=15)
plt.xlabel("Background Efficiency", horizontalalignment="right", x=1.0, fontsize=15)
plt.xticks(fontsize=13)
plt.yticks(fontsize=13)
# plt.axhline(y=0.9, color="black", linestyle='--')
# plt.axhline(y=0.8, color="black")
# plt.text(0.5,0.1,'WP80: bkg eff = %.4f'%WP80_effBkg, fontsize=12)
# plt.text(0.5,0.2,'WP90: bkg eff = %.4f'%WP90_effBkg, fontsize=12)
# plt.text(0.5,0.3,'WP90: S/sqrt(B) = %.2f'%WP90_significance, fontsize=12)
plt.text(0.5, 0.3, "AUC = %.4f" % AUC, fontsize=12)
# plt.title('Receiver operating characteristic example')
# plt.legend(loc="lower right")
# plt.show()
plt.text(
    0.0,
    1.01,
    "CMS",
    ha="left",
    va="bottom",
    transform=ax.transAxes,
    weight="bold",
    fontsize=17,
)
plt.text(
    0.12,
    1.01,
    "Simulation Preliminary",
    ha="left",
    va="bottom",
    transform=ax.transAxes,
    style="italic",
    fontsize=16,
)
plt.text(
    1.0, 1.01, "13 TeV", ha="right", va="bottom", transform=ax.transAxes, fontsize=16
)
plt.savefig(plotDir + "training/myroc_" + test_name + ".pdf")
plt.savefig(plotDir + "training/myroc_" + test_name + ".png")

# Pickle dictionary using protocol 0.
output = open("models/model_" + test_name + ".pkl", "wb")
pickle.dump(model, output)
output.close()
model.get_booster().dump_model("models/model_" + test_name + ".txt")
model.get_booster().save_model("models/model_" + test_name + ".xgb")

# plot feature importances

model.get_booster().feature_names = [row[1] for row in variables[:-1]]

xgb.plot_importance(
    model, max_num_features=len(variables) - 1, xlabel="F score (weight)"
)
plt.savefig(
    plotDir + "training/myImportances_Fscore_" + test_name + ".pdf", bbox_inches="tight"
)
plt.savefig(
    plotDir + "training/myImportances_Fscore_" + test_name + ".png", bbox_inches="tight"
)

# xgb.plot_tree( model.get_booster() )
xgb.plot_tree(model)
fig = plt.gcf()
# fig.set_size_inches(500, 50)
plt.draw()
plt.savefig(plotDir + "training/myTree_" + test_name + ".pdf")
plt.savefig(plotDir + "training/myTree_" + test_name + ".png")

print(
    "[INFO]: S ="
    + str(signal_events)
    + "; B ="
    + str(bkg_events)
    + "; S/sqrt(B) = "
    + str(signal_events / math.sqrt(bkg_events))
)
print(
    "[INFO] WP90: S = %6.3f" % (signal_events * 0.90)
    + ", B = %6.3f" % (bkg_events * WP90_effBkg)
)
print(
    "[INFO] WP80: S = %6.3f" % (signal_events * 0.80)
    + ", B = %6.3f" % (bkg_events * WP80_effBkg)
)
