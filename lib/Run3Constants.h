#ifndef LIB_RUN3CONTANTS_H
#define LIB_RUN3CONTANTS_H

#include <TString.h>
#include <map>

constexpr float H_TO_MUMU_BRANCHING_RATIO = 2.176e-4;

//// Luminosity in fb-1
const std::map<TString, float> LUMINOSITY = {
    {"2022B", 0.09656}, {"2022C", 5.0104},   {"2022D", 2.9700},
    {"2022E", 5.8070},  {"2022F", 17.7819},  {"2022G", 3.0828},
    {"2022", 7.9804},   {"2022EE", 26.6717},
};

//// Cross section in pb
const std::map<TString, float> CROSS_SECTION = {
    //********************//
    //     Background     //
    //********************//
    // TT
    {"TTto2L2Nu", 86.61},
    {"TTtoLNu2Q", 358.61},
    {"TWminusto2L2Nu", -1},

    // DY
    //{"DYJetstoLL", 6244.8},
    {"DYto2L-2Jets", 6244.8},
    {"DY50to120", 2219.},
    {"DY120to200", 21.65},
    // Diboson
    {"WWto2L2Nu", 12.178},
    {"WWto4Q", -1},
    {"WWtoLNu2Q", -1},
    {"WZto2L2Q", 6.321},
    {"WZto3LNu", 4.658},
    {"WZtoLNu2Q", -1},
    {"ZZto2L2Nu", 0.601},
    {"ZZto2L2Q", 3.696},
    {"ZZto4L", 1.325},
    //  EWK
    {"EWK_2L2J", 1.410},
    // TriBoson
    {"WWW_4F", 0.2086},
    //********************//
    //       Signal       //
    //********************//
    {"ggH", 52.23 * H_TO_MUMU_BRANCHING_RATIO},
    {"VBF", 4.078 * H_TO_MUMU_BRANCHING_RATIO},
    {"ttH", 0.57 * H_TO_MUMU_BRANCHING_RATIO},
    //********************//
    //  Dummy data value  //
    //********************//
    {"Data", -1},
    {"DoubleMuon_2022C", -1},
    {"Muon_2022C", -1},
    {"Muon_2022D", -1},
    {"Muon_2022E", -1},
    {"Muon_2022F", -1},
    {"Muon_2022G", -1},
    {"Muon0_2023B", -1},
    {"Muon0_2023C_v1", -1},
    {"Muon0_2023C_v2", -1},
    {"Muon0_2023C_v3", -1},
    {"Muon0_2023C_v4", -1},
    {"Muon1_2023B", -1},
    {"Muon1_2023C_v1", -1},
    {"Muon1_2023C_v2", -1},
    {"Muon1_2023C_v3", -1},
    {"Muon1_2023C_v4", -1},
    {"Muon0_2023D_v1", -1},
    {"Muon0_2023D_v2", -1},
    {"Muon1_2023D_v1", -1},
    {"Muon1_2023D_v2", -1},
};

#endif // LIB_RUN3CONTANTS_H
