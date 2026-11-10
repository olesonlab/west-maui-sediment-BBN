"""Reproduce the hotspot and scenario figures from the final-run rasters.
Inputs (unzip 03_data/WestMaui_R2R_data_for_Zach.zip to ./zach):
  zach/model_output/scenarios/baseline_ken.tif and scenario_*.tif  (final run)
  zach/spatial/subwatersheds/subws_WM_final_USGS.lpk (7z; extract .shp)
Clips to the 15 study subwatersheds (New_Number below)."""
import numpy as np, rasterio, shapefile, py7zr, os
from rasterio.features import rasterize
from shapely.geometry import shape, mapping
from shapely.ops import transform
from pyproj import Transformer
NAMED15=[2,4,6,8,9,13,14,16,20,22,26,28,30,31,35]
SC={'L_P':1,'L_R':2,'L_T':3,'L_P+R':4,'F_P':6,'R_200':7,'VH_T':8,'VH_P':12,'VH_A':10,'H_T':9,'H_P':13,'H_A':11}
if not os.path.exists('lpk'): py7zr.SevenZipFile('zach/spatial/subwatersheds/subws_WM_final_USGS.lpk').extractall('lpk')
def rd(f):
    with rasterio.open('zach/model_output/scenarios/'+f) as r:
        a=r.read(1).astype(float); a[a<-1e30]=np.nan; return a,r
b,r=rd('baseline_ken.tif')
tr=Transformer.from_crs('EPSG:26904','EPSG:4326',always_xy=True).transform
sf=shapefile.Reader('lpk/commondata/subwatersheds_uh/subws_WM_final_USGS.shp')
ws=rasterize([(mapping(transform(tr,shape(s.__geo_interface__))),rec['New_Number']) for s,rec in zip(sf.shapes(),sf.records())],out_shape=b.shape,transform=r.transform,fill=0,dtype='int32')
b=np.where(np.isin(ws,NAMED15),b,np.nan); S=np.nansum(b); n=int((b>0).sum())
print('stream cells in 15 subwatersheds',n)
for nm,sel in [('very high >19.3',b>19.3),('high >=16.78',b>=16.78)]:
    print(nm,int(sel.sum()),'cells',round(sel.sum()/n*100,1),'% of cells',round(b[sel].sum()/S*100,1),'% of erosion')
for nm,k in SC.items():
    s,_=rd(f'scenario_{k}.tif'); s=np.where(np.isfinite(b),s,np.nan)
    print(nm,'reduction %',round(100*(1-np.nansum(s)/S),2),'cells changed',int((np.abs(s-b)>1e-6).sum()))
