from . import fix_uv, set_point

class Vec2:
    def __init__(self, x, y) -> None:
        self.x=x
        self.y=y

def getLine(start, end):
    # RETURNS ALL THE PIXELS THAT NEEDS TO BE FILLED TO FORM A LINE
    x1, y1 = int(start.x), int(start.y)
    x2, y2 = int(end.x), int(end.y)
    dx = x2 - x1
    dy = y2 - y1

    is_steep = abs(dy) > abs(dx)

    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True

    dx = x2 - x1
    dy = y2 - y1

    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1

    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = Vec2(y, x) if is_steep else Vec2(x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx

    if swapped:
        points.reverse()

    return points

RED = (255, 0, 0)
BLUE = (0, 105, 255)
GREEN = (0, 255, 0)

def drawLine(p1, p2, img, col):
    # DRAWS A LINE BY FILLING IN THE PIXELS RETURNED BY getLine
    points = getLine(p1, p2)
    for point in points:
        set_point(img, point.x, point.y, col)

# TRIANGLE
v1 = Vec2(500, 500)
v2 = Vec2(100, 100)
v3 = Vec2(1000, 200)

def fillFlatBottom(v1, v2, v3, img, col):
    # FILL IN TRIANGLE WITH A FLAT BOTTOM 
    invm1 = (v1.x - v2.x)/(v1.y - v2.y)
    invm2 = (v1.x - v3.x)/(v1.y - v3.y)

    curx1 = v1.x
    curx2 = v1.x

    for y in range(int(v1.y), int(v2.y+1)):
        drawLine(Vec2(curx1, y), Vec2(curx2, y), img, col)
        curx1 += invm1
        curx2 += invm2

def fillFlatTop(v1, v2, v3, img, col):
    # FILL IN TRIANGLE WITH A FLAT TOP
    invm1 = (v3.x - v2.x)/ (v3.y - v2.y)
    invm2 = (v3.x - v1.x)/ (v3.y - v1.y)

    curx1 = v3.x
    curx2 = v3.x

    for y in range(int(v3.y), int(v1.y), -1):
        drawLine(Vec2(curx1, y), Vec2(curx2, y), img, col)
        curx1 -= invm1
        curx2 -= invm2

def drawTriangle(v1, v2, v3, img, tlpos, res, col):
    # DRAWS ANY TRIANGLE BY SPLITTING THEM INTO FLAT TOP AND 
    # FLAT BOTTOM
    v = [Vec2(*fix_uv(*v1, *tlpos, res)), Vec2(*fix_uv(*v2, *tlpos, res)), Vec2(*fix_uv(*v3, *tlpos, res))]
    for i in range(0, len(v)):    
        for j in range(i+1, len(v)):    
            if(v[i].y > v[j].y):    
                tempy = v[i].y   
                v[i].y = v[j].y    
                v[j].y = tempy
                tempx = v[i].x
                v[i].x = v[j].x   
                v[j].x = tempx

    v1, v2, v3 = v[0], v[1], v[2]

    if v1.y == v2.y == v3.y:
        drawLine(v1, v2, img, col)
    elif v2.y == v3.y:
        fillFlatBottom(v1, v2, v3, img, col)
    elif v1.y == v2.y:
        fillFlatTop(v1, v2, v3, img, col)
    else:
        v4 = Vec2(v1.x + ((v2.y - v1.y)/ (v3.y - v1.y))* (v3.x - v1.x), v2.y)
        fillFlatBottom(v1, v2, v4, img, col)
        fillFlatTop(v2, v4, v3, img, col)