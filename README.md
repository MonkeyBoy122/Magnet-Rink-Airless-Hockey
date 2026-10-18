# Magnet Rink: Airless Hockey

A tabletop hockey game with **no electronics and no air**. Each player holds a wand *under* a clear-topped board. Two stacked N52 magnets in the wand drag a magnetic striker across the top, and the strikers knock a non-magnetic puck around. Everything is 3D printed except the magnets, felt/PTFE pads and M2 screws.

![Day 4 assembly: rink on its frame, walls and goals, two strikers, puck, wands under the board](renders/day4/day4_stage_10.png)

**Status:** the full CAD is done through Day 4 (parts, walls, goals, seam joint, frame). **Nothing has been printed or tested yet.** Every pull, sag and friction number in this repo comes from a model, not a measurement, and is labelled as an estimate in the journals. Still to do (Day 5 of the plan): goal catch tray with a score counter, a full parts/print-order sheet, and final polish.

## How it works

| | |
|---|---|
| Magnets | 2 stacked N52 discs, 10 x 3 mm, in each striker and each wand, both N-up, so striker and wand attract and the two strikers repel |
| Gap between magnet stacks | 6.0 mm = 1.0 pad + 4.0 board + 1.0 wand clearance |
| Pull / peak drag (model) | about 5.4 N pull, 2.6 N peak sideways force at that gap. Friction margin about 1.6 at a friction coefficient of 0.3 |
| Striker | 35 mm wide, 21.5 mm tall, prints knob-down with no supports |
| Puck | 28 x 7 mm, non-magnetic, skid recess on the underside |
| Wand | 150 x 26 x 8 mm, 24 mm head with a pocket for the magnets |
| Rink | 360 x 200 mm in two halves (183 x 200 mm each, fits a 220 mm bed), 4.0 mm plate, 8 mm deep underside ribs, 12 mm walls, 50 mm goals |
| Seam | planar dovetail (5 tails, 15 degree flanks, 0.2 mm clearance) plus four screwed bridges that hold the halves down |
| Table | six leg brackets, 80 mm from rib to table |

## Tolerances (all parameters in `cad/day4.scad`)

| Fit | Value |
|---|---|
| Magnet pocket | 10.2 mm for a 10 mm magnet (0.2 mm radial clearance), 0.1 mm extra depth for glue |
| Dovetail tail and socket | 0.2 mm per flank, tuned with `stl/final/test_joint_a.stl` + `test_joint_b.stl` (three pairs: 0.1, 0.2, 0.3 mm) |
| Seam gap | each half stops 0.1 mm short of the seam line, 0.2 mm total |
| Wand to ribs | 0.6 mm minimum (measured on the meshes); to bridges 2.1 mm, to brackets 5.4 mm |
| Screws | M2 self-tapping: 1.8 mm pilot, 2.2 mm clearance hole, 4.4 mm counterbore |
| Engraved lines | 1.2 mm wide, 0.25 mm deep (`line_depth`, set to 0 if they affect puck glide) |

## Parts list

| Part | File (`stl/final/`) | Qty |
|---|---|---|
| Rink half, left | `rink_left.stl` | 1 |
| Rink half, right | `rink_right.stl` | 1 |
| Walls (4 L-shaped pieces) | `wall_tl.stl`, `wall_bl.stl`, `wall_tr.stl`, `wall_br.stl` | 1 each |
| Seam bridge | `bridge.stl` | 4 |
| Leg bracket, player end | `bracket_end.stl` | 4 |
| Leg bracket, seam | `bracket_seam.stl` | 2 |
| Striker | `striker.stl` | 2 |
| Wand | `wand.stl` | 2 |
| Puck | `puck.stl` | 1 |
| Dovetail test joint | `test_joint_a.stl`, `test_joint_b.stl` | 1 pair, print first |
| Magnet pull test coupon | `pull_test_coupon.stl` | 1 (still the 2.0/2.5/3.0 mm Day 1 steps; add a 4.0 mm step before use) |

**Hardware:** 8 x N52 disc magnets 10 x 3 mm, 2 felt or PTFE pads (30 mm, 1 mm thick), 16 x M2 x 16, 4 x M2 x 10, 28 x M2 x 8 self-tapping screws.

**Printing:** rink halves plate-down (ribs up, no supports); strikers knob-down; walls, bridges and brackets as exported. All parts are single closed solids (checked with trimesh).

## Repo layout

| Folder | What is in it |
|---|---|
| `cad/` | OpenSCAD source: `day4.scad` is the current model, `day1` to `day3` are the earlier versions. Export a part with `openscad -D 'part="rink_left"' -o rink_left.stl cad/day4.scad` |
| `stl/final/` | the current print set. `stl/day1` to `stl/day4` hold each day's exports |
| `journal/` | `BUILD_LOG_ALL_DAYS.md` (everything, with all images) and one journal per day |
| `renders/` | 51 ray-traced renders, one per journal hour (Day 1: 11, Day 2: 15, Day 3: 15, Day 4: 10) |
| `analysis/` | the magnet-pull model, the plate-bending finite-element sag model, mesh and clearance checks, and their outputs |
| `render/` | the Blender script and stage files used for the renders |

## What changed along the way

| | Day 1 | Now |
|---|---|---|
| Board thickness | 2.5 mm | 4.0 mm (a finite-element check showed 3.0 mm would sag about 1.2 mm at the free player end, more than the wand gap) |
| Magnet gap | 4.0 mm | 6.0 mm |
| Striker magnets | dipped 0.8 mm into the felt recess (Day 1 bug) | sit above the pad |
| Wand handle | 30 mm wide | 26 mm wide, so side ribs fit |

## Day by day

**Day 1: coupon, striker, wand.** [journal](journal/journal_day1.md)

![](renders/day1/day1_stage_11.png)

**Day 2: magnet and sag model, fixes, puck, first rink half.** [journal](journal/journal_day2.md)

![](renders/day2/day2_stage_15.png)

**Day 3: ribs, dovetail seam, test joint, thicker board.** [journal](journal/journal_day3.md)

![](renders/day3/day3_stage_12.png)

![](renders/day3/day3_stage_13.png)

**Day 4: walls, goals, seam bridges, leg frame.** [journal](journal/journal_day4.md)

![](renders/day4/day4_stage_04.png)

![](renders/day4/day4_stage_07.png)

## Honest limits

- Nothing is printed. Pull, sag and friction come from models (N52 at 1.45 T, printed PLA at 3.0 GPa, friction coefficient 0.15 to 0.3), and PETG would sag more (about 0.6 mm instead of 0.4).
- Plate flatness over 200 mm with 8 mm ribs, the screw pilot sizes, and the 0.2 mm dovetail clearance all need a print to confirm.
- Journals are drafts: edit the hours to match your real work.
