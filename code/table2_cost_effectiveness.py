"""Table 2: % of total erosion reduced and cost (number of cell-level actions) per alternative,
plus the derived cost-effectiveness ratio (% of total erosion reduced per 1,000 actions).
Source: 'Scenario_results' sheet. Writes table2_values.csv.

Cost counts cell-level actions: combined alternatives count each action separately, so a cell
where both a fill terrace and a disturbance are treated counts twice (sheet columns I-K summed).
Three counts differ from the sheet's 'Total' column:
- The disturbance node is exclusive: 13,786 cells are 'pig disturbance alone' (Table S5) and
  319 cells are 'road crossings/multiple disturbances'. The sheet's note says the 319 road-crossing
  cells also intersect pig cells, so pigs are present in 13,786 + 319 = 14,105 cells.
  L_P removes pigs from 14,105 cells; L_P+R removes pigs from the same 14,105 cells and fixes
  319 road crossings (14,424 actions). The sheet hard-codes 13,786 (pigs alone) and subtracts
  the road cells for L_P+R.
- F_P removes pigs from the 633 pig cells in fenced areas. The sheet's total for F_P subtracts
  319 road cells that F_P does not treat.
"""
import csv
from common import sheet_rows, FIGDIR

NEW = {"2_T": "VH_T", "2_P": "VH_P", "2_A": "VH_A", "9_T": "H_T", "9_P": "H_P", "9_A": "H_A"}
rows = {r[2]: r for r in sheet_rows("Scenario_results", min_row=4, max_row=15, max_col=12)}
road_cells = rows["L_R"][9]                     # 319
pig_present = rows["L_P"][8] + road_cells       # 13,786 pigs-alone + 319 multiple = 14,105
CELLS = {"L_P": pig_present, "L_P+R": pig_present + road_cells, "F_P": rows["F_P"][8]}

out = []
for key, r in rows.items():
    alt = NEW.get(key, key)
    pct = 100 * r[5]                       # % change in total erosion (negative = reduction)
    cells = CELLS.get(alt, r[11])
    ratio = 0.0 if round(pct, 1) == 0 else -pct / cells * 1000
    out.append([alt, r[3], round(pct, 1), cells, round(ratio, 1)])
    print(f"{alt:6s} {pct:7.1f}%  actions={cells:>6}  per1000={ratio:5.1f}")
with open(FIGDIR.parent / "code" / "table2_values.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["alternative", "description", "pct_total_erosion_change", "cell_level_actions",
                "pct_reduced_per_1000_actions"])
    w.writerows(out)
print("table2_values.csv written")
