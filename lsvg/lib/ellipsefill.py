from .flowerdist import sunflower
from .trifill import drawTriangle

def fill_circle(img, pos, radius, filcol, squaresize, res, tl):
    points=sunflower(pos, radius, int((radius**2/squaresize)*10))
    for point in points:
        img[int((point[1]-tl[1])*res-1)][int((point[0]-tl[0])*res-1)]=filcol
        for x in range(squaresize*res):
            img[int((point[1]-tl[1])*res-1)][int((point[0]-tl[0])*res-1)+x]=filcol
            img[int((point[1]-tl[1])*res-1)][int((point[0]-tl[0])*res-1)-x]=filcol
            for y in range(squaresize*res):
                img[int((point[1]-tl[1])*res-1)+y][int((point[0]-tl[0])*res-1)+x]=filcol
                img[int((point[1]-tl[1])*res-1)+y][int((point[0]-tl[0])*res-1)-x]=filcol
                img[int((point[1]-tl[1])*res-1)-y][int((point[0]-tl[0])*res-1)-x]=filcol
                img[int((point[1]-tl[1])*res-1)-y][int((point[0]-tl[0])*res-1)+x]=filcol

def fill_circle1(beziers):
    pts=[]
    for x in beziers:
        pts.extend(x.draw(100))
    oldpt=None
    f=[]
    print(pts)
    for x in pts[1:]:
        if not oldpt:
            oldpt=x
            continue
        f.append((x, oldpt, pts[0]))
        oldpt=x
    return f