"""Final-run subwatershed, landowner and scenario summaries (Table S5, Table S6, Figs. 5, 6, S2, S3).

Usage: final_tables_figs.py SCEN_DIR ws_ken.npy LandTenure.shp Subwatershed-characteristics.xlsx OUT_DIR
SCEN_DIR holds baseline_ken.tif and scenario_*.tif (final run on the NHDPlus network, EPSG:4326).
Cell areas are computed on the WGS84 ellipsoid (about 0.0093 ha); erosion = value (t/ha/yr) x area.
Cell counts per input come from the scenario rasters: a fill-terrace cell is one changed by L_T
(scenario_3), a pig cell one changed by L_P (scenario_1), a road-crossing cell one changed by L_R
(scenario_2). Pig-only = pig cells minus road-crossing cells. Watershed area, precipitation and mean
susceptibility (shear stress on the 10 m DEM network) are watershed properties carried over from
Subwatershed-characteristics.xlsx.
"""
import sys, os, csv, numpy as np, rasterio, shapefile, openpyxl
from pyproj import Geod, Transformer, CRS
from rasterio.features import rasterize
from shapely.geometry import shape, mapping
from shapely.ops import transform
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import journal_style as js
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt, matplotlib.ticker as mt

sd, wsf, ten, xlsx, out = sys.argv[1:6]; os.makedirs(out, exist_ok=True)
def rd(f):
    with rasterio.open(os.path.join(sd, f)) as r:
        a = r.read(1).astype(float); a[~(a > -1e30)] = np.nan; return a, r
b, ref = rd("baseline_ken.tif")
g = Geod(ellps="WGS84")
lat = ref.transform[5] + (np.arange(ref.shape[0]) + 0.5) * ref.transform[4]
dx = np.array([g.inv(0, la, ref.res[0], la)[2] for la in lat])
dy = np.array([g.inv(0, la - ref.res[1] / 2, 0, la + ref.res[1] / 2)[2] for la in lat])
A = (dx * dy)[:, None] * np.ones(ref.shape[1]) / 1e4
ws = np.load(wsf)
SW = [("Honolua Stream", [2], "a"), ("Mokuleʻia Bay", [4], "a"), ("Kahauiki", [6], "b"), ("Mokupeʻa Gulch", [8], "a"),
      ("Honokahua Stream", [9], "a"), ("Napili 2-3", [13], "b"), ("Napili 4-5", [14], "a"), ("Honokeana", [16], "b"),
      ("Kaʻōpala Gulch", [20], "a"), ("Kahana Stream", [22], "a"), ("Mahinahina", [26], "d"), ("Honokōwai Stream", [28], "c"),
      ("Hanakaʻōʻō", [30], "d"), ("Kāʻanapali-Kahua", [31, 33], "c"), ("Wahikuli Gulch", [35], "c")]
study = (b > 0) & np.isin(ws, sum([k for _, k, _ in SW], []))
SC = [("L_P", 1), ("L_R", 2), ("L_T", 3), ("L_P+R", 4), ("F_P", 6), ("R_200", 7), ("VH_T", 8), ("VH_P", 12),
      ("VH_A", 10), ("H_T", 9), ("H_P", 13), ("H_A", 11)]
S = {n: np.where(study, rd(f"scenario_{k}.tif")[0], np.nan) for n, k in SC}
bb = np.where(study, b, np.nan)
chg = lambda n: study & (np.abs(S[n] - bb) > 1e-6)
fill, pig, road = chg("L_T"), chg("L_P"), chg("L_R")
E0 = np.nansum(bb * A)
# watershed properties from the original sheet (rows in the same north-to-south order)
wb = openpyxl.load_workbook(xlsx, data_only=True).active
props = [r for r in wb.iter_rows(min_row=3, max_row=17, values_only=True)]
rows = []
for (name, ks, fn), p in zip(SW, props):
    m = study & np.isin(ws, ks)
    rows.append(dict(name=name, foot=fn, usgs=p[1], final=np.nansum(bb[m] * A[m]), cells=int(m.sum()),
                     susc=p[4], fill=int((fill & m).sum()), pigonly=int((pig & m & ~road).sum()),
                     road=int((road & m).sum()), area=p[8], pmean=p[9], ptot=p[10],
                     red={n: 100 * (1 - np.nansum(S[n][m] * A[m]) / np.nansum(bb[m] * A[m])) for n, _ in SC},
                     share={n: 100 * (np.nansum(bb[m] * A[m]) - np.nansum(S[n][m] * A[m])) / E0 for n, _ in SC}))
with open(f"{out}/TableS5_subwatershed_characteristics.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["subwatershed", "flow_type", "usgs_t_yr", "modeled_final_t_yr", "stream_cells", "mean_susceptibility_dem",
                "fill_terrace_cells", "pig_only_cells", "road_crossing_and_multiple_cells", "area_km2",
                "mean_annual_precip_mm", "total_annual_precip_mm"])
    for r in rows:
        w.writerow([r["name"], "perennial-intermittent" if r["foot"] in "ab" else "ephemeral", f'{r["usgs"]:.1f}',
                    f'{r["final"]:.1f}', r["cells"], f'{r["susc"]:.0f}', r["fill"], r["pigonly"], r["road"],
                    r["area"], f'{r["pmean"]:.0f}', r["ptot"]])
    w.writerow(["Total", "", f'{sum(r["usgs"] for r in rows):.1f}', f'{sum(r["final"] for r in rows):.1f}',
                sum(r["cells"] for r in rows), "", sum(r["fill"] for r in rows), sum(r["pigonly"] for r in rows),
                sum(r["road"] for r in rows), round(sum(r["area"] for r in rows), 2), "", ""])
with open(f"{out}/TableS6_reduction_by_subwatershed.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["subwatershed"] + [n for n, _ in SC])
    for r in rows: w.writerow([r["name"]] + [f'{r["red"][n]:.1f}' for n, _ in SC])
    w.writerow(["Study area"] + [f'{100 * (1 - np.nansum(S[n] * A) / E0):.1f}' for n, _ in SC])

plt.rcParams.update({"axes.unicode_minus": True, "font.family": "sans-serif", "font.size": 9, "axes.linewidth": 0.8, "axes.edgecolor": "#444",
                     "xtick.color": "#444", "ytick.color": "#444", "axes.spines.top": False, "axes.spines.right": False})
# ---- Figs. S2 and S3
P = [("A. Mean susceptibility", "susc", "Mean susceptibility (shear stress)"), ("B. Fill terrace cells", "fill", "Fill terrace cells"),
     ("C. Pig-only cells", "pigonly", "Pig-only cells"), ("D. Road crossing cells", "road", "Road crossing & multiple-disturbance cells"),
     ("E. Watershed area", "area", "Watershed area (km²)"), ("F. Mean annual precipitation", "pmean", "Mean annual precipitation (mm)"),
     ("G. Total annual precipitation", "ptot", "Total annual precipitation (mm)")]
r2s = {}
for tag, fl, fn in [("S2", "ab", "perennial-intermittent"), ("S3", "cd", "ephemeral")]:
    sub = [r for r in rows if r["foot"] in fl]; y = np.array([r["final"] for r in sub])
    fig, axs = plt.subplots(2, 4, figsize=(11, 6.0)); axs = axs.ravel(); axs[-1].axis("off")
    for ax, (tt, k, xl) in zip(axs, P):
        x = np.array([r[k] for r in sub], float); c = np.polyfit(x, y, 1); r2 = np.corrcoef(x, y)[0, 1] ** 2
        r2s[(tag, k)] = r2
        xx = np.linspace(x.min(), x.max(), 10)
        ax.plot(xx, np.polyval(c, xx), color="#888", lw=1); ax.scatter(x, y, s=28, color="#1f6fb2", edgecolor="white", lw=0.5, zorder=3)
        ax.set_title(f"{tt}\nR² = {r2:.2f}", fontsize=9, fontweight="bold"); ax.set_xlabel(xl); ax.set_ylabel("Modeled bank erosion (t/yr)")
        if k == "ptot": ax.xaxis.set_major_formatter(mt.FuncFormatter(lambda v, _: f"{v/1000:.0f}k"))
    plt.tight_layout(); fig.savefig(f"{out}/Fig{tag}_final.png", dpi=300); plt.close(fig)
with open(f"{out}/FigS2_S3_r2.csv", "w") as f:
    f.write("figure,characteristic,r2\n"); [f.write(f"{t},{k},{v:.3f}\n") for (t, k), v in r2s.items()]
js.setup(8)
# ---- Fig. 5 (contribution of each subwatershed to the study-area reduction)
cols = ["#d9f0d3", "#91cf8e", "#d6e2ef", "#93bdd6", "#2f6da8", "#fde5d2", "#f9b67f", "#fd8432", "#d7480f", "#8c2a04",
        "#e5e6f4", "#a9a9d8", "#e6e6e6", "#adadad", "#525252"]
fig, ax = plt.subplots(figsize=(js.W, 3.9)); xs = np.arange(len(SC))
for j, (name, *_ ) in enumerate(SW):
    vals = np.array([rows[j]["share"][n] for n, _ in SC]); bot = np.array([sum(rows[i]["share"][n] for i in range(j)) for n, _ in SC])
    ax.bar(xs, -vals, bottom=-bot, color=cols[j], width=0.75, label=name, edgecolor="none")
ax.set_xticks(xs, [n for n, _ in SC]); ax.set_ylim(-100, 2); ax.set_ylabel("Reduction in bank erosion (% of study-area baseline)")
ax.yaxis.set_major_formatter(mt.FuncFormatter(lambda v, _: f"{abs(v):.0f}%")); ax.set_xlabel("Alternative")
ax.grid(axis="y", color="#ddd", lw=0.5); ax.set_axisbelow(True)
ax.legend(title="Subwatershed", bbox_to_anchor=(1.01, 1), loc="upper left", frameon=False, handlelength=1.2, labelspacing=0.3)
ax.set_ylabel("Reduction in bank erosion\n(% of study-area baseline)")
plt.tight_layout(); js.save(fig, f"{out}/Fig5_final"); plt.close(fig)
# ---- Fig. 6 (landowners)
sf = shapefile.Reader(ten)
tr = Transformer.from_crs(CRS.from_wkt(open(ten[:-4] + ".prj").read()), "EPSG:4326", always_xy=True).transform
grp = {"Maui Land & Pine": 1, "Govt. State": 2, "Govt. State DHHL": 2, "Kaanapali Dev.": 3}
own = rasterize([(mapping(transform(tr, shape(s.__geo_interface__))), grp.get(r["MajorOwner"], 4))
                 for s, r in zip(sf.shapes(), sf.records())], out_shape=b.shape, transform=ref.transform, fill=4, dtype="uint8")
OW = [(2, "State government", "#4a7ef0"), (4, "Other", "#f3f0d8"), (1, "Maui Land & Pine", "#e5b800"), (3, "Kāʻanapali Land Mgt. Corp.", "#8b5a2b")]
F6 = ["Baseline", "R_200", "VH_T", "VH_A", "H_T", "H_A"]
tab = {}
for a in F6:
    arr = bb if a == "Baseline" else S[a]
    tab[a] = {k: np.nansum(arr[study & (own == k)] * A[study & (own == k)]) for k, _, _ in OW}
with open(f"{out}/Fig6_landowner.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["alternative"] + [n for _, n, _ in OW] + ["total"])
    for a in F6: w.writerow([a] + [f"{tab[a][k]:.1f}" for k, _, _ in OW] + [f"{sum(tab[a].values()):.1f}"])
fig, ax = plt.subplots(figsize=(js.W, 3.4)); xs = np.arange(len(F6))
for i, a in enumerate(F6):
    bot = 0
    for k, n, c in OW:
        v = tab[a][k]; ax.bar(i, v, bottom=bot, color=c, width=0.75, edgecolor="white", lw=0.4, label=n if i == 0 else None)
        if a != "Baseline" and v > 12:
            pct = round(100 * (v - tab["Baseline"][k]) / tab["Baseline"][k])
            ax.text(i, bot + v / 2, "0%" if pct == 0 else f"−{abs(pct)}%", ha="center", va="center", fontsize=8, color="white" if k in (2, 3) else "black")
        bot += v
    ax.text(i, bot + 8, f"{bot:.0f}", ha="center", va="bottom", fontsize=8, color="#333")
ax.set_xticks(xs, F6); ax.set_ylabel("Bank erosion (t/yr)"); ax.set_xlabel("Alternative"); ax.set_ylim(0, 1000)
ax.grid(axis="y", color="#ddd", lw=0.5); ax.set_axisbelow(True)
h, l = ax.get_legend_handles_labels(); ax.legend(h[::-1], l[::-1], bbox_to_anchor=(1.01, 0.5), loc="center left", frameon=False)
plt.tight_layout(); js.save(fig, f"{out}/Fig6_final"); plt.close(fig)
print("total", round(E0, 1), "fill", int(fill.sum()), "pig", int(pig.sum()), "road", int(road.sum()), "pig-only", int((pig & ~road).sum()))
