"""Graphical abstract.

Laid out in code (matplotlib) from the paper's own material only:
  - field photographs from Figure 1 (J. Stock), cropped, not altered
  - the hotspot panel of Figure 4, cropped, not altered
  - result values from the data workbook (Scenario_results), drawn as bars
No generative image tool was used; every graphic element is a plain shape,
line or text drawn by this script, or a crop of an author figure.

Run from the repository root:  python code/graphical_abstract.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from PIL import Image

from common import sheet_rows

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"

for fam in ("Liberation Sans", "DejaVu Sans"):
    if any(fam == f.name for f in matplotlib.font_manager.fontManager.ttflist):
        plt.rcParams["font.family"] = fam
        break

INK, MUTED, SED, WATER = "#1f2a33", "#55606a", "#a0522d", "#1f5f8b"
RED, ORANGE, GREY = "#c0392b", "#e08a1e", "#9aa3ab"

# --- results from the workbook (percent change in total erosion)
rows = {r[2]: r for r in sheet_rows("Scenario_results", min_row=4, max_row=15, max_col=12)}
OLD = {"H_A": "9_A"}                     # workbook still uses the old hotspot codes
pct = {k: -100 * rows[OLD.get(k, k)][5] for k in ("L_T", "H_A", "L_P", "L_R", "L_P+R")}
dist_hi = max(pct["L_P"], pct["L_R"], pct["L_P+R"])

# --- source images (crops only)
f1 = Image.open(FIG / "Figure1_composite.jpg")
w1, h1 = f1.size
terrace = f1.crop((0, 0, w1 // 2, int(h1 * 0.335)))
plume = f1.crop((w1 // 2, 0, w1, int(h1 * 0.335)))
f4 = Image.open(FIG / "Figure4_2panel.jpg")
w4, h4 = f4.size
hotspots = f4.crop((int(w4 * 0.512), int(h4 * 0.03), int(w4 * 0.977), int(h4 * 0.955)))   # right (hotspot) panel

W, H = 10.0, 4.0                       # inches; Elsevier GA is 13 x 5 cm (same ratio)
fig = plt.figure(figsize=(W, H), dpi=100)
fig.patch.set_facecolor("white")


def box(x, y, w, h):                   # figure-fraction axes
    ax = fig.add_axes([x / W, y / H, w / W, h / H])
    ax.set_axis_off()
    return ax


def label(x, y, s, size=13, weight="bold", color=INK, ha="center", **kw):
    fig.text(x / W, y / H, s, size=size, weight=weight, color=color, ha=ha, va="center", **kw)


def arrow(x0, x1, y):
    fig.patches.append(FancyArrowPatch((x0 / W, y / H), (x1 / W, y / H), transform=fig.transFigure,
                                       arrowstyle="-|>", mutation_scale=16, lw=2, color=MUTED))


def fit(img, w, h, ax_=0.5, ay=0.5):
    """Centre-crop img to the w:h aspect of its panel (crop only, no stretching)."""
    iw, ih = img.size
    if iw / ih > w / h:
        nw = int(ih * w / h); x0 = int((iw - nw) * ax_)
        return img.crop((x0, 0, x0 + nw, ih))
    nh = int(iw * h / w); y0 = int((ih - nh) * ay)
    return img.crop((0, y0, iw, y0 + nh))


def photo(x, y, w, h, img, **kw):
    a = box(x, y, w, h)
    a.imshow(fit(img, w, h, **kw))
    return a


# title band
fig.patches.append(FancyBboxPatch((0, 3.42 / H), 1, 0.58 / H, boxstyle="square,pad=0",
                                  transform=fig.transFigure, color=INK, zorder=0))
label(0.22, 3.71, "Targeting legacy fill terraces at erosion hotspots cuts streambank erosion upstream of West Maui reefs",
      size=13.5, color="white", ha="left")

TOP, MID, CAP = 3.12, 1.75, 0.34
PW, PY, PH = 1.62, 0.66, 2.18           # panel width, bottom, height
X = [0.15, 2.17, 4.19, 6.21, 8.23]      # panel left edges (equal gaps)
C = [x + PW / 2 for x in X]

for i in range(4):
    arrow(X[i] + PW + 0.06, X[i + 1] - 0.06, MID)

# 1. legacy fill terraces (photo)
label(C[0], TOP, "Legacy fill terraces", size=12.5)
photo(X[0], PY, PW, PH, terrace, ax_=0.45)
label(C[0], CAP, "Plantation-era sediment\nerodes in small storms", size=10, weight="normal", color=MUTED)

# 2. BBN
label(C[1], TOP, "Bayesian belief network", size=12.5)
ax = box(X[1] - 0.05, PY - 0.08, PW + 0.1, PH + 0.1); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
nodes = [(0.17, 0.62, "Fill\nterrace", SED), (0.50, 0.86, "Disturb-\nance", MUTED), (0.83, 0.62, "Bank\nsuscept.", WATER)]
for x, y, t, c in nodes:
    ax.add_patch(FancyBboxPatch((x - 0.15, y - 0.085), 0.30, 0.17, boxstyle="round,pad=0.01,rounding_size=0.04",
                                fc="white", ec=c, lw=2))
    ax.text(x, y, t, ha="center", va="center", size=9, weight="bold", color=c, linespacing=1.0)
    ax.annotate("", xy=(0.5 + (x - 0.5) * 0.35, 0.42), xytext=(x, y - 0.095),
                arrowprops=dict(arrowstyle="-|>", lw=1.6, color=c, mutation_scale=12))
ax.add_patch(FancyBboxPatch((0.16, 0.26), 0.68, 0.15, boxstyle="round,pad=0.01,rounding_size=0.04",
                            fc=INK, ec=INK))
ax.text(0.5, 0.335, "Bank erosion", ha="center", va="center", size=10.5, weight="bold", color="white")
for i, c in enumerate(["#2c7bb6", "#7fbf7b", "#ffd84d", "#f08c3a", "#d7301f"]):
    ax.add_patch(plt.Rectangle((0.16 + i * 0.136, 0.15), 0.136, 0.065, color=c))
ax.text(0.16, 0.09, "very low", size=8.5, color=MUTED, ha="left", va="center")
ax.text(0.84, 0.09, "very high", size=8.5, color=MUTED, ha="right", va="center")
label(C[1], CAP, "Expert-elicited, calibrated\nto USGS sediment budget", size=10, weight="normal", color=MUTED)

# 3. hotspots (Figure 4 panel, map only)
label(C[2], TOP, "Erosion hotspots", size=12.5)
a = box(X[2] - 0.05, PY - 0.02, PW + 0.1, PH + 0.04)
a.imshow(hotspots)                      # whole hotspot panel incl. its legend, aspect preserved
label(C[2], CAP, "78% of erosion from\n<9% of streambanks", size=10, weight="normal", color=MUTED)

# 4. results bars
label(C[3], TOP, "Erosion reduced", size=12.5)
ax = box(X[3], PY + 0.04, PW + 0.08, PH - 0.02)
items = [("All fill terraces fixed", pct["L_T"], RED, f"{pct['L_T']:.0f}%"),
         ("Hotspots only\n(9% of streams)", pct["H_A"], ORANGE, f"{pct['H_A']:.0f}%"),
         ("Pigs or road\ncrossings only", dist_hi, GREY, f"0\u2013{dist_hi:.0f}%")]
for i, (t, v, c, s) in enumerate(items):
    y = 2 - i
    ax.barh(y, 100, height=0.32, color="#eef1f3")
    ax.barh(y, v, height=0.32, color=c)
    ax.text(0, y + 0.3, t, size=9.5, color=INK, va="bottom", ha="left", linespacing=1.0)
    ax.text(v + 3 if v < 60 else v - 3, y, s, size=10.5, weight="bold",
            color=INK if v < 60 else "white", va="center", ha="left" if v < 60 else "right")
ax.set_xlim(0, 100); ax.set_ylim(-0.35, 2.95); ax.set_axis_off()
label(C[3], CAP, "12 alternatives compared;\nterrace fixes dominate", size=10, weight="normal", color=MUTED)

# 5. reef (photo)
label(C[4], TOP, "Nearshore reefs", size=12.5)
photo(X[4], PY, PW, PH, plume, ax_=0.25)
label(C[4], CAP, "Less sediment at the\nsource of plumes", size=10, weight="normal", color=MUTED)

fig.text(0.995, 0.008, "Photos: J. Stock. Map: Figure 4.", size=7, color=MUTED, ha="right", va="bottom")

for ext, kw in ((".png", dict(dpi=400)), (".tif", dict(dpi=400, pil_kwargs={"compression": "tiff_lzw"})),
                (".pdf", {})):
    fig.savefig(FIG / f"GraphicalAbstract{ext}", facecolor="white", **kw)
print("Graphical abstract written to", FIG, {k: round(v, 1) for k, v in pct.items()})
