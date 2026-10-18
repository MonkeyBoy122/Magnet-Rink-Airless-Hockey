// Magnet Rink: Airless Hockey -- Day 4 (builds on day3.scad: walls, goals, seam bridges, leg brackets, screw holes)
// Finished rink halves: underside ribs, planar dovetail seam, dovetail test joint. Wand v3 (narrower handle).
// Export one named part at a time:  openscad -D 'part="rink_left"' -o rink_left.stl day3.scad
//
// part names:
//   striker  striker_section  striker_magnets  striker_magnets_section  striker_pad  striker_pad_section
//   wand  wand_magnets  wand_head_section  wand_magnets_section  board_strip_section
//   puck  puck_flipped
//   rink_half  rink_half_blank  rink_marks  rink_half_r  rink_marks_r
//   magnet_pairs  pad_pairs  board_strip

part = "";
$fn  = 160;

/* ---------------- PARAMETERS (mm) ---------------- */
// magnets (N52 discs)
magnet_d    = 10;
magnet_h    = 3;
magnets_per = 2;      // discs stacked per striker and per wand
clearance   = 0.2;    // radial press-fit clearance on pockets
axial_slack = 0.1;    // extra pocket depth for glue / print tolerance
pocket_d    = magnet_d + clearance;
pocket_h    = magnets_per*magnet_h + axial_slack;

// gap budget between the two magnet stacks  (Day 2: board 2.5 -> 3.0, wand clearance 0.5 -> 1.0)
board_t     = 4.0;    // playing surface thickness (Day 3: 3.0 -> 4.0 after the FE sag check)
wand_gap    = 1.0;    // air between wand top face and board underside
pad_t       = 1.0;    // felt / PTFE pad stack under the striker
pad_d       = 30;     // pad recess diameter
gap_total   = pad_t + board_t + wand_gap;

// striker
striker_d   = 35;
wall_h      = 6;      // vertical wall height before the shoulder
knob_d      = 16;
knob_up     = 6;      // knob height above the shoulder
knob_round  = 1.5;
glide_ch    = 0.6;    // bottom edge chamfer
mark_depth  = 0.5;    // engraved "N"
striker_R   = striker_d/2;
knob_r      = knob_d/2;
shoulder_h  = striker_R - knob_r;          // 45 degree shoulder -> prints knob-down with no supports
striker_H   = wall_h + shoulder_h + knob_up;

// wand
wand_l      = 150;
wand_w      = 26;    // Day 3: 30 -> 26 so the side rib strips get wider
wand_t      = 8;
wand_tip_d  = 24;
wand_r      = 1.5;
hx          = wand_l - wand_tip_d/2;       // magnet centre along the wand

// puck (non-magnetic)
puck_d      = 28;
puck_h      = 7;
puck_ch_top = 1.0;
puck_ch_bot = 0.6;
skid_d      = 20;     // raised contact ring outside this diameter
skid_depth  = 0.4;

// rink (two halves joined at x = 0)
rink_l      = 360;
rink_w      = 200;
rink_half_l = rink_l/2;
corner_r    = 15;
line_w      = 1.2;
line_depth  = 0.25;
seam_gap    = 0.10;   // each half stops this far short of the seam line (0.2 mm total gap at the seam)

/* ---------------- STRIKER ---------------- */
module striker_outer() {
    rotate_extrude() {
        polygon([[0,0],[striker_R-glide_ch,0],[striker_R,glide_ch],[striker_R,wall_h],
                 [knob_r,wall_h+shoulder_h],[0,wall_h+shoulder_h]]);
        hull() {
            translate([0,wall_h+shoulder_h-0.01]) square([knob_r,0.01]);
            translate([knob_r-knob_round, striker_H-knob_round]) circle(r=knob_round);
            translate([0, striker_H-knob_round]) square([0.01, knob_round]);
        }
    }
}
module striker_cuts() {
    // pad recess, open at the bottom
    translate([0,0,-0.01]) cylinder(d=pad_d, h=pad_t+0.01);
    // magnet pocket now starts at the recess ceiling, so the magnets sit ABOVE the pad
    translate([0,0,-0.01]) cylinder(d=pocket_d, h=pad_t + pocket_h + 0.01);
}
module striker_mark() {
    translate([0,0,striker_H-mark_depth])
        linear_extrude(mark_depth+0.01) text("N", size=6.5, halign="center", valign="center");
}
module striker()         { difference() { striker_outer(); striker_cuts(); striker_mark(); } }
module striker_magnets() {
    for (i=[0:magnets_per-1])
        translate([0,0, pad_t + pocket_h - (i+1)*magnet_h]) cylinder(d=magnet_d, h=magnet_h-0.02);
}
module striker_pad()     { cylinder(d=pad_d-0.4, h=pad_t); }

/* ---------------- WAND ---------------- */
module wand_profile(grip=true) {
    difference() {
        hull() {
            translate([hx, 0]) circle(d=wand_tip_d);
            translate([wand_w/2, 0]) circle(d=wand_w);
        }
        if (grip)
            for (x = [45:14:95], s = [-1,1])
                translate([x, s*(wand_w/2 + 2.5)]) circle(d=12);
    }
}
module wand_solid(grip=true) {
    n = 6;
    linear_extrude(wand_t - wand_r) wand_profile(grip);
    for (i = [0:n-1]) {
        z0  = wand_t - wand_r + i*wand_r/n;
        zm  = z0 + wand_r/(2*n) - (wand_t - wand_r);
        ins = wand_r - sqrt(wand_r*wand_r - zm*zm);
        translate([0,0,z0 - 0.001]) linear_extrude(wand_r/n + 0.001) offset(delta=-ins) wand_profile(grip);
    }
}
module wand_pocket() { translate([hx, 0, wand_t - pocket_h]) cylinder(d=pocket_d, h=pocket_h+0.01); }
module wand_mark()   {
    translate([hx-9.5, 0, wand_t-mark_depth])
        linear_extrude(mark_depth+0.01) text("N", size=5, halign="center", valign="center");
}
module wand()         { difference() { wand_solid(true); wand_pocket(); wand_mark(); } }
module wand_magnets() {
    for (i=[0:magnets_per-1])
        translate([hx, 0, wand_t - pocket_h + i*magnet_h]) cylinder(d=magnet_d, h=magnet_h-0.02);
}

/* ---------------- SECTION HELPERS ---------------- */
module cut_x0()  { translate([0,-300,-100]) cube([600,600,400]); }          // removes x > 0
module cut_hx()  { translate([hx,-300,-100]) cube([600,600,400]); }         // removes x > hx
module head_window() { translate([hx-34,-30,-1]) cube([34.01, 60, wand_t+2]); }

/* ---------------- PUCK ---------------- */
module puck() {
    difference() {
        rotate_extrude() polygon([[0,0],[puck_d/2-puck_ch_bot,0],[puck_d/2,puck_ch_bot],
                                  [puck_d/2,puck_h-puck_ch_top],[puck_d/2-puck_ch_top,puck_h],[0,puck_h]]);
        translate([0,0,-0.01]) cylinder(d=skid_d, h=skid_depth+0.01);
    }
}
module puck_flipped() { translate([0,0,puck_h]) rotate([180,0,0]) puck(); }

/* ---------------- RINK HALF (left half, x from -180 to 0) ---------------- */
module half_outline_2d() {
    hull() {
        translate([-rink_half_l+corner_r, -rink_w/2+corner_r]) circle(r=corner_r);
        translate([-rink_half_l+corner_r,  rink_w/2-corner_r]) circle(r=corner_r);
        translate([-seam_gap-0.01, -rink_w/2]) square([0.01, rink_w]);
    }
}
module ring2d(r, w) { difference() { circle(r=r+w/2); circle(r=r-w/2); } }
module marks_2d() {
    ring2d(30, line_w);                                    // centre ring, centred on the seam
    translate([-rink_half_l, 0]) ring2d(40, line_w);       // goal crease
    for (s=[-1,1]) translate([-90, s*55]) circle(d=6);     // face-off dots
}
module marks_clipped_2d() {
    intersection() {
        union() {
            offset(delta=-3) half_outline_2d();            // stay 3 mm clear of the outer edges
            translate([-6, -rink_w/2+3]) square([6-seam_gap, rink_w-6]);   // but run all the way to the seam
        }
        marks_2d();
    }
}
module rink_half_blank() { linear_extrude(board_t) half_outline_2d(); }
module rink_half() {
    difference() {
        rink_half_blank();
        translate([0,0,board_t-line_depth]) linear_extrude(line_depth+0.01) marks_clipped_2d();
    }
}
module rink_marks()     { translate([0,0,board_t-line_depth]) linear_extrude(line_depth-0.01) marks_clipped_2d(); }

/* ---------------- DAY 3: RIBS ---------------- */
rib_depth = 8;          // ribs hang 8 mm below the plate underside (wand body spans 1..9 mm below it)
rib_clear = 0.6;        // air between the swept wand and any rib
seam_beam = striker_R - wand_tip_d/2 - rib_clear;   // 4.9 mm: strip at the seam
side_rib  = striker_R - wand_w/2 - rib_clear;       // 3.9 mm: strip at each long side
cx_min = -(rink_half_l - striker_R);                // striker centre limits on one half
cx_max = -striker_R;
cy_max = rink_w/2 - striker_R;

// Wand footprint relative to its head centre (handle points toward -x, out the player end). Convex.
module wand_fp() {
    hull() {
        circle(d=wand_tip_d);
        translate([-(hx - wand_w/2), 0]) circle(d=wand_w);
    }
}
// Minkowski sum of a convex footprint with a rectangle of centre positions = hull of the 4 corner placements
module swept_2d() {
    hull() for (cx=[cx_min, cx_max], cy=[-cy_max, cy_max]) translate([cx, cy]) wand_fp();
}
module ribs_2d() {      // where the wand never goes, with slivers thinner than 1.4 mm removed
    offset(delta=0.7) offset(delta=-0.7)
        difference() { half_outline_2d(); offset(delta=rib_clear) swept_2d(); }
}
module ribs_seam_2d()  { intersection() { ribs_2d(); translate([-8,-rink_w]) square([8.01, 2*rink_w]); } }
module ribs_sides_2d() { difference()   { ribs_2d(); translate([-8,-rink_w]) square([8.01, 2*rink_w]); } }
module ribs_solid(r2d) { translate([0,0,-rib_depth]) linear_extrude(rib_depth+0.01) children(0); }

/* ---------------- DAY 3: PLANAR DOVETAIL (profile in x-y, extruded through plate and ribs) ---------------- */
dv_L     = 3.0;     // tail length
dv_neck  = 10;      // tail width at the root
dv_ang   = 15;      // flank angle
dv_c     = 0.20;    // clearance added to each socket wall (the number the test joint is for)
dv_A     = [-80, 0, 80];     // left half owns these tails
dv_B     = [-40, 40];        // right half owns these tails
module tail2d(y0) {            // protrudes toward +x from the seam line x = 0
    t = tan(dv_ang);
    translate([0, y0]) polygon([[-1,-dv_neck/2],[0,-dv_neck/2],[dv_L,-dv_neck/2-dv_L*t],
                                [dv_L, dv_neck/2+dv_L*t],[0,dv_neck/2],[-1,dv_neck/2]]);
}
module socket2d(y0, c) {       // socket for the OTHER half's tail (which protrudes toward -x), grown by c
    offset(delta=c) mirror([1,0]) tail2d(y0);
}
dv_h = rib_depth + board_t;
module dove_tails(ys)   { translate([0,0,-rib_depth]) linear_extrude(dv_h) for (y=ys) tail2d(y); }
module dove_sockets(ys, c) { translate([0,0,-rib_depth-1]) linear_extrude(dv_h+2) for (y=ys) socket2d(y, c); }

module half_core() {
    linear_extrude(board_t) half_outline_2d();
    translate([0,0,-rib_depth]) linear_extrude(rib_depth+0.01) ribs_2d();
}
module half_dove(tails, socks, c=dv_c) {
    difference() {
        union() { half_core(); dove_tails(tails); }
        dove_sockets(socks, c);
    }
}
module rink_left() {
    difference() {
        half_dove(dv_A, dv_B);
        translate([0,0,board_t-line_depth]) linear_extrude(line_depth+0.01) marks_clipped_2d();
    }
}
module rink_right() { mirror([1,0,0]) difference() {
        half_dove(dv_B, dv_A);
        translate([0,0,board_t-line_depth]) linear_extrude(line_depth+0.01) marks_clipped_2d();
} }
module rink_marks_l() { translate([0,0,board_t-line_depth]) linear_extrude(line_depth-0.01) marks_clipped_2d(); }

/* ---------------- DAY 3: TEST JOINT (three clearances on one pair) ---------------- */
tj_w = 30;  tj_l = 96;
tj_y = [-30, 0, 30];
tj_c = [0.10, 0.20, 0.30];    // clearance of the pair at tj_y[i]
module tj_label(i, xs=-15) {
    translate([xs, tj_y[i], board_t-0.4]) linear_extrude(0.41)
        text(str(tj_c[i]), size=5, halign="center", valign="center");
}
module tj_core() {
    translate([-tj_w, -tj_l/2, 0]) cube([tj_w-seam_gap, tj_l, board_t]);
    translate([-seam_beam, -tj_l/2, -rib_depth]) cube([seam_beam-seam_gap, tj_l, rib_depth+0.01]);
}
// A: tails at y=-30 and +30, socket at y=0.   B: socket at -30 and +30, tail at 0.
module tj_a() {
    difference() {
        union() { tj_core(); dove_tails([tj_y[0], tj_y[2]]); }
        dove_sockets([tj_y[1]], tj_c[1]);
        for (i=[0:2]) tj_label(i);
    }
}
module tj_b() {
    difference() {
        mirror([1,0,0]) difference() {
            union() { tj_core(); dove_tails([tj_y[1]]); }
            dove_sockets([tj_y[0]], tj_c[0]);
            dove_sockets([tj_y[2]], tj_c[2]);
        }
        for (i=[0:2]) tj_label(i, 15);     // placed on the +x side directly, so the text is not mirrored
    }
}

/* ---------------- DIAGRAM PARTS ---------------- */
module slab2d(zoff=0.01) { translate([0,0,board_t+zoff]) linear_extrude(0.3) children(0); }
module striker_flipped() { translate([0,0,striker_H]) rotate([180,0,0]) striker(); }

closeup_y = 0;
module closeup_box(x0, x1) { translate([x0, closeup_y-20, -rib_depth-2]) cube([x1-x0, 40, rib_depth+board_t+4]); }


/* ================= DAY 4 ================= */
rwall_h      = 12;               // wall height above the plate
side_wall_t  = side_rib;         // 3.9: same footprint as the side rib below it
end_wall_t   = 6;                // thicker so the counterbores fit
goal_w       = 50;               // goal opening in the player-end wall
pilot_d = 1.8;  hole_d = 2.2;  cb_d = 4.4;  cb_depth = 5;     // M2 self-tapping screws
side_y       = rink_w/2 - side_wall_t/2;                      // 98.05, centre line of the side rib
side_screw_x = [-132, -96, -60, -30];
end_screw    = [[-177, 60], [-177, -60]];
bridge_y     = [-60, -20, 20, 60];
bridge_len   = 24;  bridge_w = 10;  bridge_t = 2;
floor_z      = -80;              // table surface, measured from the plate underside (z=0)
br_len       = 40;  br_t = 4;  br_flange_t = 2;  br_foot = 34;
br_x         = [-160, 0];        // bracket centres on the left half / at the seam (right half: mirrored)

module wall_ring_2d() {
    difference() {
        union() {
            difference() { half_outline_2d(); offset(delta=-side_wall_t) half_outline_2d(); }
            intersection() { half_outline_2d(); translate([-rink_half_l,-rink_w/2]) square([end_wall_t, rink_w]); }
        }
        translate([-8,-rink_w]) square([20, 2*rink_w]);                                   // seam end stays open
        translate([-rink_half_l-1, -goal_w/2]) square([end_wall_t+2, goal_w]);            // goal
    }
}
module wall_holes() {
    for (x=side_screw_x, s=[-1,1]) translate([x, s*side_y, board_t-0.01]) cylinder(d=pilot_d, h=5.01, $fn=24);
    for (p=end_screw) {
        translate([p[0], p[1], board_t-1]) cylinder(d=hole_d, h=rwall_h+2, $fn=24);
        translate([p[0], p[1], board_t+rwall_h-cb_depth]) cylinder(d=cb_d, h=cb_depth+1, $fn=32);
    }
}
module wall_left_all() { difference() { translate([0,0,board_t]) linear_extrude(rwall_h) wall_ring_2d(); wall_holes(); } }
module wall_tl() { intersection() { wall_left_all(); translate([-300,0,-50]) cube([600,300,200]); } }
module wall_bl() { intersection() { wall_left_all(); translate([-300,-300,-50]) cube([600,300,200]); } }

module plate_holes() {      // everything drilled into a LEFT-half plate (right half uses the mirror)
    for (x=side_screw_x, s=[-1,1]) translate([x, s*side_y, -rib_depth-1]) cylinder(d=hole_d, h=rib_depth+board_t+2, $fn=24);
    for (p=end_screw) translate([p[0], p[1], board_t-3.5]) cylinder(d=pilot_d, h=3.6, $fn=24);
    // leg bracket screws (pilots in the rib underside)
    for (xb=[-170,-150,-12], s=[-1,1]) translate([xb, s*side_y, -rib_depth-0.01]) cylinder(d=pilot_d, h=6.5, $fn=24);
    // seam bridge screws (pilots in the seam beam underside)
    for (yb=bridge_y, dy=[-8,8]) translate([-2.5, yb+dy, -rib_depth-0.01]) cylinder(d=pilot_d, h=6.5, $fn=24);
}
module rink4_left()  { difference() { rink_left();  plate_holes(); } }
module rink4_right() { difference() { rink_right(); mirror([1,0,0]) plate_holes(); } }

module bridge() {
    difference() {
        translate([-bridge_w/2, -bridge_len/2, -rib_depth-bridge_t]) cube([bridge_w, bridge_len, bridge_t]);
        for (x=[-2.5,2.5], dy=[-8,8]) translate([x, dy, -rib_depth-bridge_t-1]) cylinder(d=hole_d, h=bridge_t+2, $fn=24);
    }
}
module bridges_all() { for (yb=bridge_y) translate([0,yb,0]) bridge(); }

module bracket(xb, xs=[-10,10]) {   // top-side bracket (y > 0) centred at x = xb
    translate([xb,0,0]) difference() {
        union() {
            translate([-br_len/2, 97, -rib_depth-br_flange_t]) cube([br_len, 104.2-97, br_flange_t]);        // flange under the rib
            translate([-br_len/2, 100.2, floor_z]) cube([br_len, br_t, -floor_z-rib_depth]);                  // upright
            translate([-br_len/2, 100.2, floor_z]) cube([br_len, br_foot, 4]);                                // foot
            for (gx=[-br_len/2+6, br_len/2-9]) translate([gx,0,0]) rotate([90,0,90]) linear_extrude(3)
                polygon([[104.2, floor_z+4],[100.2+br_foot, floor_z+4],[104.2, floor_z+40]]);
        }
        for (x=xs) translate([x, side_y, -rib_depth-br_flange_t-1]) cylinder(d=hole_d, h=br_flange_t+2, $fn=24);
    }
}
module bracket_pair(xb, xs) { bracket(xb, xs); mirror([0,1,0]) bracket(xb, xs); }
module frame_all() {
    bracket_pair(-160, [-10,10]);                        // player end, left half
    mirror([1,0,0]) bracket_pair(-160, [-10,10]);        // player end, right half
    bracket_pair(0, [-12,12]);                           // seam, carries both halves
}
module screw_m2(len) {
    cylinder(d=3.8, h=1.4, $fn=24);
    translate([0,0,1.4]) cylinder(d=2, h=len, $fn=16);
}
// screws drawn in place (head toward the viewer's "outside" of each joint)
module screws_wall_left() {
    for (x=side_screw_x, s=[-1,1]) translate([x, s*side_y, -8]) mirror([0,0,1]) screw_m2(16);
    for (p=end_screw) translate([p[0], p[1], board_t+rwall_h-cb_depth]) mirror([0,0,1]) screw_m2(10);
}
module screws_frame_left() {
    for (xb=[-170,-150,-12], s=[-1,1]) translate([xb, s*side_y, -rib_depth-br_flange_t]) mirror([0,0,1]) screw_m2(8);
}
module screws_bridge_left() {
    for (yb=bridge_y, dy=[-8,8], x=[-2.5]) translate([x, yb+dy, -rib_depth-bridge_t]) mirror([0,0,1]) screw_m2(8);
}
module screws_bridge_right() { mirror([1,0,0]) screws_bridge_left(); }
module walls_left()  { wall_tl(); wall_bl(); }
module walls_right() { mirror([1,0,0]) walls_left(); }
module corner_box(x0,x1,y0,y1) { translate([x0,y0,-20]) cube([x1-x0, y1-y0, 60]); }

/* ---------------- DAY 4 PART SELECTOR ---------------- */
if      (part == "rink_left")          rink4_left();
else if (part == "rink_right")         rink4_right();
else if (part == "wall_tl")            wall_tl();
else if (part == "wall_bl")            wall_bl();
else if (part == "wall_tr")            mirror([1,0,0]) wall_tl();
else if (part == "wall_br")            mirror([1,0,0]) wall_bl();
else if (part == "walls_left")         walls_left();
else if (part == "walls_right")        walls_right();
else if (part == "bridge")             bridge();
else if (part == "bridges_all")        bridges_all();
else if (part == "bracket_end")        bracket(0, [-10,10]);
else if (part == "bracket_seam")       bracket(0, [-12,12]);
else if (part == "frame_all")          frame_all();
else if (part == "screws_wall_left")   screws_wall_left();
else if (part == "screws_wall_right")  mirror([1,0,0]) screws_wall_left();
else if (part == "screws_frame")       { screws_frame_left(); mirror([1,0,0]) screws_frame_left(); }
else if (part == "screws_bridge")      { screws_bridge_left(); screws_bridge_right(); }
else if (part == "corner_plate")       intersection() { rink4_left(); corner_box(-181,-116,56,101); }
else if (part == "corner_wall")        intersection() { wall_tl();    corner_box(-181,-116,56,101); }
else if (part == "corner_screws")      intersection() { screws_wall_left(); corner_box(-181,-116,56,101); }
else if (part == "rink_left_flipped")  rotate([180,0,0]) rink4_left();
else if (part == "rink_right_flipped") rotate([180,0,0]) rink4_right();
else if (part == "frame_flipped")      rotate([180,0,0]) frame_all();
else if (part == "bridges_flipped")    rotate([180,0,0]) bridges_all();
else if (part == "screws_flipped")     rotate([180,0,0]) { screws_frame_left(); mirror([1,0,0]) screws_frame_left(); screws_bridge_left(); screws_bridge_right(); }
else if (part == "screws_bridge_flipped") rotate([180,0,0]) { screws_bridge_left(); screws_bridge_right(); }
else if (part == "striker")            striker();
else if (part == "puck")               puck();
else if (part == "wand")               wand();
else if (part == "wand_magnets")       wand_magnets();
else if (part == "rink_marks_l")       rink_marks_l();
else if (part == "rink_marks_r")       mirror([1,0,0]) rink_marks_l();
else if (part == "wands_clear_flipped")     rotate([180,0,0]) for (p=[[-156.5,-78.6],[-90,0],[-17.5,78.6]]) translate([p[0]-hx, p[1], -wand_gap-wand_t]) wand();
else if (part == "wands_clear_mag_flipped") rotate([180,0,0]) for (p=[[-156.5,-78.6],[-90,0],[-17.5,78.6]]) translate([p[0]-hx, p[1], -wand_gap-wand_t]) wand_magnets();
