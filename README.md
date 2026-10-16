# Ridge-to-reef sediment management under uncertainty: a Bayesian belief network approach

**Oleson Lab | University of Hawaiʻi at Mānoa**

## Overview

This repository contains data, code, figures, and supplementary materials for:

> Oleson, K.L.L., Barnes, M.D., Bagstad, K.J., Callender, T., Cerovski-Darriau, C., Falinski, K., Goodell, W., Hilleary, M., Stock, J., Voigt, B., and Ancona, Z.H. (*under review*). Ridge-to-reef sediment management under uncertainty: a Bayesian belief network approach. *Marine Pollution Bulletin*.

We developed an expert-elicited Bayesian belief network (BBN) model of streambank erosion for the West Maui Priority Coral Reef Conservation Area, Hawaiʻi. The model integrates three parent nodes (fill terrace presence, disturbance from feral pigs and road crossings, and bank susceptibility as shear stress) to predict bank erosion across 15 subwatersheds (97 km²). We apply the model in a structured decision analysis framework to evaluate 12 management alternatives for reducing sediment delivery to coral reefs.

## Key findings

- 78% of total bank erosion originates from less than 9% of streambank length.
- Addressing fill terraces and co-occurring disturbances at high-erosion cells (Alternative H_A) reduces bank erosion by 78% while treating only 9% of stream length.
- Fixing fill terraces within 200 m of road crossings (Alternative R_200) reduces bank erosion by 30% in a small, feasible footprint. Pig and road-crossing actions alone reduce it by less than 6%.
- Reductions are large enough to plausibly lower nearshore sediment concentrations below documented coral stress thresholds.

## Repository structure

```
west-maui-sediment-BBN/
├── code/                 # Reproducible scripts for Figure 7, Figures S1-S3 and Table 2 values
│   ├── run_all.sh
│   ├── common.py
│   ├── fig7_cumulative_benefit.py
│   ├── figS1_calibration.py
│   ├── figS2_S3_watershed_characteristics.py
│   ├── table2_cost_effectiveness.py
│   ├── table2_values.csv  # output of table2_cost_effectiveness.py
│   └── requirements.txt
├── data/
│   └── Results-scenario-landowner-subwatershed.xlsx   # Scenario results, landowner analysis, subwatershed characteristics
├── figures/              # All manuscript and supplementary figures
└── docs/
    └── SupplementaryInformation.docx                  # Model inputs, CPTs, calibration tables, methods
```

## Reproducing the figures

Figures 6 and 7, Figures S1-S3 and the cost-effectiveness values in Table 2 are generated directly from `data/Results-scenario-landowner-subwatershed.xlsx`:

```bash
pip install -r code/requirements.txt
Rscript -e 'install.packages(c("ggplot2", "readxl"))'
bash code/run_all.sh
```

Outputs are written to `figures/`, `code/table2_values.csv` and `code/fig6_values.csv`. Tested with Python 3.13 (matplotlib 3.11, numpy 2.5) and Python 3.10 (matplotlib 3.10, numpy 2.2), openpyxl 3.1; outputs are identical. Figure 6 tested with R 4.3, ggplot2 3.4 and readxl 1.4.

| Output | Script | Workbook source |
|---|---|---|
| Figure 6 | `fig6_landowner.R` | `Landowner_analysis`, rows 4, 11, 12, 14, 15, 17 (R_200 uses the "(ORIGINAL)" row) |
| Figure 7 | `fig7_cumulative_benefit.py` | `baseline_values`, columns E-K, rows 3-14 |
| Figure S1 | `figS1_calibration.py` | `Subwatershed characteristics` (validation subwatersheds) |
| Figures S2, S3 | `figS2_S3_watershed_characteristics.py` | `Subwatershed characteristics` |
| Table 2 ratios | `table2_cost_effectiveness.py` | `Scenario_results` |

Figures 1-5 were produced outside this code base: field photographs (Figure 1), ArcGIS (Figures 2 and 4), GeNIe 2.0 (Figure 3), and R/ggplot2 (Figure 5). `fig6_landowner.R` is adapted from W. Goodell's original ggplot2 script; it now computes the per-landowner percentages that were previously added to the exported figure by hand. The BBN itself runs in ARIES (see Model below).

### Use of AI-assisted tools

The plotting and regression code in `code/` (including the Figure 6 adaptation) was drafted with Claude (Anthropic) and checked by the authors against the source workbook. This use is disclosed in the manuscript's Methods and AI declaration, following Elsevier's generative AI policy for journals.

## Model

The BBN was built in [GeNIe 2.0](https://www.bayesfusion.com/) and implemented within the [ARIES](https://aries.integratedmodelling.org) (Artificial Intelligence for Environment and Sustainability) modeling platform. The model structure, conditional probability tables, and calibration data are documented in the Supplementary Information. Model code: https://bitbucket.org/integratedmodelling/org.aries.oc/src/master/ (requires k.LAB 0.9.11).

**Three parent nodes:**
- **FillTerrace**: presence/absence of fill terrace deposits along streambanks (legacy of former pineapple agriculture)
- **DisturbanceType**: feral pig activity, road crossings, multiple disturbances, or undisturbed
- **Susceptibility**: bank susceptibility to erosion based on shear stress (high/moderate/low)

**Output node:**
- **BankErosion**: predicted erosion class (VeryHigh / High / Moderate / Low / VeryLow)

## Study area

West Maui Priority Coral Reef Conservation Area, Maui, Hawaiʻi. 15 subwatersheds, 97 km², spanning perennial-intermittent (northern) and ephemeral (southern) flow regimes. Major landowners: Maui Land & Pine, State of Hawaiʻi (including DHHL), and Kāʻanapali Land Management Corporation.

## Data availability

Spatial input datasets are available from the U.S. Geological Survey ScienceBase repository (Stock and Cerovski-Darriau, 2021) and the Hawaiʻi Division of Aquatic Resources. Model outputs and scenario results are provided in `data/`. Additional data are available from the corresponding author on request.

## Citation

If you use this code or data, please cite:

> Oleson et al. (*under review*). Ridge-to-reef sediment management under uncertainty: a Bayesian belief network approach. *Marine Pollution Bulletin*.

## Contact

**Kirsten L. L. Oleson** | koleson@hawaii.edu  
Oleson Lab  
Department of Natural Resources and Environmental Management  
University of Hawaiʻi at Mānoa

## License

Data and figures © University of Hawaiʻi. Code and documentation released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
