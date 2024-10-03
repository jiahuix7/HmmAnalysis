#!/usr/bin/python

import os
import datetime
import time
import subprocess
import glob
import sys
from collections import OrderedDict

list_datasets = []
analysis_job_sender = open("condor_job_sender.sh", "r")
for line in analysis_job_sender:
    line = line.strip()
    if line[0:3] != "cd ":
        continue

    setname = line.split("/")[-2]
    if "ext1" in setname:
        continue
    
    list_datasets.append(setname)
analysis_job_sender.close()

# # You can hardcode a list of datasets here if you want!
# list_datasets = [
#     "Muon_2022C",
#     "Muon_2022D",
#     "Muon_2022E",
#     "Muon_2022F",
#     "Muon_2022G",
#     "DYto2L-2Jets_Summer22EE",
#     "TTto2L2Nu_Summer22",
#     "TTto2L2Nu_Summer22EE",
# ]

os.system("mkdir -p hadd/log/")
os.system("mkdir -p hadd/out/")
os.system("mkdir -p hadd/err/")

DIR_eos = "store/user/csanmart/analyzer_HiggsMuMu"
for dataset in list_datasets:
    FILESDIR = ""
    for dir_type in ["Data", "MC_background", "MC_signal"]:
        if os.path.exists("/eos/uscms/" + DIR_eos + "/%s/%s"%(dir_type, dataset)):
            print("Directory found!")
            FILESDIR = DIR_eos + "/%s/%s"%(dir_type, dataset)
            break

    if not FILESDIR:
        print("No folder found for " + dataset + " :(. Skipping.")
        continue
    elif os.path.exists("/eos/uscms/" + FILESDIR + "/SumGenWeight.root"):
        print("Dataset already merged! Skipping " + dataset)
        continue

    #####################################
    # Create Condor JDL file
    #####################################
    jobfile = open("hadd_%s.jdl"%(dataset), "w+")
    jobfile.write("Universe  = vanilla" + "\n")
    jobfile.write("Executable = ./hadd_datasets.sh" + "\n")
    args = dataset + " " + FILESDIR
    jobfile.write("Arguments = " + args + "\n")

    jobfile.write("Log = hadd/log/job_%s.$(Cluster).log"%(dataset) + "\n")
    jobfile.write("Output = hadd/out/job_%s.$(Cluster).out"%(dataset) + "\n")
    jobfile.write("Error = hadd/err/job_%s.$(Cluster).err"%(dataset) + "\n")
    jobfile.write("x509userproxy = $ENV(X509_USER_PROXY)" + "\n")

    transfer_files = "hadd_datasets.sh, "

    jobfile.write("transfer_input_files = " + transfer_files + "\n")

    jobfile.write("should_transfer_files = YES" + "\n")
    jobfile.write("when_to_transfer_output = ON_EXIT" + "\n\n# Resources request\n")
    jobfile.write("RequestMemory = 2000 \n\n")
    jobfile.write("Queue 1" + "\n")

    jobfile.close()

    print(" Submitting job for " + dataset)
    os.system("condor_submit " + "hadd_%s.jdl"%(dataset))

    os.remove("hadd_%s.jdl"%(dataset))


