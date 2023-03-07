'''`lsvg` module

Objects:

`Canvas`: A class which rasterizes objects'''
import lsvg.lib.raster
import turtle as t
import pickle

class Canvas:
    '''`lsvg.Canvas` Object
    
    A canvas used to rasterize objects in `lsvg.shapes`'''
    def __init__(self, width:int, height:int, *args, tlpos:tuple=None) -> None:
        self.width=width
        self.height=height
        self.tlpos=tlpos
        self.objects=args
        if not tlpos:
            self.tlpos=(-width/2, -height/2)
    
    def rasterize(self, step:int=1000, res:int=3, antialiasres:int=2):
        '''`lsvg.Canvas.rasterize()`
        
        `step` -> resolution of bezier curves
        `res` -> resolution of final image (multiplied by canvas size)
        `antialiasres` -> resolution to render at (multiplied by `res`)'''
        return lsvg.lib.raster.rasterize(self.objects, self.height, self.width, self.tlpos, step, res, antialiasres)

    def visualize(self) -> None:
        x=[self.tlpos, [self.tlpos[0], self.tlpos[1]+self.height], [self.tlpos[0]+self.width, self.tlpos[1]+self.height], [self.tlpos[0]+self.width, self.tlpos[1]], self.tlpos]
        t.goto(x[0])
        t.pendown()
        t.pensize(4)
        t.pencolor('purple')
        for y in x:
            t.goto(y)
        t.penup()
    
    def save(self, path:str='img.lsvg') -> None:
        with open(path, 'wb') as r:
            pickle.dump([self.width, self.height, self.tlpos, self.objects], r)
    def load(self, path:str='img.lsvg') -> None:
        with open(path, 'rb') as r:
            self.width, self.height, self.tlpos, self.objects=pickle.load(r)

def _filter(pointlist:list, res:int) -> list:
    n=[]
    for x in pointlist:
        if [int(x[0]*res)/res, int(x[1]*res)/res] not in n:
            n.append([int(x[0]*res)/res, int(x[1]*res)/res])
    return n