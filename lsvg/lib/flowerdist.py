from math import sin, cos, tau

def sunflower(centre, radius, points, exp=0.5, turnfraction=(1+5**0.5)/2):
    l=[]
    for i in range(points):
        dst=(i/(points-1))**exp
        angle=tau*turnfraction*i
        l.append((dst*cos(angle)*radius+centre[0], dst*sin(angle)*radius+centre[1]))
    return l

if __name__=='__main__':
    import turtle as t
    t.Screen().tracer(0)
    y=sunflower([0, 0], 300, 4500)
    for x in y:
        t.penup()
        t.goto(x[0], x[1]-5)
        t.pendown()
        t.begin_fill()
        t.fd(5)
        t.lt(90)
        t.fd(10)
        t.lt(90)
        t.fd(10)
        t.lt(90)
        t.fd(10)
        t.lt(90)
        t.fd(5)
        t.end_fill()
    t.penup()
    t.goto(0, -300)
    t.pendown()
    t.circle(300)
    t.update()
    while True:
        pass