// Magnet Rink: Airless Hockey -- Day 1 (v2)
// Parameters + test coupon + striker + wand, with rounded edges.
// Set `stage` (1..11) to preview the build-up, or set `part` to one named part.
// part names: coupon_blank coupon_rail coupon_labels coupon
//             striker_body striker_knobbed striker_v7 striker
//             magnets felt wand_blank wand_v10 wand
//             concept_plate

stage = 11;
part  = "";
$fn   = 160;

/* ---------- PARAMETERS (all mm) ---------- */
board_t     = 2.5;    // playing surface thickness (final value comes from coupon test)
magnet_d    = 10;     // N52 disc diameter
magnet_h    = 3;      // N52 disc thickness
magnets_per = 2;      // stacked per striker / per wand
clearance   = 0.2;    // press-fit clearance on magnet pockets
rink_w      = 200;
rink_l      = 360;
leg_h       = 70;     // space under the board for hands + wands

striker_d   = 35;
striker_h   = 12;
knob_d      = 16;
knob_h      = 10;
felt_d      = 30;     // felt / PTFE pad recess
felt_t      = 1.0;
edge_r      = 2.0;    // top-edge round on striker
glide_ch    = 0.6;    // bottom chamfer on striker (glides, hides elephant foot)

wand_l      = 150;
wand_w      = 30;
wand_t      = 8;
wand_tip_d  = 24;     // rounded head that holds the magnet
wand_r      = 1.5;    // top-edge round on wand

pocket_d = magnet_d + clearance;
pocket_h = magnets_per * magnet_h + clearance;

/* ---------- COUPON ---------- */
coupon_steps = [2.0, 2.5, 3.0];
step_len = 30;
step_w   = 40;
rail_w   = 7;
rail_h   = 3.6;

module coupon_blank() {
    for (i = [0:2])
        translate([i*step_len, 0, 0]) cube([step_len, step_w, coupon_steps[i]]);
}
module coupon_rail() {
    translate([0, step_w, 0]) cube([3*step_len, rail_w, rail_h]);
}
module coupon_labels() {
    for (i = [0:2])
        translate([i*step_len + step_len/2, step_w + rail_w/2, rail_h])
            linear_extrude(0.6)
                text(str(coupon_steps[i]), size=3.6, halign="center", valign="center");
}
module coupon() { coupon_blank(); coupon_rail(); coupon_labels(); }

/* ---------- STRIKER ---------- */
module striker_body() {
    R = striker_d/2;
    rotate_extrude() hull() {
        polygon([[0,0],[R-glide_ch,0],[R,glide_ch],[R,striker_h-edge_r],[0,striker_h-edge_r]]);
        translate([R-edge_r, striker_h-edge_r]) circle(r=edge_r);
        translate([0, striker_h-edge_r]) square([0.01, edge_r]);
    }
}
module striker_knob() {
    kr = knob_d/2; fr = 1.5;
    rotate_extrude() hull() {
        translate([0, striker_h-0.5]) square([kr, 0.5]);
        translate([kr-fr, striker_h+knob_h-fr]) circle(r=fr);
        translate([0, striker_h+knob_h-fr]) square([0.01, fr]);
    }
}
module striker_pocket() { translate([0,0,-0.01]) cylinder(d=pocket_d, h=pocket_h); }
module striker_felt()   { translate([0,0,-0.01]) cylinder(d=felt_d, h=felt_t+0.01); }
module striker_polarity_mark() {
    // small dimple on the knob top = "N-up" striker, so both players match
    translate([0,0,striker_h+knob_h-0.6]) cylinder(d=3, h=1);
}
module striker_knobbed() { difference() { union(){ striker_body(); striker_knob(); } striker_pocket(); } }
module striker_v7()      { difference() { union(){ striker_body(); striker_knob(); } striker_pocket(); striker_felt(); } }
module striker()         { difference() { union(){ striker_body(); striker_knob(); } striker_pocket(); striker_felt(); striker_polarity_mark(); } }

/* ---------- WAND ---------- */
module wand_profile(grip=true) {
    difference() {
        hull() {
            translate([wand_l - wand_tip_d/2, 0]) circle(d=wand_tip_d);
            translate([wand_w/2, 0]) circle(d=wand_w);
        }
        if (grip)
            for (x = [45:14:95], s = [-1,1])
                translate([x, s*(wand_w/2 + 2.5)]) circle(d=12);
    }
}
module wand_solid(grip=true) {
    // flat bar with a rounded top edge (stacked offset layers)
    n = 6;
    linear_extrude(wand_t - wand_r) wand_profile(grip);
    for (i = [0:n-1]) {
        z0  = wand_t - wand_r + i*wand_r/n;
        zm  = z0 + wand_r/(2*n) - (wand_t - wand_r);
        ins = wand_r - sqrt(wand_r*wand_r - zm*zm);
        translate([0,0,z0 - 0.001]) linear_extrude(wand_r/n + 0.001) offset(delta=-ins) wand_profile(grip);
    }
}
module wand_pocket() {
    translate([wand_l - wand_tip_d/2, 0, wand_t - pocket_h + 0.01]) cylinder(d=pocket_d, h=pocket_h);
}
module wand_polarity_mark() {
    translate([wand_l - wand_tip_d/2 + 7, 0, wand_t - 0.6]) cylinder(d=3, h=1);
}
module wand_blank() { wand_solid(false); }
module wand_v10()   { difference() { wand_solid(true); wand_pocket(); } }
module wand()       { difference() { wand_solid(true); wand_pocket(); wand_polarity_mark(); } }

/* ---------- EXPLODED STRIKER HARDWARE ---------- */
module magnets() {
    for (i=[0:magnets_per-1]) translate([0,0,-14 - i*(magnet_h+2)]) cylinder(d=magnet_d, h=magnet_h);
}
module felt() { translate([0,0,-14 - magnets_per*(magnet_h+2) - 2]) cylinder(d=felt_d, h=felt_t); }

/* ---------- CONCEPT: board that the strikers ride on ---------- */
module concept_plate() { translate([-rink_l/2, -rink_w/2, 0]) cube([rink_l, rink_w, board_t]); }

/* ---------- OPENSCAD PREVIEW OF EACH STAGE ---------- */
module cut_half() { translate([0,-50,-1]) cube([100,100,60]); }
module stage_model(s) {
    if (s == 1)  { color("lightgray") concept_plate();
                   color("steelblue") translate([-100,30,board_t]) striker();
                   color("tomato")    translate([100,-30,board_t]) striker(); }
    if (s == 2)  color("lightsteelblue") coupon_blank();
    if (s == 3)  color("lightsteelblue") { coupon_blank(); coupon_rail(); }
    if (s == 4)  color("lightsteelblue") coupon();
    if (s == 5)  color("steelblue") striker_body();
    if (s == 6)  color("steelblue") striker_knobbed();
    if (s == 7)  { color("steelblue") difference(){ striker_v7(); cut_half(); }
                   color("silver") magnets(); color("dimgray") felt(); }
    if (s == 8)  color("steelblue") striker();
    if (s == 9)  color("tomato") wand_blank();
    if (s == 10) color("tomato") wand_v10();
    if (s == 11) { coupon();
                   translate([-10,-60,0]) color("steelblue") striker();
                   translate([-10,-110,0]) color("tomato") wand(); }
}

if      (part == "coupon_blank")    coupon_blank();
else if (part == "coupon_rail")     coupon_rail();
else if (part == "coupon_labels")   coupon_labels();
else if (part == "coupon")          coupon();
else if (part == "striker_body")    striker_body();
else if (part == "striker_knobbed") striker_knobbed();
else if (part == "striker_v7")      striker_v7();
else if (part == "striker")         striker();
else if (part == "magnets")         magnets();
else if (part == "felt")            felt();
else if (part == "wand_blank")      wand_blank();
else if (part == "wand_v10")        wand_v10();
else if (part == "wand")            wand();
else if (part == "concept_plate")   concept_plate();
else if (part == "striker_v7_section") difference() { striker_v7(); cut_half(); }
else if (part == "striker_knobbed_section") difference() { striker_knobbed(); cut_half(); }
else stage_model(stage);
