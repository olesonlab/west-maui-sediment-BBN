"""Fig. 2: study area, analyzed subwatersheds and land tenure (vector redraw of the ArcGIS map).
Usage: fig2_map.py subws_WM_final_USGS.shp LandTenure.shp maui_outline.geojson|cb_2023_us_county_500k.shp out_prefix"""
import sys, os, numpy as np, shapefile, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch, Rectangle, Polygon as MPoly, PathPatch
from matplotlib.path import Path
from matplotlib.lines import Line2D
from shapely.geometry import shape, Point, box
from shapely.ops import unary_union, transform
from pyproj import Transformer
from PIL import Image
plt.rcParams.update({'font.family':'Liberation Sans','pdf.fonttype':42,'ps.fonttype':42,'font.size':8})
SUB,TEN,CTY,OUT=sys.argv[1:5]
NORTH=[2,4,6,8,9,13,14,16,20,22]; SOUTH=[26,28,30,31,35]; KAANAPALI=33   # Kāʻanapali is modeled with Kahua
NAMES={2:'Honolua',4:'Mokuleʻia Bay',6:'Kahauiki',8:'Mokupeʻa',9:'Honokahua',13:'Nāpili\n2-3',14:'Nāpili\n4-5',
       16:'Honokeana',20:'Kaʻōpala',22:'Kahana',26:'Māhinahina',28:'Honokōwai',30:'Hanakaʻōʻō',31:'Kahua',33:'Kāʻanapali',35:'Wahikuli'}
r=shapefile.Reader(SUB); ws={rec['New_Number']:shape(s.__geo_interface__).buffer(0) for s,rec in zip(r.shapes(),r.records())}
analyzed=NORTH+SOUTH+[KAANAPALI]
from shapely.geometry import Polygon
def solid(gs):                                   # merge, close slivers between neighbours, drop interior rings
    u=unary_union([g.buffer(2) for g in gs]).buffer(-2)
    return unary_union([Polygon(p.exterior) for p in getattr(u,'geoms',[u]) if p.area>1e4])
north=solid([g for k,g in ws.items() if k<=25]); south=solid([g for k,g in ws.items() if k>=26])
studied=unary_union([ws[k] for k in analyzed])
CLS=[('Kāʻanapali Dev.','#a47a57',{'Kaanapali Dev.'}),('Maui Land & Pine','#efbf5e',{'Maui Land & Pine'}),
     ('State','#5f8fbf',{'Govt. State'}),('State DHHL','#7cc35e',{'Govt. State DHHL'}),('Other','#fdf8c8',None)]
t=shapefile.Reader(TEN); polys={c[0]:[] for c in CLS}
for s,rec in zip(t.shapes(),t.records()):
    g=shape(s.__geo_interface__).buffer(0); own=rec['MajorOwner']
    lab=next((c[0] for c in CLS if c[2] and own in c[2]),'Other'); polys[lab].append(g)
W,H=174,146                                     # figure size, mm
fig=plt.figure(figsize=(W/25.4,H/25.4)); ax=fig.add_axes([0.025,0.02,0.92,0.925])
x0,y0,x1,y1=735000,2311300,754000,2327100
ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); ax.set_aspect('equal'); ax.set_xticks([]); ax.set_yticks([])
for sp in ax.spines.values(): sp.set_linewidth(0.8)
def draw(g,a=None,**kw):
    a=a or ax
    for p in getattr(g,'geoms',[g]):
        if p.is_empty or p.geom_type!='Polygon': continue
        rings=[np.asarray(p.exterior.coords)]+[np.asarray(h.coords) for h in p.interiors]
        verts=np.concatenate(rings); codes=np.concatenate([[Path.MOVETO]+[Path.LINETO]*(len(r)-2)+[Path.CLOSEPOLY] for r in rings])
        a.add_patch(PathPatch(Path(verts,codes),**kw))
draw(unary_union(list(ws.values())),fc='#d9d9d9',ec='none',zorder=1)          # unanalyzed watersheds
other_bg=studied
draw(other_bg,fc=dict((c[0],c[1]) for c in CLS)['Other'],ec='none',zorder=2)
for lab,col,_ in CLS[:4]:
    g=unary_union(polys[lab]).intersection(studied); draw(g,fc=col,ec='none',zorder=3)
for k in analyzed: draw(ws[k],fc='none',ec='black',lw=0.5,zorder=4)
for k,g in ws.items():
    if k not in analyzed: draw(g,fc='none',ec='#9a9a9a',lw=0.3,zorder=4)
draw(north,fc='none',ec='#1565e0',lw=2.0,zorder=5); draw(south,fc='none',ec='#e0198c',lw=2.0,zorder=5)
OFF={2:(600,600),4:(-2300,1500),6:(150,0),8:(400,-200),9:(1200,-1300),13:(0,150),14:(250,-150),16:(-300,100),20:(250,-250),22:(900,-200),
     26:(-200,250),28:(1300,100),30:(0,0),31:(-150,0),33:(-200,0),35:(0,-150)}
ROT={9:-58,16:-28,20:-28}
for k,nm in NAMES.items():
    p=ws[k].representative_point(); dx,dy=OFF.get(k,(0,0))
    if k==4:
        ax.annotate(nm,xy=(p.x,p.y),xytext=(p.x+dx,p.y+dy),fontsize=6.5,fontweight='bold',ha='center',va='center',zorder=7,
                    arrowprops=dict(arrowstyle='-',lw=0.5,color='black',shrinkA=1,shrinkB=0))
    else:
        ax.text(p.x+dx,p.y+dy,nm,fontsize=6.5,fontweight='bold',ha='center',va='center',rotation=ROT.get(k,0),zorder=7,linespacing=0.95)
# graticule ticks
tf=Transformer.from_crs(4326,32604,always_xy=True)
for lon in (-156.7,-156.6):
    for yy,va,off in ((y1,'bottom',120),):
        # find x on the top edge for this longitude
        lats=np.linspace(20.85,21.05,400); xs,ys=tf.transform(np.full_like(lats,lon),lats); x=np.interp(yy,ys,xs)
        ax.plot([x,x],[yy,yy-250],color='black',lw=0.6,clip_on=False); ax.text(x,yy+off,f'{-lon:.1f}°W',ha='center',va='bottom',fontsize=7)
for lat in (20.9,21.0):
    lons=np.linspace(-156.75,-156.55,400); xs,ys=tf.transform(lons,np.full_like(lons,lat)); y=np.interp(x1,xs,ys)
    ax.plot([x1,x1-250],[y,y],color='black',lw=0.6,clip_on=False); ax.text(x1+150,y,f'{lat:.1f}°N',rotation=90,ha='left',va='center',fontsize=7)
# legend
h=[Line2D([],[],color='#1565e0',lw=2.4,label='North'),Line2D([],[],color='#e0198c',lw=2.4,label='South'),
   Patch(fc='none',ec='black',lw=0.6,label='Analyzed'),Patch(fc='#d9d9d9',ec='#9a9a9a',lw=0.3,label='Not analyzed')]
l1=ax.legend(handles=h,title='Watershed regions',loc='upper left',bbox_to_anchor=(0.005,0.995),frameon=False,fontsize=7.5,title_fontsize=8.5,
             alignment='left',handlelength=2.2,borderaxespad=0.3)
ax.add_artist(l1)
h2=[Patch(fc=c,ec='#777777',lw=0.3,label=l) for l,c,_ in CLS]
ax.legend(handles=h2,title='Landowners',loc='upper left',bbox_to_anchor=(0.005,0.775),frameon=False,fontsize=7.5,title_fontsize=8.5,alignment='left',handlelength=2.2,borderaxespad=0.3)
# scale bar and north arrow
sx,sy=745300,2311700
for i in range(5): ax.add_patch(Rectangle((sx+i*1000,sy),1000,180,fc='black' if i%2==0 else 'white',ec='black',lw=0.5,zorder=8))
for i in range(6): ax.text(sx+i*1000,sy+300,str(i),ha='center',va='bottom',fontsize=7)
ax.text(sx+5000+250,sy+90,'km',ha='left',va='center',fontsize=7)
ax.annotate('',xy=(752700,2313600),xytext=(752700,2312300),arrowprops=dict(arrowstyle='-|>',lw=1,color='black',mutation_scale=10))
ax.text(752700,2313750,'N',ha='center',va='bottom',fontsize=9,fontweight='bold')
# inset: Maui
if CTY.endswith('.geojson'):
    import json; maui=shape(json.load(open(CTY))['features'][0]['geometry'])
else:                                            # US Census cartographic boundary counties
    c=shapefile.Reader(CTY); f=[x[0] for x in c.fields[1:]]
    for s_,rec in zip(c.shapes(),c.records()):
        d=dict(zip(f,rec))
        if d['STATEFP']=='15' and d['NAME']=='Maui':
            g=shape(s_.__geo_interface__); maui=[p for p in g.geoms if p.contains(Point(-156.3,20.8))][0]
import shapely; maui=shapely.transform(maui,lambda a: np.column_stack(tf.transform(a[:,0],a[:,1])))
ia=fig.add_axes([0.745,0.66,0.195,0.28]); ia.set_aspect('equal'); ia.set_xticks([]); ia.set_yticks([])
for sp in ia.spines.values(): sp.set_linewidth(0.6)
ia.add_patch(MPoly(np.asarray(maui.exterior.coords),fc='#cfcfcf',ec='#555555',lw=0.4))
sa=unary_union([north,south]).buffer(150)
ia.add_patch(MPoly(np.asarray(max(getattr(sa,'geoms',[sa]),key=lambda p:p.area).exterior.coords),fc='none',ec='red',lw=1.2))
bx=maui.bounds; pad=4000; ia.set_xlim(bx[0]-pad,bx[2]+pad); ia.set_ylim(bx[1]-pad-9000,bx[3]+pad)
isx=bx[0]+2000; isy=bx[1]-pad-6500
for i in range(2): ia.add_patch(Rectangle((isx+i*10000,isy),10000,1200,fc='black' if i==0 else 'white',ec='black',lw=0.4))
for i,v in enumerate((0,10,20)): ia.text(isx+i*10000,isy+1800,str(v),ha='center',va='bottom',fontsize=6.5)
ia.text(isx+20000+1200,isy+600,'km',ha='left',va='center',fontsize=6.5); ia.text(bx[2]-2000,bx[3]-2000,'Maui',ha='right',va='top',fontsize=7.5)
for ext in ('pdf','eps'): fig.savefig(OUT+'.'+ext)
fig.savefig(OUT+'.png',dpi=600)
fig.savefig(OUT+'_tmp.png',dpi=1200); Image.open(OUT+'_tmp.png').convert('RGB').save(OUT+'.tif',compression='tiff_lzw',dpi=(1200,1200)); os.remove(OUT+'_tmp.png')
