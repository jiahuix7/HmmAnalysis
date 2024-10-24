#ifndef LIB_CreateTuple_H
#define LIB_CreateTuple_H

#include "Constants.h"
#include "Run3Constants.h"
#include "Utils.h"
#include <TChain.h>
#include <TFile.h>
#include <TH1F.h>
#include <TLorentzVector.h>
#include <TString.h>
#include <TTree.h>
#include <cmath>
#include <iostream>
#include <math.h>

class CreateTuple {
  public:
    // Methods
    CreateTuple(TString input, TString output, TString era, TString channel,
                bool is_data, bool is_signal_);
    virtual ~CreateTuple();
    void fillChain();
    void setBranchesAddressesInput();
    void setBranchesAddressesOutput();
    void fillOutputTree();
    void saveTree();

  private:
    // Members

    TChain *tree_input;
    TTree *tree_output;
    bool is_signal;
    long double gen_weight_sum;
    const float luminosity;
    const float cross_section;
    TString input_name;
    TString output_name;
    TString output_directory;
    TFile *output_file;

    // Read Tuples
    // DiMuon variables
    float diMuon_mass, diMuon_pt, diMuon_phi, diMuon_eta, gen_weight,
        pileup_weight, pileup;
    // Muon variables
    int mu1_index, mu2_index;
    std::vector<int> *mu_charge;
    std::vector<float> *mu_pt, *mu_phi, *mu_eta;
    // Jet variables
    int n_jet;
    std::vector<float> *jet_mass, *jet_pt, *jet_phi, *jet_eta;
    // diJet variables
    float diJet_pt, diJet_eta, diJet_phi, diJet_mass, diJet_mass_mo;

    // New Variables
    double scale_factor; // luminosity * cross_section / gen_weight_sum
    double weight;
    int is_data_int, is_signal_int;

    // DiMuon variables
    float diMuon_rapidity;

    // Muon variables
    float mu1_pt_mass_ratio, mu2_pt_mass_ratio, mu1_eta, mu2_eta, phi_CS,
        cos_theta_CS;
};

CreateTuple::CreateTuple(TString input, TString output, TString era,
                         TString channel, bool is_data, bool is_signal_)
    : luminosity(LUMINOSITY.at(era)), cross_section(CROSS_SECTION.at(channel)) {

    tree_input = new TChain("tree");
    tree_output = new TTree("tree_output", "tree_output");
    input_name = input;
    output_directory = output;
    is_signal = is_signal_;
    output_name = channel + "_" + era + "_tuples.root";
    std::cout << "Luminosity: " << luminosity
              << ", cross section: " << cross_section << std::endl;
    if (!is_data) {
        gen_weight_sum = GetGenWeightSum(input_name);
        scale_factor =
            GetScaleFactor(luminosity, cross_section, gen_weight_sum);
        is_data_int = 0;
        if (is_signal_) {
            is_signal_int = 1;
        } else {
            is_signal_int = 0;
        }
    } else {
        is_data_int = 1;
    }

    mu_charge = nullptr;
    mu_pt = nullptr;
    mu_phi = nullptr;
    mu_eta = nullptr;
    // elec_pt = nullptr;
    jet_eta = nullptr;
    jet_pt = nullptr;
    jet_phi = nullptr;
    jet_mass = nullptr;

    fillChain();
}

CreateTuple::~CreateTuple() {
    delete tree_input->GetCurrentFile();
    delete tree_output;
    delete output_file;
}

void CreateTuple::fillChain() {
    tree_input->Add(input_name);
    if (!tree_input) {
        throw std::runtime_error("Tuple file not found");
        return;
    }
    std::cout << "Tuple loaded" << std::endl;
}

void CreateTuple::setBranchesAddressesOutput() {

    tree_output->Branch("gen_weight", &gen_weight, "gen_weight/f");
    tree_output->Branch("pileup_weight", &pileup_weight, "pileup_weight/f");
    tree_output->Branch("scale_factor", &scale_factor, "scale_factor/d");
    tree_output->Branch("weight", &weight, "weight/d");
    tree_output->Branch("is_data", &is_data_int, "is_data/i");
    tree_output->Branch("is_signal", &weight, "signal/i");

    // DiMuon variables
    tree_output->Branch("diMuon_mass", &diMuon_mass, "diMuon_mass/f");
    tree_output->Branch("diMuon_pt", &diMuon_pt, "diMuon_pt/f");
    tree_output->Branch("diMuon_phi", &diMuon_phi, "diMuon_phi/f");
    tree_output->Branch("diMuon_eta", &diMuon_eta, "diMuon_eta/f");
    tree_output->Branch("diMuon_rapidity", &diMuon_rapidity,
                        "diMuon_rapidity/f");

    // Muon variables
    tree_output->Branch("mu1_pt_mass_ratio", &mu1_pt_mass_ratio,
                        "mu1_pt_mass_ratio/f");
    tree_output->Branch("mu2_pt_mass_ratio", &mu1_pt_mass_ratio,
                        "mu2_pt_mass_ratio/f");
    tree_output->Branch("mu1_eta", &mu1_eta, "mu1_eta/f");
    tree_output->Branch("mu2_eta", &mu2_eta, "mu2_eta/f");
    tree_output->Branch("phi_CS", &phi_CS, "phi_CS/f");
    tree_output->Branch("cos_theta_CS", &cos_theta_CS, "cos_theta_CS/f");

    // Jet variables

    // DiJet variables
    std::cout << "Output Branches addressed setted" << std::endl;
}

void CreateTuple::setBranchesAddressesInput() {

    tree_input->SetBranchAddress("t_genWeight", &gen_weight);
    tree_input->SetBranchAddress("t_puWeight", &pileup_weight);

    // DiMuon variables
    tree_input->SetBranchAddress("t_diMuon_mass", &diMuon_mass);
    tree_input->SetBranchAddress("t_diMuon_pt", &diMuon_pt);
    tree_input->SetBranchAddress("t_diMuon_phi", &diMuon_phi);
    tree_input->SetBranchAddress("t_diMuon_eta", &diMuon_eta);

    // Muon variables
    tree_input->SetBranchAddress("t_mu1", &mu1_index);
    tree_input->SetBranchAddress("t_mu2", &mu2_index);
    tree_input->SetBranchAddress("t_Mu_charge", &mu_charge);
    tree_input->SetBranchAddress("t_Mu_pt", &mu_pt);
    tree_input->SetBranchAddress("t_Mu_phi", &mu_phi);
    tree_input->SetBranchAddress("t_Mu_eta", &mu_eta);

    // Jet variables
    tree_input->SetBranchAddress("t_nJet", &n_jet);
    tree_input->SetBranchAddress("t_Jet_mass", &jet_mass);
    tree_input->SetBranchAddress("t_Jet_pt", &jet_pt);
    tree_input->SetBranchAddress("t_Jet_phi", &jet_phi);
    tree_input->SetBranchAddress("t_Jet_eta", &jet_eta);

    // DiJet variables
    tree_input->SetBranchAddress("t_diJet_mass", &diJet_mass);
    tree_input->SetBranchAddress("t_diJet_mass_mo", &diJet_mass_mo);
    tree_input->SetBranchAddress("t_diJet_pt", &diJet_pt);
    tree_input->SetBranchAddress("t_diJet_phi", &diJet_phi);
    tree_input->SetBranchAddress("t_diJet_eta", &diJet_eta);

    std::cout << "Input Branches addressed setted" << std::endl;
}

void CreateTuple::fillOutputTree() {

    std::cout << "Filling Output Tree" << std::endl;
    double total_entries = tree_input->GetEntries();
    TLorentzVector mu1_vector;
    TLorentzVector mu2_vector;
    std::pair<float, float> angles_CS;
    for (int event_index = 0; event_index < total_entries; event_index++) {
        tree_input->GetEntry(event_index);
        if (diMuon_mass < 110 || diMuon_mass > 150)
            continue;

        weight = GetEventWeight(gen_weight, pileup_weight, scale_factor);

        // DiMuon variables
        diMuon_rapidity = (mu1_vector + mu2_vector).Rapidity();

        // Muon variables
        mu1_vector.SetPtEtaPhiM((*mu_pt)[mu1_index], (*mu_eta)[mu1_index],
                                (*mu_phi)[mu1_index], MUON_MASS);
        mu2_vector.SetPtEtaPhiM((*mu_pt)[mu2_index], (*mu_eta)[mu2_index],
                                (*mu_phi)[mu2_index], MUON_MASS);

        angles_CS = CSAngles(mu1_vector, mu2_vector, (*mu_charge)[mu1_index]);

        mu1_pt_mass_ratio = (*mu_pt)[mu1_index] / diMuon_mass;
        mu2_pt_mass_ratio = (*mu_pt)[mu2_index] / diMuon_mass;
        mu1_eta = (*mu_eta)[mu1_index];
        mu2_eta = (*mu_eta)[mu2_index];
        phi_CS = angles_CS.second;
        cos_theta_CS = angles_CS.first;

        tree_output->Fill();
        // Jet variables
        // n_jet_hist.Fill(n_jet, weight);
        // if (n_jet < 2)
        // continue;
        // for (int j = 0; j < n_jet; j++) {
        // jet_mass_hist.Fill(jet_mass->at(j), weight);
        // jet_pt_hist.Fill(jet_pt->at(j), weight);
        // jet_phi_hist.Fill(jet_phi->at(j), weight);
        // jet_eta_hist.Fill(jet_eta->at(j), weight);
        //}

        //// diJet variables
        // diJet_pt_hist.Fill(diJet_pt, weight);
        // diJet_eta_hist.Fill(diJet_eta, weight);
        // diJet_phi_hist.Fill(diJet_phi, weight);
        // diJet_mass_hist.Fill(diJet_mass, weight);
        // diJet_mass_mo_hist.Fill(diJet_mass_mo, weight);
        // delta_eta_hist.Fill(jet_eta->at(0) - jet_eta->at(1), weight);
    }

    std::cout << "Output Tuple filled" << std::endl;
}

void CreateTuple::saveTree() {

    output_file = new TFile(output_directory + output_name, "RECREATE");
    output_file->cd();

    tree_output->Write();

    output_file->Close();
    std::cout << "Tuple saved" << std::endl;
}

#endif // if LIB_CreateTuple_H
