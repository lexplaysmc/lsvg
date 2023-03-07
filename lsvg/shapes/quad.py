'''`lsvg.shapes.quad` module

Objects:

`Quad`: A class representing a quadrilateral shape
`Rect`: A class representing a rectangle
'''

from .bezier import Bezier
from lsvg.lib.trifill import drawTriangle

class Quad:
    '''`lsvg.shapes.quad.Quad` Object
    
    A quadrilateral shape which can be drawn with variable precision, thickness, fill color and line color'''
    def __init__(self, point1:tuple, point2:tuple, point3:tuple, point4:tuple, linecolor:tuple=(255, 255, 255), fillcolor:tuple=None, thickness:int=2, step:int=100) -> None:
        self.color=linecolor
        self.thickness=thickness
        self.step=step
        self.points=[point1, point2, point3, point4]
        self.curves=self._recurve()
        self.fill=fillcolor

    def draw(self, step:int=None) -> list:
        if step==None:
            step=self.step
        return self.curves[0].draw(step)+self.curves[1].draw(step)+self.curves[2].draw(step)+self.curves[3].draw(step)

    def _recurve(self):
        return [Bezier(self.points[0], self.points[1]), Bezier(self.points[1], self.points[2]), Bezier(self.points[2], self.points[3]), Bezier(self.points[3], self.points[0])]
    
    def _tripoints(self):
        return [self.points[0:3], self.points[2:]+[self.points[0]]]


class Rect:
    '''`lsvg.shapes.quad.Rect` Object
    
    A rectangle which can be drawn with variable precision, thickness and color'''
    def __init__(self, point1:tuple, point2:tuple, linecolor:tuple=(255, 255, 255), fillcolor:tuple=None, thickness:int=2, step:int=100) -> None:
        self.color=linecolor
        self.fill=fillcolor
        self.thickness=thickness
        self.step=step
        self.points=[point1, point2]
        self.curves=self._recurve()

    def draw(self, step:int=None) -> list:
        if step==None:
            step=self.step
        return self.curves[0].draw(step)+self.curves[1].draw(step)+self.curves[2].draw(step)+self.curves[3].draw(step)
        
    def _recurve(self):
        self._quad=Quad(self.points[0], [self.points[0][0], self.points[1][1]], self.points[1], [self.points[1][0], self.points[0][1]])
        return self._quad._recurve()
    
    def _tripoints(self):
        self._quad=Quad(self.points[0], [self.points[0][0], self.points[1][1]], self.points[1], [self.points[1][0], self.points[0][1]])
        return self._quad._tripoints()