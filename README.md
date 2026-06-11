# finite-element-analysis

Rahul Deb and Ryan Zhao
AP Physics C
Ms. Sharaf

This is a 3D cantilever beam simulation written in GlowScript VPython. It models how a beam deforms and stresses under applied forces using the Euler-Bernoulli beam theory.

To use it, start GlowScript and run the program. Choose a shape from the drop-down menu, choose material and type of the boundary conditions and modify beam size using the sliders. You can add a force vector using a mouse click on the beam, and you can adjust magnitude and direction before placement. The beam will be updated after each new force with color gradients for bending stresses and graph updates for deflection and bending stress. The Undo button removes the last force and clear button resets everything.

This simulation shows the following: bending moment M(x) = F(a - x); stress calculated based on bending formula using the Euler-Bernoulli relation with double integration of moment equation under cantilever boundary condition; strain calculated using Hooke's law (epsilon = sigma / E). The beam displays the 2D stress field from bending stresses using the blue-to-red color gradient when the show tension/compression is clicked.
