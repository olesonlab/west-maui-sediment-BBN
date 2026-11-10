"""Fig. S1 from the final model run (NHDPlus network): BBN vs USGS bank erosion
for the validation subwatersheds. Final-run values from table_s3_final_run.py."""
import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
eph = {"Honokowai": (61.97, 55.7), "Ka'anapali-Kahua": (25.12, 23.2), "Wahikuli": (42.43, 46.6)}
per = {"Honolua": (91.39, 166.9), "Mokule'ia": (23.26, 26.0), "Mokupe'a": (45.87, 45.2), "Honokahua": (44.90, 40.5),
       "Napili 4-5": (55.68, 50.7), "Ka'opala": (62.05, 73.5), "Kahana": (285.24, 211.9)}
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
