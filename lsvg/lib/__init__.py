def set_point_fix_uv(img, x, y, col, tl, res, transform=[0, 0]):
    pos=fix_uv(x, y, *tl, res)
    pos[0]+=transform[0]
    pos[1]+=transform[1]
    img[pos[1]][pos[0]]=col

def fix_uv(x, y, tlx, tly, res):
    return [int((x-tlx)*res)-1, int((y-tly)*res)-1]