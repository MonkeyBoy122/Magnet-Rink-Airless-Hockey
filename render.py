"""Render the Day 1 stages with Blender (Cycles). Usage: python3 render.py <stage|all> [width] [samples]"""
import sys, math, os
import bpy, bmesh
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PARTS = os.environ.get("PARTS_DIR", os.path.join(HERE, "parts"))
PREFIX = os.environ.get("PREFIX", "day1_stage_")
TAG = os.environ.get("TAG", "Magnet Rink: Airless Hockey  |  Day 1")
OUT = os.environ.get("OUTDIR", os.path.join(HERE, "png"))
os.makedirs(OUT, exist_ok=True)

def lin(h):
    h = h.lstrip("#")
    c = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    return tuple(x ** 2.2 for x in c) + (1.0,)

COL = dict(blue="#2F6FE0", red="#E5472C", coupon="#2EA89A", ground="#F1F2F5")

def material(name, color, rough=0.4, metal=0.0, alpha=1.0, coat=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = lin(color)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    b.inputs["Alpha"].default_value = alpha
    if "Coat Weight" in b.inputs:
        b.inputs["Coat Weight"].default_value = coat
    return m

def material_ribs(name, base, tint, thr=0.02):
    m = material(name, base, 0.32, coat=0.15)
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    gt = nt.nodes.new("ShaderNodeMath"); gt.operation = "GREATER_THAN"; gt.inputs[1].default_value = thr
    mix = nt.nodes.new("ShaderNodeMix"); mix.data_type = "RGBA"
    mix.inputs[6].default_value = lin(base); mix.inputs[7].default_value = lin(tint)
    nt.links.new(geo.outputs["Position"], sep.inputs["Vector"])
    nt.links.new(sep.outputs["Z"], gt.inputs[0])
    nt.links.new(gt.outputs["Value"], mix.inputs["Factor"])
    nt.links.new(mix.outputs[2], b.inputs["Base Color"])
    return m

# (stl, material key, location, rot_z_deg)
LEG = 70.0
BOARD = 2.5
STAGES = {
    1:  dict(az=-32, el=24, title="Hour 1  |  Layout and parameters",
             sub="Board 2.5 mm  /  magnet 10 x 3 mm  /  pocket clearance 0.2 mm  /  hands + wands live under the board",
             ground_z=0.0,
             items=[("concept_plate", "plate", (0, 0, LEG), 0),
                    ("striker", "blue", (-100, 30, LEG + BOARD), 0),
                    ("striker", "red", (100, -30, LEG + BOARD), 0),
                    ("wand", "blue", (-238, 30, LEG - 8), 0),
                    ("wand", "red", (238, -30, LEG - 8), 180)]),
    2:  dict(az=-35, el=30, title="Hour 2  |  Test coupon: thickness steps",
             sub="2.0 / 2.5 / 3.0 mm steps, 30 x 40 mm each",
             items=[("coupon_blank", "coupon", (0, 0, 0), 0)]),
    3:  dict(az=-35, el=30, title="Hour 3  |  Test coupon: stiffening rail",
             sub="7 mm rail keeps the thin steps flat and gives a spot for labels",
             items=[("coupon_blank", "coupon", (0, 0, 0), 0), ("coupon_rail", "coupon", (0, 0, 0), 0)]),
    4:  dict(az=-35, el=30, title="Hour 4  |  Test coupon: labels",
             sub="0.6 mm raised numbers so the sections can't get mixed up",
             items=[("coupon", "coupon", (0, 0, 0), 0)]),
    5:  dict(az=-35, el=26, title="Hour 5  |  Striker body",
             sub="35 mm diameter x 12 mm, rounded top edge, 0.6 mm glide chamfer",
             items=[("striker_body", "blue", (0, 0, 0), 0)]),
    6:  dict(az=42, el=24, title="Hour 6  |  Knob and magnet pocket (section view)",
             sub="16 mm finger knob, 10.2 x 6.2 mm pocket cut in from the bottom for two stacked magnets",
             items=[("striker_knobbed_section", "blue", (0, 0, 0), 0)]),
    7:  dict(az=42, el=20, title="Hour 7  |  Felt recess, exploded view",
             sub="Magnets go in the pocket, felt or PTFE pad covers the bottom",
             items=[("striker_v7_section", "blue", (0, 0, 0), 0),
                    ("magnets", "magnet", (0, 0, 0), 0),
                    ("felt", "felt", (0, 0, 0), 0)]),
    8:  dict(az=-35, el=42, title="Hour 8  |  Polarity mark",
             sub="Dimple on the knob = N-up, so both strikers repel each other",
             items=[("striker", "blue", (0, 0, 0), 0)]),
    9:  dict(az=-28, el=32, title="Hour 9  |  Wand handle",
             sub="150 x 30 x 8 mm flat bar, tapering to a 24 mm head, rounded top edge",
             items=[("wand_blank", "red", (0, 0, 0), 0)]),
    10: dict(az=-28, el=42, title="Hour 10  |  Wand magnet pocket and finger grips",
             sub="Open-top pocket keeps the magnets as close to the board as possible",
             items=[("wand_v10", "red", (0, 0, 0), 0)]),
    11: dict(az=-30, el=36, title="Hour 11  |  Day 1 parts, finished",
             sub="Test coupon, striker and wand laid out together as a set",
             items=[("coupon", "coupon", (0, 0, 0), 0),
                    ("striker", "blue", (-10, -60, 0), 0),
                    ("wand", "red", (-10, -110, 0), 0)]),
}

_sf = os.environ.get("STAGES_FILE")
if _sf:
    import importlib.util
    _spec = importlib.util.spec_from_file_location("stages_ext", _sf)
    _mod = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_mod)
    STAGES = _mod.STAGES

def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def load_part(name, mat, loc, rotz):
    bpy.ops.wm.stl_import(filepath=os.path.join(PARTS, name + ".stl"))
    ob = bpy.context.selected_objects[0]
    bm = bmesh.new(); bm.from_mesh(ob.data)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-4)
    bm.edges.ensure_lookup_table()
    for e in bm.edges:
        e.smooth = True
        if len(e.link_faces) == 2 and e.calc_face_angle(0) > math.radians(32):
            e.smooth = False
    for f in bm.faces:
        f.smooth = True
    bm.to_mesh(ob.data); bm.free()
    ob.data.materials.append(mat)
    ob.rotation_euler[2] = math.radians(rotz)
    ob.location = loc
    return ob

def world_bbox(obs):
    pts = []
    for ob in obs:
        bpy.context.view_layer.update()
        pts += [ob.matrix_world @ Vector(c) for c in ob.bound_box]
    lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    return lo, hi, pts

def render_stage(n, width, samples):
    cfg = STAGES[n]
    reset()
    sc = bpy.context.scene
    mats = dict(
        blue=material("blue", COL["blue"], 0.32, coat=0.4),
        red=material("red", COL["red"], 0.32, coat=0.4),
        coupon=material("coupon", COL["coupon"], 0.42),
        magnet=material("magnet", "#C9CDD3", 0.16, metal=1.0),
        felt=material("felt", "#3B3C42", 0.95),
        plate=material("plate", "#BFD7EE", 0.08, alpha=0.30),
        ground=material("ground", "#E6E9EF", 0.8),
        ice=material("ice", "#B9D3EC", 0.32, coat=0.15),
        mark=material("mark", "#22304D", 0.35),
        puck=material("puck", "#F0A32F", 0.28, coat=0.5),
        board=material("board", "#A9C9E8", 0.12, alpha=0.38),
        sweep=material("sweep", "#F2B84B", 0.5),
        okgreen=material("okgreen", "#2FAE6B", 0.5),
        openred=material("openred", "#D8412F", 0.5),
        iceribs=material_ribs("iceribs", "#B9D3EC", "#3F7FE0"),
    )
    obs = [load_part(*[(it[0], mats[it[1]], it[2], it[3])][0]) for it in cfg["items"]]
    lo, hi, pts = world_bbox(obs)
    ctr = (lo + hi) / 2
    gz = cfg.get("ground_z", lo.z)

    # ground
    bpy.ops.mesh.primitive_plane_add(size=1, location=(ctr.x, ctr.y, gz))
    g = bpy.context.object
    size = max((hi - lo).x, (hi - lo).y, 120) * 14
    g.scale = (size, size, 1)
    g.data.materials.append(mats["ground"])

    # world
    sc.world = bpy.data.worlds.new("w")
    sc.world.use_nodes = True
    nt = sc.world.node_tree
    for nd in list(nt.nodes):
        nt.nodes.remove(nd)
    amb = nt.nodes.new("ShaderNodeBackground")
    amb.inputs["Color"].default_value = lin("#DDE3EE"); amb.inputs["Strength"].default_value = 0.45
    vis = nt.nodes.new("ShaderNodeBackground")
    vis.inputs["Color"].default_value = lin("#EEF0F4"); vis.inputs["Strength"].default_value = 1.0
    lp = nt.nodes.new("ShaderNodeLightPath")
    mix = nt.nodes.new("ShaderNodeMixShader")
    outn = nt.nodes.new("ShaderNodeOutputWorld")
    nt.links.new(lp.outputs["Is Camera Ray"], mix.inputs["Fac"])
    nt.links.new(amb.outputs["Background"], mix.inputs[1])
    nt.links.new(vis.outputs["Background"], mix.inputs[2])
    nt.links.new(mix.outputs["Shader"], outn.inputs["Surface"])

    extent = (hi - lo).length

    lrz = cfg.get("light_rz", 0)
    def sun(name, rot, energy, angle):
        d = bpy.data.lights.new(name, "SUN")
        d.energy = energy; d.angle = math.radians(angle)
        o = bpy.data.objects.new(name, d); sc.collection.objects.link(o)
        o.rotation_euler = [math.radians(rot[0]), math.radians(rot[1]), math.radians(rot[2] + lrz)]
    sun("key", (48, 8, -38), 2.4, 3)
    sun("fill", (62, -5, 140), 0.35, 14)
    sun("rim", (115, 0, 25), 1.2, 6)

    # camera
    cam_d = bpy.data.cameras.new("cam"); cam_d.lens = 70; cam_d.clip_start = 1; cam_d.clip_end = 1000000
    cam = bpy.data.objects.new("cam", cam_d); sc.collection.objects.link(cam)
    sc.camera = cam
    az, el = math.radians(cfg["az"]), math.radians(cfg["el"])
    direction = Vector((math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el), math.sin(el)))
    sc.render.resolution_x = width
    sc.render.resolution_y = int(width * 0.75)
    focus = ctr.copy()
    dist = extent * 3
    for _ in range(14):
        cam.location = focus + direction * dist
        look = (focus - cam.location).to_track_quat("-Z", "Y")
        cam.rotation_euler = look.to_euler()
        bpy.context.view_layer.update()
        m = 0
        for p in pts:
            v = world_to_camera_view(sc, cam, p)
            m = max(m, abs(v.x - 0.5), abs(v.y - 0.5))
        dist *= (m / 0.38) if m > 0 else 1
    # shift subject slightly up to leave room for the caption
    cam.data.shift_y = -0.07

    # render settings
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = samples
    sc.cycles.use_denoising = True
    sc.cycles.max_bounces = 6
    sc.cycles.transparent_max_bounces = 8
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    sc.render.film_transparent = False
    path = os.path.join(OUT, f"{PREFIX}{n:02d}.png")
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)

    # caption (keep an uncaptioned copy too)
    import shutil
    shutil.copy(path, path.replace(".png", "_raw.png"))
    im = Image.open(path).convert("RGB")
    W, H = im.size
    d = ImageDraw.Draw(im)
    fb = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", int(W * 0.026))
    fr = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", int(W * 0.0165))
    pad = int(W * 0.035)
    d.text((pad, H - pad - int(W * 0.062)), cfg["title"], font=fb, fill=(28, 30, 40))
    d.text((pad, H - pad - int(W * 0.026)), cfg["sub"], font=fr, fill=(95, 100, 115))
    tag = TAG
    tw = d.textlength(tag, font=fr)
    d.text((W - pad - tw, pad * 0.8), tag, font=fr, fill=(120, 125, 140))
    im.save(path)
    print("saved", path)

if __name__ == "__main__":
    which = sys.argv[1]
    width = int(sys.argv[2]) if len(sys.argv) > 2 else 1600
    samples = int(sys.argv[3]) if len(sys.argv) > 3 else 96
    stages = range(1, 12) if which == "all" else [int(which)]
    for s in stages:
        render_stage(s, width, samples)
