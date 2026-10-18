"""Hour 13 image: FE deflection maps, 3.0 mm board (Day 2 setup) vs 4.0 mm board (Day 3). Estimates only."""
import sys, numpy as np
sys.path.insert(0, 'tools')
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
from PIL import Image, ImageDraw, ImageFont
import magnet_pull as mp
import sag_fe as fe

def pull(n, gap):
    return abs(mp.stack_force(n*3e-3, gap*1e-3, 0.0)[1])

cases = []
for bt in (3.0, 4.0):
    Fz = pull(2, 1.0 + bt + 1.0)
    fe.T0 = bt; fe.LOAD = Fz + 0.13
    s = fe.solver(fe.thickness(ribs=True, wall=False), ('sides',))
    cx, cy = -162.5, 0.0
    u = s(cx, cy)
    c, m = fe.probe(u, cx, cy)
    cases.append(dict(bt=bt, Fz=Fz, u=fe.nodal(u).copy(), head=m, gap=1.0 + bt + 1.0))
    print(bt, Fz, m)
vmax = 1.3
P = fe.mesh.p; T = fe.mesh.t
bg = '#DDE3EE'
fig = plt.figure(figsize=(10, 6.6), dpi=150, facecolor=bg)
axs = [fig.add_axes([0.04, 0.08, 0.40, 0.80]), fig.add_axes([0.50, 0.08, 0.40, 0.80])]
cax = fig.add_axes([0.93, 0.12, 0.014, 0.72])
levels = np.linspace(0, vmax, 27)
for ax, c in zip(axs, cases):
    ax.set_facecolor(bg)
    cf = ax.tricontourf(P[0], P[1], T.T, np.clip(c['u'], 0, vmax), levels=levels, cmap='YlOrRd')
    ax.tricontour(P[0], P[1], T.T, c['u'], levels=[1.0], colors=['#1b2a4a'], linewidths=1.4)
    ax.add_patch(Circle((-162.5, 0), 17.5, fill=False, ec='#1b2a4a', lw=1.2, ls='--'))
    ax.add_patch(Rectangle((-180, 100 - fe.side_w), 180, fe.side_w, fc='#3F7FE0', alpha=0.9, lw=0))
    ax.add_patch(Rectangle((-180, -100), 180, fe.side_w, fc='#3F7FE0', alpha=0.9, lw=0))
    ax.add_patch(Rectangle((-fe.seam_w, -100), fe.seam_w, 200, fc='#E5472C', alpha=0.9, lw=0))
    ax.set_xlim(-182, 2); ax.set_ylim(-102, 102); ax.set_aspect('equal'); ax.axis('off')
    ax.set_title(f"Board {c['bt']:.1f} mm   |   pull {c['Fz']:.1f} N\nworst sag under the wand head: {c['head']:.2f} mm",
                 fontsize=11, color='#1c1e28', pad=10)
    ax.text(-180, 0, 'player end\n(free)', rotation=90, ha='right', va='center', fontsize=8, color='#4a4f60')
    ax.text(1, 0, 'seam (free)', rotation=270, ha='left', va='center', fontsize=8, color='#4a4f60')
fig.text(0.47, 0.025, 'blue: side ribs, supported on the frame     red: seam beam, no support (free)     dashed: striker outline', ha='center', fontsize=8.5, color='#4a4f60')
cb = fig.colorbar(cf, cax=cax, ticks=[0, 0.25, 0.5, 0.75, 1.0, 1.25])
cb.set_label('board deflection (mm)', color='#1c1e28', fontsize=9)
cb.ax.tick_params(colors='#4a4f60', labelsize=8)
fig.savefig('png4/_sag_plot.png', facecolor=bg)

# same caption layout as the renders
W, H = 1500, 1125
im = Image.new('RGB', (W, H), (0xDD, 0xE3, 0xEE))
pl = Image.open('png4/_sag_plot.png').convert('RGB')
pl = pl.resize((int(pl.width * 0.95), int(pl.height * 0.95)))
im.paste(pl, ((W - pl.width) // 2, 30))
d = ImageDraw.Draw(im)
fb = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", int(W * 0.026))
fr = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", int(W * 0.0165))
pad = int(W * 0.035)
d.text((pad, H - pad - int(W * 0.062)), "Hour 13  |  Board sag estimate (finite elements)", font=fb, fill=(28, 30, 40))
d.text((pad, H - pad - int(W * 0.026)), "Striker at the free player end. 3.0 mm board sags 1.2 mm, 4.0 mm board 0.4 mm. Black line = 1.0 mm wand gap", font=fr, fill=(95, 100, 115))
tag = "Magnet Rink: Airless Hockey  |  Day 3"
d.text((W - pad - d.textlength(tag, font=fr), pad * 0.8), tag, font=fr, fill=(120, 125, 140))
im.save('png4/day3_stage_13.png')
im2 = Image.open('png4/_sag_plot.png'); im2.save('png4/day3_stage_13_raw.png')
print('ok')
