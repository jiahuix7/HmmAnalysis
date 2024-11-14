
## declare an array variable
declare -a bkg_subset=("Full" "NoDY50")
# declare -a sig_subset=("Full" "NottH" "VBF")
declare -a sig_subset=("NottH" "VBF")
# declare -a eras=("2022" "2022EE" "2022Combined" "2023" "2023BPix" "2023Combined" "Combined")
declare -a eras=("2022" "2022Combined" "2023Combined" "Combined")

## now loop through the above array
for bs in "${bkg_subset[@]}"; do
    for ss in "${sig_subset[@]}"; do
        echo "--------- B ${bs} - S ${ss} ---------"
        for era in "${eras[@]}"; do
            python3 train.py VBF ${era} ${bs} ${ss}

            for type in "signal" "background"; do
                echo "         --- ${era} ${type} ---"
                python3 append_xgboost_discriminator_to_tree.py VBF ${era} ${type} ${bs} ${ss}
            done
        done
    done
done
