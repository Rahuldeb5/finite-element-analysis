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
 
num_forces = 0
 
def place_force(evt):
    global num_forces
    clicked = scene.mouse.pick
    if clicked is beam:

        p = scene.mouse.project(normal=vec(0,1,0), point=vec(0, 0.25, 0))
        if p is None:
            return
        
        fx = max(-2.9, min(2.9, p.x))
        fz = max(-0.2, min(0.2, p.z))
        num_forces = num_forces + 1
        arrow(pos=vec(fx, 2.5, fz), axis=vec(0, -2, 0),
              color=color.red, shaftwidth=0.1,
              headwidth=0.25, headlength=0.18)
        label(pos=vec(fx, 3.1, fz), text="50 kN",
              color=color.red, box=False, height=13)
 
scene.bind("click", place_force)