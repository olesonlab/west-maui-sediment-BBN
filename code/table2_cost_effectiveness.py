"""Table 2: % of total erosion reduced and cells treated per alternative, from the
'Scenario_results' sheet, plus the derived cost-effectiveness ratio
(% of total erosion reduced per 1,000 cells treated). Writes table2_values.csv.
Cell counts are unique cells: the 319 road-crossing cells fall inside the pig range (see the
note in Scenario_results), so L_P and L_P+R both treat 13,786 cells."""
import csv
from common import sheet_rows, FIGDIR

NEW = {"2_T": "VH_T", "2_P": "VH_P", "2_A": "VH_A", "9_T": "H_T", "9_P": "H_P", "9_A": "H_A"}
rows = sheet_rows("Scenario_results", min_row=4, max_row=15, max_col=12)
out = []
for r in rows:
    alt = NEW.get(r[2], r[2])
    pct = -100 * r[5]
    cells = r[11]
    ratio = pct / cells * 1000 if cells else float("nan")
    if round(pct, 1) == 0:  # F_P changes erosion by +0.02%, reported as 0.0% in Table 2
        ratio = 0.0
    out.append([alt, r[3], round(-pct, 1), cells, round(ratio, 1), r[8], r[9], r[10]])
    print(f"{alt:6s} {-pct:7.1f}%  cells={cells:>6}  per1000={ratio:5.1f}  (pigs={r[8]}, roads={r[9]}, terraces={r[10]})")
with open(FIGDIR.parent / "code" / "table2_values.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["alternative", "description", "pct_total_erosion_change", "cells_treated",
                "pct_reduced_per_1000_cells", "pig_cells", "road_cells", "terrace_cells"])
    w.writerows(out)
print("table2_values.csv written")
