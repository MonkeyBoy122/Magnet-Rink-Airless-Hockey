# Build Log: Magnet Rink: Airless Hockey

All four days of journal entries with the render for each hour. Written as drafts: edit the hours to match what you actually did. Nothing has been printed yet, and every force, sag and friction number is a model estimate, not a measurement.


---

# Journal Log: Day 1 (Magnet Rink: Airless Hockey)

**Goal for today:** set up the parametric foundation, then design the three parts that decide whether the game works at all: the board-thickness test coupon, the striker, and the wand. This is a CAD-only day, nothing printed yet.

**Tools:** OpenSCAD (parametric modeling), planned materials PLA/PETG, N52 10 x 3 mm neodymium disc magnets.

> Draft note: the hour breakdown below matches the 11 renders (`day1_stage_01.png` to `day1_stage_11.png`). Edit the times and wording so they match what you actually did.

---

## Hour 1: Parameters and layout (image 1)

![Day 1, hour 1](../renders/day1/day1_stage_01.png)
Defined every dimension as a variable at the top of the file: `board_t` (2.5), `magnet_d` (10), `magnet_h` (3), `clearance` (0.2), `rink_w` (200), `rink_l` (360), plus striker and wand sizes. Built a concept view of the whole mechanism: a clear board on legs, a striker on top for each player, and a wand underneath that drags it. **Why:** magnet pull drops off fast with distance, so every size has to be changeable with one number after testing.

## Hour 2: Test coupon, thickness steps (image 2)

![Day 1, hour 2](../renders/day1/day1_stage_02.png)
Modeled three stepped plates at 2.0, 2.5, and 3.0 mm, each 30 x 40 mm. The idea: drag a striker across each step with a wand and find the thinnest board that still has enough pull and doesn't flex.

## Hour 3: Test coupon, stiffening rail (image 3)

![Day 1, hour 3](../renders/day1/day1_stage_03.png)
Added a 7 mm wide, 3.6 mm tall rail along one edge. It keeps the thin steps from warping and gives me a flat place for labels that doesn't change the thickness being tested.

## Hour 4: Test coupon, labels (image 4)

![Day 1, hour 4](../renders/day1/day1_stage_04.png)
Added raised 0.6 mm number labels (2, 2.5, 3) on the rail so the sections can't be mixed up later.

## Hour 5: Striker body (image 5)

![Day 1, hour 5](../renders/day1/day1_stage_05.png)
Started the striker as a 35 mm diameter, 12 mm tall puck-style body. Rounded the top edge (2 mm radius) so it never catches the puck, and added a 0.6 mm chamfer on the bottom edge so it glides smoothly.

## Hour 6: Striker knob and magnet pocket (image 6)

![Day 1, hour 6](../renders/day1/day1_stage_06.png)
Added a 16 mm finger knob with a rounded top. Cut the magnet pocket from the bottom: 10.2 mm diameter (10 + 0.2 clearance) and 6.2 mm deep, sized for two stacked 3 mm discs. The `pocket_h` variable updates automatically if I change the magnet count. The image is a section view so the pocket is visible.

## Hour 7: Felt recess and exploded view (image 7)

![Day 1, hour 7](../renders/day1/day1_stage_07.png)
Cut a 30 mm x 1 mm recess in the striker bottom for a felt or PTFE pad to cut friction. Built an exploded view showing the striker (cut open), the two magnets, and the felt pad so the assembly order is clear: magnets into the pocket, then the pad over the bottom.

## Hour 8: Polarity mark (image 8)

![Day 1, hour 8](../renders/day1/day1_stage_08.png)
Added a small dimple on the knob top to mark "N-up". Both strikers get the same orientation, so they repel each other instead of snapping together mid-game.

## Hour 9: Wand handle (image 9)

![Day 1, hour 9](../renders/day1/day1_stage_09.png)
Modeled the wand as a flat 150 mm bar, 8 mm thick, tapering from 30 mm wide at the grip to a 24 mm round head that holds the magnet. Flat so it slides under the board without tipping, with a 1.5 mm rounded top edge so it's comfortable to hold.

## Hour 10: Wand magnet pocket and finger grips (image 10)

![Day 1, hour 10](../renders/day1/day1_stage_10.png)
Cut the matching 10.2 x 6.2 mm pocket into the head, open on top so the magnets sit as close to the board as possible. Added finger scallops along both sides of the handle.

## Hour 11: Day 1 parts complete (image 11)

![Day 1, hour 11](../renders/day1/day1_stage_11.png)
Added a polarity dimple on the wand head to match the striker, then laid out the coupon, striker, and wand together to check they work as a set. Exported the three STL files (`coupon.stl`, `striker.stl`, `wand.stl`) and confirmed each is a single closed solid with no errors.

---

## Plan for Day 2
1. Model the puck.
2. Start the rink top and its center dovetail joint.
3. Update the parameters if any sizes need to change.

## Still to verify (when I get to printing)
- Does 2.0 mm give enough pull but too much flex, or does 2.5 mm win?
- Felt vs PTFE tape: which slides better?
- Does 0.2 mm pocket clearance hold the magnets, or does it need glue?


---

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


---

# Journal Log: Day 3 (Magnet Rink: Airless Hockey)

**Goal for today:** finish the two rink halves: underside ribs, a dovetail seam between the halves, and a small test joint for tuning the dovetail clearance. This is a CAD-only day, nothing printed yet.

**One big change came out of today:** checking the board with the real support layout (a finite-element plate model) showed the Day 2 board would sag more than the wand gap. The board is now **4.0 mm** (was 3.0), the total magnet gap is **6.0 mm** (was 5.0), and the wand handle is 26 mm wide (was 30). Details in hours 2 and 13.

**Tools:** OpenSCAD (parametric modeling), Python (magnet-force model, plate finite elements with scikit-fem, mesh checks with trimesh), N52 10 x 3 mm disc magnets, planned PLA/PETG.

> Draft note: the 15 entries below match the 15 renders (`day3_stage_01.png` to `day3_stage_15.png`). Edit times and wording to match what you actually did. All pull, sag and clearance-under-load numbers are **model estimates, not measurements**. The distances between CAD parts (0.6 mm, 0.2 mm and so on) are measured on the exported meshes.

---

## Hour 1: Exact wand sweep (image 1)

![Day 3, hour 1](../renders/day3/day3_stage_01.png)
Day 2 had a rough rib map. Today I computed the real one. The wand head can sit anywhere the striker centre can go (17.5 mm in from every edge of a half). The wand footprint is convex, so everything it can ever cover is the hull of the footprint placed at the four extreme positions. That hull is the amber area. Nothing may hang below the plate inside it.

## Hour 2: Wand v3, narrower handle (image 2)

![Day 3, hour 2](../renders/day3/day3_stage_02.png)
With the 30 mm handle the free strip along each long side was only 2.5 mm, too thin to be a useful rib. Narrowed the handle to **26 mm**, so the strip is **4.5 mm** (3.9 mm after a 0.6 mm safety clearance). The head, magnet pocket and N marking are unchanged, the finger scallops moved in with the edge (grip is still 19 mm wide at the scallops), and the wand drops to about 33 g if solid PLA. The wand is still a single closed solid.

## Hour 3: Where ribs can go (image 3)

![Day 3, hour 3](../renders/day3/day3_stage_03.png)
Subtracted the sweep plus 0.6 mm clearance from the half outline and removed slivers thinner than 1.4 mm. What is left is **3.9 mm along each long side** and **4.9 mm at the seam** (the wand tip stops 5.5 mm from the seam). The player end stays open so the handle can slide out. The interior stays flat.

## Hour 4: Side ribs (image 4)

![Day 3, hour 4](../renders/day3/day3_stage_04.png)
Added the long-side ribs, 3.9 mm wide and **8 mm deep** (the wand body spans 1 to 9 mm below the plate, so the ribs sit beside it, not in its way). Shown from the underside. Along most of their length the wand handle is 0.9 mm or more from them, and the ribs are what the Day 4 walls can clip onto. The plate in this image is the 4.0 mm version; the reason is in hour 13.

## Hour 5: Seam beam (image 5)

![Day 3, hour 5](../renders/day3/day3_stage_05.png)
The seam gets a 4.9 mm wide, 8 mm deep beam on each half. Each half stops 0.1 mm short of the seam line, so the two halves leave a 0.2 mm gap when joined. Without that, a slightly over-extruded edge would make the halves jam.

## Hour 6: Dovetail layout (image 6)

![Day 3, hour 6](../renders/day3/day3_stage_06.png)
The dovetail is **planar**: its profile is drawn in the top view and extruded straight through the plate and the ribs. That makes every flank a vertical wall, so it prints with no supports and no overhangs. Five tails on a 40 mm pitch: the left half owns three (y = -80, 0, 80), the right half owns two (y = -40, 40). That makes the two halves different parts, as they must be (a mirrored copy would put tails on tails).

## Hour 7: One tail and its socket (image 7)

![Day 3, hour 7](../renders/day3/day3_stage_07.png)
Tail: 3.0 mm long, 10 mm at the root, 15 degree flanks, so it is 11.6 mm wide at the tip. Longer tails would not fit: the beam on the other half is only 4.9 mm wide, and a 3.0 mm tail plus its 0.2 mm clearance leaves about 1.7 mm of beam behind the socket. The socket is the other half's tail grown by `dv_c` (0.2 mm). That is the number to tune.

## Hour 8: Dovetail test joint, two pieces (image 8)

![Day 3, hour 8](../renders/day3/day3_stage_08.png)
Made a small test pair, each piece 33 x 96 mm (about 19 g if solid PLA). It has the same tail, socket, beam and plate as the real seam, in three pairs with clearances **0.1, 0.2 and 0.3 mm** per flank. The numbers are engraved on both pieces. I checked the exported meshes: the tight pair's flank gap measures 0.1 mm.

## Hour 9: Test joint, closed (image 9)

![Day 3, hour 9](../renders/day3/day3_stage_09.png)
The two pieces mated in CAD. Print both plate-down, then try the three pairs: the tightest one that closes with light pressure and no wobble is the value for `dv_c`. Nothing has been printed, so this is a plan for later.

## Hour 10: Left half, top (image 10)

![Day 3, hour 10](../renders/day3/day3_stage_10.png)
The finished left half: 4.0 mm plate, engraved markings, three tails reaching 3 mm past the seam, two sockets for the right half's tails. It is 183 x 200 mm and 12 mm tall with the ribs. It is one closed solid, about 164 cm^3, so roughly 200 g if solid PLA (much less at normal infill). It prints plate-down, ribs up, no supports.

## Hour 11: Underside (image 11)

![Day 3, hour 11](../renders/day3/day3_stage_11.png)
Both halves flipped to show the 8 mm deep structure: the side ribs and the seam beam (blue), with the tail columns running the same depth. Still nothing crosses the interior, so the wand has the whole underside.

## Hour 12: Right half drops in along z (image 12)

![Day 3, hour 12](../renders/day3/day3_stage_12.png)
Because the tails run the full depth, the right half simply lowers onto the left from above. It does not slide along the seam. **A limit:** nothing stops the halves lifting apart again, and the joint carries no vertical shear. I assumed the seam is free in the sag check, which is the safe way to do it. Day 4 has to hold the halves down.

## Hour 13: Board sag, and why the board is now 4.0 mm (image 13)

![Day 3, hour 13](../renders/day3/day3_stage_13.png)
I ran a plate-bending finite-element model of one half (printed PLA at 3.0 GPa, uniform pad load for pull plus striker weight, long sides on the frame, player end and seam free, ribs as thicker strips). Before the rest of the day's work, I checked it against Day 2's setup (all four edges supported, no ribs): it gives **0.37 mm**, which agrees with Day 2's 0.2 to 0.4 mm. But the real layout has a free player end and a free seam, and there the 3.0 mm board sags **1.2 mm** when a striker sits at the player end. That is more than the 1.0 mm wand gap, so the board would rest on the wand.

| Option (2 discs, pull model estimates) | Gap | Pull | Peak drag | Worst sag |
|---|---|---|---|---|
| Day 2: board 3.0 mm | 5.0 mm | 7.1 N | 3.4 N | 1.21 mm (too much) |
| Board 3.5 mm | 5.5 mm | 6.2 N | 2.9 N | 0.72 mm |
| **Board 4.0 mm (chosen)** | **6.0 mm** | **5.4 N** | **2.6 N** | **0.44 mm** |
| 1 disc, board 3.0 mm | 5.0 mm | 3.4 N | 1.7 N | 0.60 mm |

The drag-to-pull ratio stays about 0.48, so the friction margin is still about 1.56 at a friction coefficient of 0.3. A 4.0 mm board leaves about 0.56 mm of the wand gap free at the worst spot. A Day 4 end wall should bring that down further (about 0.36 mm in the model).

## Hour 14: Wand clearance under the ribs (image 14)

![Day 3, hour 14](../renders/day3/day3_stage_14.png)
Put the wand at a 3 x 3 grid of positions (corners, edge middles, centre) against the left half and measured the closest distance on the meshes: **0.60 mm at the seam**, **0.92 mm or more at the long sides**, and the plate's own 1.0 mm gap everywhere else. That is purely geometric. It does not include sag, which only closes the gap to the plate, not the gap to the ribs.

## Hour 15: Day 3 assembly (image 15)

![Day 3, hour 15](../renders/day3/day3_stage_15.png)
Everything together at the new gap: both halves joined, two strikers, the puck and two wands under the board. Exported the final print files into `stl3/`: `rink_left.stl`, `rink_right.stl`, `wand.stl` (v3), `striker.stl`, `puck.stl`, `test_joint_a.stl`, `test_joint_b.stl`, plus `wand_magnets.stl` for the diagrams. All are single closed solids. The two halves do not overlap (0 mm^3), and the closest approach between them is the planned 0.2 mm.

---

## Plan for Day 4
1. Walls clipped over the side ribs, and end walls with 50 mm goals. The player-end wall should also stiffen the free edge.
2. A way to hold the halves down at the seam (clips or a frame), since the dovetail does not stop them lifting.
3. Legs or a frame under the side ribs, tall enough for the wands to pass underneath.

## Assumptions to verify when I get to printing
- Sag scales with 1/stiffness. The model uses 3.0 GPa. If the print is PETG (about 2.1 GPa) the worst sag is closer to 0.6 mm. Real printed plates are stiffer or weaker depending on layers and infill.
- The model assumes the side ribs sit on a rigid frame along their whole length, ignores the corner radii, and treats ribs as strips of thicker plate. Pull and friction numbers still assume N52 at 1.45 T and a friction coefficient of 0.15 to 0.3.
- Does a 183 x 200 mm plate stay flat when printed with 8 mm tall ribs along its edges? Warping across 200 mm is a real risk. Also check your printer's bed size (assumed 220 mm).
- Dovetail clearance: is 0.2 mm right? The test joint answers that. The 0.1 mm per-half seam gap is a guess as well.
- The Day 1 coupon steps (2.0 / 2.5 / 3.0 mm) are still the way to measure real pull; they should now include a 4.0 mm step.


---

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
