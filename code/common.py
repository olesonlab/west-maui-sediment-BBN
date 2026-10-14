"""Shared helpers: load the results workbook and set a common plot style."""
from pathlib import Path
import openpyxl
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
WORKBOOK = ROOT / "data" / "Results-scenario-landowner-subwatershed.xlsx"
FIGDIR = ROOT / "figures"

# Table S3/S5 footnotes: a/b perennial-intermittent (validation/calibration),
# c/d ephemeral (validation/calibration)
GROUP = {"Honolua Stream": "a", "Mokule'ia Bay": "a", "Kanauiki": "b", "Mokupe'a Gulch": "a",
         "Honokahua Stream": "a", "Napili 2-3": "b", "Napili 4-5": "a", "Honokeana": "b",
         "Ka'Opala Gulch": "a", "Kahana Stream": "a", "Mahinahina": "d", "Honokowai Stream": "c",
         "Hanakaoo": "d", "Kahua": "c", "Wahikuli Gulch": "c"}


def sheet_rows(name, **kw):
    wb = openpyxl.load_workbook(WORKBOOK, data_only=True, read_only=True)
    return list(wb[name].iter_rows(values_only=True, **kw))


def subwatersheds():
    """Rows of the 'Subwatershed characteristics' sheet (same values as SI Table S5, unrounded)."""
    keys = ["name", "empirical", "modeled", "summed_sus", "mean_sus", "fill", "pig", "road",
            "area", "mean_p", "tot_p"]
    out = []
    for r in sheet_rows("Subwatershed characteristics", min_row=3, max_row=17, max_col=11):
        d = dict(zip(keys, r))
        d["group"] = GROUP[d["name"]]
        out.append(d)
    return out


def style():
    plt.rcParams.update({"font.family": "sans-serif", "font.size": 9, "axes.linewidth": 0.8,
                         "axes.edgecolor": "#444", "xtick.color": "#444", "ytick.color": "#444",
                         "savefig.dpi": 300, "figure.dpi": 300, "savefig.bbox": "tight",
                         "savefig.pad_inches": 0.12})
    return plt
