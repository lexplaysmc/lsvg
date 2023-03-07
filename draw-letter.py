from lsvg import Canvas
from lsvg.shapes import Bezier, Circle, Rect, Quad

curves=[]
curves.extend([Rect((233, 233), (-200, -200), fillcolor=(255, 0, 0))])
curves.extend([Quad((200, 200), (-100, -200), (-150, -150), (-150, -10), fillcolor=(0, 255, 255))])
curves.extend([Bezier((0, 0), (100, 0), (0, 100), (0, 0)), Bezier((0, 0), (-100, 0), (0, 100), (0, 0)), Bezier((0, 0), (-100, 0), (0, -100), (0, 0)), Bezier((0, 0), (100, 0), (0, -100), (0, 0))])
#curves.extend([Circle((0, 0), 200)])
canvas=Canvas(700, 500, *curves)

canvas.rasterize(step=1000).save('img.png')
canvas.save()