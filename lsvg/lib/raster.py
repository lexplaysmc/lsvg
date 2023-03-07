import numpy, lsvg.shapes.bezier as bezier, PIL.Image
import lsvg.shapes
from .trifill import drawTriangle

def rasterize(objects, height, width, tl, step:int=10000, res:int=3, antialiasres:int=2) -> PIL.Image.Image:
    antialiasres*=res
    img=numpy.zeros((height*antialiasres, width*antialiasres, 3), dtype=numpy.uint8)
    #setup
    processed=[]
    for x in objects:
        if isinstance(x, bezier.Bezier):
            processed.append([x.color, None, [x], []])
        elif isinstance(x, bezier.BezierChain):
            for y in x.curves:
                processed.append([y.color, None, [y], []])
        elif isinstance(x, (lsvg.shapes.Circle, lsvg.shapes.Ellipse)):
            processed.append([x.color, None, x.curves, []])
        else:
            processed.append([x.color, x.fill, x.curves, x._tripoints()])
    #rasterisation
    for color, fill, curves, tris in processed:
        if tris and fill:
            for tri in tris:
                drawTriangle(*tri, img, tl, antialiasres, numpy.asarray(fill, dtype=numpy.uint8))
        for curve in curves:
            _draw_curve(img, _filter(curve.draw(step), antialiasres), color, int(int(curve.thickness/2)*antialiasres), tl, antialiasres)
    x=PIL.Image.fromarray(img, 'RGB').resize((int(width*res), int(height*res)), 1)
    print('rasterizing complete')
    return x

def _draw_curve(img, curvepoints, color, thickness, tl, res):
    for point in curvepoints:
        img[int((point[1]-tl[1])*res-1)][int((point[0]-tl[0])*res-1)]=color
        for x in range(thickness):
            img[int((point[1]-tl[1])*res-1)][int((point[0]-tl[0])*res-1)+x]=color
            img[int((point[1]-tl[1])*res-1)][int((point[0]-tl[0])*res-1)-x]=color
            for y in range(thickness):
                if x**2+y**2<=thickness**2:
                    img[int((point[1]-tl[1])*res-1)+y][int((point[0]-tl[0])*res-1)+x]=color
                    img[int((point[1]-tl[1])*res-1)+y][int((point[0]-tl[0])*res-1)-x]=color
                    img[int((point[1]-tl[1])*res-1)-y][int((point[0]-tl[0])*res-1)-x]=color
                    img[int((point[1]-tl[1])*res-1)-y][int((point[0]-tl[0])*res-1)+x]=color

def _filter(pointlist:list, res:int) -> list:
    n=[]
    for x in pointlist:
        if [int(x[0]*res)/res, int(x[1]*res)/res] not in n:
            n.append([int(x[0]*res)/res, int(x[1]*res)/res])
    return n