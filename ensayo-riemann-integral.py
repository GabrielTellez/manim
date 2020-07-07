from manimlib.imports import *
from scipy.misc import derivative

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


class VvsTintegral(GraphScene):
    CONFIG = {
        "x_axis_label": "$t$",
        "x_min": 0,
        "x_max": 10,
        "x_labeled_nums" : list(range(1, 11)),
        "x_axis_label" : "Tiempo $t$ (s)",
        "y_axis_label": "$x$",
        'y_min': -5,
        'y_max': 5,
        "y_tick_frequency" : 1,
        "y_labeled_nums" : list(range(-5, 6, 1)),
        "y_axis_label" : "Velocidad $v$ (m/s)",
        "graph_origin": 5 * LEFT,
        "t_min_integral": 3.0,
        "t_max_integral": 9.0,
    }
    def X(self,t):
        ts=t*0.55
        return 2*(0.3*ts**3-2.0*ts**2+3.0*ts)
    def V(self, t):
        return derivative(self.X, t, dx=0.0001)
    def animate_integral(self, tmin = None, tmax = None, n_iterations=5, max_dt=0.5):
        """Animates the Riemman sums/integral over the range [tmin, tmax]

        Args:
            tmin (float, optional): lower bound for the integral. Defaults to t_min_integral.
            tmax (float, optional): upper bound for the integral. Defaults to t_max_integral.
            n_iterations (int): number of iterations of rectangles.
            max_dt (float): starting dt
        """
        if tmin == None:
            tmin = self.t_min_integral   
        if tmax == None:
            tmax = self.t_max_integral   
        rects = self.get_riemann_rectangles_list(self.gr, n_iterations, max_dx=max_dt, x_min=tmin, x_max=tmax)
        last_rect = self.get_riemann_rectangles(
                        graph=self.gr,
                        dx=float(max_dt) / (2**(n_iterations+1)),
                        stroke_width=1.0/(2**(n_iterations+1)),
                        x_min=tmin, x_max=tmax
                    )
        self.play(ShowCreation(rects[0]))
        self.wait(2)
        for rect, next_rect in zip(rects,rects[1:]+[last_rect]):
            self.transform_between_riemann_rects(rect, next_rect)
            self.wait(2)
            self.remove(rect)
        self.add(last_rect)

    def construct(self):
        self.setup_axes()
        self.gr = self.get_graph(self.V)
        self.play(ShowCreation(self.gr))
        self.wait()
        self.animate_integral()
        self.wait()
        