"""Day 3: trade board thickness / disc count against sag (FE) and drag margin. Estimates only."""
import sys, json
import numpy as np
sys.path.insert(0, 'tools')
import magnet_pull as mp
import sag_fe as fe

def pull(n, gap):
    fz0 = None; pk = 0
    for dx in np.linspace(0, 12e-3, 25):
        fx, fz = mp.stack_force(n*3e-3, gap*1e-3, dx)
        if fz0 is None: fz0 = abs(fz)
        pk = max(pk, abs(fx))
    return fz0, pk

POS = [(-162.5, 0), (-100, 0), (-60, 41), (-17.5, 0)]
rows = []
for n in (1, 2):
    for bt in (3.0, 3.5, 4.0, 4.5):
        gap = 1.0 + bt + 1.0
        Fz, Fx = pull(n, gap)
        fe.T0 = bt; fe.LOAD = Fz + 0.13
        for scen, kw in (('C ribs, sides only', dict(ribs=True, wall=False)),
                         ('E ribs + end wall', dict(ribs=True, wall=True))):
            t = fe.thickness(**kw)
            s = fe.solver(t, ('sides',))
            worst = 0
            for (cx, cy) in POS:
                c, m = fe.probe(s(cx, cy), cx, cy)
                worst = max(worst, m)
            rows.append(dict(discs=n, board=bt, gap=gap, Fz=Fz, Fx=Fx, scen=scen, sag=worst,
                             margin03=Fx/(0.30*(Fz+0.13)), margin015=Fx/(0.15*(Fz+0.13))))
            print(f"{n} disc  board {bt}  gap {gap}:  pull {Fz:4.2f} N  drag {Fx:4.2f} N  {scen:20s} worst sag {worst:4.2f} mm   margin mu.3 {rows[-1]['margin03']:.2f}")
json.dump(rows, open('day3_options.json', 'w'), indent=1)
