# Web VPython 3.2
from vpython import *

forces = list()

def add_force(x, y, theta):
    forces.append({
        "x": x,
        "y": y,
        "angle": theta
    })


scene.background = color.white
scene.width = 800
scene.height = 500

beam = box(pos=vec(0, 0, 0), length=6, height=0.5, width=0.5, color=color.gray(0.7))

wall = box(pos=vec(-3.2, 0, 0), length=0.3, height=1.5, width=1, color=color.gray(0.4))

force_arrow = arrow(pos=vec(3, 1.5, 0), axis=vec(0, -1, 0),
                    color=color.red, shaftwidth=0.1)

label(pos=vec(3, 2, 0), text="F = 50 N", color=color.red, box=False)
label(pos=vec(-3.2, -1.2, 0), text="Fixed support", color=color.black, box=False)
label(pos=vec(0, -0.7, 0), text="Steel beam", color=color.black, box=False)
