from utils.sim_vs_data import draw_data_and_simul_and_ratio


# ordered from bottom to top in the plot, so order it from lower to bigger cross section
# background_sources = ["TT", "DY120-200", "DY50-120"]
background_sources = [
    "TT",
    "DiBoson",
    "DYto2L-2Jets",
    # "DYJetstoLL",
]
# "ZZto2L2QNu",
# "WZto2L2QNu",
# "ZZto2L2Nu",
# "ZZto4L",
# "WWto2L2Nu",
# ]
# signal_sources = ["ggH", "VBF"]
signal_sources = ["ggH", "VBF"]
variables = ["pt", "mass", "mass_full_range", "phi", "eta"]
era = "2022EE"

for variable in variables:
    draw_data_and_simul_and_ratio(variable, era, background_sources, signal_sources)
