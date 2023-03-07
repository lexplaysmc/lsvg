import lsvg.shapes.bezier as bezier
import lsvg
import lsvg.lib.beziertri
import math as m

chain=bezier.BezierChain()
chain.add(bezier.Bezier([-100, 0], [-100, -50], [-50, -100], [0, -100], (255, 255, 255), 2))
chain.add(bezier.Bezier([0, 100], [-50, 100], [-100, 50], [-100, 0], (255, 255, 255), 2))
chain.add(bezier.Bezier([100, 0], [100, 50], [50, 100], [0, 100], (255, 255, 255), 2))
chain.add(bezier.Bezier([0, -100], [50, -100], [100, -50], [100, 0], (255, 255, 255), 2))

chain.move(1, 0, [50*m.sin(1)-100, 50*m.cos(1)])
canvas=lsvg.Canvas(500, 300, chain)#*lsvg.lib.beziertri.fill_tri(100, 100, -100, 100, -100, -100, 6, (255, 0, 0)))


chain.move(0, 0, [-abs(100*m.sin(1.5)), 0])
chain.move(1, 0, [50*m.sin(1), 50*m.cos(1)], relative=True)
canvas.rasterize().save('img.png')