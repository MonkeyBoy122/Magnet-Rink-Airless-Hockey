# Journal Log: Day 4 (Magnet Rink: Airless Hockey)

**Goal for today:** finish the rink body: walls with a 50 mm goal, a way to hold the two halves down, and legs. This is a CAD-only day, nothing printed yet.

**Tools:** OpenSCAD (parametric modeling), Python (plate finite elements with scikit-fem, mesh checks with trimesh), M2 self-tapping screws as the only fasteners (hardware, no electronics).

> Draft note: the 10 entries below match the 10 renders (`day4_stage_01.png` to `day4_stage_10.png`). Edit times and wording to match what you actually did. Sag numbers are **model estimates, not measurements**. Distances between CAD parts are measured on the exported meshes.

---

## Hour 1: How a wall is fastened (image 1)

![Day 4, hour 1](../renders/day4/day4_stage_01.png)
Walls sit on top of the plate, exactly over the side ribs. An M2 self-tapping screw goes up from the rib underside through the rib (8 mm) and plate (4 mm) and bites 4 mm into the wall (a 1.8 mm pilot hole in the wall, 2.2 mm clearance holes below). That keeps the wall in one vertical stack with the rib, so it cannot be knocked off sideways. The screw head sits on the rib underside, away from the wand. This relies on the walls: they keep the striker, and so the wand head, at least 17.5 mm from the inner wall face, so the wand edge stays 4.5 mm or more from these screw heads. Without walls it would be only about 0.7 mm.

## Hour 2: Side walls (image 2)

![Day 4, hour 2](../renders/day4/day4_stage_02.png)
12 mm high, 3.9 mm thick, the same footprint as the rib below. 12 mm is twice the striker's straight wall (6 mm) and well above the puck (7 mm). Each side wall is one printable piece with four screws at x = -132, -96, -60 and -30. They stop 8 mm short of the seam, so the puck can cross centre ice.

## Hour 3: Player-end wall and the 50 mm goal (image 3)

![Day 4, hour 3](../renders/day4/day4_stage_03.png)
The end wall is 6 mm thick (so a screw head fits in a 4.4 mm counterbore) with a **50 mm goal opening**, a little under twice the 28 mm puck. The end wall joins the side wall, so each half has two L-shaped pieces (top and bottom). Each L has one screw from the top at the end wall (M2 x 10 into the plate). The wand handle still slides out underneath the board and wall, because the wall is above the plate.

## Hour 4: Both halves with walls (image 4)

![Day 4, hour 4](../renders/day4/day4_stage_04.png)
Both halves together, walls blue (left) and red (right). Four wall pieces in total, mirror pairs. The striker can now only get 17.5 mm from the inner face of the walls, so the play area is 78.6 mm either side of centre and 156.5 mm from the seam to the player end. That makes the Day 3 rib strips slightly conservative. I left them alone.

## Hour 5: Seam bridges (image 5)

![Day 4, hour 5](../renders/day4/day4_stage_05.png)
Day 3's dovetail locks the halves sideways but not up and down. So four small bridges (10 x 24 x 2 mm) go under the seam beams at y = -60, -20, 20 and 60 (between the tails), each with four M2 x 8 screws, two into each half. They also carry vertical shear across the seam, which the sag model assumed was free (safe side).

## Hour 6: Leg bracket (image 6)

![Day 4, hour 6](../renders/day4/day4_stage_06.png)
One bracket design: a 40 mm flange that sits under the side rib (two M2 x 8 screws into the rib), a 4 mm upright just outside the board edge, and a foot with two gussets. The table is 80 mm below the rib, so there is room under the board for the wand and a hand. The bracket sits outside the wand's reach (the handle never gets past 95.5 mm from the centre).

## Hour 7: Frame, six brackets (image 7)

![Day 4, hour 7](../renders/day4/day4_stage_07.png)
One at each player end and one at the seam, on each long side. The two seam brackets clamp both halves together and double as the seam hold-down. The whole table is about 84 mm from table to playing surface.

## Hour 8: Sag recheck with the real supports (image 8)

![Day 4, hour 8](../renders/day4/day4_stage_08.png)
Day 3's sag model assumed the side ribs rest on a continuous frame. Now they rest only on the brackets. Re-ran the finite-element model with supports only on the 40 mm bracket flanges (4.0 mm board, 2 discs, 5.4 N pull): worst sag **0.40 mm** (the same as continuous support, since the worst spot is at the free player end, next to a bracket). If the walls are bonded to the plate and rib (screws plus a glue line), it drops to **0.28 mm**. A striker at the seam end sags about 0.2 mm. The wand gap is 1.0 mm, so the margin is about 0.6 mm.

## Hour 9: Wand clearance to the new parts (image 9)

![Day 4, hour 9](../renders/day4/day4_stage_09.png)
Placed the wand at a 3 x 3 grid of positions (player end, middle, seam; both sides and centre) and measured the closest distance to each new part on the exported meshes: seam bridges **2.1 mm**, bridge screw heads **4.7 mm**, leg brackets **5.4 mm**, bracket screw heads **5.2 mm**. Together with Day 3's 0.6 mm to the ribs, nothing is tight except the ribs.

## Hour 10: Day 4 assembly (image 10)

![Day 4, hour 10](../renders/day4/day4_stage_10.png)
Everything together: both halves with walls on the frame, two strikers, the puck and two wands under the board. Exported the print files into `stl4/`: `rink_left.stl`, `rink_right.stl` (now with screw holes), the four wall pieces, `bridge.stl`, `bracket_end.stl` and `bracket_seam.stl` (same shape, different screw positions; print six brackets in total), plus `wand.stl`, `striker.stl` and `puck.stl` unchanged from Day 3. All are single closed solids. No overlaps between the plate, walls, bridges and frame (0 mm^3).

**Hardware list (M2 self-tapping, all estimates to confirm when ordering):** 16 x M2 x 16 (walls), 4 x M2 x 10 (end walls), 28 x M2 x 8 (12 bracket screws, 16 bridge screws). That is 48 screws.

---

## Plan for Day 5
1. Score counters (no electronics), probably a bead or flip counter behind each goal. Something has to catch the puck: the goal is currently an open gap at the plate edge.
2. Full assembly check, parts list, print order and tolerances in one sheet.
3. Final polish: fillets on the wall ends, labels, glue lines.

## Assumptions to verify when I get to printing
- Walls are 12 mm of PLA only 3.9 mm wide: they may flex. The 0.28 mm sag number assumes they are bonded to the plate.
- Self-tapping M2 screws into 1.8 mm pilot holes in printed PLA: the pilot size and the 4 mm engagement are guesses. Try them on a scrap piece.
- The model still uses PLA at 3.0 GPa. In PETG (about 2.1 GPa) the worst sag would be about 0.6 mm.
- The 80 mm table height has not been checked against your hand and the wand handle length.
- Whether a 183 x 200 mm plate with 8 mm ribs stays flat is still open from Day 3.
