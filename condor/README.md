
## How to run
- Add/remove/update dataset list in `create_analyzer_jobs_LPC.py` using the corresponding `.list` file as the key.
- Run `python3 create_analyzer_jobs_LPC.py`. This will create an analyzer directory with a subfolder for each dataset in the list.
- To submit a single job, run `condor_submit task.jdl` inside the corresponding dataset directory. Note that the output of step 2 provides a one-line command to do this!
- You can also run `bash condor_job_sender.sh` to send the jobs for all of the new datasets!
- Once all jobs have finished, you might want to add the created tuples in order to compute the total SumGenWeight. To do so, run `python3 condor_job_hadd.py`. This will send a job that does hadd over all datasets listed in `condor_job_sender.sh`. You can also hardcode the datasets you want to hadd inside the `condor_job_hadd.py` macro. Note that this hadd includes the extended runs (i.e. those with the suffix `_ext1`) to the dataset.

## Considerations
- The `/err/` folder in each dataset directory contains the error output of each job. By construction, these files should have info about the missing input files (done on purpose) and, in some cases, missing branches from problematic runs. Any other message might be indication of an error.
- The `/out/` folder contains the output info and have the final tuples path at the end!
