"""Figures S2 (perennial-intermittent, footnotes a+b) and S3 (ephemeral, c+d):
BBN-modeled bank erosion (y) vs. subwatershed characteristics (x), OLS line and R^2."""
import numpy as np
import matplotlib.ticker as mt
from common import subwatersheds, style, FIGDIR

PANELS = [("mean_sus", "A. Mean susceptibility", "Mean susceptibility"),
          ("fill", "B. Fill terrace cells", "# fill terrace cells"),
          ("pig", "C. Pig disturbance cells", "# pig disturbance cells"),
          ("road", "D. Road crossing & multiple dist. cells", "# road crossing & multiple disturbance cells"),
          ("area", "E. Watershed area", "Watershed area (km²)"),
          ("mean_p", "F. Mean annual precipitation", "Mean annual precipitation (mm)"),
          ("tot_p", "G. Total annual precipitation", "Total annual precipitation (mm)")]
d = subwatersheds()
plt = style()
for groups, color, out in [("ab", "#1f6aa5", "FigureS2.png"), ("cd", "#c45a2c", "FigureS3.png")]:
    sub = [r for r in d if r["group"] in groups]
    y = np.array([r["modeled"] for r in sub])
    fig, axes = plt.subplots(2, 4, figsize=(13, 6.6))
    for ax, (key, title, xlabel) in zip(axes.ravel(), PANELS):
        x = np.array([r[key] for r in sub], dtype=float)
        b, a = np.polyfit(x, y, 1)
        xx = np.linspace(x.min(), x.max(), 50)
        ax.plot(xx, a + b * xx, color="0.5", lw=1.2, zorder=2)
        ax.scatter(x, y, s=38, color=color, edgecolor="white", linewidth=0.6, zorder=3)
        r2 = np.corrcoef(x, y)[0, 1] ** 2
        ax.text(0.97, 0.05, f"R² = {r2:.2f}", transform=ax.transAxes, ha="right", va="bottom", color="0.3")
        ax.set_title(title, fontweight="bold"); ax.set_xlabel(xlabel)
        ax.set_ylabel("Modeled bank erosion (T/yr)")
        ax.spines[["top", "right"]].set_visible(False)
        ax.xaxis.set_major_formatter(mt.FuncFormatter(lambda v, _: f"{v/1000:.0f}k" if abs(v) >= 10000 else f"{v:g}"))
        print(f"{out} {title}: R2={r2:.3f}")
    axes.ravel()[7].set_visible(False)
    fig.tight_layout(); fig.savefig(FIGDIR / out)
    print(out, "written,", len(sub), "subwatersheds")
