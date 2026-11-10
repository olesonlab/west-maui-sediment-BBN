"""Rasterize the subwatershed polygons onto the final ARIES raster grid.
Usage: python make_ws_index.py subws_WM_final_USGS.shp baseline_ken.tif ws_ken.npy
Cell values are the polygon New_Number field (0 = outside all subwatersheds).
The 15 modeled subwatersheds are New_Number 2,4,6,8,9,13,14,16,20,22,26,28,30,31,35."""
import sys, numpy as np, shapefile, rasterio
from rasterio.features import rasterize
from shapely.geometry import shape, mapping
from shapely.ops import transform
from pyproj import Transformer
shp, ras, out = sys.argv[1:4]
tr = Transformer.from_crs('EPSG:26904', 'EPSG:4326', always_xy=True).transform
sf = shapefile.Reader(shp)
with rasterio.open(ras) as r:
    T, sh = r.transform, r.shape
shapes = [(mapping(transform(tr, shape(s.__geo_interface__))), rec['New_Number']) for s, rec in zip(sf.shapes(), sf.records())]
np.save(out, rasterize(shapes, out_shape=sh, transform=T, fill=0, dtype='int32'))
