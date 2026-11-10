#!/usr/bin/env bash
# Regenerate the v1.1.0 figures and tables from the final ARIES rasters.
# Run from the top of the v1.1.0 folder: bash run_all.sh
set -euo pipefail
I=inputs; S=$I/scenarios; O=regenerated; mkdir -p $O figS1
python3 scripts/make_ws_index.py $I/subwatersheds/subws_WM_final_USGS.shp $S/baseline_ken.tif $O/ws_index.npy
python3 scripts/table_s3_final_run.py $S/baseline_ken.tif $O/ws_index.npy > $O/table_s3_final_run.txt
python3 scripts/fig2_map.py $I/subwatersheds/subws_WM_final_USGS.shp $I/land_tenure/LandTenure.shp $I/maui_outline.geojson $O/Fig2
python3 scripts/fig3_bbn.py $I/model/ChannelErosionSource.xdsl $O/Fig3
python3 scripts/fig4_final.py $S/baseline_ken.tif $O/ws_index.npy $I/subwatersheds/subws_WM_final_USGS.shp $O/Fig4_final
python3 scripts/fig7_nhdplus.py $S/baseline_ken.tif $O/ws_index.npy $I/land_tenure/LandTenure.shp $O/Fig7_final
python3 scripts/final_tables_figs.py $S $O/ws_index.npy $I/land_tenure/LandTenure.shp $I/Subwatershed-characteristics.xlsx $O
python3 scripts/figS1_final.py && mv figS1/* $O/ && rmdir figS1
echo "Outputs in $O/"
