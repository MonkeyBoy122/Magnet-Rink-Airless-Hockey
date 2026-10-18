"""Day 3: plate-bending finite-element estimate of board sag under a striker.

Kirchhoff plate, Morley triangles (scikit-fem). One rink half, 180 x 200 mm, 3.0 mm plate.
Ribs are modelled as strips of thicker plate (thickness = plate + rib depth), which is a
beam-like approximation (rectangular section 3.9 mm wide). Corner radii are ignored.
Load = striker pull + weight, spread uniformly over the pad patch (r = 14.8 mm).
All numbers are MODEL ESTIMATES (E = 3.0 GPa printed PLA, nu = 0.35), not measurements.

Usage: python3 tools/sag_fe.py            -> prints table, writes sag_fe.json and sag_map.npz
"""
import json, sys
import numpy as np
from scipy.sparse.linalg import splu
from skfem import MeshTri, Basis, BilinearForm, LinearForm
from skfem.element import ElementTriMorley
from skfem.helpers import dd, ddot, trace

E, NU = 3000.0, 0.35            # N/mm^2, -
T0 = 3.0                         # plate thickness
H = 2.0                          # mesh size (mm)
LOAD = 7.1 + 0.13                # N: pull (2 discs at 5.0 mm gap) + striker weight
PATCH_R = 14.8
W_L, W_H = 180.0, 200.0          # half size

# rib layout (matches day3.scad): side strips beyond the wand handle, seam strip beyond the wand tip
WAND_W = float(sys.argv[1]) if len(sys.argv) > 1 else 26.0
STRIKER_R = 17.5
CLEAR = 0.6
RIB_D = 8.0
side_w = W_H/2 - (W_H/2 - STRIKER_R + WAND_W/2 + CLEAR)     # strip width at each long side
seam_w = STRIKER_R - 12.0 - CLEAR                           # strip width at the seam

mesh = MeshTri.init_tensor(np.arange(-W_L, 0 + 1e-9, H), np.arange(-W_H/2, W_H/2 + 1e-9, H))
basis = Basis(mesh, ElementTriMorley())
X = basis.global_coordinates().value
x, y = X[0], X[1]


def thickness(ribs=True, wall=False, wall_t=3.0, wall_h=12.0, goal=50.0, rib_d=RIB_D):
    t = np.full_like(x, T0)
    if ribs:
        m = (np.abs(y) > W_H/2 - side_w) | (x > -seam_w)
        t[m] = T0 + rib_d
    if wall:       # Day 4 idea: end wall clipped on the player end, with a goal gap
        m = (x < -W_L + wall_t) & (np.abs(y) > goal/2)
        t[m] = T0 + wall_h
    return t


@BilinearForm
def stiff(u, v, w):
    return w['D'] * ((1 - NU) * ddot(dd(u), dd(v)) + NU * trace(dd(u)) * trace(dd(v)))


@LinearForm
def load(v, w):
    return w['q'] * v


def solver(t, support):
    D = E * t**3 / (12 * (1 - NU**2))
    K = stiff.assemble(basis, D=D)
    fixed = set()
    if 'sides' in support:
        fixed |= set(basis.get_dofs(lambda p: np.isclose(np.abs(p[1]), W_H/2)).nodal['u'].tolist())
    if 'seam' in support:
        fixed |= set(basis.get_dofs(lambda p: np.isclose(p[0], 0)).nodal['u'].tolist())
    if 'end' in support:
        fixed |= set(basis.get_dofs(lambda p: np.isclose(p[0], -W_L)).nodal['u'].tolist())
    fixed = np.array(sorted(fixed), dtype=int)
    free = basis.complement_dofs(fixed)
    lu = splu(K[free][:, free].tocsc())

    def solve(cx, cy):
        q = LOAD / (np.pi * PATCH_R**2) * (((x - cx)**2 + (y - cy)**2) < PATCH_R**2)
        f = load.assemble(basis, q=q)
        u = np.zeros(basis.N)
        u[free] = lu.solve(f[free])
        return u
    return solve


def nodal(u):
    """vertex deflection values (Morley: first N_vertices dofs are vertex values)"""
    return u[:mesh.p.shape[1]]


def probe(u, cx, cy, r=12.0):
    """deflection at striker centre and the max within the wand head footprint (r = 12)"""
    P = mesh.p
    d = np.hypot(P[0] - cx, P[1] - cy)
    v = nodal(u)
    return float(v[np.argmin(d)]), float(v[d < r].max())


SCENARIOS = {
    # name: (rib layout, edge supports)
    'A  day-2 assumption: no ribs, all 4 edges simply supported': dict(ribs=False, wall=False, support=('sides', 'seam', 'end')),
    'B  no ribs, long sides only (seam and end free)':            dict(ribs=False, wall=False, support=('sides',)),
    'C  ribs, long sides only (seam and end free)':               dict(ribs=True, wall=False, support=('sides',)),
    'D  ribs, sides + seam supported (seam joint carries shear)': dict(ribs=True, wall=False, support=('sides', 'seam')),
    'E  ribs + Day-4 end wall, long sides only':                  dict(ribs=True, wall=True, support=('sides',)),
}
POS = [(-162.5, 0), (-162.5, 82.5), (-100, 0), (-100, 82.5), (-60, 41), (-17.5, 0), (-17.5, 82.5), (-17.5, -82.5)]

if __name__ == '__main__':
    out = {}
    for name, cfg in SCENARIOS.items():
        t = thickness(cfg['ribs'], cfg['wall'])
        s = solver(t, cfg['support'])
        rows = []
        for (cx, cy) in POS:
            u = s(cx, cy)
            c, m = probe(u, cx, cy)
            rows.append(dict(x=cx, y=cy, centre=c, head_max=m))
        worst = max(r['head_max'] for r in rows)
        out[name] = dict(rows=rows, worst=worst)
        print(f"{name}\n   worst deflection in wand-head footprint: {worst:.2f} mm")
        for r in rows:
            print(f"      striker at ({r['x']:7.1f},{r['y']:6.1f}):  centre {r['centre']:.2f}  head max {r['head_max']:.2f}")
    json.dump(dict(side_w=side_w, seam_w=seam_w, load=LOAD, E=E, results=out), open('sag_fe.json', 'w'), indent=1)
