# Ridge-to-reef sediment management under uncertainty: a Bayesian belief network approach

**Oleson Ecological Economics Lab | University of Hawaiʻi at Mānoa**

## Overview

This repository contains data, figures, and supplementary materials for:

> Oleson, K.L.L., Barnes, M.D., Bagstad, K.J., Callender, T., Cerovski-Darriau, C., Falinski, K., Goodell, W., Haynes, M., Stock, J., and Voigt, B. (*under review*). Ridge-to-reef sediment management under uncertainty: a Bayesian belief network approach. *Marine Pollution Bulletin*.

We developed an expert-elicited Bayesian belief network (BBN) model of streambank erosion for the West Maui Priority Coral Reef Conservation Area, Hawaiʻi. The model integrates three parent nodes — fill terrace presence, disturbance (feral pigs and road crossings), and bank susceptibility (shear stress) — to predict bank erosion across 15 subwatersheds (97 km²). We apply the model in a structured decision analysis framework to evaluate 12 management alternatives for reducing sediment delivery to coral reefs.

## Key findings

- 78% of total bank erosion originates from less than 9% of streambank length
- Addressing fill terraces and co-occurring disturbances at high-erosion cells (Alternative H_A) reduces bank erosion by 78% while treating only 9% of stream length
- Road-crossing interventions yield 30% erosion reduction in a small, feasible spatial footprint
- Reductions are large enough to plausibly lower nearshore sediment concentrations below documented coral stress thresholds

## Repository structure

```
west-maui-sediment-BBN/
├── data/
│   └── Results-scenario-landowner-subwatershed.xlsx   # Scenario results, landowner analysis, subwatershed characteristics
├── figures/
│   ├── Figure1_composite.jpg        # Fill terrace field photos
│   ├── Figure2_LandownersMap.tif    # West Maui subwatershed and landowner map
│   ├── Figure3_BBN.png              # Bayesian belief network structure
│   ├── Figure4_2panel.jpg           # Modeled bank erosion and hotspot maps
│   ├── Figure5_subwatershed.jpg     # Erosion reduction by subwatershed
│   ├── Figure6_landowner.pdf        # Erosion by landowner under select alternatives
│   ├── Figure7.png                  # Cumulative benefit curves
│   ├── FigureS1.png                 # Calibration curves
│   ├── FigureS2.png                 # Perennial-intermittent watershed characteristics
│   └── FigureS3.png                 # Ephemeral watershed characteristics
└── docs/
    └── SupplementaryInformation.docx  # Model inputs, CPTs, calibration tables, methods
```

## Model

The BBN was built in [GeNIe 2.0](https://www.bayesfusion.com/) and implemented within the [ARIES](https://aries.integratedmodelling.org) (Artificial Intelligence for Ecosystem Services) modeling platform. The model structure, conditional probability tables, and calibration data are documented in the Supplementary Information.

**Three parent nodes:**
- **FillTerrace** — presence/absence of fill terrace deposits along streambanks (legacy of former pineapple agriculture)
- **DisturbanceType** — feral pig activity, road crossings, multiple disturbances, or undisturbed
- **Susceptibility** — bank susceptibility to erosion based on shear stress (high/moderate/low)

**Output node:**
- **BankErosion** — predicted erosion class (VeryHigh / High / Moderate / Low / VeryLow)

## Study area

West Maui Priority Coral Reef Conservation Area, Maui, Hawaiʻi. 15 subwatersheds, 97 km², spanning perennial-intermittent (northern) and ephemeral (southern) flow regimes. Major landowners: Maui Land & Pine, State of Hawaiʻi (including DHHL), and Kaʻanapali Land Management Corporation.

## Data availability

Spatial input datasets are available from the U.S. Geological Survey ScienceBase repository (Stock and Cerovski-Darriau, 2021) and the Hawaiʻi Division of Aquatic Resources. Model outputs and scenario results are provided in `data/`. Additional data available from the corresponding author upon request.

## Citation

If you use this code or data, please cite:

> Oleson et al. (*under review*). Ridge-to-reef sediment management under uncertainty: a Bayesian belief network approach. *Marine Pollution Bulletin*.

## Contact

**Kirsten L.L. Oleson** | oleson@hawaii.edu  
Oleson Ecological Economics Lab  
Department of Natural Resources and Environmental Management  
University of Hawaiʻi at Mānoa

## License

Data and figures © University of Hawaiʻi. Code and documentation released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
