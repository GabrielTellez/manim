from manimlib.imports import *
import numpy as np

class BareOscilator(GraphScene):
    CONFIG = {
        "x_min": -10,
        "x_max": 10,
        "x_axis_width": FRAME_WIDTH,
        "y_min": 0,
        "y_max": 30,
        "y_axis_height": FRAME_HEIGHT * 0.7,
        "y_tick_frequency": 5,
        "graph_origin": BOTTOM + UP,
        "y_axis_label": "$U$",
        "x_extreme_complete_min": -6,
        "x_extreme_complete_max": 6,
        "x_extreme_osc_min": -4,
        "x_extreme_osc_max": 4,
        "run_time_def": 5,
        "loops": 2,
    }
    def initialize(self):
        pass
    def U(self, x):
        return 0.0
    def X(self, x):
        return 0.0
    def construct(self):
        self.setup_axes(animate=False)
        self.initialize()
        funcs=(('X', self.X), ('U', self.U))
        path_complete=self.get_graph(self.U, x_min=self.x_extreme_complete_min, x_max=self.x_extreme_complete_max) 
        E = self.U(self.x_extreme_osc_min)
        energy_line=self.get_graph(lambda x: E) 
        paths={}
        for label, fnc in funcs:
            paths[label]={
                'dot': Dot(self.coords_to_point(self.x_extreme_osc_min,self.U(self.x_extreme_osc_min))),
                'forward': self.get_graph(fnc, x_min=self.x_extreme_osc_min, x_max=self.x_extreme_osc_max), 
                'backwards': self.get_graph(fnc, x_min=self.x_extreme_osc_max, x_max=self.x_extreme_osc_min)
                } 
        self.play(ShowCreation(path_complete),
            ShowCreation(energy_line))
        for label, fnc in funcs:
            ShowCreation(paths[label]['dot'])
        for loop in range(self.loops):
            for direction in ['forward', 'backwards']:
                self.play(MoveAlongPath(paths['U']['dot'], paths['U'][direction]),
                    MoveAlongPath(paths['X']['dot'], paths['X'][direction]),
                    run_time=self.run_time_def)

class SimpleHarmonicOscilator(BareOscilator):
    CONFIG = {
        'k': 1.0,
        'loops': 4
        }
    def U(self, x):
        return 0.5 * self.k* x**2



class QuarticOscilator(BareOscilator):
    CONFIG = {
        "x_min": -5,
        "x_max": 5,
        'a': 0.05,
        'b': -0.5,
        'c': 3.0,
        'loops': 4,
        }
    def U(self, x):
        return self.a * x**4 + self.b * x**2 + self.c  


class QuarticOscilatorR(BareOscilator):
    CONFIG = {
        "x_min": -5,
        "x_max": 5,
        'x_extreme_osc_min': 0,
        'a': 0.08,
        'b': -1.5,
        'c': 10.0,
        }
    def U(self, x):
        return self.a * x**4 + self.b * x**2 + self.c  
    def initialize(self):
        self.x_extreme_osc_max = (-self.b/self.a)**0.5

class QuarticOscilatorArb(BareOscilator):
    CONFIG = {
        "x_min": -5,
        "x_max": 5,
        'x_extreme_osc_min': 1.0,
        'a': 0.08,
        'b': -1.5,
        'c': 10.0,
        'loops': 4,
        }
    def U(self, x):
        return self.a * x**4 + self.b * x**2 + self.c  
    def initialize(self):
        E=self.U(self.x_extreme_osc_min)
        self.x_extreme_osc_max = np.sqrt((-self.b+ np.sqrt(self.b**2-4*self.a*(self.c-E)))/(2*self.a))

class QuarticOscilatorSmall(QuarticOscilatorArb):
    CONFIG = {
        "x_min": 0,
        "x_max": 6,
        "graph_origin": 2.5 * DOWN + 5 * LEFT,
        }
    def initialize(self):
        x_mini=np.sqrt(-self.b/(2*self.a))
        eps=0.2
        self.x_extreme_osc_min=x_mini*(1-eps)
        def Uapprox(x):
            return self.U(x_mini)-2*self.b*(x-x_mini)**2
        path_approx=self.get_graph(Uapprox, x_min=self.x_extreme_complete_min, x_max=self.x_extreme_complete_max)
        self.play(ShowCreation(path_approx))
        super().initialize()

class point_and_shadow(Dot):
    CONFIG = {
        "fill_color": RED,
        "fill_opacity": 1,   
    }
    # def get_x_shadow(self):
    #     x=self.get_x()
    #     return Dot((x,0,0))
    # def get_y_shadow(self):
    #     y=self.get_y()
    #     return Dot((0,y,0))
    # def get_x_line(self):
    #     x,y = self.get_x(), self.get_y()
    #     return Line((x,0,0),(x,y,0))
    def get_shadows(self):
        x,y = self.get_x(), self.get_y()
        return Dot((x,0,0)), Dot((0,y,0)),Line((x,0,0),(x,y,0)),Line((0,y,0),(x,y,0)),Line((0,0,0),(x,y,0))
    
class CircleHarmonicOscillator(GraphScene):
    CONFIG = {
        "x_min": -1,
        "x_max": 1,
        'y_min': -1,
        'y_max': 1,
        "graph_origin": ORIGIN,
        "x_axis_width": 0.5*FRAME_WIDTH,
        "y_axis_height": 0.5*FRAME_WIDTH,
        'update_x_shadow': True,
        'update_x_line': False,
        'update_y_shadow': False,
        'update_y_line': False,
        'update_d_line': False,
        'loops': 2,
        'run_time': 25,
        'phi0': 0
    }

    def construct(self):
        self.setup_axes()
        point=point_and_shadow(self.coords_to_point(1,0))
        x_shadow, y_shadow, x_line, y_line, d_line = point.get_shadows()
#        x_shadow=point.get_x_shadow()
#        x_line=point.get_x_line()
#        y_shadow=point.get_y_shadow()
        group=VGroup(point, x_shadow, y_shadow, x_line, y_line, d_line)
        r=get_norm(point.get_center())
        circle=Circle(radius=r)
        phi=ValueTracker(self.phi0)
        self.add(circle)
        self.add(group)
    #    self.play(MoveAlongPath(point, circle))
    #    self.play(Rotating(point,radians=loops*2*PI,about_point=ORIGIN))
        def update_points(group):
            point, x_shadow, y_shadow, x_line, y_line, d_line = group
            point.move_to(circle.point_from_proportion(phi.get_value()%1))
            new_x_shadow, new_y_shadow, new_x_line, new_y_line, new_d_line = point.get_shadows()
            if self.update_x_shadow:
                x_shadow.become(new_x_shadow)
            if self.update_x_line:
                x_line.become(new_x_line)
            if self.update_d_line:
                d_line.become(new_d_line)
            if self.update_y_shadow:
                y_shadow.become(new_y_shadow)
            if self.update_y_line:
                y_line.become(new_y_line)
        group.add_updater(update_points)
        self.play(phi.increment_value, self.loops, run_time=self.run_time , rate_func=linear)

class CircleHarmonicOscillatorXY(CircleHarmonicOscillator):
    CONFIG = {
        'update_x_line': True,
        'update_y_shadow': True,
        'update_y_line': True,
        'update_d_line': True,
    }
