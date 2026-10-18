"""Estimate pull between two coaxial N52 disc stacks (equivalent magnetic-charge model).
Axial force Fz (attraction, presses striker onto board) and peak lateral force Fx (what drags the striker).
Usage: python3 magnet_pull.py
"""
import numpy as np, json
MU0 = 4e-7*np.pi
BR  = 1.45                     # T, N52 nominal (real lots vary 1.42-1.48)
M   = BR/MU0                   # A/m  -> surface pole density sigma = M
D   = 10e-3                    # magnet diameter, m
CELL= 0.4e-3

def disc_cells(r, cell):
    n = int(np.ceil(r/cell))
    xs = (np.arange(-n, n)+0.5)*cell
    X, Y = np.meshgrid(xs, xs)
    m = X**2+Y**2 <= r*r
    return X[m], Y[m], cell*cell

X, Y, dA = disc_cells(D/2, CELL)

def face_force(z_sep, dx, s1, s2):
    """force on face 2 (above, at z_sep) from face 1, charges s1,s2 (units of M). returns (Fx,Fz)"""
    ddx = (X[None,:]+dx) - X[:,None]
    ddy = (Y[None,:])    - Y[:,None]
    r2  = ddx**2 + ddy**2 + z_sep**2
    inv = 1.0/np.power(r2, 1.5)
    k = MU0/(4*np.pi) * (s1*M)*(s2*M) * dA*dA
    return k*np.sum(ddx*inv), k*np.sum(z_sep*inv)

def stack_force(L, gap, dx):
    """wand stack (length L) below, striker stack above; gap between wand top face and striker bottom face.
    attraction: wand top face +, striker bottom face -."""
    fx = fz = 0.0
    # wand faces: top (+1) at z=L, bottom (-1) at z=0 ; striker faces: bottom (-1) at z=L+gap, top (+1) at z=2L+gap
    for z1, s1 in ((L, +1), (0.0, -1)):
        for z2, s2 in ((L+gap, -1), (2*L+gap, +1)):
            a, b = face_force(z2-z1, dx, s1, s2)
            fx += a; fz += b
    return fx, fz

if __name__ == "__main__":
    h = 3e-3                                   # one disc thickness
    out = {}
    print("gap = felt 1.0 + board_t + wand air gap 0.5 (mm)")
    print(f"{'discs':>5} {'board':>6} {'gap':>5} {'pull Fz (N)':>12} {'peak drag Fx (N)':>17}")
    for n in (2, 3, 4):
        for bt in (2.0, 2.5, 3.0):
            gap = (1.0 + bt + 0.5)*1e-3
            L = n*h
            dxs = np.linspace(0, 12e-3, 25)
            fxs = []
            fz0 = None
            for dx in dxs:
                fx, fz = stack_force(L, gap, dx)
                if fz0 is None: fz0 = fz
                fxs.append(abs(fx))
            peak = max(fxs)
            print(f"{n:5d} {bt:6.1f} {gap*1e3:5.1f} {abs(fz0):12.2f} {peak:17.2f}")
            out[f"{n}_{bt}"] = dict(Fz=abs(fz0), Fx=peak, gap_mm=gap*1e3)
    json.dump(out, open("magnet_pull.json", "w"), indent=1)
