'''Deprecated incredibly slow'''

from lsvg.shapes import Bezier
import math
def fill_tri(x1,y1,x2,y2,x3,y3,res,col):
    beziers=[]
    d1 = math.sqrt(((y2-y1)**2)+((x2-x1)**2))
    d2 = math.sqrt(((y3-y2)**2)+((x3-x2)**2))
    d3 = math.sqrt(((y1-y3)**2)+((x1-x3)**2))
    if (d1<d2) or (d1==d2):
        tx = x1
        ty = y1
        vx = (x2-x1)/d1
        vy = (y2-y1)/d1
        counter = 0
        while(counter<d1):
            beziers.append(create_bezier(x3,y3,tx,ty,res,col,max(d1,d2,d3)))
            tx = tx + vx
            ty = ty + vy
            counter = counter + 1
    elif (d2<d3) or (d2==d3):
        tx = x2
        ty = y2
        vx = (x3-x2)/d2
        vy = (y3-y2)/d2
        counter = 0
        while(counter<d2):
            beziers.append(create_bezier(x1,y1,tx,ty,res,col,max(d1,d2,d3)))
            tx = tx + vx
            ty = ty + vy
            counter = counter + 1
    else:
        tx = x3
        ty = y3
        vx = (x1-x3)/d3
        vy = (y1-y3)/d3
        counter = 0
        while counter<d3:
            beziers.append(create_bezier(x2,y2,tx,ty,res,col,max(d1,d2,d3)))
            tx += vx
            ty += vy
            counter += 1
    return beziers

def create_bezier(x1, y1, x2, y2, res, col, step):
    return Bezier((x1, y1), (x2, y2), thickness=res, color=col, step=step)