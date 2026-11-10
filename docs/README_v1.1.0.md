# West Maui sediment BBN – v1.1.0 additions

Version 1.1.0 supports the Environmental Management submission of Oleson et al., "Ridge-to-reef sediment management under uncertainty: a Bayesian belief network approach". It adds the GeNIe model file, the final ARIES model rasters and the code that produces every figure and table in the paper that depends on them. v1.0.0 built Figs. 6, 7 and S1–S3 from an earlier results workbook. The paper now uses the final run throughout.

Copy these folders into the top level of olesonlab/west-maui-sediment-BBN, next to the v1.0.0 `code/`, `data/`, `docs/` and `figures/`.

## Contents

`inputs/`
- `model/ChannelErosionSource.xdsl` – the Bayesian belief network (structure, priors and conditional probability table, Table S2) as saved in GeNIe 2.0.5494. The child node is named MaximumBankErosion in the file and BankErosion in Fig. 3.
- `scenarios/baseline_ken.tif` – baseline bank erosion (tonnes/ha/yr) from the final ARIES run. Geographic grid (EPSG:4326), 10 m stream cells.
- `scenarios/scenario_N.tif` – the 12 alternatives from the same run. 1 L_P, 2 L_R, 3 L_T, 4 L_P+R, 6 F_P, 7 R_200, 8 VH_T, 9 H_T, 10 VH_A, 11 H_A, 12 VH_P, 13 H_P. There is no scenario 5.
- `subwatersheds/subws_WM_final_USGS.*` – subwatershed polygons (UTM 4N). The 15 modeled subwatersheds are New_Number 2, 4, 6, 8, 9, 13, 14, 16, 20, 22, 26, 28, 30, 31, 35.
- `ws_ken.npy` – the polygons rasterized onto the model grid (`scripts/make_ws_index.py` rebuilds it).
- `land_tenure/LandTenure.*` – major landowner polygons used for Figs. 2, 6 and 7. Parcel attributes other than MajorOwner (TMK, assessed values, exemptions) were removed before archiving.
- `maui_outline.geojson` – Maui coastline for the Fig. 2 inset (US Census Bureau 2023 cartographic boundary file, cb_2023_us_county_500k).
- `Subwatershed-characteristics.xlsx` – area, precipitation and susceptibility by subwatershed. Susceptibility was computed on the 10 m DEM stream network used to set the priors, not on the NHDPlus network of the final run.

`scripts/`
- `make_ws_index.py` – subwatershed index raster.
- `table_s3_final_run.py` – final-run erosion by subwatershed (Table S3, 907.8 tonnes/yr, 1.5% below the USGS budget) and the hotspot shares (very high 5% of cells and 20% of erosion; high and very high 22% and 78%).
- `fig2_map.py` – Fig. 2, study area, subwatersheds and land tenure (PDF, EPS, 1200 dpi TIFF).
- `fig3_bbn.py` – Fig. 3, the network redrawn from the model file (PDF, EPS, 1200 dpi TIFF). Arrow widths scale with each parent's average Euclidean influence on the child (FillTerrace 1.11, DisturbanceType 0.26, Susceptibility 0.16). Uses Liberation Sans (metric-compatible with Arial).
- `fig4_final.py` – Fig. 4, baseline erosion and hotspots.
- `fig7_nhdplus.py` – Fig. 7, cumulative benefit curves for the study area, State and MLP lands.
- `final_tables_figs.py` – Fig. 5 (reduction by subwatershed), Fig. 6 (erosion by landowner), Figs. S2–S3 (erosion vs. subwatershed characteristics) and Tables S5–S6.
- `figS1_final.py` – Fig. S1, BBN vs. USGS for the validation subwatersheds (R² 0.92 ephemeral, 0.77 perennial-intermittent).
- `hotspot_trace.py` – diagnostic trace of the high and very-high treatment sets (paths point to the original data folders).

`outputs/`
- `table2_recount.csv` – cell-level action counts and cost-effectiveness ratios for Table 2.
- `Fig7_values.csv` – the Fig. 7 points.
- `Fig6_landowner.csv` – erosion by landowner group (tonnes/yr). Baseline 907.8: Maui Land & Pine 633.0, State and DHHL 76.6, Kāʻanapali Land Management Corp. 78.4, other 119.8.
- `FigS2_S3_r2.csv` – R² values for Figs. S2 and S3.
- `TableS5_subwatershed_characteristics.csv`, `TableS6_reduction_by_subwatershed.csv`.

`figures/` – the final Figs. 4–7 and S1–S3 as submitted.

## Methods notes
- Cell area (about 0.0093 ha) is computed per raster row on the WGS84 ellipsoid. Stream lengths in the paper are cell counts × 10 m (19,222 cells = 192 km). The NHDPlus flowline length is 168 km.
- Cell counts in Table S5 come from the scenario rasters. Fill terrace cells are those changed by L_T (7,193). Pig disturbance cells are those changed by L_P (17,592), and pig disturbance only cells exclude the 522 that are also road crossings (17,070). Road crossing and multiple disturbance cells are those changed by L_R (527).
- Table S6 gives each subwatershed's reduction as a share of its own baseline. Its percentages use per-cell ellipsoidal areas, so whole-study-area values can differ from Table 2 by up to 0.3 percentage points. Table 2 is the reference for study-area totals.

## Reproduce
```
pip install -r requirements.txt
bash run_all.sh
```
Outputs go to `regenerated/` and match `outputs/` and `figures/` (`Fig7_final.csv` there is `Fig7_values.csv` here).

## How to publish
1. Copy `inputs/`, `scripts/`, `outputs/`, `figures/`, `run_all.sh`, `requirements.txt` and this README (as `docs/README_v1.1.0.md`, or merged into the top-level README) into the GitHub repo, and replace `.zenodo.json` with the one here.
2. Commit, push and create GitHub release `v1.1.0`. The Zenodo–GitHub integration mints a new version under concept DOI 10.5281/zenodo.23428358.
3. The manuscript and cover letter cite the concept DOI, so no text change is needed after release.
