"""Fig. S1 from the final model run (NHDPlus network): BBN vs USGS bank erosion
for the validation subwatersheds.

Usage: figS1_final.py table_s3_final_run.txt
Reads the USGS and final-run columns written by table_s3_final_run.py.
Calibration subwatersheds (Kahauiki, Napili 2-3, Honokeana, Mahinahina,
Hanakaoo) are left out, as in Table S3.
"""
import sys, csv, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
EPH = ["Honokowai", "Ka'anapali-Kahua", "Wahikuli"]
PER = ["Honolua", "Mokule'ia", "Mokupe'a", "Honokahua", "Napili 4-5", "Ka'opala", "Kahana"]
vals = {}
with open(sys.argv[1]) as f:
    for row in csv.DictReader(f):
        if row['subwatershed'] == 'Total': break
        vals[row['subwatershed']] = (float(row['usgs_t_yr']), float(row['final_t_yr']))
missing = [n for n in EPH + PER if n not in vals]
if missing: sys.exit(f"Missing from {sys.argv[1]}: {missing}")
eph = {n: vals[n] for n in EPH}; per = {n: vals[n] for n in PER}
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11})
fig, axs = plt.subplots(1, 2, figsize=(10, 4.976))
for ax, d, col, title, lim in ((axs[0], eph, '#C55A2B', 'A. Ephemeral', (19, 69)),
                               (axs[1], per, '#1F6FAE', 'B. Perennial-intermittent', (20, 320))):
    x = np.array([v[0] for v in d.values()]); y = np.array([v[1] for v in d.values()])
    r2 = np.corrcoef(x, y)[0, 1] ** 2
    ax.plot(lim, lim, '--', color='#BBBBBB', lw=1.2, zorder=1)
    ax.scatter(x, y, s=60, color=col, edgecolor='white', lw=0.8, zorder=3)
    ax.set_xlim(lim); ax.set_ylim(lim); ax.set_aspect('equal')
    ax.set_title(title, fontweight='bold', fontsize=13)
    ax.set_xlabel('USGS modeled (tonnes/yr)'); ax.set_ylabel('BBN modeled, final run (tonnes/yr)')
    ax.text(0.96, 0.06, f'R² = {r2:.2f}', transform=ax.transAxes, ha='right', color='#444444')
    for s in ('top', 'right'): ax.spines[s].set_visible(False)
    ax.tick_params(colors='#444444')
    print(title, round(r2, 3))
fig.tight_layout(); fig.savefig('figS1/FigS1_final.png', dpi=300); fig.savefig('figS1/FigS1_final.pdf')
