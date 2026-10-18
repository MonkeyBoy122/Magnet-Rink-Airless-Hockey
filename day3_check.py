import numpy as np, trimesh, json
P = 'parts3/'
def L(n): return trimesh.load(P + n + '.stl')
out = {}
for n in ['striker','puck','wand','rink_left','rink_right','test_joint_a','test_joint_b','ribs_seam','ribs_sides']:
    m = L(n); out[n] = dict(watertight=bool(m.is_watertight), volume=round(float(m.volume),1), bounds=np.round(m.bounds,2).tolist(), bodies=len(m.split(only_watertight=False)))
    print(f"{n:14s} watertight={m.is_watertight} vol={m.volume:9.1f} mm3 bodies={out[n]['bodies']}  size={np.round(m.extents,1)}")
l, r = L('rink_left'), L('rink_right')
try:
    inter = trimesh.boolean.intersection([l, r], engine='manifold')
    iv = float(inter.volume) if not inter.is_empty else 0.0
except Exception as e:
    iv = None; print('boolean failed', e)
print('left/right overlap volume (mm3):', iv)
# minimum gap between halves at the seam (surface sampling)
pts = l.sample(60000)
from trimesh.proximity import closest_point
_, d, _ = closest_point(r, pts)
# only pts near the seam
sel = np.abs(pts[:,0]) < 8
print('min distance left->right near seam: %.3f mm (expect ~0.20)' % d[sel].min())
tja, tjb = L('test_joint_a'), L('test_joint_b')
pa = tja.sample(60000); _, dd, _ = closest_point(tjb, pa); s = np.abs(pa[:,0]) < 8
print('test joint min distance: %.3f' % dd[s].min())
# per-clearance gap: sample points at tail flanks near y=-30,0,30
for y in (-30,0,30):
    q = (np.abs(pa[:,1]-y) < 8) & s
    print('  y=%+d gap %.3f' % (y, dd[q].min()))
# wand vs ribs clearance at extreme striker positions (wand in place, z top at -1)
w = L('wand'); hx = 138.0
res = []
for cx in (-162.5, -90, -17.5):
    for cy in (-82.5, 0, 82.5):
        wm = w.copy(); wm.apply_translation([cx - hx, cy, -1.0 - 8.0])
        for name, m in (('left', l),):
            sp = wm.sample(30000)
            _, dist, _ = closest_point(m, sp)
            # ignore the plate itself: only ribs matter, plate is >=1 mm above by construction; report overall min
            res.append((cx, cy, float(dist.min())))
for c in res: print('wand head at (%.1f,%.1f): min wand-to-rink distance %.2f mm' % c)
out['overlap'] = iv; out['wand_clear'] = res
json.dump(out, open('day3_check.json','w'), indent=1)
