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
