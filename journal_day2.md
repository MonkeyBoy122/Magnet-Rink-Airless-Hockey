# Journal Log: Day 2 (Magnet Rink: Airless Hockey)

**Goal for today:** lock in the physics on paper, fix and finish the striker and wand, model the puck, and start the rink top. This is a CAD-only day, nothing printed yet. The plan said "test the coupon", so instead I built a numerical model of the magnet pull to choose the board thickness and gap. The coupon from Day 1 is still the real test for later.

**Tools:** OpenSCAD (parametric modeling), a small Python model of magnet force, N52 10 x 3 mm disc magnets, planned PLA/PETG.

> Draft note: the 15 entries below match the 15 renders (`day2_stage_01.png` to `day2_stage_15.png`). Edit times and wording to match what you actually did. All pull, sag and friction numbers are **model estimates, not measurements**.

---

## Hour 1: Magnet pull model (image 1)

![Day 2, hour 1](../renders/day2/day2_stage_01.png)
Wrote a Python model of two coaxial disc-magnet stacks (equivalent magnetic-charge method, N52 at 1.45 T). Checked it against the standard dipole formula at long range (within 4% at 80 mm, converging as the gap grows) and checked that the answer stops moving as the mesh gets finer (about 2%). Then compared 1, 2 and 3 discs per side. Two findings:
- **Pull at the 5.0 mm gap:** 1 disc 3.4 N, 2 discs 7.1 N, 3 discs 9.4 N.
- **Drag-to-pull ratio is about 0.48 for every stack.** The sideways force that drags the striker is always about half the downward pull, and the downward pull is also what creates friction. So stronger magnets don't make the striker more responsive in ratio terms. The surface friction does. That makes the pad material the most important choice, so PTFE tape over felt is better than felt alone.

## Hour 2: Gap budget and board thickness (image 2)

![Day 2, hour 2](../renders/day2/day2_stage_02.png)
Added up the gap between the two magnet stacks: pad 1.0 + board + wand clearance. Then estimated how much the plate sags under the pull (plate formula, 3.0 GPa printed PLA, a 180 x 200 mm half held at its edges, which assumes the clip-on walls stiffen all four edges). With the Day 1 values (2.5 mm board, 0.5 mm clearance) the sag was **0.4 to 0.9 mm, more than the 0.5 mm clearance**, so the board would rest on the wand and rub. Changed to a **3.0 mm board and 1.0 mm clearance**: gap 5.0 mm, sag 0.2 to 0.4 mm, well inside the clearance. I kept 2 discs per side because they give about twice the spare drag force of 1 disc (about 1.2 N vs 0.6 N at a friction coefficient of 0.3), without the heavier board load of 3 discs.

| Config (2 discs) | Gap | Pull | Peak drag | Est. sag | Sag vs clearance |
|---|---|---|---|---|---|
| Day 1: board 2.5, clearance 0.5 | 4.0 mm | 9.5 N | 4.5 N | 0.4 to 0.9 mm | too close, would rub |
| **Day 2: board 3.0, clearance 1.0** | **5.0 mm** | **7.1 N** | **3.4 N** | **0.2 to 0.4 mm** | **fine** |

## Hour 3: Striker bug fix (image 3)

![Day 2, hour 3](../renders/day2/day2_stage_03.png)
While checking the stack-up I found a Day 1 error: the magnet pocket started at the bottom face, so the two stacked magnets dipped 0.8 mm into the 1 mm felt recess and left almost no room for the pad. Moved the pocket so it starts at the recess ceiling. The magnets now sit above the pad with 0.1 mm to spare. Confirmed with a mesh check: zero overlap between the striker, magnets and pad.

## Hour 4: Striker v2 shape (image 4)

![Day 2, hour 4](../renders/day2/day2_stage_04.png)
Reshaped the striker into a 6 mm wall, a 45 degree shoulder, and a 16 mm knob with a rounded top, 21.5 mm tall in total. Replaced the polarity dimple with an engraved **N** (0.5 mm) on the knob top. Solid PLA would be about 13 g.

## Hour 5: Striker print orientation (image 5)

![Day 2, hour 5](../renders/day2/day2_stage_05.png)
Checked how it would print: knob-down on the bed. That puts the pad recess and magnet pocket facing up, so there is no bridging over open cavities, and the 45 degree shoulder is at the usual limit for printing without supports. The engraved N ends up on the first layer, so it comes out crisp.

## Hour 6: Wand v2 (image 6)

![Day 2, hour 6](../renders/day2/day2_stage_06.png)
Pocket depth now equals the stack height plus 0.1 mm, so the magnets sit flush with the top face (the closest they can get to the board). Replaced the dimple with an engraved **N** on the head, the same pole marking as the striker. Kept the finger scallops and the rounded top edge. Both parts use the same 10.2 mm pocket (10 mm magnet + 0.2 mm clearance).

## Hour 7: Wand head section (image 7)

![Day 2, hour 7](../renders/day2/day2_stage_07.png)
Cut the wand head open to check the pocket: 6.1 mm deep in an 8 mm bar leaves a 1.9 mm floor, and the two stacked magnets sit about 0.1 mm below the top face, leaving room for glue.

## Hour 8: Hardware and assembly order (image 8)

![Day 2, hour 8](../renders/day2/day2_stage_08.png)
Laid out the assembly as an exploded view. Striker: magnets go in from the bottom, then the pad covers them. Wand: magnets go in from the top. Both get glue. Mark the N face of each stack before gluing: the striker's top face and the wand's top face should both be N, so the striker's bottom faces the wand with opposite poles and they attract.

## Hour 9: Puck body (image 9)

![Day 2, hour 9](../renders/day2/day2_stage_09.png)
Modeled the puck as a 28 mm x 7 mm cylinder with a 1.0 mm top chamfer and 0.6 mm bottom chamfer. It must be non-magnetic so it never sticks to the strikers. Solid PLA would be about 5 g.

## Hour 10: Puck skid ring and scale check (image 10)

![Day 2, hour 10](../renders/day2/day2_stage_10.png)
Cut a 0.4 mm recess into the underside, leaving a thin contact ring so the puck slides on less area. Compared the puck, flipped puck and striker side by side: the puck is 0.8x the striker diameter and fits the planned 50 mm goal with room to spare.

## Hour 11: Rink half, plate (image 11)

![Day 2, hour 11](../renders/day2/day2_stage_11.png)
Started the rink top: one 180 x 200 x 3.0 mm half with 15 mm radius on the two outer corners. The seam edge at center ice is left plain on purpose for the Day 3 dovetail. 180 x 200 should fit a 220 mm bed (check yours).

## Hour 12: Rink half, markings (image 12)

![Day 2, hour 12](../renders/day2/day2_stage_12.png)
Engraved 0.25 mm deep, 1.2 mm wide lines: a center ring (centered on the seam, so each half gets half of it), a goal crease at the end, and two face-off dots. The lines stop 3 mm short of the outer edges where the walls will clip on. The depth is a parameter (`line_depth`), so it can be set to 0 if the lines affect puck glide. The line color in the render is only for display.

## Hour 13: Two halves at the seam (image 13)

![Day 2, hour 13](../renders/day2/day2_stage_13.png)
Mirrored the half to get the right side and checked both halves together at center ice, shown pulled 30 mm apart. Each half prints separately and they join at the seam.

## Hour 14: Where ribs can go (image 14)

![Day 2, hour 14](../renders/day2/day2_stage_14.png)
Mapped out where underside ribs can go, because the wand sweeps under the board. The striker center can't get closer to a wall than its 17.5 mm radius, and the wand handle is up to 30 mm wide (15 mm each side), so along the long sides only about **2.5 mm** is free. At the seam the wand head is 12 mm in radius, so about **5.5 mm** is free on each half. The player end has to stay open so the handle can slide out. The rest of the underside has to stay flat. These widths ignore the wall thickness: if the clip-on walls inset the playable area, the free strips get wider.

## Hour 15: Assembly concept and checks (image 15)

![Day 2, hour 15](../renders/day2/day2_stage_15.png)
Put everything together to check scale: the rink, two strikers, the puck on the ice, and each wand under the board with its handle sticking out past the end. Exported the four print files (`striker.stl`, `wand.stl`, `puck.stl`, `rink_half.stl`) and confirmed every part is a single closed solid with no interference between parts.

---

## Plan for Day 3
1. Dovetail joint at the seam, with a test joint to tune the clearance.
2. Underside ribs, limited to the strips from hour 14 (**thin: about 2.5 mm along the sides and 5.5 mm at the seam**). That is not much stiffness, so Day 3 has to weigh a few options: a narrower wand handle near the head to widen the side strips, a thicker plate, or relying on the Day 4 walls as the edge supports.
3. Finish both rink halves.

## Assumptions to verify when I get to printing
- Pull and sag numbers assume N52 at 1.45 T, printed PLA at 3.0 GPa, and walls that stiffen all four plate edges. Real magnets, prints and walls vary.
- Friction coefficient is a guess (about 0.3 felt, 0.15 PTFE). The Day 1 coupon steps (2.0 / 2.5 / 3.0 mm) are still useful for checking real pull.
- Does the 0.1 mm axial slack on the pockets leave enough room for glue?
- Do the engraved lines affect how the puck glides?
