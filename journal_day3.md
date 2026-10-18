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
