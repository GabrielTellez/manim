from manimlib.imports import *

class RiemannIntegral(GraphScene):
    def construct(self):
        self.setup_axes()
        gr = self.get_graph(lambda x: 0.1* x**2)
        self.play(ShowCreation(gr))
        xmin, xmax = 3, 8
        rect = self.get_riemann_rectangles(gr, x_min=xmin, x_max=xmax)
        self.play(ShowCreation(rect))
        self.wait()
        self.remove(rect)
        self.wait()
        rects = self.get_riemann_rectangles_list(gr, 5, x_min=xmin, x_max=xmax)
        area = self.get_area(gr,xmin,xmax)
        for rect, next_rect in zip(rects,rects[1:]+[area]):
            self.transform_between_riemann_rects(rect, next_rect)
        self.wait()


   