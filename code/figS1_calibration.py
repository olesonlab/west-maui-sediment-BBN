"""Figure S1: BBN-modeled vs. USGS sediment-budget bank erosion for the validation
subwatersheds (ephemeral: footnote c; perennial-intermittent: footnote a).
R^2 = squared Pearson correlation; dashed line = 1:1."""
import numpy as np
from common import subwatersheds, style, FIGDIR

d = subwatersheds()
plt = style()
fig, axes = plt.subplots(1, 2, figsize=(6.4, 3.2))
for ax, g, title, color, lim in [(axes[0], "c", "A. Ephemeral", "#C65B2B", (19, 69)),
                                 (axes[1], "a", "B. Perennial-intermittent", "#1B6CA8", (20, 320))]:
    x = np.array([r["empirical"] for r in d if r["group"] == g])
    y = np.array([r["modeled"] for r in d if r["group"] == g])
    ax.plot(lim, lim, ls="--", color="#bbb", lw=1, zorder=1)
    ax.scatter(x, y, color=color, s=40, edgecolor="white", linewidth=0.6, zorder=3)
    r2 = np.corrcoef(x, y)[0, 1] ** 2
    ax.text(0.97, 0.05, f"R² = {r2:.2f}", transform=ax.transAxes, ha="right", va="bottom", color="#555")
    ax.set_xlim(*lim); ax.set_ylim(*lim)
    ax.set_title(title, fontweight="bold")
    ax.set_xlabel("USGS modeled (tonnes/yr)"); ax.set_ylabel("BBN modeled (tonnes/yr)")
    ax.spines[["top", "right"]].set_visible(False)
    print(f"{title}: n={len(x)}, R2={r2:.4f}")
plt.tight_layout()
fig.savefig(FIGDIR / "FigureS1.png")
print("FigureS1.png written")
