
## How to run
- Add/remove/update dataset list in `submit_analyzer_jobs_LPC.py` using the corresponding `.list` file as the key.
- Run `python3 submit_analyzer_jobs_LPC.py`. This will create an analyzer directory with a subfolder for each dataset in the list.
- Submit a single job by running `condor_submit task.jdl` inside the corresponding dataset directory. Note that the output of step 2 provides a one-line command to send the jobs of a dataset.
- You can also run `bash condor_job_sender.sh` to send the jobs for all of the datasets!

## Considerations
- The `/err/` folder in each dataset directory contains the error output of each job. In principle these files should have info about the missing input files (done on purpose) and missing branches for problematic runs.
- The `/out/` folder contains the output info and have the final tuples path at the end!
