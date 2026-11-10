"""Final-run bank erosion by subwatershed (Table S3 final column) and erosion shares.

Usage: table_s3_final_run.py baseline_ken.tif ws_ken.npy
The raster is on a geographic (EPSG:4326) grid, so each cell's area is computed
on the WGS84 ellipsoid (about 0.0093 ha). Values are tonnes/ha/yr; totals are
value x cell area. Subwatershed 33 is counted with Ka'anapali-Kahua (31).
"""
import sys, numpy as np, rasterio
from pyproj import Geod
r = rasterio.open(sys.argv[1]); b = r.read(1).astype(float); b[~(b > -1e30)] = np.nan
ws = np.load(sys.argv[2]); g = Geod(ellps='WGS84')
lat = r.transform[5] + (np.arange(r.shape[0]) + 0.5) * r.transform[4]
dx = np.array([g.inv(0, la, r.res[0], la)[2] for la in lat])
dy = np.array([g.inv(0, la - r.res[1] / 2, 0, la + r.res[1] / 2)[2] for la in lat])
A = (dx * dy)[:, None] * np.ones(r.shape[1]) / 1e4
rows = [("Honolua", [2], 91.39), ("Mokule'ia", [4], 23.26), ("Kahauiki", [6], 26.94), ("Mokupe'a", [8], 45.87),
        ("Honokahua", [9], 44.90), ("Napili 2-3", [13], 43.70), ("Napili 4-5", [14], 55.68), ("Honokeana", [16], 42.62),
        ("Ka'opala", [20], 62.05), ("Kahana", [22], 285.24), ("Mahinahina", [26], 44.87), ("Honokowai", [28], 61.97),
        ("Hanakaoo", [30], 25.87), ("Ka'anapali-Kahua", [31, 33], 25.12), ("Wahikuli", [35], 42.43)]
tot = 0; ut = 0; study = np.zeros(b.shape, bool)
print("subwatershed,usgs_t_yr,final_t_yr,pct_diff")
for n, ks, u in rows:
    m = (b > 0) & np.isin(ws, ks); study |= m; s = (b[m] * A[m]).sum(); tot += s; ut += u
    print(f"{n},{u:.2f},{s:.1f},{(s-u)/u*100:.1f}")
print(f"Total,{ut:.1f},{tot:.1f},{(tot-ut)/ut*100:.1f}")
v = b[study]; a = A[study]; t = v * a
for lab, lo in (("very high (>=19.31)", 19.3), ("high + very high (>=16.78)", 16.7)):
    s = v >= lo
    print(f"{lab}: {s.sum()} of {study.sum()} cells ({s.mean()*100:.1f}%), {t[s].sum()/t.sum()*100:.1f}% of erosion")
