#ifndef LIB_RUN3CONTANTS_H
#define LIB_RUN3CONTANTS_H

#include <TString.h>
#include <map>

const std::map<TString, float> LUMINOSITY = {
    {"2022B", 0.09656}, {"2022C", 5.0104},  {"2022D", 2.9700},
    {"2022E", 5.8070},  {"2022F", 17.7819}, {"2022G", 3.0828},
};

const std::map<TString, float> CROSS_SECTION = {
    // Background
    {"TT", 102.41},
    {"DY", 6244.8},
    {"DY50-120", 16793 * 8 / 70.},
    {"DY120-200", 1970.12 / 80},
    // Signal
    {"ggF", 52.1},
    {"VBF", 4.075},
    {"ttH", 0.5688},
    // Dummy data value 
    {"Data", -1},
};

#endif // LIB_RUN3CONTANTS_H
