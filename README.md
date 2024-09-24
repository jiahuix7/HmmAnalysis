This code is based in the Run2 Anaylis https://github.com/irenedutta23/HmmAna

## Setup

```
cmsrel CMSSW_14_0_14
cd CMSSW_14_0_14/src
git clone git@github.com:MatBarria/HmmAnalysis.git
cd HmmAnalysis
```

## Run the analysis 
For simulations
```
./bin/HmmAnalyzer runList.txt out.root mc F 2016
```

For data
```
./bin/HmmAnalyzer runList.txt out.root data T 2016
```


