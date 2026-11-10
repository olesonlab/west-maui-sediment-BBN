"""Table 2: percent of total erosion reduced, cost (cell-level actions) and cost-effectiveness
for the 12 alternatives, from the final ARIES rasters.

Usage: table2_final.py SCEN_DIR ws_index.npy ZONAL_DIR OUT_CSV
SCEN_DIR holds baseline_ken.tif and scenario_*.tif (final run on the NHDPlus network, EPSG:4326).
ZONAL_DIR holds the ArcGIS zonal summaries (baseline_watershed.txt, scenarioN_watershed.txt) for the
15 study subwatersheds.

Actions. A cell counts as a fill-terrace, pig or road-crossing cell when L_T (scenario 3), L_P
(scenario 1) or L_R (scenario 2) changes its value. Each alternative treats those cells inside its
own footprint:
- L_* treat every cell of their type. L_P+R treats all pig and all road cells.
- F_P treats the pig cells it changes (pigs inside fenced areas).
- R_200 treats the fill-terrace and road cells it changes (within 200 m of a road crossing).
- VH_* treat cells with baseline erosion > 19.3 t/ha/yr (the lowest value in the very high class
  is 19.31). H_* treat cells with baseline erosion >= 16.78 t/ha/yr.
- *_A alternatives treat fill terraces, pigs and road crossings, so a cell with two treated inputs
  counts twice.
Cost is the sum of the three action counts.

Percent reduced. Zonal sums are converted to tonnes/yr as SUM x 0.01 ha (the nominal cell area
used in the results workbook), which gives a baseline of 882.7 tonnes/yr over the 15 zones.
- pct_reduced_zonal = 100 x (1 - scenario total / 882.7), with both totals from the zonal summaries.
  These are the Table 2 values. (The v1.0.0 results workbook divided by a typed baseline of 882.3,
  which put L_P, VH_T, H_P and H_A 0.1 point lower.)
- pct_reduced_native recomputes the reduction on native cells (area-weighted, same 15
  subwatersheds), because ArcGIS resampled the rasters to slightly larger cells. It agrees with
  pct_reduced_zonal within 0.3 percentage points.
pct_reduced_per_1000_actions = pct_reduced_zonal (rounded to 0.1) / cost x 1000 (the Table 2 column).

untreated_cells_changed counts cells that F_P changes although no input is treated there. The same
205 cells (value set to zero in the ARIES run) appear in every alternative that uses a spatial
footprint. They are reported, not counted as actions.
"""
import sys, os, csv, numpy as np, rasterio
from pyproj import Geod

sd, wsf, zd, out = sys.argv[1:5]
SC = [("L_P", 1), ("L_R", 2), ("L_T", 3), ("L_P+R", 4), ("F_P", 6), ("R_200", 7), ("VH_T", 8), ("VH_P", 12),
      ("VH_A", 10), ("H_T", 9), ("H_P", 13), ("H_A", 11)]
STUDY_WS = [2, 4, 6, 8, 9, 13, 14, 16, 20, 22, 26, 28, 30, 31, 33, 35]   # 31 + 33 = Kaanapali-Kahua


def rd(f):
    with rasterio.open(os.path.join(sd, f)) as r:
        a = r.read(1).astype(float); a[~(a > -1e30)] = np.nan; return a, r


b, ref = rd("baseline_ken.tif")
g = Geod(ellps="WGS84")
lat = ref.transform[5] + (np.arange(ref.shape[0]) + 0.5) * ref.transform[4]
dx = np.array([g.inv(0, la, ref.res[0], la)[2] for la in lat])
dy = np.array([g.inv(0, la - ref.res[1] / 2, 0, la + ref.res[1] / 2)[2] for la in lat])
A = (dx * dy)[:, None] * np.ones(ref.shape[1]) / 1e4
study = (b > 0) & np.isin(np.load(wsf), STUDY_WS)
bb = np.where(study, b, np.nan)
S = {n: np.where(study, rd(f"scenario_{k}.tif")[0], np.nan) for n, k in SC}
ch = {n: study & (np.abs(S[n] - bb) > 1e-6) for n in S}
T, P, R = ch["L_T"], ch["L_P"], ch["L_R"]
ART = ch["F_P"] & ~T & ~P & ~R
VH, H = study & (b > 19.3), study & (b >= 16.78)

acts = {"L_P": (0, P, 0), "L_R": (0, 0, R), "L_T": (T, 0, 0), "L_P+R": (0, P, R),
        "F_P": (0, ch["F_P"] & P, 0), "R_200": (ch["R_200"] & T, 0, ch["R_200"] & R)}
for pre, m in (("VH", VH), ("H", H)):
    acts[pre + "_T"] = (m & T, 0, 0)
    acts[pre + "_P"] = (0, m & P, 0)
    acts[pre + "_A"] = (m & T, m & P, m & R)


def zsum(f):
    with open(os.path.join(zd, f), newline="") as fh:
        rows = list(csv.DictReader(fh))
    assert len(rows) == 15, (f, len(rows))
    return sum(float(r["SUM"].replace(",", "")) for r in rows)


Z0 = zsum("baseline_watershed.txt") / 100       # tonnes/yr, 882.7
E0 = np.nansum(bb * A)
hdr = ["alternative", "fill_terrace_actions", "pig_actions", "road_actions", "cost_cell_level_actions",
       "untreated_cells_changed", "pct_reduced_zonal", "pct_reduced_native",
       "pct_reduced_per_1000_actions"]
rows = []
for n, k in SC:
    t, p, r = [int(np.sum(x)) for x in acts[n]]
    cost = t + p + r
    zs = zsum(f"scenario{k}_watershed.txt") / 100
    pz = 100 * (1 - zs / Z0)
    pn = 100 * (1 - np.nansum(S[n] * A) / E0)
    per = lambda x: round(x, 1) / cost * 1000 if cost and round(x, 1) > 0 else 0.0
    f1 = lambda x: f"{x:.1f}".replace("-0.0", "0.0")   # F_P changes total erosion by < 0.05%
    rows.append([n, t, p, r, cost, int((ch[n] & ART).sum()), f1(pz), f1(pn), f"{per(pz):.1f}"])
    print(f"{n:6s} actions {cost:6d}  zonal {pz:5.1f}%  native {pn:5.1f}%")
with open(out, "w", newline="") as f:
    w = csv.writer(f); w.writerow(hdr); w.writerows(rows)
