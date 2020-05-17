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
        'radius': 0.2,  
    }
    def __init__(self, point=ORIGIN, phi0=0, **kwargs):
        if phi0 == 0:
            self.phi_t_str='\\omega_0 t'
        else:
            self.phi_t_str='\\omega_0 t+\\varphi'
        super().__init__(point=point, **kwargs)
    def get_shadows(self):
        x,y = self.get_x(), self.get_y()
        x_p =  Dot((x,0,0), name='x_shadow', color=BLUE, radius=0.2) 
        y_p = Dot((0,y,0), name='y_shadow', color=BLUE, radius=0.2)
        r_v = Vector((x,y,0), name='r_vector', color=RED_A)
        angle = r_v.get_angle()
        if angle<0 :
            angle=TAU+angle
        r_arc = Arc(angle=angle, name='r_arc')
        return (
                x_p,
                Line((x,0,0),(x,y,0), name='x_line', color=GREY),
                Vector((x,0,0), name='x_vector', color=BLUE_A),
                TextMobject('$x=A\\cos(%s)$' % (self.phi_t_str), name='x_text').next_to(x_p, direction=DOWN),
                y_p,
                Line((0,y,0),(x,y,0),name='y_line', color=GREY),
                Vector((0,y,0), name='y_vector', color=BLUE_A),
                TextMobject('$y=A\\sin(%s)$' % (self.phi_t_str), name='y_text').next_to(y_p, direction=UP),
                Line((0,0,0),(x,y,0),name='r_line', color=RED_A),
                r_v,
                TextMobject('$z=Ae^{i(%s)}$' % (self.phi_t_str), name='r_text').next_to(self, direction=RIGHT),
                r_arc,
                TextMobject('$%s$' % (self.phi_t_str), name='r_arc_text').next_to(r_arc.get_end(), direction=RIGHT),
                )
    
class CircleHarmonicOscillator(GraphScene):
    CONFIG = {
        "x_min": -1,
        "x_max": 1,
        'y_min': -1,
        'y_max': 1,
        "graph_origin": ORIGIN,
        "x_axis_width": 0.5*FRAME_WIDTH,
        "y_axis_height": 0.5*FRAME_WIDTH,
        'show_objects_list': [
            'x_shadow', 
        #    'x_line',
        #    'x_vector',
        #    'y_shadow',
        #    'y_line',
        #    'y_vector',
        #    'r_line',
        #    'r_vector',
        #    'r_arc',
        #    'r_arc_text'   
            ],
        'loops': 2,
        'run_time': 25,
        'phi0': 0,
    }

    def construct(self):
        self.setup_axes()
        point=point_and_shadow(self.coords_to_point(1,0),phi0=self.phi0)
        shadows = point.get_shadows()
        for s in shadows:
            s.fade(darkness=1.0)
        group=VGroup(point, *shadows)
        r=get_norm(point.get_center())
        circle=Circle(radius=r)
        phi=ValueTracker(self.phi0)
        self.add(circle)
        self.add(group)
        show_objects_list=self.show_objects_list
        def update_points(group):
            point, *shadows = group
            point.move_to(circle.point_from_proportion(phi.get_value()%1))
            new_objects = point.get_shadows()
            for obj, new_obj in zip(shadows,new_objects): 
                if obj.name in show_objects_list:
                    obj.become(new_obj)

        group.add_updater(update_points)
        self.play(phi.increment_value, self.loops, run_time=self.run_time , rate_func=linear)

class CircleHarmonicOscillatorX(CircleHarmonicOscillator):
    CONFIG = {
        'show_objects_list': [
            'x_shadow', 
        #    'y_shadow',
            'x_line',
        #    'y_line',
        #    'r_line'
        ]
    }

class CircleHarmonicOscillatorXY(CircleHarmonicOscillator):
    CONFIG = {
        'show_objects_list': [
            'x_shadow', 
            'x_line',
            'x_vector',
            'y_shadow',
            'y_line',
            'y_vector',
            # 'r_line',
            # 'r_vector'
        ]
    }

class CircleHarmonicOscillatorAll(CircleHarmonicOscillator):
    CONFIG = {
        'show_objects_list': [
            'x_shadow', 
            'x_line',
            'x_vector',
            'x_text',
            'y_shadow',
            'y_line',
            'y_vector',
            'y_text',
            # 'r_line',
            'r_vector',
            'r_text',
            'r_arc',
            'r_arc_text',
        ]
    }
class CircleHarmonicOscillatorAllphi(CircleHarmonicOscillator):
    CONFIG = {
        'show_objects_list': [
            'x_shadow', 
            'x_line',
            'x_vector',
            'x_text',
            'y_shadow',
            'y_line',
            'y_vector',
            'y_text',
            # 'r_line',
            'r_vector',
            'r_text',
            'r_arc',
            'r_arc_text',
        ],
        'phi0': 1.0/8.0 
    }

class CircleHarmonicOscillatorXYR(CircleHarmonicOscillator):
    CONFIG = {
        'show_objects_list': [
            'x_shadow', 
            # 'x_line',
            'x_vector',
            'y_shadow',
            # 'y_line',
            'y_vector',
            # 'r_line',
            'r_vector',
        ]
    }

class CircleHarmonicOscillatorXYRA(CircleHarmonicOscillator):
    CONFIG = {
        'show_objects_list': [
            'x_shadow', 
            'x_line',
            'x_vector',
            'y_shadow',
            'y_line',
            'y_vector',
            # 'r_line',
            'r_vector',
            'r_arc',
            'r_arc_text'
        ]
    }
class CircleHarmonicOscillatorNone(CircleHarmonicOscillator):
    CONFIG = {
        'show_objects_list': [
        ]
    }
