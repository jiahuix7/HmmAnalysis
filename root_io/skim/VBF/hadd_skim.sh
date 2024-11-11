
mkdir -p merged
##############  2022  ##############
hadd merged/background_2022_skimFull.root DY50to120_2022_skim.root DY120to200_2022_skim.root EWK_2L2J_2022_skim.root TTto2L2Nu_2022_skim.root TTtoLNu2Q_2022_skim.root TWminusto2L2Nu_2022_skim.root WZto2L2Q_2022_skim.root WZto3LNu_2022_skim.root WZtoLNu2Q_2022_skim.root ZZto2L2Nu_2022_skim.root ZZto2L2Q_2022_skim.root ZZto4L_2022_skim.root WWto2L2Nu_2022_skim.root WWtoLNu2Q_2022_skim.root
hadd merged/background_2022_skim2L.root DY50to120_2022_skim.root DY120to200_2022_skim.root EWK_2L2J_2022_skim.root TTto2L2Nu_2022_skim.root TTtoLNu2Q_2022_skim.root TWminusto2L2Nu_2022_skim.root WZto2L2Q_2022_skim.root WZto3LNu_2022_skim.root ZZto2L2Nu_2022_skim.root ZZto2L2Q_2022_skim.root ZZto4L_2022_skim.root WWto2L2Nu_2022_skim.root
hadd merged/background_2022_skimNoDY50.root DY120to200_2022_skim.root EWK_2L2J_2022_skim.root TTto2L2Nu_2022_skim.root TTtoLNu2Q_2022_skim.root TWminusto2L2Nu_2022_skim.root WZto2L2Q_2022_skim.root WZto3LNu_2022_skim.root ZZto2L2Nu_2022_skim.root ZZto2L2Q_2022_skim.root ZZto4L_2022_skim.root WWto2L2Nu_2022_skim.root

hadd merged/signal_2022_skimFull.root ggH_2022_skim.root  VBF_2022_skim.root ttH_2022_skim.root
hadd merged/signal_2022_skimNottH.root ggH_2022_skim.root  VBF_2022_skim.root
hadd merged/signal_2022_skimVBF.root VBF_2022_skim.root

##############  2022EE  ##############
hadd merged/background_2022EE_skimFull.root DY50to120_2022EE_skim.root DY120to200_2022EE_skim.root EWK_2L2J_2022EE_skim.root TTto2L2Nu_2022EE_skim.root TTtoLNu2Q_2022EE_skim.root WZto2L2Q_2022EE_skim.root WZto3LNu_2022EE_skim.root WZtoLNu2Q_2022EE_skim.root ZZto2L2Nu_2022EE_skim.root ZZto2L2Q_2022EE_skim.root ZZto4L_2022EE_skim.root WWto2L2Nu_2022EE_skim.root WWtoLNu2Q_2022EE_skim.root
hadd merged/background_2022EE_skim2L.root DY50to120_2022EE_skim.root DY120to200_2022EE_skim.root EWK_2L2J_2022EE_skim.root TTto2L2Nu_2022EE_skim.root TTtoLNu2Q_2022EE_skim.root WZto2L2Q_2022EE_skim.root WZto3LNu_2022EE_skim.root ZZto2L2Nu_2022EE_skim.root ZZto2L2Q_2022EE_skim.root ZZto4L_2022EE_skim.root WWto2L2Nu_2022EE_skim.root
hadd merged/background_2022EE_skimNoDY50.root DY120to200_2022EE_skim.root EWK_2L2J_2022EE_skim.root TTto2L2Nu_2022EE_skim.root TTtoLNu2Q_2022EE_skim.root WZto2L2Q_2022EE_skim.root WZto3LNu_2022EE_skim.root ZZto2L2Nu_2022EE_skim.root ZZto2L2Q_2022EE_skim.root ZZto4L_2022EE_skim.root WWto2L2Nu_2022EE_skim.root

hadd merged/signal_2022EE_skimFull.root ggH_2022EE_skim.root VBF_2022EE_skim.root ttH_2022EE_skim.root
hadd merged/signal_2022EE_skimNottH.root ggH_2022EE_skim.root VBF_2022EE_skim.root
hadd merged/signal_2022EE_skimVBF.root VBF_2022EE_skim.root

##############  2022Combined  ##############
hadd merged/background_2022Combined_skimFull.root merged/background_2022_skimFull.root merged/background_2022EE_skimFull.root
hadd merged/background_2022Combined_skim2L.root merged/background_2022_skim2L.root merged/background_2022EE_skim2L.root
hadd merged/background_2022Combined_skimNoDY50.root merged/background_2022_skimNoDY50.root merged/background_2022EE_skimNoDY50.root

hadd merged/signal_2022Combined_skimFull.root merged/signal_2022_skimFull.root merged/signal_2022EE_skimFull.root
hadd merged/signal_2022Combined_skimNottH.root merged/signal_2022_skimNottH.root merged/signal_2022EE_skimNottH.root
hadd merged/signal_2022Combined_skimVBF.root merged/signal_2022_skimVBF.root merged/signal_2022EE_skimVBF.root

##############  2023  ##############
hadd merged/background_2023_skimFull.root DY50to120_2023_skim.root DY120to200_2023_skim.root EWK_2L2J_2023_skim.root TTto2L2Nu_2023_skim.root TTtoLNu2Q_2023_skim.root WZto2L2Q_2023_skim.root WZto3LNu_2023_skim.root WZtoLNu2Q_2023_skim.root ZZto2L2Nu_2023_skim.root ZZto2L2Q_2023_skim.root ZZto4L_2023_skim.root WWto2L2Nu_2023_skim.root WWtoLNu2Q_2023_skim.root
hadd merged/background_2023_skim2L.root DY50to120_2023_skim.root DY120to200_2023_skim.root EWK_2L2J_2023_skim.root TTto2L2Nu_2023_skim.root TTtoLNu2Q_2023_skim.root WZto2L2Q_2023_skim.root WZto3LNu_2023_skim.root ZZto2L2Nu_2023_skim.root ZZto2L2Q_2023_skim.root ZZto4L_2023_skim.root WWto2L2Nu_2023_skim.root
hadd merged/background_2023_skimNoDY50.root DY120to200_2023_skim.root EWK_2L2J_2023_skim.root TTto2L2Nu_2023_skim.root TTtoLNu2Q_2023_skim.root WZto2L2Q_2023_skim.root WZto3LNu_2023_skim.root ZZto2L2Nu_2023_skim.root ZZto2L2Q_2023_skim.root ZZto4L_2023_skim.root WWto2L2Nu_2023_skim.root

hadd merged/signal_2023_skimFull.root ggH_2023_skim.root VBF_2023_skim.root ttH_2023_skim.root
hadd merged/signal_2023_skimNottH.root ggH_2023_skim.root VBF_2023_skim.root
hadd merged/signal_2023_skimVBF.root VBF_2023_skim.root

##############  2023BPix  ##############
hadd merged/background_2023BPix_skimFull.root DY50to120_2023BPix_skim.root DY120to200_2023BPix_skim.root EWK_2L2J_2023BPix_skim.root TTto2L2Nu_2023BPix_skim.root TTtoLNu2Q_2023BPix_skim.root WZto2L2Q_2023BPix_skim.root WZto3LNu_2023BPix_skim.root WZtoLNu2Q_2023BPix_skim.root ZZto2L2Nu_2023BPix_skim.root ZZto2L2Q_2023BPix_skim.root ZZto4L_2023BPix_skim.root WWto2L2Nu_2023BPix_skim.root WWtoLNu2Q_2023BPix_skim.root
hadd merged/background_2023BPix_skim2L.root DY50to120_2023BPix_skim.root DY120to200_2023BPix_skim.root EWK_2L2J_2023BPix_skim.root TTto2L2Nu_2023BPix_skim.root TTtoLNu2Q_2023BPix_skim.root WZto2L2Q_2023BPix_skim.root WZto3LNu_2023BPix_skim.root ZZto2L2Nu_2023BPix_skim.root ZZto2L2Q_2023BPix_skim.root ZZto4L_2023BPix_skim.root WWto2L2Nu_2023BPix_skim.root
hadd merged/background_2023BPix_skimNoDY50.root DY120to200_2023BPix_skim.root EWK_2L2J_2023BPix_skim.root TTto2L2Nu_2023BPix_skim.root TTtoLNu2Q_2023BPix_skim.root WZto2L2Q_2023BPix_skim.root WZto3LNu_2023BPix_skim.root ZZto2L2Nu_2023BPix_skim.root ZZto2L2Q_2023BPix_skim.root ZZto4L_2023BPix_skim.root WWto2L2Nu_2023BPix_skim.root

hadd merged/signal_2023BPix_skimFull.root ggH_2023BPix_skim.root VBF_2023BPix_skim.root ttH_2023BPix_skim.root
hadd merged/signal_2023BPix_skimNottH.root ggH_2023BPix_skim.root VBF_2023BPix_skim.root
hadd merged/signal_2023BPix_skimVBF.root VBF_2023BPix_skim.root

##############  2023Combined  ##############
hadd merged/background_2023Combined_skimFull.root merged/background_2023_skimFull.root merged/background_2023BPix_skimFull.root
hadd merged/background_2023Combined_skim2L.root merged/background_2023_skim2L.root merged/background_2023BPix_skim2L.root
hadd merged/background_2023Combined_skimNoDY50.root merged/background_2023_skimNoDY50.root merged/background_2023BPix_skimNoDY50.root

hadd merged/signal_2023Combined_skimFull.root merged/signal_2023_skimFull.root merged/signal_2023BPix_skimFull.root
hadd merged/signal_2023Combined_skimNottH.root merged/signal_2023_skimNottH.root merged/signal_2023BPix_skimNottH.root
hadd merged/signal_2023Combined_skimVBF.root merged/signal_2023_skimVBF.root merged/signal_2023BPix_skimVBF.root

##############  Combined  ##############
hadd merged/background_Combined_skimFull.root merged/background_2022Combined_skimFull.root merged/background_2023Combined_skimFull.root
hadd merged/background_Combined_skim2L.root merged/background_2022Combined_skim2L.root merged/background_2023Combined_skim2L.root
hadd merged/background_Combined_skimNoDY50.root merged/background_2022Combined_skimNoDY50.root merged/background_2023Combined_skimNoDY50.root

hadd merged/signal_Combined_skimFull.root merged/signal_2022Combined_skimFull.root merged/signal_2023Combined_skimFull.root
hadd merged/signal_Combined_skimNottH.root merged/signal_2022Combined_skimNottH.root merged/signal_2023Combined_skimNottH.root
hadd merged/signal_Combined_skimVBF.root merged/signal_2022Combined_skimVBF.root merged/signal_2023Combined_skimVBF.root
