#ifndef LIB_GETHISTOGRAMS_H
#define LIB_GETHISTOGRAMS_H

#include "Run3Constants.h"
#include <TChain.h>
#include <TFile.h>
#include <TH1F.h>
#include <TString.h>
#include <cmath>
#include <iostream>
#include <math.h>

class CreateHistograms {
  public:
    // Methods
    CreateHistograms(TString input, TString output, TString era,
                     TString channel);
    virtual ~CreateHistograms();
    double eventWeight();
    void fillChain();
    void defineHistograms();
    void setBranchesAddresses();
    void getGenWeightSum();
    void getScaleFactor();
    void fillHistogramsData();
    void fillHistogramsSimulation();
    void saveHistograms();
    // Members
    TChain *tuple;
    float diMuon_mass, diMuon_pt, diMuon_phi, diMuon_eta, gen_weight,
        pileup_weight, pileup;
    // int mu1_index, mu2_index;
    // std::vector<float> t_Mu_pt;
    long double gen_weight_sum;
    double scale_factor; // luminosity * cross_section / gen_weight_sum
    const float luminosity;
    const float cross_section;
    // const TString era;
    // const TString channel;
    TH1F diMuon_mass_hist, diMuon_pt_hist, diMuon_eta_hist, diMuon_phi_hist;
    TH1F diMuon_mass_hist_full_range, diMuon_pileup_hist,
        diMuon_pileup_hist_weighted, diMuon_pileup_hist_gen_weighted,
        diMuon_pileup_hist_pugen_weighted;
    TString input_name;
    TString output_name;
    TString output_directory;
    TFile *output_file;
};

CreateHistograms::CreateHistograms(TString input, TString output, TString era,
                                   TString channel)
    : luminosity(LUMINOSITY.at(era)), cross_section(CROSS_SECTION.at(channel)) {

    tuple = new TChain("tree");
    input_name = input;
    output_directory = output;
    output_name = channel + "_" + era + "_histograms.root";
    std::cout << "Luminosity: " << luminosity
              << ", cross section: " << cross_section << std::endl;
    fillChain();
}

CreateHistograms::~CreateHistograms() { delete tuple->GetCurrentFile(); }

void CreateHistograms::fillChain() {
    tuple->Add(input_name);
    if (!tuple) {
        std::cout << "Tuple file DID NOT found" << std::endl;
        return;
    }
    std::cout << "Tuple loaded" << std::endl;
}

void CreateHistograms::defineHistograms() {

    diMuon_mass_hist = TH1F("diMuon_mass", "diMuon_mass", 80, 110, 150);
    diMuon_pt_hist = TH1F("diMuon_pt", "diMuon_pt", 250, 0, 250);
    diMuon_phi_hist = TH1F("diMuon_phi", "diMuon_phi", 100, -3.1415, 3.1415);
    diMuon_eta_hist = TH1F("diMuon_eta", "diMuon_eta", 200, -10, 10);
    diMuon_mass_hist_full_range =
        TH1F("diMuon_mass_full_range", "diMuon_mass_full_range", 200, 50, 150);
    diMuon_pileup_hist = TH1F("diMuon_pileup", "diMuon_pileup", 120, 0, 120);
    diMuon_pileup_hist_gen_weighted =
        TH1F("diMuon_pileup_hist_gen_weighted", "diMuon_pileup_gen_weighted",
             120, 0, 120);
    diMuon_pileup_hist_pugen_weighted =
        TH1F("diMuon_pileup_hist_pugen_weighted",
             "diMuon_pileup_pugen_weighted", 120, 0, 120);
}

void CreateHistograms::setBranchesAddresses() {

    tuple->SetBranchAddress("t_diMuon_mass", &diMuon_mass);
    tuple->SetBranchAddress("t_diMuon_pt", &diMuon_pt);
    tuple->SetBranchAddress("t_diMuon_phi", &diMuon_phi);
    tuple->SetBranchAddress("t_diMuon_eta", &diMuon_eta);
    tuple->SetBranchAddress("t_genWeight", &gen_weight);
    tuple->SetBranchAddress("t_puWeight", &pileup_weight);
    // tuple->SetBranchAddress("t_pileup", &pileup);
    std::cout << "Branches addressed setted" << std::endl;
}

void CreateHistograms::fillHistogramsData() {

    std::cout << "Filling data histograms" << std::endl;
    int total_entries = tuple->GetEntries();
    for (int event_index = 0; event_index < total_entries; event_index++) {
        tuple->GetEntry(event_index);
        diMuon_pt_hist.Fill(diMuon_pt);
        diMuon_phi_hist.Fill(diMuon_phi);
        diMuon_eta_hist.Fill(diMuon_eta);
        if (diMuon_mass > 120 && diMuon_mass < 130)
            continue;
        diMuon_mass_hist.Fill(diMuon_mass);
        diMuon_mass_hist_full_range.Fill(diMuon_mass);
    }
    std::cout << "Histograms filled" << std::endl;
}

void CreateHistograms::fillHistogramsSimulation() {

    std::cout << "Filling simulation histograms" << std::endl;
    double total_entries = tuple->GetEntries();
    double weight;
    for (int event_index = 0; event_index < total_entries; event_index++) {
        tuple->GetEntry(event_index);
        weight = eventWeight();
        diMuon_pt_hist.Fill(diMuon_pt, weight);
        diMuon_mass_hist.Fill(diMuon_mass, weight);
        diMuon_phi_hist.Fill(diMuon_phi, weight);
        diMuon_eta_hist.Fill(diMuon_eta, weight);
        diMuon_mass_hist_full_range.Fill(diMuon_mass, weight);
        // diMuon_pileup_hist.Fill(pileup);
        // diMuon_pileup_hist_pugen_weighted.Fill(pileup, weight);
        // if (pileup_weight != 0) {
        // diMuon_pileup_hist_gen_weighted.Fill(pileup, weight / pileup_weight);
        //}
    }
    std::cout << "Histograms filled" << std::endl;
}

void CreateHistograms::getGenWeightSum() {

    TFile *tuple_file = new TFile(input_name, "READ");
    if (!tuple_file) {
        std::cerr << "Tuple file DID NOT found" << std::endl;
        return;
    }
    TH1F *gen_weight_sum_histogram =
        (TH1F *)tuple_file->Get("h_sumOfgenWeight");
    // TH1F *gen_weight_sum_histogram =
    //(TH1F *)tuple_file->Get("h_sumOfgenpuWeight");

    if (!gen_weight_sum_histogram) {
        std::cerr << "Sum gen weight histogram WAS NOT found" << std::endl;
        tuple_file->Close();
        return; // Exit if the histogram is not found
    }

    gen_weight_sum = gen_weight_sum_histogram->GetBinContent(1);
    std::cout << "The sum of gen weights is: " << gen_weight_sum << std::endl;
    tuple_file->Close();
}

void CreateHistograms::getScaleFactor() {
    scale_factor = luminosity * (cross_section * 1000) / gen_weight_sum;
    std::cout << "The Scale Factor is: " << scale_factor << std::endl;
}

double CreateHistograms::eventWeight() {
    // return gen_weight * pileup_weight * scale_factor;
    //  if(pileup_weight > 100000){
    //  std::cout << "pileup: " <<  pileup<< std::endl;
    //  std::cout << "pileup_weight: " <<  pileup_weight << std::endl;
    //  std::cout << "gen_weight: " <<  gen_weight << std::endl;
    //  std::cout << "------------------------" << std::endl;
    ////}
    return gen_weight * scale_factor;
}

void CreateHistograms::saveHistograms() {

    output_file = new TFile(output_directory + output_name, "RECREATE");
    output_file->cd();
    diMuon_mass_hist.Write();
    diMuon_pt_hist.Write();
    diMuon_phi_hist.Write();
    diMuon_eta_hist.Write();
    diMuon_mass_hist_full_range.Write();
    diMuon_pileup_hist.Write();
    diMuon_pileup_hist_pugen_weighted.Write();
    diMuon_pileup_hist_gen_weighted.Write();
    output_file->Close();
    std::cout << "Histograms saved" << std::endl;
}

#endif // if LIB_GETHISTOGRAMS_H
