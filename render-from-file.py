from lsvg import Canvas
x=input('file: ')
canvas=Canvas(1, 1)
canvas.load(x)
canvas.rasterize().save(x.split('.')[0]+'.png')