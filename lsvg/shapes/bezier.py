'''`lsvg.shapes.bezier` module

Objects:

`Bezier`: A class representing a linear, quadratic or cubic bezier curve
`Chain`: A class which helps chain cubic bezier curves together
'''

import turtle as t

class Bezier:
    '''`lsvg.shapes.bezier.Bezier` Object
    
    A linear, quadratic or cubic bezier curve which can be drawn with variable precision, thickness and color'''
    def __init__(self, point1:tuple, point2:tuple, point3:tuple=None, point4:tuple=None, color:tuple=(255, 255, 255), thickness:int=2, step:int=100) -> None:
        self.color=color
        self.thickness=thickness
        self.step=step
        if point4:
            self.curvetype=3
            self.points=[point1, point2, point3, point4]
        elif point3:
            self.curvetype=2
            self.points=[point1, point2, point3]
        else:
            self.curvetype=1
            self.points=[point1, point2]
    def draw(self, step:int=None) -> list:
        '''Returns `step` evenly spaced points on the bezier curve'''
        points=[]
        if step==None:
            step=self.step
        for t in range(0, 1*step+1):
            v=t/step
            if self.curvetype==1:
                x=(1-v)*self.points[0][0]+v*self.points[1][0]
                y=(1-v)*self.points[0][1]+v*self.points[1][1]
            elif self.curvetype==2:
                x=(1-v)**2*self.points[0][0]+v*2*(1-v)*self.points[1][0]+v**2*self.points[2][0]
                y=(1-v)**2*self.points[0][1]+v*2*(1-v)*self.points[1][1]+v**2*self.points[2][1]
            elif self.curvetype==3:
                x=(1-v)**3*self.points[0][0]+3*(1-v)**2*v*self.points[1][0]+3*(1-v)*v**2*self.points[2][0]+v**3*self.points[3][0]
                y=(1-v)**3*self.points[0][1]+3*(1-v)**2*v*self.points[1][1]+3*(1-v)*v**2*self.points[2][1]+v**3*self.points[3][1]
            points.append([x, y])
        return points

class BezierChain:
    '''`lsvg.shapes.bezier.BezierChain` Object
    
    A chain of cubic bezier curves'''
    def __init__(self) -> None:
        self.curves=[]
    def add(self, curve:Bezier) -> None:
        '''Adds a curve to the chain and links it smoothly'''
        if self.curves:
            self.curves.append(curve)
            self.link(-1)
        else:
            self.curves.append(curve)
    def move(self, point:int, curve:int, pos:tuple, relative:bool=False) -> None:
        oldpos=self.curves[curve].points[point].copy()
        if relative and point==1:
            self.curves[curve].points[point]=[pos[0]+self.curves[curve].points[0][0], pos[1]+self.curves[curve].points[0][1]]
        elif relative and point==2:
            self.curves[curve].points[point]=[pos[0]+self.curves[curve].points[3][0], pos[1]+self.curves[curve].points[3][1]]
        else:
            self.curves[curve].points[point]=pos
        if point==0:
            self.curves[curve].points[1]=[pos[0]-oldpos[0]+self.curves[curve].points[1][0], pos[1]-oldpos[1]+self.curves[curve].points[1][1]]
        elif point==3:
            self.curves[curve].points[2]=[pos[0]-oldpos[0]+self.curves[curve].points[2][0], pos[1]-oldpos[1]+self.curves[curve].points[2][1]]
        if point in [0, 1]:
            self.update(-1)
        else:
            self.update()

    def link(self, i:int) -> list:
        '''Links the chain smoothly at one connection so that control points are opposite to each other and end points are at the same point.'''
        if i==0:
            self.curves[0].points[-1]=self.curves[-1].points[0]
            self.curves[0].points[-2]=flip(self.curves[-1].points[1], self.curves[-1].points[0])
        else:
            self.curves[i].points[-1]=self.curves[i-1].points[0]
            self.curves[i].points[-2]=flip(self.curves[i-1].points[1], self.curves[i-1].points[0])

    def update(self, ord:int=1) -> None:
        '''Links the whole chain smoothly so that control points are opposite to each other and end points are at the same point.'''
        for x in range(*sorted([0, len(self.curves)-1], reverse=bool(1-(ord+1)/2)), ord):
            self.link(x)

    def draw(self) -> list:
        return self.curves
        
def flip(pos1:tuple, pos2:tuple) -> list:
    '''Mirrors a point around another point on both axes.'''
    return [pos2[0]-(pos1[0]-pos2[0]), pos2[1]-(pos1[1]-pos2[1])]

def draw(curve:Bezier, points:bool=False) -> None:
    '''Draws a bezier curve in a turtle window'''
    t.pensize(curve.thickness)
    if points:
        t.pencolor('red')
        t.goto(curve.points[0])
        t.pendown()
        t.goto(curve.points[1])
        t.pencolor('blue')
        t.penup()
        t.goto(curve.points[2])
        t.pendown()
        t.goto(curve.points[3])
        t.penup()
    t.pencolor('#%02x%02x%02x'%curve.color)
    for x in curve.draw():
        t.goto(x)
        t.pendown()
    t.penup()

def draw_chain(curves:BezierChain, points:bool=False) -> None:
    '''Draws a bezier chain in a turtle window'''
    for x in curves:
        draw(x, points)