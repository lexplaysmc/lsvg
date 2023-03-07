'''`lsvg` module

Objects:

`Canvas`: A class which rasterizes objects'''
from .lib.trifill import drawTriangle
import lsvg.lib.raster
import numpy, PIL.Image
from matplotlib.colors import to_rgb
import turtle as t
from .shapes import bezier
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
    
    def rasterize_old(self, step:int=100, res:int=1, antialiasres:int=1.5) -> PIL.Image.Image:
        '''Deprecated, use `lsvg.Canvas.rasterize()`
        
        DOES NOT support filling triangles'''
        antialiasres*=res
        curves={}
        for x in self.objects:
            if type(x)==bezier.BezierChain:
                for y in x.curves:
                    curves.setdefault(str(y.thickness)+'#%02x%02x%02x'%y.color, [])
                    curves[str(y.thickness)+'#%02x%02x%02x'%y.color].append(_filter(y.draw(step)))
            else:
                curves.setdefault(str(x.thickness)+'#%02x%02x%02x'%x.color, [])
                curves[str(x.thickness)+'#%02x%02x%02x'%x.color].append(_filter(x.draw(step)))
        print('done')
        img=[]
        for y in range(int(self.height*antialiasres)):
            print('rasterizing', str(int(y/(self.height*antialiasres)*1000)/10)+'%')
            img.append([])
            for x in range(int(self.width*antialiasres)):
                pixelcolor=None
                xpos, ypos=self.tlpos[0]+x/antialiasres, self.tlpos[1]+y/antialiasres
                for props, curvess in curves.items():
                    thickness=int(props.split('#')[0])
                    color=props.split('#')[1]
                    for curve in curvess:
                        for point in curve:
                            if abs(int(point[0])+int(xpos))**2+abs(int(point[1])-int(ypos))**2<=(thickness/2)**2:
                                pixelcolor=color
                                break
                        if pixelcolor:
                            break
                    if pixelcolor:
                        break
                if pixelcolor==None:
                    pixelcolor='000000'
                img[-1].append(to_rgb('#'+pixelcolor))
        x=PIL.Image.fromarray((numpy.asarray(img)*255).astype(numpy.uint8), 'RGB').resize((int(self.width*res), int(self.height*res)), PIL.Image.BICUBIC)
        return x
    
    def rasterize(self, step:int=1000, res:int=3, antialiasres:int=1) -> PIL.Image.Image:
        '''`lsvg.Canvas.rasterize()`
        
        `step` -> resolution of bezier curves
        `res` -> resolution of final image (multiplied by canvas size)
        `antialiasres` -> resolution to render at (multiplied by `res`)'''
        print('setting up 0.0%', end='\r')
        v=0
        for x in self.objects:
            if not isinstance(x, bezier.Bezier):
                for y in x.curves:
                    v+=1
            else:
                v+=1
        percent=0
        w=0
        antialiasres*=res
        curves={}
        for x in self.objects:
            if not isinstance(x, bezier.Bezier):
                for y in x.curves:
                    curves.setdefault(str(y.thickness)+'#%02x%02x%02x'%y.color, [])
                    _=_filter(y.draw(step), antialiasres)
                    percent+=len(_)
                    curves[str(y.thickness)+'#%02x%02x%02x'%y.color].append(_)
                    w+=1
                    print('setting up', str(int(w/v*1000)/10)+'%       ', end='\r')
            else:
                curves.setdefault(str(x.thickness)+'#%02x%02x%02x'%x.color, [])
                _=_filter(x.draw(step), antialiasres)
                percent+=len(_)
                curves[str(x.thickness)+'#%02x%02x%02x'%x.color].append(_)
                w+=1
                print('setting up', str(int(w/v*1000)/10)+'%       ', end='\r')
        print('generating', end='\r')
        img=numpy.zeros((self.height*antialiasres, self.width*antialiasres, 3), dtype=numpy.uint8)
        completion=0
        print('tri          ', end='\r')
        tris={}
        for x in self.objects:
            if isinstance(x, (shapes.Quad, shapes.Rect)) and x.fill:
                tris.setdefault('#%02x%02x%02x'%x.fill, [])
                tris['#%02x%02x%02x'%x.fill].append(x._tripoints())
        v=0
        for x, y in tris.items():
            for z in y:
                col=to_rgb(x)
                color=numpy.asarray((col[0]*255, col[1]*255, col[2]*255), dtype=numpy.uint8)
                v+=1
                drawTriangle(*(z[0]), img, self.tlpos, antialiasres, color)
                v+=1
                drawTriangle(*(z[1]), img, self.tlpos, antialiasres, color)
        print('rasterizing 0.0%', end='\r')
        for props, curvess in curves.items():
            thickness=int(int(props.split('#')[0])/2*antialiasres)
            col=to_rgb('#'+props.split('#')[1])
            color=numpy.asarray((col[0]*255, col[1]*255, col[2]*255), dtype=numpy.uint8)
            for curve in curvess:
                for point in curve:
                    img[int((point[1]-self.height/2)*antialiasres-1)][int((point[0]-self.width/2)*antialiasres-1)]=color
                    for x in range(thickness):
                        img[int((point[1]-self.height/2)*antialiasres-1)][int((point[0]-self.width/2)*antialiasres-1)+x]=color
                        img[int((point[1]-self.height/2)*antialiasres-1)][int((point[0]-self.width/2)*antialiasres-1)-x]=color
                        for y in range(thickness):
                            if x**2+y**2<=thickness**2:
                                img[int((point[1]-self.height/2)*antialiasres-1)+y][int((point[0]-self.width/2)*antialiasres-1)+x]=color
                                img[int((point[1]-self.height/2)*antialiasres-1)+y][int((point[0]-self.width/2)*antialiasres-1)-x]=color
                                img[int((point[1]-self.height/2)*antialiasres-1)-y][int((point[0]-self.width/2)*antialiasres-1)-x]=color
                                img[int((point[1]-self.height/2)*antialiasres-1)-y][int((point[0]-self.width/2)*antialiasres-1)+x]=color
                    completion+=1
                    print('rasterizing', str(int(completion/percent*1000)/10)+'%       ', end='\r')
        print('converting           ', end='\r')
        x=PIL.Image.fromarray(img, 'RGB').resize((int(self.width*res), int(self.height*res)), 1)
        print('rasterizing complete. final res='+str((self.width*res, self.height*res)))
        return x
    
    def rasterlib(self, step:int=1000, res:int=3, antialiasres:int=2):
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