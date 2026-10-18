import sys; sys.path.insert(0,'tools')
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
from PIL import Image, ImageDraw, ImageFont
import day4_sag as d4, sag_fe as fe
P=fe.mesh.p; T=fe.mesh.t; bg='#DDE3EE'
cases=[('Ribs only (walls not bonded)', d4.SC['bracket-only support, ribs only (walls not bonded)']),
       ('Ribs + bonded walls', d4.SC['bracket-only support, ribs + bonded walls'])]
res=[]
for name,(t,spans) in cases:
    s=d4.solver(t,spans); cx,cy=-156.5,0.0; u=s(cx,cy); c,m=fe.probe(u,cx,cy); res.append((name,fe.nodal(u).copy(),m,spans))
vmax=0.5
fig=plt.figure(figsize=(10,6.6),dpi=150,facecolor=bg)
axs=[fig.add_axes([0.04,0.08,0.40,0.80]),fig.add_axes([0.50,0.08,0.40,0.80])]; cax=fig.add_axes([0.93,0.12,0.014,0.72])
lv=np.linspace(0,vmax,26)
for ax,(name,u,m,spans) in zip(axs,res):
    ax.set_facecolor(bg)
    cf=ax.tricontourf(P[0],P[1],T.T,np.clip(u,0,vmax),levels=lv,cmap='YlOrRd')
    ax.add_patch(Circle((-156.5,0),17.5,fill=False,ec='#1b2a4a',lw=1.2,ls='--'))
    for a,b in spans:
        for yy in (100,-100): ax.add_patch(Rectangle((a,yy-(3 if yy>0 else -0)),b-a,3,fc='#2EA89A',lw=0,clip_on=False))
    ax.add_patch(Rectangle((-fe.seam_w,-100),fe.seam_w,200,fc='#E5472C',alpha=0.9,lw=0))
    ax.set_xlim(-182,2); ax.set_ylim(-104,104); ax.set_aspect('equal'); ax.axis('off')
    ax.set_title(f"{name}\nworst sag under the wand head: {m:.2f} mm",fontsize=11,color='#1c1e28',pad=10)
    ax.text(-180,0,'player end\n(free)',rotation=90,ha='right',va='center',fontsize=8,color='#4a4f60')
    ax.text(1,0,'seam (free)',rotation=270,ha='left',va='center',fontsize=8,color='#4a4f60')
fig.text(0.47,0.025,'teal: leg brackets (the only side supports)     red: seam beam, free     dashed: striker at the worst spot',ha='center',fontsize=8.5,color='#4a4f60')
cb=fig.colorbar(cf,cax=cax,ticks=[0,0.1,0.2,0.3,0.4,0.5]); cb.set_label('board deflection (mm)',color='#1c1e28',fontsize=9); cb.ax.tick_params(colors='#4a4f60',labelsize=8)
fig.savefig('png5/_sag_plot.png',facecolor=bg)
W,H=1500,1125; im=Image.new('RGB',(W,H),(0xDD,0xE3,0xEE)); pl=Image.open('png5/_sag_plot.png').convert('RGB'); pl=pl.resize((int(pl.width*.95),int(pl.height*.95))); im.paste(pl,((W-pl.width)//2,30))
d=ImageDraw.Draw(im); fb=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",int(W*.026)); fr=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",int(W*.0165)); pad=int(W*.035)
d.text((pad,H-pad-int(W*.062)),"Hour 8  |  Sag recheck with the real supports",font=fb,fill=(28,30,40))
d.text((pad,H-pad-int(W*.026)),"Ribs on the 40 mm brackets only: 0.40 mm, or 0.28 mm if the walls are bonded on. Wand gap is 1.0 mm",font=fr,fill=(95,100,115))
tag="Magnet Rink: Airless Hockey  |  Day 4"; d.text((W-pad-d.textlength(tag,font=fr),pad*.8),tag,font=fr,fill=(120,125,140))
im.save('png5/day4_stage_08.png'); Image.open('png5/_sag_plot.png').save('png5/day4_stage_08_raw.png'); print('ok')
