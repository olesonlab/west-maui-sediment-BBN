"""Fig. 4 from the final baseline raster (baseline_ken.tif, NHDPlus stream network).

Left: baseline bank erosion (t/ha/yr) on network cells in the study area (15 USGS subwatersheds plus
Ka'anapali), in five classes that follow the raster's discrete values. Right: high (>= 16.78) and
very-high (>= 19.31) erosion cells. Each 10 m cell is drawn as a 50 m square for visibility, with higher
values drawn on top. Subwatersheds outside the study area are hatched.
Usage: fig4_final.py baseline_ken.tif ws_ken.npy subws_WM_final_USGS.shp out_prefix
"""
import sys, numpy as np, rasterio, shapefile
from pyproj import Transformer, CRS
from shapely.geometry import shape
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.patches import Patch

base, zones, shp, out = sys.argv[1:5]
STUDY = [2, 4, 6, 8, 9, 13, 14, 16, 20, 22, 26, 28, 30, 31, 35, 33]
ref = rasterio.open(base); b = ref.read(1).astype(float); b[~(b > -1e30)] = np.nan
ws = np.load(zones); net = (b > 0) & np.isin(ws, STUDY)
rr, cc = np.nonzero(net); v = b[rr, cc]
lon, lat = rasterio.transform.xy(ref.transform, rr, cc)
utm = CRS.from_wkt(open(shp[:-4] + ".prj").read())
x, y = Transformer.from_crs("EPSG:4326", utm, always_xy=True).transform(np.array(lon), np.array(lat))
o = np.argsort(v, kind="stable"); x, y, v = x[o], y[o], v[o]
print("cells", len(v), "sum", round(v.sum(), 1))

sf = shapefile.Reader(shp)
polys = []
for s, r in zip(sf.shapes(), sf.records()):
    g = shape(s.__geo_interface__)
    for p in (g.geoms if g.geom_type == "MultiPolygon" else [g]):
        polys.append((np.asarray(p.exterior.coords), r["New_Number"] in STUDY))

bins = [(0, 0.2, "0.05–0.15", "#08519c"), (0.2, 1, "0.20–0.65", "#7fa7a0"), (1, 10, "6.16–8.08", "#f2e34c"),
        (10, 19.3, "16.78–18.47", "#f08a2c"), (19.3, 99, "19.31–22.09", "#d7191c")]
H = 25  # half-width of drawn square, m

def squares(xs, ys):
    return [np.array([[a - H, c - H], [a + H, c - H], [a + H, c + H], [a - H, c + H]]) for a, c in zip(xs, ys)]

def basemap(ax):
    for xy, st in polys:
        ax.fill(xy[:, 0], xy[:, 1], facecolor="#e6e6e6", edgecolor="#222", lw=0.6,
                hatch=None if st else "////", zorder=1)
    ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_linewidth(0.8)

plt.rcParams.update({"font.family": "sans-serif", "font.size": 8, "hatch.linewidth": 0.4, "hatch.color": "#777"})
fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 3.9))
for ax in (a1, a2): basemap(ax)
cols = np.empty(len(v), object)
for lo, hi, lab, c in bins: cols[(v >= lo) & (v < hi)] = c
a1.add_collection(PolyCollection(squares(x, y), facecolors=list(cols), edgecolors="none", zorder=3))
h = (v >= 16.78) & (v < 19.3); vh = v >= 19.3
a2.add_collection(PolyCollection(squares(x[h], y[h]), facecolors="#f08a2c", edgecolors="none", zorder=3))
a2.add_collection(PolyCollection(squares(x[vh], y[vh]), facecolors="#d7191c", edgecolors="none", zorder=4))
print("high", h.sum(), "very high", vh.sum())

leg1 = [Patch(facecolor="#e6e6e6", edgecolor="#222", label="Study subwatersheds"),
        Patch(facecolor="#e6e6e6", edgecolor="#222", hatch="////", label="Outside study area")] + \
       [Patch(facecolor=c, label=lab) for _, _, lab, c in bins]
a1.legend(handles=leg1, loc="upper left", title="Baseline bank erosion\n(t/ha/yr)", title_fontsize=7.5, fontsize=7,
          frameon=True, facecolor="white", edgecolor="#bbb", framealpha=0.92, alignment="left", handlelength=1.2)
leg2 = [Patch(facecolor="#d7191c", label=f"Very high, ≥ 19.31 ({vh.sum():,} cells)"),
        Patch(facecolor="#f08a2c", label=f"High, 16.78–18.47 ({h.sum():,} cells)")]
a2.legend(handles=leg2, loc="upper left", title="Erosion hotspots (t/ha/yr)", title_fontsize=7.5, fontsize=7,
          frameon=True, facecolor="white", edgecolor="#bbb", framealpha=0.92, alignment="left", handlelength=1.2)
for ax, lab in ((a1, "a"), (a2, "b")):
    ax.text(0.97, 0.98, lab, transform=ax.transAxes, ha="right", va="top", fontsize=11, fontweight="bold")
# room for legends on the west side
for ax in (a1, a2):
    ax.autoscale_view(); lo, hi = ax.get_xlim(); ax.set_xlim(lo - 0.30 * (hi - lo), hi + 0.02 * (hi - lo))
# scale bar and north arrow
x0, x1 = a1.get_xlim(); y0, y1 = a1.get_ylim()
sx, sy = x0 + 0.35 * (x1 - x0), y0 + 0.04 * (y1 - y0)
for i in range(4):
    a1.add_patch(plt.Rectangle((sx + i * 1000, sy), 1000, 120, facecolor="k" if i % 2 == 0 else "w", edgecolor="k", lw=0.5, zorder=5))
for i in (0, 2, 4): a1.text(sx + i * 1000, sy + 220, f"{i}", ha="center", va="bottom", fontsize=7)
a1.text(sx + 4000 + 350, sy + 60, "km", va="center", fontsize=7)
nx, ny = x0 + 0.06 * (x1 - x0), y0 + 0.05 * (y1 - y0)
a1.annotate("", xy=(nx, ny + 1100), xytext=(nx, ny), arrowprops=dict(arrowstyle="-|>", color="k", lw=1.2))
a1.text(nx, ny + 1250, "N", ha="center", va="bottom", fontsize=9, fontweight="bold")
plt.tight_layout(w_pad=0.6)
fig.savefig(out + ".png", dpi=600, bbox_inches="tight", pad_inches=0.05)
fig.savefig(out + ".pdf", bbox_inches="tight", pad_inches=0.05)
