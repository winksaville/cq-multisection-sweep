#!/usr/bin/env python
#  Based on: https://github.com/CadQuery/cadquery/issues/507#issuecomment-729078867
import cadquery as cq
from cadquery.vis import show

radius = 2
x = 50
y = 0
z = -5

pts = [(x, y, z), (x, (y+2), z), ((x-2), (y+14), z)]
#path = cq.Workplane("XY").moveTo(x, y).spline(pts) # moveTo does nothing and is not needed

wp = cq.Workplane("XY");
print(f"wp: {wp}")
print(f"wp.size(): {wp.size()}")
print(f"type(wp): {type(wp)}")
#print(f"dir(wp): {dir(wp)}") # print long list of methods and attributes

path = wp.spline(pts)
print(f"path: {path}")
print(f"path.size(): {path.size()}")
print(f"type(path): {type(path)}")
#print(f"dir(path): {dir(path)}") # print long list of methods and attributes
print(f"path.val(): {path.val()}")
print(f"type(path.val()): {type(path.val())}")
#print(f"dir(path.val()): {dir(path.val())}") # print long list of methods and attributes

first_item = path.first()
print(f"first_item: {first_item}, path.size(): {path.size()}")
print(f"type(first_item): {type(first_item)}")
#print(f"dir(first_item): {dir(first_item)}") # print long list of methods and attributes

loc0 = [path.val().locationAt(0)]
print(f"loc0: {loc0[0].toTuple()}, path.size(): {path.size()}")
loc1 = [path.val().locationAt(1)]
print(f"loc1: {loc1[0].toTuple()}, path.size(): {path.size()}")

def showCounts(name, wp):
    wire_count = len(wp.ctx.pendingWires)
    edge_count = len(wp.ctx.pendingEdges)
    parent_count = 0
    wp_pc = wp
    while(wp_pc.parent):
        parent_count += 1
        wp_pc = wp_pc.parent
    obj_count = len(wp.objects)
    print(f"{name} wp.size={wp.size()}, parents={parent_count}, wire_count={wire_count}, edge_count={edge_count}, obj_count={obj_count}")

# Original code and there are 6 invocations on the Workplane object
# and showCounts shows the same as showCounts(sweep) below
org_sweep = (cq.Workplane("XY")
    .pushPoints(loc0).circle(radius)
    .pushPoints(loc1).circle(radius * 2)
    .consolidateWires()
    .sweep(path,multisection=True)
)
showCounts("org_sweep", org_sweep)
show(org_sweep, title="org_sweep", edges=True, alpha=0.5)

# The following is the same as the original code but with
# but we break out into individual steps to show the counts
wp2 = cq.Workplane("XY")
showCounts("wp2", wp2)

wp2 = wp2.pushPoints(loc0);
showCounts("pushPoints(loc0)", wp2)
wp2 = wp2.circle(radius)
showCounts(f"circle({radius})", wp2)
wp2 = wp2.pushPoints(loc1);
showCounts("pushPoints(loc1)", wp2)
wp2 = wp2.circle(radius * 2)
showCounts(f"circle({radius * 2})", wp2)
wp2 = wp2.consolidateWires()
showCounts(f"consolidatedWires", wp2)
sweep = wp2.sweep(path,multisection=True)
showCounts(f"sweep", sweep)

# Export as ASCII STL
cq.Assembly(sweep).export("sweep.stl", exportType="STL", ascii=True)
showCounts("export sweep", sweep)

# Show the shape
show(sweep, title="sweep", edges=True, alpha=0.5)
showCounts("exiting sweep", sweep)
