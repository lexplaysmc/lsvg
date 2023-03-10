def fill_circle(beziers):
    pts=[]
    for x in beziers:
        pts.extend(x.draw(100))
    oldpt=None
    f=[]
    for x in pts[1:]:
        if not oldpt:
            oldpt=x
            continue
        f.append((x, oldpt, pts[0]))
        oldpt=x
    return f