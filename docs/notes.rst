

Preparing the paper figures
---------------------------

Needs fly.pickle and sick.pickle.


    cbc_main --data_sick cbc_submission_data/sick.pickle \
             --data_fly  cbc_submission_data/fly.pickle \
             --set 'paper*' --fast \
             --outdir cbc_main_output 