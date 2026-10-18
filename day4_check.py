import numpy as np, trimesh, json
from trimesh.proximity import closest_point
P='parts4/'
L=lambda n: trimesh.load(P+n+'.stl')
for n in ['rink_left','rink_right','wall_tl','wall_bl','wall_tr','wall_br','bridge','bracket_end','bracket_seam','striker','puck','wand']:
    m=L(n); print(f"{n:13s} watertight={m.is_watertight} bodies={len(m.split(only_watertight=False))} vol={m.volume:9.0f} size={np.round(m.extents,1)}")
l,r=L('rink_left'),L('rink_right')
inter=trimesh.boolean.intersection([l,r],engine='manifold'); print('left/right overlap mm3:', 0 if inter.is_empty else inter.volume)
for w in ['wall_tl','wall_bl']:
    i=trimesh.boolean.intersection([l,L(w)],engine='manifold'); print(w,'vs left plate overlap mm3:', 0 if i.is_empty else round(i.volume,3))
fr=L('frame_all'); br=L('bridges_all')
for nm,m in (('frame_all',fr),('bridges_all',br)):
    for side,plate in (('left',l),('right',r)):
        i=trimesh.boolean.intersection([plate,m],engine='manifold'); print(nm,'vs',side,'overlap mm3:', 0 if i.is_empty else round(i.volume,3))
# wall clip: opening and end wall
wl=L('walls_left'); print('walls_left bounds', np.round(wl.bounds,1).tolist())
# goal gap: check no wall material at x<-176, |y|<25
pts=wl.vertices; sel=(pts[:,0]<-175)&(np.abs(pts[:,1])<25); print('wall vertices inside goal opening:', int(sel.sum()))
# wand clearance (wand in place) vs frame, bridges, walls (walls are above, check anyway), plate+ribs excluded here
w=L('wand'); hx=138.0; pos=[(cx,cy) for cx in (-156.5,-90,-17.5) for cy in (-78.6,0,78.6)]
others={'frame':fr,'bridges':br}
res={}
for nm,m in others.items():
    dm=9
    for cx,cy in pos:
        wm=w.copy(); wm.apply_translation([cx-hx,cy,-1.0-8.0]); s=wm.sample(20000)
        # also the right half's bridges/frame are mirrored; wand left only, fine
        _,d,_=closest_point(m,s); dm=min(dm,float(d.min()))
    res[nm]=dm; print(f'min wand-to-{nm} distance over 9 positions: {dm:.2f} mm')
# also with the 4 screw-head groups
for nm in ('screws_frame','screws_bridge'):
    m=L(nm); dm=9
    for cx,cy in pos:
        wm=w.copy(); wm.apply_translation([cx-hx,cy,-1.0-8.0]); s=wm.sample(20000)
        _,d,_=closest_point(m,s); dm=min(dm,float(d.min()))
    res[nm]=dm; print(f'min wand-to-{nm} distance: {dm:.2f} mm')
json.dump(res,open('day4_check.json','w'))
# screw-hole alignment: pilot in wall at (x,98.05) vs hole in plate
print('side screw y centre', 100-3.9/2)
