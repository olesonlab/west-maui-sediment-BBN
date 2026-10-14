"""Table 2: % of total erosion reduced and cells treated per alternative, plus the derived
cost-effectiveness ratio (% of total erosion reduced per 1,000 cells treated).
Source: 'Scenario_results' sheet. Writes table2_values.csv.

Cell-count logic (differs from three spreadsheet formulas; see notes below):
- The disturbance node is exclusive: 13,786 cells are 'pig disturbance alone' (Table S5) and
  319 cells are 'road crossings/multiple disturbances'. The sheet's note says the 319 road-crossing
  cells also intersect pig cells, so pigs are present in 13,786 + 319 = 14,105 cells.
  L_P (eliminate all pigs) and L_P+R therefore both treat 14,105 cells. (The sheet hard-codes
  13,786, the pigs-alone class, in I4 and reuses it in I7.)
- F_P treats the 633 pig cells in fenced areas. The sheet's total for F_P (L8) subtracts 319
  road cells that F_P does not treat; that subtraction is not applied here.
- VH_A and H_A totals are taken from the sheet unchanged. Their formulas add the road cells twice
  (pigs column = VH_P/H_P pigs + road cells, then pigs + roads + terraces), and terrace and
  disturbance actions on the same cell are counted separately. Flagged for author review.
"""
import csv
from common import sheet_rows, FIGDIR

NEW = {"2_T": "VH_T", "2_P": "VH_P", "2_A": "VH_A", "9_T": "H_T", "9_P": "H_P", "9_A": "H_A"}
rows = {r[2]: r for r in sheet_rows("Scenario_results", min_row=4, max_row=15, max_col=12)}
road_cells = rows["L_R"][9]                     # 319
pig_present = rows["L_P"][8] + road_cells       # 13,786 pigs-alone + 319 multiple = 14,105
CELLS = {"L_P": pig_present, "L_P+R": pig_present, "F_P": rows["F_P"][8]}

out = []
for key, r in rows.items():
    alt = NEW.get(key, key)
    pct = 100 * r[5]                       # % change in total erosion (negative = reduction)
    cells = CELLS.get(alt, r[11])
    ratio = 0.0 if round(pct, 1) == 0 else -pct / cells * 1000
    flag = "check: road cells counted twice in sheet total" if alt in ("VH_A", "H_A") else ""
    out.append([alt, r[3], round(pct, 1), cells, round(ratio, 1), flag])
    print(f"{alt:6s} {pct:7.1f}%  cells={cells:>6}  per1000={ratio:5.1f}  {flag}")
with open(FIGDIR.parent / "code" / "table2_values.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["alternative", "description", "pct_total_erosion_change", "cells_treated",
                "pct_reduced_per_1000_cells", "note"])
    w.writerows(out)
print("table2_values.csv written")
