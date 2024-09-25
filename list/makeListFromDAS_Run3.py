#!/usr/bin/python

import os
import json


datasets = {
    ####################################################################################################
    # 2022 Datasets
    ####################################################################################################
    "DoubleMuon_2022A": "/DoubleMuon/Run2022A-22Sep2023-v1/NANOAOD",
    "DoubleMuon_2022B": "/DoubleMuon/Run2022B-22Sep2023-v1/NANOAOD",
    "DoubleMuon_2022C": "/DoubleMuon/Run2022C-22Sep2023-v1/NANOAOD",
    "Muon_2022C": "/Muon/Run2022C-22Sep2023-v1/NANOAOD",
    "Muon_2022D": "/Muon/Run2022D-22Sep2023-v1/NANOAOD",
    "Muon_2022E": "/Muon/Run2022E-22Sep2023-v1/NANOAOD",
    "Muon_2022F": "/Muon/Run2022F-22Sep2023-v2/NANOAOD",
    "Muon_2022G": "/Muon/Run2022G-22Sep2023-v1/NANOAOD",
    ####################################################################################################
    # 2022 Simulations Backgrounds
    ####################################################################################################
    "DY120to200_Summer22": "/DYto2Mu_MLL-120to200_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM",
    "DY50to120_Summer22": "/DYto2Mu_MLL-50to120_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM",
    "DY120to200_Summer22EE": "/DYto2Mu_MLL-120to200_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM",
    "DY50to120_Summer22EE": "/DYto2Mu_MLL-50to120_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2/NANOAODSIM",
    "TTto2L2Nu_Summer22": "/TTto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM",
    "TTto2L2Nu_Summer22_ext1": "/TTto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5_ext1-v2/NANOAODSIM",
    "TTtoLNu2Q_Summer22": "/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM",
    "TTtoLNu2Q_Summer22_ext1": "/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5_ext1-v2/NANOAODSIM",
    ####################################################################################################
    # 2022 Simulations Signal
    ####################################################################################################
    "ggH_Summer22": "/GluGluHto2Mu_M-125_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v1/NANOAODSIM",
    "ggH_Summer22EE": "/GluGluHto2Mu_M-125_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v1/NANOAODSIM",
    "VBF_Summer22": "/VBFHto2Mu_M-125_TuneCP5_withDipoleRecoil_13p6TeV_powheg-pythia8/Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v3/NANOAODSIM",
    "VBF_Summer22EE": "/VBFHto2Mu_M-125_TuneCP5_withDipoleRecoil_13p6TeV_powheg-pythia8/Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v3/NANOAODSIM",
}

for processName in datasets.keys():
    outputFile = open(processName + ".list", "w")
    print(processName)
    # command = "dasgoclient -query=\"file dataset=" + datasets[processName] + " instance=prod/phys03 \" -json > tmpOutput.json"
    command = (
        'dasgoclient -query="file dataset='
        + datasets[processName]
        + ' " -json > tmpOutput.json'
    )
    print(command)
    os.system(command)

    jsonFile = open("tmpOutput.json", "r")
    data = json.load(jsonFile)

    for p in data:
        blockName = p["file"][0]["block.name"]
        fileName = p["file"][0]["name"]
        outputFile.write("root://cmsxrootd.fnal.gov/" + fileName + "\n")

    os.remove("tmpOutput.json")
