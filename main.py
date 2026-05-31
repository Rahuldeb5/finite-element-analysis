# Web VPython 3.2
from vpython import *

# forces = list()

# def add_force(x, y, z, theta):
#     forces.append({
#         "x": x,
#         "y": y,
#         "z": z,
#         "angle": theta
#     })

scene.background = color.white
scene.width = 900
scene.height = 600
scene.camera.pos = vec(0, 5, 14)
scene.camera.axis = vec(0, -0.35, -1)
scene.title = "Click on the beam to add a force arrow"
 
wall = box(pos=vec(-3.25, 0, 0), length=0.5, height=2, width=2,
           color=vec(0.5, 0.5, 0.55))
 
beam = box(pos=vec(0, 0, 0), length=6, height=0.5, width=0.5,
           color=vec(0.5, 0.6, 0.8))
 
arrow(pos=vec(-5, -3, 0), axis=vec(0.7, 0, 0), color=color.red,   shaftwidth=0.05)
arrow(pos=vec(-5, -3, 0), axis=vec(0, 0.7, 0), color=color.green, shaftwidth=0.05)
arrow(pos=vec(-5, -3, 0), axis=vec(0, 0, 0.7), color=color.blue,  shaftwidth=0.05)
label(pos=vec(-4.2, -3, 0), text="X", color=color.red, box=False)
label(pos=vec(-5, -2.2, 0), text="Y", color=color.green, box=False)
label(pos=vec(-5, -3, 1),  text="Z", color=color.blue, box=False)
 
label(pos=vec(-3.25, -1.4, 0), text="Fixed end", color=color.black, box=False)
label(pos=vec(3,-1.4, 0), text="Free end",  color=color.black, box=False)
 
scene.append_to_caption("\nClick the beam to place a 50 kN downward force arrow.\n")
 
placed_arrows = []
placed_labels = []
net_force_y = 0
num_forces = 0
 
def get_direction():
    d = dir_menu.selected
    if d == "Down":
        return vec(0, -1, 0)
    if d == "Up":
        return vec(0, 1, 0)
    if d == "Left":
        return vec(-1, 0, 0)
    return vec(1, 0, 0)
 
def get_arrow_color():
    d = dir_menu.selected
    if d == "Down":
        return color.red
    if d == "Up":
        return color.orange
    if d == "Left":
        return color.purple
    return color.magenta
 
def update_readout(s):
    force_readout.text = str(int(s.value))
 
def on_dir(m):
    pass
 
def clear_forces(b):
    global net_force_y, num_forces
    for a in placed_arrows:
        a.visible = False
    for lbl in placed_labels:
        lbl.visible = False
    placed_arrows.clear()
    placed_labels.clear()
    net_force_y = 0
    num_forces = 0
    count_text.text = "0"
    net_text.text = "0 kN"
 
def place_force(evt):
    global net_force_y, num_forces
    clicked = scene.mouse.pick
    if clicked is beam:

        p = scene.mouse.project(normal=vec(0,1,0), point=vec(0, 0.25, 0))
        if p is None:
            return

        fx = max(-2.9, min(2.9, p.x))
        fz = max(-0.2, min(0.2, p.z))
        mag = force_slider.value
        direction = get_direction()
        col = get_arrow_color()
        if direction.y < 0:
            start = vec(fx, 2.5, fz)
        elif direction.y > 0:
            start = vec(fx, -2.5, fz)
        elif direction.x < 0:
            start = vec(4, 0, fz)
        else:
            start = vec(-4, 0, fz)
        a = arrow(pos=start, axis=direction * 2,
                  color=col, shaftwidth=0.1,
                  headwidth=0.25, headlength=0.18)
        lbl = label(pos=start + direction * (-0.5),
                    text=str(int(mag)) + " kN",
                    color=col, box=False, height=13)
        placed_arrows.append(a)
        placed_labels.append(lbl)
        net_force_y = net_force_y + direction.y * mag
        num_forces = num_forces + 1
        count_text.text = str(num_forces)
        net_text.text = str(round(net_force_y, 1)) + " kN"
 
scene.append_to_caption("\n  Force magnitude (kN): ")
force_readout = wtext(text="50")
scene.append_to_caption(" kN\n  ")
force_slider = slider(min=10, max=200, value=50, length=250, bind=update_readout)
scene.append_to_caption("\n\n  Direction:  ")
dir_menu = menu(choices=["Down", "Up", "Left", "Right"], bind=on_dir)
scene.append_to_caption("\n\n  ")
clear_btn = button(text="Clear all forces", bind=clear_forces)
scene.append_to_caption("\n\n  Forces placed: ")
count_text = wtext(text="0")
scene.append_to_caption("\n  Net Y force: ")
net_text = wtext(text="0 kN")
scene.append_to_caption("\n\n  Click the beam to place an arrow.\n")
 
scene.bind("click", place_force)