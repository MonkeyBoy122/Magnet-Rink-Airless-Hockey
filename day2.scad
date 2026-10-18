// Magnet Rink: Airless Hockey -- Day 2
// Revised striker + wand, new puck, first rink half. Every size is a parameter.
// Export one named part at a time:  openscad -D 'part="striker"' -o striker.stl day2.scad
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
board_t     = 3.0;    // playing surface thickness
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
wand_w      = 30;
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
        translate([-0.01, -rink_w/2]) square([0.01, rink_w]);
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
            translate([-6, -rink_w/2+3]) square([6, rink_w-6]);   // but run all the way to the seam
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

/* ---------------- PRINT ORIENTATION + RIB MAP PARTS ---------------- */
module striker_flipped() { translate([0,0,striker_H]) rotate([180,0,0]) striker(); }   // knob-down, as printed
module bed_plate()       { translate([-26,-26,-2]) cube([52,52,2]); }

// Where can underside ribs go? The wand sweeps under the plate, so ribs only fit where it cannot reach.
side_free = striker_R - wand_w/2;       // strip along the long sides (striker edge to wand handle edge)
seam_free = striker_R - wand_tip_d/2;   // strip at the seam (striker stays on its own half)
end_open  = 6;                          // player end stays open for the wand handle
module zone_ok_2d() {
    intersection() {
        half_outline_2d();
        union() {
            translate([-rink_half_l, -rink_w/2]) square([rink_half_l, side_free]);
            translate([-rink_half_l,  rink_w/2 - side_free]) square([rink_half_l, side_free]);
            translate([-seam_free, -rink_w/2]) square([seam_free, rink_w]);
        }
    }
}
module zone_open_2d() { intersection() { half_outline_2d(); translate([-rink_half_l, -rink_w/2]) square([end_open, rink_w]); } }
module zone_wand_2d() {
    intersection() {
        half_outline_2d();
        translate([-rink_half_l+end_open, -rink_w/2+side_free]) square([rink_half_l-end_open-seam_free, rink_w-2*side_free]);
    }
}
module zone_ok()   { translate([0,0,board_t+0.01]) linear_extrude(0.3) zone_ok_2d(); }
module zone_open(){ translate([0,0,board_t+0.01]) linear_extrude(0.3) zone_open_2d(); }
module zone_wand() { translate([0,0,board_t+0.01]) linear_extrude(0.3) zone_wand_2d(); }

/* ---------------- DIAGRAM PARTS ---------------- */
module magnet_pairs() {
    // lower (wand) stacks hang down from z=0, upper (striker) stacks start at the gap
    for (k=[0:2]) {
        n = k+1; x = (k-1)*32;
        for (i=[0:n-1]) {
            translate([x,0,-(i+1)*magnet_h]) cylinder(d=magnet_d, h=magnet_h-0.12);
            translate([x,0,gap_total + i*magnet_h + 0.12]) cylinder(d=magnet_d, h=magnet_h-0.12);
        }
    }
}
module pad_pairs() { for (k=[0:2]) translate([(k-1)*32,0,gap_total-pad_t]) cylinder(d=14, h=pad_t-0.05); }
module board_strip() { translate([-52,-14,wand_gap]) cube([104,28,board_t]); }

/* ---------------- PART SELECTOR ---------------- */
if      (part == "striker")                  striker();
else if (part == "striker_section")          difference() { striker(); cut_x0(); }
else if (part == "striker_magnets")          striker_magnets();
else if (part == "striker_magnets_section")  difference() { striker_magnets(); cut_x0(); }
else if (part == "striker_pad")              striker_pad();
else if (part == "striker_pad_section")      difference() { striker_pad(); cut_x0(); }
else if (part == "wand")                     wand();
else if (part == "wand_magnets")             wand_magnets();
else if (part == "wand_head_section")        intersection() { difference() { wand(); cut_hx(); } head_window(); }
else if (part == "wand_magnets_section")     difference() { wand_magnets(); cut_hx(); }
else if (part == "board_strip_section")      translate([-38,-30,0]) cube([38,60,board_t]);
else if (part == "puck")                     puck();
else if (part == "puck_flipped")             puck_flipped();
else if (part == "rink_half")                rink_half();
else if (part == "rink_half_blank")          rink_half_blank();
else if (part == "rink_marks")               rink_marks();
else if (part == "rink_half_r")              mirror([1,0,0]) rink_half();
else if (part == "rink_marks_r")             mirror([1,0,0]) rink_marks();
else if (part == "striker_flipped")          striker_flipped();
else if (part == "bed_plate")                bed_plate();
else if (part == "zone_ok")                  zone_ok();
else if (part == "zone_open")                zone_open();
else if (part == "zone_wand")                zone_wand();
else if (part == "magnet_pairs")             magnet_pairs();
else if (part == "pad_pairs")                pad_pairs();
else if (part == "board_strip")              board_strip();
else {
    // default preview: the whole Day 2 set side by side
    translate([-40,-80,0]) striker();
    translate([-60,-130,0]) wand();
    translate([30,-80,0]) puck();
    rink_half();
}
