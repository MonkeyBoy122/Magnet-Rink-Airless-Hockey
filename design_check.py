"""Candidate comparison: pull, drag, friction margin, plate sag. Estimates only - nothing here is measured."""
import numpy as np, magnet_pull as mp, json
E = 3.0e9          # Pa, printed PLA (layer-direction, conservative)
a_long, b_short = 0.200, 0.180   # rink half plate (m); short side drives deflection
alpha_ss, alpha_clamped = 0.138, 0.066   # Roark center point load, a/b ~1.1 (simply supported / fixed edges)
m_striker = 0.015  # kg, solid-PLA upper bound ~15 g
g = 9.81
rows = []
print(f"{'discs':>5} {'board':>5} {'wandgap':>7} {'gap':>5} {'Fz N':>6} {'Fx N':>6} {'sag SS':>7} {'sag cl':>7} {'sagSS/wg':>8} {'Fx/fric(mu.3)':>13} {'Fx/fric(mu.15)':>14}")
for n in (1, 2, 3):
    for bt in (2.0, 2.5, 3.0):
        for wg in (0.5, 1.0):
            gap = 1.0 + bt + wg
            L = n*3e-3
            fx_peak = 0; fz0 = None
            for dx in np.linspace(0, 12e-3, 25):
                fx, fz = mp.stack_force(L, gap*1e-3, dx)
                if fz0 is None: fz0 = abs(fz)
                fx_peak = max(fx_peak, abs(fx))
            t = bt*1e-3
            sag_ss = alpha_ss*fz0*b_short**2/(E*t**3)*1e3
            sag_cl = alpha_clamped*fz0*b_short**2/(E*t**3)*1e3
            n3  = fx_peak/(0.30*(fz0 + m_striker*g))
            n15 = fx_peak/(0.15*(fz0 + m_striker*g))
            rows.append(dict(discs=n, board=bt, wand_gap=wg, gap=gap, Fz=fz0, Fx=fx_peak, sag_ss=sag_ss, sag_cl=sag_cl, margin_mu30=n3, margin_mu15=n15))
            print(f"{n:5d} {bt:5.1f} {wg:7.1f} {gap:5.1f} {fz0:6.2f} {fx_peak:6.2f} {sag_ss:7.2f} {sag_cl:7.2f} {sag_ss/wg:8.2f} {n3:13.2f} {n15:14.2f}")
json.dump(rows, open("design_check.json","w"), indent=1)
