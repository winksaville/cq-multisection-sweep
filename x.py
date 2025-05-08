#!/usr/bin/env python
import cadquery as cq
from cadquery.vis import show

dia = 2
x = 50
y = 0
z = -5

pts = [(x, y, z), (x, (y+2), z), ((x-2), (y+14), z)]
path= cq.Workplane("XY").moveTo(x, 0).spline(pts)
#path= cq.Workplane("XY").spline(pts)

loc0 = [path.val().locationAt(0)]
loc1 = [path.val().locationAt(1)]
print(f"loc0: {loc0[0].toTuple()}, loc1: {loc1[0].toTuple()}")

#c2cir = cq.Workplane.pushPoints(loc0).circle(2)
c2wp = cq.Workplane("XY")
#show(c2wp, title="c2wp", edges=True, alpha=0.5) # empty
c2pts = c2wp.pushPoints(loc0)
#show(c2pts, title="c2pts", edges=True, alpha=0.5) # empty
c2cir = c2pts.circle(2)
show(c2cir, title="c2cir", edges=True, alpha=0.5) # shows just c2cir

c4cir = c2cir.pushPoints(loc1).circle(4)
show(c4cir, title="c4cir-no-consolidateWires", edges=True, alpha=0.5) # shows just c4cir
#c4cir = c4cir.consolidateWires() # unnecessary, no visible effect on s
#show(c4cir, title="c4cir-consolidateWires", edges=True, alpha=0.5) # Shows both circles

# Create the shape by sweeping the circle along the path
s = c4cir.sweep(path, multisection=True)
show(s, title="shape", edges=True, alpha=0.5)

#cq.exporters.export(shape) # Export as binary STL
cq.Assembly(s).export("s.stl", exportType="STL", ascii=True) # Export as ASCII STL

#sweep = (cq.Workplane("XY")
#    .pushPoints(loc0).circle(2)
#    .pushPoints(loc1).circle(4)
#    .consolidateWires()
#    .sweep(path,multisection=True)
#    )
#show(sweep, title="sweep")