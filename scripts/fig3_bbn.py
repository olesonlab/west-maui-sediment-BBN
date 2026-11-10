"""Redraw Fig. 3 (BBN structure) as vector art from the GeNIe model file ChannelErosionSource.xdsl."""
import re, sys, itertools, numpy as np, matplotlib
from PIL import Image
XDSL=sys.argv[1] if len(sys.argv)>1 else "ChannelErosionSource.xdsl"
OUT=sys.argv[2] if len(sys.argv)>2 else "Fig3"
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
plt.rcParams.update({'font.family':'Liberation Sans','pdf.fonttype':42,'ps.fonttype':42,'font.size':7.5})
s=open(XDSL,encoding='latin-1').read()
D,F,S,C=[np.array(x.split(),float) for x in re.findall(r'<probabilities>(.*?)</probabilities>',s)]
C=C.reshape(2,3,4,5)                      # parents: FillTerrace, Susceptibility, DisturbanceType
child=np.einsum('f,s,d,fsdc->c',F,S,D,C)
def infl(ax):                             # average Euclidean distance between child distributions
    Cm=np.moveaxis(C,ax,0); n=Cm.shape[0]
    return np.mean([np.mean([np.linalg.norm(Cm[(i,)+ix]-Cm[(j,)+ix]) for i,j in itertools.combinations(range(n),2)])
                    for ix in itertools.product(*[range(k) for k in Cm.shape[1:-1]])])
I={'FillTerrace':infl(0),'Susceptibility':infl(1),'DisturbanceType':infl(2)}
nodes={
 'BankErosion':(['Very high','High','Moderate','Low','Very low'],child,(62,42)),
 'DisturbanceType':(['Feral pigs','Road crossing','Multiple disturbance','Undisturbed'],D,(2,2)),
 'FillTerrace':(['Present','Absent'],F,(62,10.4)),
 'Susceptibility':(['High','Moderate','Low'],S,(122,6.2)),
}
W,RH,HH,LW,PW,BW=48,4.2,4.8,25,8,13     # node width, row height, header height, label/pct/bar widths (mm)
fig=plt.figure(figsize=(174/25.4,70/25.4)); ax=fig.add_axes([0,0,1,1]); ax.set_xlim(0,174); ax.set_ylim(0,70); ax.axis('off')
box={}
for nm,(st,p,(x,y)) in nodes.items():
    h=HH+RH*len(st); box[nm]=(x,y,h)
    ax.add_patch(Rectangle((x,y),W,h,fc='white',ec='#1f2d5a',lw=0.8))
    ax.add_patch(Rectangle((x,y+h-HH),W,HH,fc='#dbe4f0',ec='#1f2d5a',lw=0.8))
    ax.text(x+W/2,y+h-HH/2,nm,ha='center',va='center',fontweight='bold')
    for k,(lab,v) in enumerate(zip(st,p)):
        yy=y+h-HH-RH*(k+0.5)
        ax.text(x+1.2,yy,lab,va='center'); ax.text(x+LW+PW,yy,f'{100*v:.0f}%',va='center',ha='right')
        ax.add_patch(Rectangle((x+LW+PW+1.2,yy-1.2),BW*v,2.4,fc='#3b6aa0',ec='none'))
        ax.add_patch(Rectangle((x+LW+PW+1.2,yy-1.2),BW,2.4,fc='none',ec='#9aa7b8',lw=0.3))
cx,cy,ch=box['BankErosion']
tgt={'DisturbanceType':(cx+6,cy),'FillTerrace':(cx+W/2,cy),'Susceptibility':(cx+W-6,cy)}
mx=max(I.values())
for nm,(tx,ty) in tgt.items():
    x,y,h=box[nm]; lw=0.6+3.4*I[nm]/mx
    ax.add_patch(FancyArrowPatch((x+W/2,y+h),(tx,ty),arrowstyle='-|>',mutation_scale=6+2*lw,lw=lw,color='#1f2d5a',shrinkA=0,shrinkB=0))
for ext in ('pdf','eps'): fig.savefig(OUT+'.'+ext)
fig.savefig(OUT+'.png',dpi=600)
import os; fig.savefig(OUT+'_tmp.png',dpi=1200); Image.open(OUT+'_tmp.png').convert('RGB').save(OUT+'.tif',compression='tiff_lzw',dpi=(1200,1200)); os.remove(OUT+'_tmp.png')
print({k:round(v,3) for k,v in I.items()}, np.round(child*100,1))
