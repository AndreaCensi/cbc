#!/bin/bash
set -e
set -x
# python resize_calibration.py
python tc_0_prepare_data_dirs.py
python tc_1_join_signals.py
python tc_2_compute_stats.py
