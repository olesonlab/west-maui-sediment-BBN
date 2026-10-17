#!/usr/bin/env bash
# Regenerate Figures 6 and 7, Figures S1-S3 and the Table 2 values from data/.
# Figure 6 needs R with ggplot2 and readxl.
set -e
cd "$(dirname "$0")"
python fig7_cumulative_benefit.py
python figS1_calibration.py
python figS2_S3_watershed_characteristics.py
python table2_cost_effectiveness.py
python graphical_abstract.py
Rscript fig6_landowner.R
