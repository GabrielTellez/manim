from manimlib.imports import *

class RiemannIntegral(GraphScene):
    CONFIG = {
        "y_min": -1.5,
        "y_max": 1.5,
        "x_min": -5.0,
        "x_max": 5.0,
        "graph_origin": (0,0,0),
    }
    def construct(self):
        self.setup_axes()
        # gr = self.get_graph(lambda x: 0.1* x**2)
        # gr = self.get_graph(lambda x: 0.1* (x-4.0)**2-1.0)
        gr = self.get_graph(lambda x: np.sin(2.0*x))
        self.play(ShowCreation(gr))
        xmin, xmax = -2.0, 3.0
        rect = self.get_riemann_rectangles(gr, x_min=xmin, x_max=xmax)
        self.play(ShowCreation(rect))
        self.wait()
        self.remove(rect)
        self.wait()
        n_iterations, max_dx = 5, 0.5
        rects = self.get_riemann_rectangles_list(gr, n_iterations, max_dx=max_dx, x_min=xmin, x_max=xmax)
        # get.area: es demasiado gruesa
        area = self.get_area(gr,xmin,xmax)
        self.play(ShowCreation(area))
        self.wait()
        self.remove(area)
        last_rect = self.get_riemann_rectangles(
                graph=gr,
                dx=float(max_dx) / (2**(n_iterations+1)),
                stroke_width=1.0/(2**(n_iterations+1)),
                x_min=xmin, x_max=xmax)
        self.play(ShowCreation(last_rect))
        self.wait()
        self.remove(last_rect)
        for rect, next_rect in zip(rects,rects[1:]+[last_rect]):
            self.transform_between_riemann_rects(rect, next_rect)
            self.remove(rect)
        self.add(last_rect)
        self.wait()


   