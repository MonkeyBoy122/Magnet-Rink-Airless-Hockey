"""Day 4: board sag with the real support layout: side ribs resting only on the leg brackets (40 mm each), optional bonded walls."""
import sys, json
import numpy as np
sys.path.insert(0, 'tools')
import sag_fe as fe
import magnet_pull as mp
from scipy.sparse.linalg import splu

fe.T0 = 4.0
Fz = abs(mp.stack_force(2*3e-3, 6.0e-3, 0.0)[1]); fe.LOAD = Fz + 0.13
x, y = fe.x, fe.y
RIB, WALL = fe.RIB_D, 12.0
side_in = fe.W_H/2 - fe.side_w            # 96.1
def thick(walls):
    t = np.full_like(x, fe.T0)
    t[(np.abs(y) > side_in) | (x > -fe.seam_w)] = fe.T0 + RIB
    if walls:
        t[(np.abs(y) > side_in) & (x < -8)] = fe.T0 + RIB + WALL
        t[(x < -174) & (np.abs(y) > 25)] = fe.T0 + WALL
    return t

def solver(t, spans):
    D = fe.E * t**3 / (12 * (1 - fe.NU**2))
    K = fe.stiff.assemble(fe.basis, D=D)
    def pred(p):
        on = np.isclose(np.abs(p[1]), fe.W_H/2)
        return on & np.any([(p[0] >= a - 1e-9) & (p[0] <= b + 1e-9) for a, b in spans], axis=0)
    fixed = fe.basis.get_dofs(pred).nodal['u']
    free = fe.basis.complement_dofs(fixed)
    lu = splu(K[free][:, free].tocsc())
    def solve(cx, cy):
        q = fe.LOAD / (np.pi * fe.PATCH_R**2) * (((x - cx)**2 + (y - cy)**2) < fe.PATCH_R**2)
        f = fe.load.assemble(fe.basis, q=q); u = np.zeros(fe.basis.N); u[free] = lu.solve(f[free]); return u
    return solve

POS = [(-156.5, 0), (-156.5, 78.6), (-120, 78.6), (-90, 78.6), (-80, 78.6), (-90, 0), (-60, 40), (-30, 78.6), (-17.5, 0), (-17.5, 78.6)]
SC = {
 'continuous side support, ribs only (Day 3 assumption)': (thick(False), [(-180, 0)]),
 'bracket-only support, ribs only (walls not bonded)':     (thick(False), [(-180, -140), (-20, 0)]),
 'bracket-only support, ribs + bonded walls':              (thick(True),  [(-180, -140), (-20, 0)]),
}
if __name__ == '__main__':
    out = {}
    print(f'pull {Fz:.2f} N (+0.13 N weight)')
    for name, (t, spans) in SC.items():
        s = solver(t, spans); rows = []
        for (cx, cy) in POS:
            c, m = fe.probe(s(cx, cy), cx, cy); rows.append(dict(x=cx, y=cy, head=m))
        w = max(r['head'] for r in rows); wp = max(rows, key=lambda r: r['head'])
        out[name] = dict(worst=w, at=(wp['x'], wp['y']), rows=rows)
        print(f"{name}\n   worst {w:.2f} mm at ({wp['x']},{wp['y']})")
    json.dump(out, open('day4_sag.json', 'w'), indent=1)
