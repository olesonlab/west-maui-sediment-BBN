"""Figure 7: cumulative benefit of treating the highest-erosion cells.
Source: 'baseline_values' sheet, columns E-K, rows 3-14 (erosion thresholds and the share of
streambank cells covered / share of erosion from those cells, overall and by landowner)."""
import matplotlib.ticker as mt
from common import sheet_rows, style, FIGDIR

rows = sheet_rows("baseline_values", min_row=3, max_row=14, min_col=5, max_col=11)
pct = lambda i: [100 * r[i] for r in rows]
series = [("Maui Land & Pine", pct(5), pct(6), "s", "#DAA520", "#8B6914"),
          ("State", pct(3), pct(4), "o", "#2171b5", "#08519c"),
          ("Overall", pct(1), pct(2), "^", "#111111", "#000000")]

plt = style()
plt.rcParams.update({"axes.grid": True, "grid.color": "#d0d0d0", "grid.linewidth": 0.5,
                     "axes.axisbelow": True})
fig, axes = plt.subplots(1, 2, figsize=(8.5, 3.8), sharey=True)
for ax, xlim, lab in [(axes[0], (0, 25), "A"), (axes[1], (0, 7), "B")]:
    for name, x, y, m, c, ec in series:
        ax.scatter(x, y, marker=m, color=c, edgecolors=ec, s=50, linewidths=0.5, zorder=4, label=name)
    ax.set_xlim(*xlim); ax.set_ylim(0, 100)
    ax.xaxis.set_major_formatter(mt.FuncFormatter(lambda v, _: f"{v:.0f}%"))
    ax.yaxis.set_major_formatter(mt.FuncFormatter(lambda v, _: f"{v:.0f}%"))
    ax.set_xlabel("% of streambanks treated")
    ax.spines[["top", "right"]].set_visible(False)
    ax.text(0.03, 0.97, lab, transform=ax.transAxes, fontsize=10, fontweight="bold", va="top")
axes[0].set_ylabel("% of bank erosion reduced")
axes[1].tick_params(labelleft=False)
h, l = axes[0].get_legend_handles_labels()
fig.legend(h, l, loc="lower center", ncol=3, bbox_to_anchor=(0.5, -0.05), frameon=True,
           edgecolor="#ccc", handletextpad=0.4, columnspacing=1.2)
plt.tight_layout(); plt.subplots_adjust(bottom=0.2, wspace=0.06)
fig.savefig(FIGDIR / "Figure7.png")
print("Figure7.png written")
