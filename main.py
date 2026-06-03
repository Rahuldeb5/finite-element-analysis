Web VPython 3.2
# from vpython import *

mat_names = ["Steel", "Aluminum", "Rubber"]
mat_E = [200e9, 69e9, 5e9]

NX = 12
L  = 6.0
BH = 0.5
BW = 0.5
I_beam = BW * BH**3 / 12.0
E = mat_E[0]
is_deflected = False
placed_arrows = []
placed_labels = []
loads = []

scene.background = color.white
scene.width  = 900
scene.height = 540
scene.title  = "FEA Beam"

wall = box(pos=vec(-3.25, 0, 0), length=0.5, height=2.0, width=2.0,
           color=vec(0.45,0.45,0.5))

beam_segs = []
for i in range(NX):
    xc = -3 + (i + 0.5) * (L / NX)
    s  = box(pos=vec(xc, 0, 0), length=(L/NX)*0.97,
             height=BH, width=BW, color=vec(0.5,0.6,0.8))
    beam_segs.append(s)

arrow(pos=vec(-5,-3,0), axis=vec(0.6,0,0), color=color.red,   shaftwidth=0.04)
arrow(pos=vec(-5,-3,0), axis=vec(0,0.6,0), color=color.green, shaftwidth=0.04)
arrow(pos=vec(-5,-3,0), axis=vec(0,0,0.6), color=color.blue,  shaftwidth=0.04)
label(pos=vec(-4.3,-3,0),  text="X", color=color.red,   box=False)
label(pos=vec(-5,-2.3,0),  text="Y", color=color.green, box=False)
label(pos=vec(-5,-3,0.9),  text="Z", color=color.blue,  box=False)
label(pos=vec(-3.25,-1.5,0), text="Fixed", color=color.black, box=False)
label(pos=vec(3,-1.5,0),     text="Free",  color=color.black, box=False)

def moment_at(x):
    M = 0.0
    for ld in loads:
        a  = ld[0]
        Fy = ld[1]
        if x < a:
            M = M + Fy * (a - x)
    return M

def deflect_at(x):
    v = 0.0
    for ld in loads:
        a  = ld[0]
        Fy = ld[1]
        if x <= a:
            v = v + Fy * (x*x) * (3*a - x) / (6*E*I_beam)
        else:
            v = v + Fy * (a*a) * (3*x - a) / (6*E*I_beam)
    return v

def compute():
    SEG_LEN = L / NX
    SCALE   = 300
    peak = 0.0
    for i in range(NX):
        x = (i + 0.5) * SEG_LEN
        M = moment_at(x)
        s = abs(M * (BH/2) / I_beam)
        if s > peak:
            peak = s
    norm = peak
    if norm == 0:
        norm = 1
    for i in range(NX):
        x   = (i + 0.5) * SEG_LEN
        xc  = -3 + x
        M   = moment_at(x)
        v   = deflect_at(x)
        t   = abs(M * (BH/2) / I_beam) / norm
        if t < 0.5:
            seg_col = vec(t*2, t*2, 1)
        else:
            seg_col = vec(1, 2*(1-t), 0)
        beam_segs[i].pos   = vec(xc, v * SCALE, 0)
        beam_segs[i].color = seg_col
    tip_v     = deflect_at(L)
    sigma_max = peak
    stress_text.text  = str(round(sigma_max/1e6, 1)) + " MPa"
    deflect_text.text = str(round(tip_v*1000, 3)) + " mm"

def reset_all():
    SEG_LEN = L / NX
    for i in range(NX):
        xc = -3 + (i + 0.5) * SEG_LEN
        beam_segs[i].pos   = vec(xc, 0, 0)
        beam_segs[i].color = vec(0.5, 0.6, 0.8)
    for a in placed_arrows: a.visible = False
    for lb in placed_labels: lb.visible = False
    placed_arrows.clear()
    placed_labels.clear()
    loads.clear()
    stress_text.text  = "0 MPa"
    deflect_text.text = "0 mm"
    count_text.text   = "0"

def place_force(evt):
    clicked = scene.mouse.pick
    on_beam = False
    for s in beam_segs:
        if clicked is s:
            on_beam = True
    if not on_beam:
        return
    p = scene.mouse.project(normal=vec(0,1,0), point=vec(0, BH/2, 0))
    if p is None:
        return
    fx    = max(-2.9, min(2.9, p.x))
    a_pos = fx + 3
    mag = force_slider.value
    ang = angle_slider.value
    rad = ang * pi / 180.0
    dx  = cos(rad)
    dy  = sin(rad)
    direction = vec(dx, dy, 0)
    start = vec(fx, 0, 0) - direction * 1.8
    ar  = arrow(pos=start, axis=direction*1.6, color=color.red,
                shaftwidth=0.08, headwidth=0.2, headlength=0.15)
    lbl = label(pos=start - direction*0.4,
                text=str(int(mag)) + " kN",
                color=color.red, box=False, height=12)
    placed_arrows.append(ar)
    placed_labels.append(lbl)
    loads.append([a_pos, dy * mag * 1000.0])
    count_text.text = str(len(loads))
    compute()

def on_mat(m):
    global E
    E = mat_E[mat_names.index(m.selected)]
    matE_text.text = str(round(E/1e9,1)) + " GPa"

def on_force(s):
    force_readout.text = str(int(s.value)) + " kN"

def on_angle(s):
    angle_readout.text = str(int(s.value)) + " deg"

def on_clear(b):
    reset_all()

scene.append_to_caption("\n  Material: ")
mat_menu = menu(choices=mat_names, bind=on_mat)
scene.append_to_caption("  E = ")
matE_text = wtext(text="200.0 GPa")

scene.append_to_caption("\n\n  Force magnitude: ")
force_readout = wtext(text="50 kN")
scene.append_to_caption("\n  ")
force_slider = slider(min=1, max=150, value=50, length=280, bind=on_force)

scene.append_to_caption("\n\n  Force angle (0=right, 90=up, 270=down): ")
angle_readout = wtext(text="270 deg")
scene.append_to_caption("\n  ")
angle_slider = slider(min=0, max=359, value=270, length=280, bind=on_angle)

scene.append_to_caption("\n\n  ")
button(text="Clear all", bind=on_clear)

scene.append_to_caption("\n\n  Forces placed: ")
count_text = wtext(text="0")
scene.append_to_caption("\n  Max stress: ")
stress_text = wtext(text="0 MPa")
scene.append_to_caption("\n  Tip deflection: ")
deflect_text = wtext(text="0 mm")
scene.append_to_caption("\n\n  Click beam to place force. Drag to rotate.\n")

scene.bind("click", place_force)