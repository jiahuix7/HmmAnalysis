import mplhep as hep

# import numpy as np
import matplotlib.pyplot as plt

from utils.helper import get_canvas, save_figure

plt.style.use(hep.style.CMS)  # or ATLAS/LHCb2


colors = ["blue", "red", "lime"]
eras = ["2022", "2022EE", "2022Combined"]

fig, ax = get_canvas()
for era, colors in zip(eras, colors):
    fpr_list = []
    tpr_list = []
    with open(
        "../python/xgboost/ggH/mumu_vs_bkg_"
        + era
        + "_roc.txt",
        "r",
    ) as file:
        for line in file:
            parts = line.strip().split(",")
            fpr = float(parts[1].split("=")[1].strip())
            tpr = float(parts[2].split("=")[1].strip())
            fpr_list.append(fpr)
            tpr_list.append(tpr)

    ax.plot(tpr_list, fpr_list, label=era + " ggH")

for era, colors in zip(eras, colors):
    fpr_list = []
    tpr_list = []
    with open(
        "../python/xgboost/signals/mumu_vs_bkg_"
        + era
        + "_roc.txt",
        "r",
    ) as file:
        for line in file:
            parts = line.strip().split(",")
            fpr = float(parts[1].split("=")[1].strip())
            tpr = float(parts[2].split("=")[1].strip())
            fpr_list.append(fpr)
            tpr_list.append(tpr)

    ax.plot(tpr_list, fpr_list, label=era + " ggh and VBF", linestyle="--")

ax.set_ylabel(r"$\epsilon_{bkg}$")
ax.set_xlabel(r"$\epsilon_{sig}$")
ax.set_ylim(0.0001, 1)
ax.set_xlim(0, 1)
ax.legend(frameon=False, loc="lower right")
hep.cms.label(data="False", label="", year="2022", com="13,6", ax=ax)
ax.set_yscale("log")
ax.grid()

save_figure(fig, "../plots/ggH_category/roc/", "roc_space_vars")
