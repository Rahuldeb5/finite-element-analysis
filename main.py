Web VPython 3.2

mat_names   = ["Steel", "Aluminum", "Rubber"]
mat_E       = [200e9, 69e9, 5e9]
mat_yield   = [250e6, 95e6, 15e6]
shape_names = ["Thin Beam", "Square Block", "Wide Plate"]
shape_BH    = [0.3, 0.3, 0.5]
shape_BW    = [0.1, 0.3, 0.1]
bc_names    = ["Cantilever", "Simply Supported"]

NX = 40
NY = 8
L  = 6.0
BH = 0.3
BW = 0.1
I_beam = BW * BH**3 / 12.0
E = mat_E[0]
YIELD = mat_yield[0]
BC = "Cantilever"
is_loaded = False
show_tc = False
placed_arrows = []
placed_labels = []
loads = []

scene.background = color.white
scene.width  = 950
scene.height = 540

wall = box(pos=vec(-3.25, 0, 0), length=0.5, height=1.2, width=1.0,
           color=vec(0.45,0.45,0.5))
left_support  = box(pos=vec(-3, 0, 0), length=0.2, height=0.4, width=max(0.6, BW*4),
                    color=vec(0.45,0.45,0.5), visible=False)
right_support = box(pos=vec(3,  0, 0), length=0.2, height=0.4, width=max(0.6, BW*4),
                    color=vec(0.45,0.45,0.5), visible=False)
click_target = box(pos=vec(0, 0, 0), length=L+1.0, height=BH+1.5, width=0.02,
                   opacity=0.0, color=vec(0.5,0.6,0.8))

verts = []
for i in range(NX + 1):
    col = []
    x = -3 + (i / NX) * L
    for j in range(NY + 1):
        y = -BH/2 + (j / NY) * BH
        vt = vertex(pos=vec(x, y, BW/2), color=vec(0,0,1), normal=vec(0,0,1))
        col.append(vt)
    verts.append(col)

quads = []
for i in range(NX):
    for j in range(NY):
        q = quad(v0=verts[i][j], v1=verts[i+1][j],
                 v2=verts[i+1][j+1], v3=verts[i][j+1])
        quads.append(q)

arrow(pos=vec(-5,-2.5,0), axis=vec(0.6,0,0), color=color.red,   shaftwidth=0.04)
arrow(pos=vec(-5,-2.5,0), axis=vec(0,0.6,0), color=color.green, shaftwidth=0.04)
arrow(pos=vec(-5,-2.5,0), axis=vec(0,0,0.6), color=color.blue,  shaftwidth=0.04)
label(pos=vec(-4.3,-2.5,0), text="X", color=color.red,   box=False)
label(pos=vec(-5,-1.9,0),   text="Y", color=color.green, box=False)
label(pos=vec(-5,-2.5,0.8), text="Z", color=color.blue,  box=False)
label(pos=vec(-3.25,-1.0,0), text="Fixed", color=color.black, box=False)
free_label = label(pos=vec(3,-1.0,0), text="Free", color=color.black, box=False)

legend_title = label(pos=vec(5.4,-1.2+11*0.28,0), text="Stress", color=color.black, box=False, height=12)
for k in range(11):
    t = k/10.0
    if t < 0.5:
        lc = vec(t*2, t*2, 1)
    else:
        lc = vec(1, 2*(1-t), 0)
    box(pos=vec(4.7, -1.2 + k*0.28, 0), length=0.35, height=0.24, width=0.05, color=lc)
label(pos=vec(5.5,-1.2,0),         text="0",   color=color.black, box=False, height=11)
legend_hi = label(pos=vec(5.6,-1.2+10*0.28,0), text="max", color=color.black, box=False, height=11)

def stress_color(t):
    if t > 1: t = 1
    if t < 0: t = 0
    if t < 0.5:
        return vec(t*2, t*2, 1)
    return vec(1, 2*(1-t), 0)

def tc_color(r):
    if r > 1: r = 1
    if r < -1: r = -1
    if r >= 0:
        return vec(1, 1-r, 1-r)
    return vec(1+r, 1+r, 1)

def moment_at(x):
    M = 0.0
    for ld in loads:
        a  = ld[0]
        Fy = ld[1]
        if BC == "Cantilever":
            if x < a:
                M = M + Fy * (a - x)
        else:
            b = L - a
            if x <= a:
                M = M + Fy * b * x / L
            else:
                M = M + Fy * a * (L - x) / L
    return M

def deflect_at(x):
    v = 0.0
    for ld in loads:
        a  = ld[0]
        Fy = ld[1]
        if BC == "Cantilever":
            if x <= a:
                v = v + Fy * (x*x) * (3*a - x) / (6*E*I_beam)
            else:
                v = v + Fy * (a*a) * (3*x - a) / (6*E*I_beam)
        else:
            b = L - a
            if x <= a:
                v = v + Fy * b * x * (L*L - b*b - x*x) / (6*E*I_beam*L)
            else:
                v = v + Fy * a * (L-x) * (2*L*x - a*a - x*x) / (6*E*I_beam*L)
    return v

def compute():
    global is_loaded
    SCALE = 100
    peak = 0.0
    for i in range(NX + 1):
        x = (i / NX) * L
        M = moment_at(x)
        s = abs(M * (BH/2) / I_beam)
        if s > peak:
            peak = s
    norm = peak
    if norm == 0:
        norm = 1
    for i in range(NX + 1):
        x = (i / NX) * L
        M = moment_at(x)
        v = deflect_at(x)
        xpos = -3 + x
        for j in range(NY + 1):
            y_fiber = -BH/2 + (j / NY) * BH
            sigma = M * y_fiber / I_beam
            if show_tc:
                sign_flip = 1 if BC == "Simply Supported" else -1
                verts[i][j].color = tc_color(sign_flip * M * y_fiber / I_beam / norm)
            else:
                verts[i][j].color = stress_color(abs(sigma) / norm)
            verts[i][j].pos = vec(xpos, y_fiber + v*SCALE, verts[i][j].pos.z)
    tip_v = deflect_at(L)
    eps = peak / E
    pct = peak / YIELD * 100
    stress_text.text  = str(round(peak/1e6, 1)) + " MPa (" + str(round(pct,0)) + "% of yield)"
    deflect_text.text = str(round(tip_v*1000, 3)) + " mm"
    strain_text.text  = str(round(eps*1e6, 1)) + " micro-strain"
    legend_hi.text    = str(round(peak/1e6,1)) + " MPa"
    update_graphs()
    is_loaded = True

stress_curve  = gcurve(graph=graph(title="Stress sigma(x)",    xtitle="x (m)", ytitle="MPa", width=440, height=220, fast=False), color=color.red)
deflect_curve = gcurve(graph=graph(title="Deflection delta(x)",xtitle="x (m)", ytitle="mm",  width=440, height=220, fast=False), color=color.blue)

def update_graphs():
    stress_curve.delete()
    deflect_curve.delete()
    for i in range(NX + 1):
        x = (i / NX) * L
        M = moment_at(x)
        v = deflect_at(x)
        stress_curve.plot(x,  M * (BH/2) / I_beam / 1e6)
        deflect_curve.plot(x, v * 1000)

def update_geometry():
    global I_beam, is_loaded
    I_beam = BW * BH**3 / 12.0
    for i in range(NX + 1):
        xpos = -3 + (i / NX) * L
        for j in range(NY + 1):
            y_fiber = -BH/2 + (j / NY) * BH
            verts[i][j].pos   = vec(xpos, y_fiber, BW/2)
            verts[i][j].color = vec(0,0,1)
    wall.height         = max(1.2, BH * 4)
    wall.width          = max(1.0, BW * 4)
    click_target.length = L + 1.0
    click_target.height = BH + 1.5
    click_target.pos    = vec(-3 + L/2, 0, 0)
    free_label.pos      = vec(-3 + L, -BH - 0.5, 0)
    wall.visible          = BC == "Cantilever"
    left_support.visible  = BC != "Cantilever"
    right_support.visible = BC != "Cantilever"
    left_support.pos    = vec(-3, -BH/2, 0)
    left_support.height = 0.4
    left_support.width  = max(0.6, BW * 4)
    right_support.pos   = vec(-3 + L, -BH/2, 0)
    right_support.height = 0.4
    right_support.width  = max(0.6, BW * 4)
    for a in placed_arrows: a.visible = False
    for lb in placed_labels: lb.visible = False
    placed_arrows.clear()
    placed_labels.clear()
    loads.clear()
    is_loaded = False
    stress_text.text  = "0 MPa"
    deflect_text.text = "0 mm"
    strain_text.text  = "0 micro-strain"
    count_text.text   = "0"
    legend_hi.text    = "max"
    I_text.text       = str(round(I_beam * 1e6, 3)) + " x10-6 m^4"
    stress_curve.delete()
    deflect_curve.delete()

def reset_all():
    global is_loaded
    for i in range(NX + 1):
        xpos = -3 + (i / NX) * L
        for j in range(NY + 1):
            y_fiber = -BH/2 + (j / NY) * BH
            verts[i][j].pos   = vec(xpos, y_fiber, verts[i][j].pos.z)
            verts[i][j].color = vec(0,0,1)
    for a in placed_arrows: a.visible = False
    for lb in placed_labels: lb.visible = False
    placed_arrows.clear()
    placed_labels.clear()
    loads.clear()
    is_loaded = False
    stress_text.text  = "0 MPa"
    deflect_text.text = "0 mm"
    strain_text.text  = "0 micro-strain"
    count_text.text   = "0"
    legend_hi.text    = "max"
    stress_curve.delete()
    deflect_curve.delete()

def place_force(evt):
    clicked = scene.mouse.pick
    on_target = clicked is click_target
    for q in quads:
        if clicked is q:
            on_target = True
    if not on_target:
        return
    p = scene.mouse.project(normal=vec(0,0,1), point=vec(0,0,BW/2))
    if p is None:
        return
    fx    = max(-3.0, min(-3.0 + L, p.x))
    a_pos = fx + 3
    mag = force_slider.value
    ang = angle_slider.value
    rad = ang * pi / 180.0
    dx  = cos(rad)
    dy  = sin(rad)
    direction = vec(dx, dy, 0)
    base_y = deflect_at(a_pos) * 100
    start  = vec(fx, base_y, BW/2) - direction * 1.8
    ar  = arrow(pos=start, axis=direction*1.6, color=color.black,
                shaftwidth=0.07, headwidth=0.18, headlength=0.13)
    lbl = label(pos=start - direction*0.3,
                text=str(int(mag)) + " kN @ " + str(int(ang)) + " deg",
                color=color.black, box=False, height=12)
    placed_arrows.append(ar)
    placed_labels.append(lbl)
    loads.append([a_pos, dy * mag * 1000.0])
    count_text.text = str(len(loads))
    compute()

def on_bc(m):
    global BC
    BC = m.selected
    if BC == "Cantilever":
        wall.visible          = True
        left_support.visible  = False
        right_support.visible = False
        free_label.text = "Free"
    else:
        wall.visible          = False
        left_support.visible  = True
        right_support.visible = True
        free_label.text = "Support"
    reset_all()

def on_shape(m):
    global BH, BW
    idx = shape_names.index(m.selected)
    BH = shape_BH[idx]
    BW = shape_BW[idx]
    BH_readout.text = str(round(BH,2)) + " m"
    BW_readout.text = str(round(BW,2)) + " m"
    BH_slider.value = BH
    BW_slider.value = BW
    update_geometry()

def on_mat(m):
    global E, YIELD
    idx   = mat_names.index(m.selected)
    E     = mat_E[idx]
    YIELD = mat_yield[idx]
    matE_text.text = str(round(E/1e9,1)) + " GPa"
    if is_loaded:
        compute()

def on_force(s):
    force_readout.text = str(int(s.value)) + " kN"

def on_angle(s):
    angle_readout.text = str(int(s.value)) + " deg"

def on_undo(b):
    if len(loads) == 0:
        return
    loads.pop()
    placed_arrows[-1].visible = False
    placed_labels[-1].visible = False
    placed_arrows.pop()
    placed_labels.pop()
    count_text.text = str(len(loads))
    if len(loads) == 0:
        reset_all()
    else:
        compute()

def on_clear(b):
    reset_all()

def on_tc(c):
    global show_tc
    show_tc = c.checked
    legend_title.text = "Red=tension Blue=compression" if show_tc else "Stress"
    if is_loaded:
        compute()

def on_L(s):
    global L
    L = s.value
    L_readout.text = str(round(L,1)) + " m"
    update_geometry()

def on_BH(s):
    global BH
    BH = s.value
    BH_readout.text = str(round(BH,2)) + " m"
    update_geometry()

def on_BW(s):
    global BW
    BW = s.value
    BW_readout.text = str(round(BW,2)) + " m"
    update_geometry()

scene.append_to_caption("\n  Boundary: ")
bc_menu = menu(choices=bc_names, index=0, bind=on_bc)
scene.append_to_caption("    Shape: ")
shape_menu = menu(choices=shape_names, bind=on_shape)
scene.append_to_caption("    Material: ")
mat_menu = menu(choices=mat_names, bind=on_mat)
scene.append_to_caption("  E = ")
matE_text = wtext(text="200.0 GPa")

scene.append_to_caption("\n\n  L: ")
L_readout = wtext(text="6.0 m")
scene.append_to_caption("  ")
L_slider = slider(min=2, max=12, value=6, length=220, bind=on_L)
scene.append_to_caption("    h: ")
BH_readout = wtext(text="0.30 m")
scene.append_to_caption("  ")
BH_slider = slider(min=0.1, max=0.8, value=0.3, length=180, bind=on_BH)
scene.append_to_caption("    b: ")
BW_readout = wtext(text="0.10 m")
scene.append_to_caption("  ")
BW_slider = slider(min=0.05, max=0.5, value=0.1, length=180, bind=on_BW)
scene.append_to_caption("   I = ")
I_text = wtext(text=str(round(I_beam*1e6,3)) + " x10-6 m^4")

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
scene.append_to_caption("    ")
button(text="Undo last", bind=on_undo)
scene.append_to_caption("    ")
checkbox(text="Show tension / compression", bind=on_tc)

scene.append_to_caption("\n\n  Forces placed: ")
count_text = wtext(text="0")

scene.append_to_caption("\n\n  Max bending stress: ")
stress_text = wtext(text="0 MPa")
scene.append_to_caption("\n  Tip deflection: ")
deflect_text = wtext(text="0 mm")
scene.append_to_caption("\n  Max strain: ")
strain_text = wtext(text="0 micro-strain")
scene.append_to_caption("\n\n  Click beam to place force. Drag to rotate.\n")

wall.visible = True
left_support.visible = False
right_support.visible = False

scene.bind("click", place_force)