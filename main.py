Web VPython 3.2

mat_names = ["Steel", "Aluminum", "Rubber"]
mat_E = [200e9, 69e9, 5e9]

NX = 40
NY = 8
L  = 6.0
BH = 0.4
BW = 0.3
I_beam = BW * BH**3 / 12.0
E = mat_E[0]
placed_arrows = []
placed_labels = []
loads = []

scene.background = color.white
scene.width  = 950
scene.height = 540
scene.title  = "FEA Beam"

wall = box(pos=vec(-3.25, 0, 0), length=0.5, height=1.6, width=1.2,
           color=vec(0.45,0.45,0.5))

click_target = box(pos=vec(0, 0, BW/2), length=L+1.0, height=BH+1.5, width=0.02,
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
label(pos=vec(3,-1.0,0),     text="Free",  color=color.black, box=False)

for k in range(11):
    t = k/10.0
    if t < 0.5:
        lc = vec(t*2, t*2, 1)
    else:
        lc = vec(1, 2*(1-t), 0)
    box(pos=vec(4.7, -1.2 + k*0.28, 0), length=0.35, height=0.24, width=0.05, color=lc)
label(pos=vec(5.5,-1.2,0),         text="Low",  color=color.black, box=False, height=11)
legend_hi = label(pos=vec(5.5,-1.2+10*0.28,0), text="High", color=color.black, box=False, height=11)
label(pos=vec(5.0,-1.2+11*0.28,0), text="Stress", color=color.black, box=False, height=12)

def stress_color(t):
    if t > 1: t = 1
    if t < 0: t = 0
    if t < 0.5:
        return vec(t*2, t*2, 1)
    return vec(1, 2*(1-t), 0)

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
    SCALE = 200
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
        x    = (i / NX) * L
        M    = moment_at(x)
        v    = deflect_at(x)
        xpos = -3 + x
        for j in range(NY + 1):
            y_fiber = -BH/2 + (j / NY) * BH
            sigma   = M * y_fiber / I_beam
            t       = abs(sigma) / norm
            verts[i][j].color = stress_color(t)
            verts[i][j].pos   = vec(xpos, y_fiber + v*SCALE, verts[i][j].pos.z)
    tip_v = deflect_at(L)
    eps   = peak / E
    legend_hi.text   = str(round(peak/1e6,1)) + " MPa"
    stress_text.text = str(round(peak/1e6,1)) + " MPa"
    deflect_text.text = str(round(tip_v*1000,3)) + " mm"
    strain_text.text  = str(round(eps*1e6,1)) + " micro-strain"

def reset_all():
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
    stress_text.text  = "0 MPa"
    deflect_text.text = "0 mm"
    strain_text.text  = "0 micro-strain"
    count_text.text   = "0"
    legend_hi.text    = "High"

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
    fx    = max(-3.0, min(-3.0+L, p.x))
    a_pos = fx + 3
    mag = force_slider.value
    ang = angle_slider.value
    rad = ang * pi / 180.0
    dx  = cos(rad)
    dy  = sin(rad)
    direction = vec(dx, dy, 0)
    base_y = deflect_at(a_pos) * 200
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
scene.append_to_caption("\n  Max strain: ")
strain_text = wtext(text="0 micro-strain")
scene.append_to_caption("\n\n  Click beam to place force. Drag to rotate.\n")

scene.bind("click", place_force)