#include "../lib/CreateHistograms.h"

int main(int argc, char *argv[]) {

    if (argc != 6) {
        std::cerr << "Please give 5 arguments: input file, output file, era, "
                     "channel, is_data(T/F)"
                  << std::endl;
        return -1;
    }

    TString input(argv[1]);
    TString output(argv[2]);
    TString era(argv[3]);
    TString channel(argv[4]);
    const bool is_data = *argv[5] == 'T';

    std::cout << "Input: " << input << std::endl;
    std::cout << "Output: " << output << std::endl;
    std::cout << "Era: " << era << std::endl;
    std::cout << "Channel: " << channel << std::endl;
    std::cout << std::boolalpha;
    std::cout << "Is data? " << is_data << std::endl;

    CreateHistograms create_histograms = CreateHistograms(input, output, era, channel);

    create_histograms.defineHistograms();
    create_histograms.setBranchesAddresses();
    if (is_data) {
        create_histograms.fillHistogramsData();
    } else {
        create_histograms.getGenWeightSum();
        create_histograms.getScaleFactor();
        create_histograms.fillHistogramsSimulation();
    }
    create_histograms.saveHistograms();
    return 0;
}
