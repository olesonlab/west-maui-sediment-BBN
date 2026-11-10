"""Fig. 7 on the NHDPlus network of the final run.

For each erosion class value T in the final baseline raster (baseline_ken.tif), select the
stream cells with baseline erosion >= T. x = selected cells (overall, or on one landowner's
land) as a % of all 19,222 network cells; y = erosion from those cells as a % of total.
Study area: the 15 USGS subwatersheds with Ka'anapali (as in Ken's zonal summaries).
Landowners: MajorOwner in LandTenure.shp; State = Govt. State + Govt. State DHHL.
"""
import sys, csv, json, numpy as np, rasterio, shapefile
from rasterio.features import rasterize
from shapely.geometry import shape, mapping
from shapely.ops import transform
from pyproj import Transformer, CRS
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt, matplotlib.ticker as mt

base, zones, tenure, out = sys.argv[1:5]   # baseline_ken.tif, ws_ken.npy, LandTenure.shp, out prefix
ref = rasterio.open(base); b = ref.read(1).astype(float); b[~(b > -1e30)] = np.nan
ws = np.load(zones); m = np.isin(ws, [2,4,6,8,9,13,14,16,20,22,26,28,30,31,35,33])
sf = shapefile.Reader(tenure)
tr = Transformer.from_crs(CRS.from_wkt(open(tenure[:-4] + ".prj").read()), "EPSG:4326", always_xy=True).transform
grp = {"Maui Land & Pine": 1, "Govt. State": 2, "Govt. State DHHL": 2}
own = rasterize([(mapping(transform(tr, shape(s.__geo_interface__))), grp.get(r["MajorOwner"], 3))
                 for s, r in zip(sf.shapes(), sf.records())], out_shape=b.shape, transform=ref.transform, fill=0, dtype="uint8")
net = (b > 0) & m; N = net.sum(); E = np.nansum(b[net])
T = [0.0] + list(np.unique(b[net & (b >= 6)]))
rows = []
for t in T:
    sel = net if t == 0 else net & (b >= t)
    r = [t]
    for k in (None, 2, 1):
        s = sel if k is None else sel & (own == k)
        r += [100 * s.sum() / N, 100 * np.nansum(b[s]) / E]
    rows.append(r)
with open(out + ".csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["threshold_t_ha_yr_ge", "overall_pct_cells", "overall_pct_erosion", "state_pct_cells",
                                   "state_pct_erosion", "mlp_pct_cells", "mlp_pct_erosion"])
    w.writerows([[f"{x:.2f}" for x in r] for r in rows])

plt.rcParams.update({"font.family": "sans-serif", "font.size": 9, "axes.linewidth": 0.8, "axes.edgecolor": "#444",
                     "xtick.color": "#444", "ytick.color": "#444", "axes.grid": True, "grid.color": "#d0d0d0",
                     "grid.linewidth": 0.5, "axes.axisbelow": True})
R = np.array(rows)
series = [("Maui Land & Pine", R[:, 5], R[:, 6], "s", "#DAA520", "#8B6914"),
          ("State", R[:, 3], R[:, 4], "o", "#2171b5", "#08519c"),
          ("Overall", R[:, 1], R[:, 2], "^", "#111111", "#000000")]
fig, axes = plt.subplots(1, 2, figsize=(8.5, 3.8), sharey=True)
for ax, xlim, lab in [(axes[0], (0, 102), "a"), (axes[1], (0, 7), "b")]:
    for name, x, y, mk, c, ec in series:
        ax.scatter(x, y, marker=mk, color=c, edgecolors=ec, s=50, linewidths=0.5, zorder=4, label=name, clip_on=True)
    ax.set_xlim(*xlim); ax.set_ylim(0, 100)
    ax.xaxis.set_major_formatter(mt.FuncFormatter(lambda v, _: f"{v:.0f}%"))
    ax.yaxis.set_major_formatter(mt.FuncFormatter(lambda v, _: f"{v:.0f}%"))
    ax.set_xlabel("% of streambanks treated"); ax.spines[["top", "right"]].set_visible(False)
    ax.text(0.03, 0.97, lab, transform=ax.transAxes, fontsize=10, fontweight="bold", va="top")
axes[0].set_ylabel("% of bank erosion reduced"); axes[1].tick_params(labelleft=False)
h, l = axes[0].get_legend_handles_labels()
fig.legend(h, l, loc="lower center", ncol=3, bbox_to_anchor=(0.5, -0.05), frameon=True, edgecolor="#ccc",
           handletextpad=0.4, columnspacing=1.2)
plt.tight_layout(); plt.subplots_adjust(bottom=0.2, wspace=0.08)
fig.savefig(out + ".png", dpi=600, bbox_inches="tight", pad_inches=0.12)
fig.savefig(out + ".pdf", bbox_inches="tight", pad_inches=0.12)
print("N", N, "E", round(E, 1)); [print([round(x, 2) for x in r]) for r in rows]
