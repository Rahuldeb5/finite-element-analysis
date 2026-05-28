# Web VPython 3.2
from vpython import *

forces = list()

def add_force(x, y, z, theta):
    forces.append({
        "x": x,
        "y": y,
        "z": z,
        "angle": theta
    })


scene.background = color.white
scene.width = 800
scene.height = 500
scene.camera.pos = vec(3, 3, 10)
scene.camera.axis = vec(0, -0.3, -1)

hatch1 = cylinder(pos=vec(-3.15, -0.8, 1.05), axis=vec(0, 1.6, 0), radius=0.03, color=color.black)
hatch2 = cylinder(pos=vec(-3.15, -0.8, 0.35), axis=vec(0, 1.6, 0), radius=0.03, color=color.black)
hatch3 = cylinder(pos=vec(-3.15, -0.8, -0.35), axis=vec(0, 1.6, 0), radius=0.03, color=color.black)
hatch4 = cylinder(pos=vec(-3.15, -0.8, -1.05), axis=vec(0, 1.6, 0), radius=0.03, color=color.black)

seg1 = box(pos=vec(-2, 0, 0), length=2, height=0.5, width=0.5, color=vec(0.3, 0.5, 1.0))
seg2 = box(pos=vec(0, 0, 0),  length=2, height=0.5, width=0.5, color=vec(0.6, 0.8, 0.4))
seg3 = box(pos=vec(2, 0, 0),  length=2, height=0.5, width=0.5, color=vec(1.0, 0.4, 0.2))

wall = box(pos=vec(-3.35, 0, 0), length=0.4, height=2, width=2,
           color=vec(0.5, 0.5, 0.55), opacity=0.8)

force_arrow = arrow(pos=vec(3, 2, 0), axis=vec(0, -1.5, 0),
                    color=color.red, shaftwidth=0.12,
                    headwidth=0.28, headlength=0.2)

x_axis = arrow(pos=vec(-4.5, -2.5, 0), axis=vec(0.6, 0, 0), color=color.red,   shaftwidth=0.04)
y_axis = arrow(pos=vec(-4.5, -2.5, 0), axis=vec(0, 0.6, 0), color=color.green, shaftwidth=0.04)
z_axis = arrow(pos=vec(-4.5, -2.5, 0), axis=vec(0, 0, 0.6), color=color.blue,  shaftwidth=0.04)
label(pos=vec(-3.8, -2.5, 0), text="X", color=color.red,   box=False, height=14)
label(pos=vec(-4.5, -1.8, 0), text="Y", color=color.green, box=False, height=14)
label(pos=vec(-4.5, -2.5, 0.8), text="Z", color=color.blue, box=False, height=14)

label(pos=vec(3, 3, 0), text="F = 50 kN", color=color.red, box=False, height=16)
label(pos=vec(-3.35, -1.5, 0), text="Fixed end", color=color.black, box=False)
label(pos=vec(3, -0.9, 0), text="Free end", color=color.black, box=False)