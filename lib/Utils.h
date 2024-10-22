#ifndef LIB_UTILS_H
#define LIB_UTILS_H

#include "Constants.h"
#include "Run3Constants.h"
#include <TFile.h>
#include <TH1F.h>
#include <TLorentzVector.h>
#include <TVector3.h>
#include <memory>

long double GetGenWeightSum(const TString &input_name) {

    // TFile *histogram_file = new TFile(input_name, "READ");
    std::unique_ptr<TFile> histogram_file(TFile::Open(input_name, "READ"));

    if (!histogram_file || histogram_file->IsZombie()) {
        throw std::runtime_error(
            "Histogram file was not found or is is Zombie: " +
            std::string(input_name));
        return -1;
    }
    TH1F *gen_weight_sum_histogram =
        static_cast<TH1F *>(histogram_file->Get("h_sumOfgenWeight"));

    if (!gen_weight_sum_histogram) {
        throw std::runtime_error("Sum gen weight histogram WAS NOT found");
        return -1;
    }

    long double gen_weight_sum = gen_weight_sum_histogram->GetBinContent(1);
    std::cout << "The sum of gen weights is: " << gen_weight_sum << std::endl;
    histogram_file->Close();
    return gen_weight_sum;
}

double GetScaleFactor(const float &luminosity, const float &cross_section,
                      const long double &gen_weight_sum) {
    return luminosity * (cross_section * 1000) / gen_weight_sum;
}

double GetEventWeight(const float &gen_weight, const float &pileup_weight,
                   const float &scale_factor) {
    return gen_weight * pileup_weight * scale_factor;
}

std::pair<float, float> CSAngles(TLorentzVector vector_1,
                                 TLorentzVector vector_2, const int charge) {
    // https://github.com/alisw/AliPhysics/blob/master/PWGDQ/dielectron/core/AliDielectronPair.cxx
    TLorentzVector proton_1_vector(
        0., 0., -BEAM_ENERGY_GEV,
        TMath::Sqrt((BEAM_ENERGY_GEV / 2) * (BEAM_ENERGY_GEV / 2) +
                    PROTON_MASS * PROTON_MASS));
    TLorentzVector proton_2_vector(
        0., 0., BEAM_ENERGY_GEV,
        TMath::Sqrt((BEAM_ENERGY_GEV / 2) * (BEAM_ENERGY_GEV / 2) +
                    PROTON_MASS * PROTON_MASS));

    TLorentzVector higgs_vector = vector_1 + vector_2;
    vector_1.Boost(-(higgs_vector.BoostVector())); // go to Higgs RFR
    vector_2.Boost(-(higgs_vector.BoostVector()));
    proton_1_vector.Boost(-(higgs_vector.BoostVector()));
    proton_2_vector.Boost(-(higgs_vector.BoostVector()));

    TVector3 y_axis =
        ((proton_1_vector.Vect()).Cross(proton_2_vector.Vect())).Unit();
    TVector3 z_Axis_CS =
        ((proton_1_vector.Vect()).Unit() - (proton_2_vector.Vect()).Unit())
            .Unit();
    TVector3 x_axis_CS = (y_axis.Cross(z_Axis_CS)).Unit();

    float cos_theta_CS;
    float phi_CS;
    if (charge > 0) {
        cos_theta_CS = z_Axis_CS.Dot((vector_2.Vect()).Unit());
        phi_CS = TMath::ATan2((vector_2.Vect()).Dot(y_axis),
                              (vector_2.Vect()).Dot(x_axis_CS));
    } else {
        cos_theta_CS = z_Axis_CS.Dot((vector_1.Vect()).Unit());
        phi_CS = TMath::ATan2((vector_1.Vect()).Dot(y_axis),
                              (vector_1.Vect()).Dot(x_axis_CS));
    }

    return std::pair<float, float>(cos_theta_CS, phi_CS);
}

#endif // if LIB_UTILS_H
