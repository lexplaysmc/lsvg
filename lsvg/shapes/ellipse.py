'''`lsvg.shapes.ellipse` module

Objects:

`Ellipse`: A class representing an ellipse
`Circle`: A class representing a circle
'''

from .bezier import Bezier
import math as m

class Ellipse:
    '''`lsvg.shapes.ellipse.Ellipse` Object
    
    An ellipse which can be drawn with variable precision, thickness and color'''
    def __init__(self, pos:tuple, radiuses:tuple, rotation:int=0, color:tuple=(255, 255, 255), thickness:int=2, step:int=100) -> None:
        self.color=color
        self.thickness=thickness
        self.step=step
        self.pos=pos
        self.radiuses=radiuses
        self.rot=rotation
        self.curves=self._recurve()

    def draw(self, step:int=None) -> list:
        '''Returns `step*2` points on the ellipse.'''
        if step==None:
            step=self.step
        return self.curves[0].draw(step)+self.curves[1].draw(step)

    def _recurve(self) -> list:
        '''Remakes the bezier curves in the ellipse.'''
        width_two_thirds = self.radiuses[0] * 4 / 3
        dx1 = m.sin(self.rot) * self.radiuses[1]
        dy1 = m.cos(self.rot) * self.radiuses[1]
        dx2 = m.cos(self.rot) * width_two_thirds
        dy2 = m.sin(self.rot) * width_two_thirds
        topCenterX = self.pos[0] - dx1
        topCenterY = self.pos[1] + dy1
        topRightX = topCenterX + dx2
        topRightY = topCenterY + dy2
        topLeftX = topCenterX - dx2
        topLeftY = topCenterY - dy2
        bottomCenterX = self.pos[0] + dx1
        bottomCenterY = self.pos[1] - dy1
        bottomRightX = bottomCenterX + dx2
        bottomRightY = bottomCenterY + dy2
        bottomLeftX = bottomCenterX - dx2
        bottomLeftY = bottomCenterY - dy2
        return [Bezier((bottomCenterX, bottomCenterY), (bottomRightX, bottomRightY), (topRightX, topRightY), (topCenterX, topCenterY)), Bezier((topCenterX, topCenterY), (topLeftX, topLeftY), (bottomLeftX, bottomLeftY), (bottomCenterX, bottomCenterY))]
    
class Circle:
    '''`lsvg.shapes.ellipse.Circle` Object
    
    A circle which can be drawn with variable precision, thickness and color'''
    def __init__(self, pos:tuple, radius:int, color:tuple=(255, 255, 255), thickness:int=2, step:int=100) -> None:
        self.color=color
        self.thickness=thickness
        self.step=step
        self.pos=pos
        self.radius=radius
        self.curves=self._recurve()

    def _recurve(self) -> list:
        '''Remakes the bezier curves in the circle.'''
        self._ellipse=Ellipse(self.pos, [self.radius, self.radius], color=self.color, thickness=self.thickness, step=self.step)
        return self._ellipse._recurve()

    def draw(self, step:int=None) -> list:
        '''Returns `step*2` points on the circle.'''
        if step==None:
            step=self.step
        return self.curves[0].draw(step)+self.curves[1].draw(step)