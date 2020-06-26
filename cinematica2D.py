from manimlib.imports import *
from scipy.misc import derivative

VELOCITY_COLOR = GREEN
TIME_COLOR= YELLOW
DISTANCE_COLOR= BLUE
ACCELERATION_COLOR = RED



class movimiento2D(GraphScene):
    """
    Anima un movimeinto en 2D, mostrando vectores velocidad (show_velocity=True)
    y aceleración (show_acceleration=True)
    """
    CONFIG = {
        "x_min": -5,
        "x_max": 5,
        "x_tick_frequency": 1.0,
        "x_labeled_nums" : list(range(-5, 6, 1)),
        "x_axis_label" : "$x$ (m)",
        "y_min": -5,
        "y_max": 5,
        "y_tick_frequency": 1.0,
        "y_labeled_nums" : list(range(-5, 6, 1)),
        "y_axis_label" : "$y$ (m)",
        "exclude_zero_label": True,
        "graph_origin": (0,0,0),
        "title": "Movimiento en dos dimensiones",
        "show_title": True, 
        "show_x_axis": True,
        "show_y_axis": True,
        "show_path": True,
        "show_velocity": True,
        "show_acceleration": True,
        "vel_scale": 0.2,
        "acc_scale": 0.2,
        "vel_label": "$\\vec{v}$",
        "acc_label": "$\\vec{a}$",
        "vel_label_dir": RIGHT,
        "acc_label_dir": LEFT+DOWN,
        "initial_time": 0.0,
        "run_time": 2.2,
    }
    def X(self, t):
        vx0=5.0
        x0=-5
        x=vx0*t+x0
        return x
    def Y(self,t):
        a=-9.8
        vy0=10.0
        y0=0.0
        y=(a/2.0)*t**2+vy0*t+y0
        return y
    def position(self,t):
        x=self.X(t)
        y=self.Y(t)
        return self.coords_to_point(x,y)
    def velocity(self,t):
        vx=derivative(self.X,t,dx=0.001)
        vy=derivative(self.Y,t,dx=0.001)
        return self.coords_to_point(vx,vy)
    def acceleration(self,t):
        ax=derivative(self.X,t,dx=0.001,n=2)
        ay=derivative(self.Y,t,dx=0.001,n=2)
        return self.coords_to_point(ax,ay)
    def mostrar_titulo(self, color = RED, pos=ORIGIN + 3.8 * UP):
        titulo_mobj=TextMobject(self.title, color = color).shift(pos)
        self.play(Write(titulo_mobj))
    def cinematic_vector(self, t, f=None, color=VELOCITY_COLOR, pos = None, scale=1.0, label_text = None, direction = None):
        """
        Creates velocity or acceleration vector

        Args:
            t (float): current time
            f (function, optional): function to create the vector: velocity or acceleration. Defaults to velocity.
            color (int, optional): color for the vector. Defaults to VELOCITY_COLOR.
            pos (ndarray, optional): position to place the vector. Defaults to self.position(t).
            scale (float): scale for the vector. Default 1.0.
            label_text (str or None): label for the vector. Default None.
            direction (ndarray): direction for the label. Default self.vec_label_dir

        Returns:
            Vector or VGroup(Vector, TextMobject(label_text))
        """
        if f == None:
            f=self.velocity
        if pos == None:
            pos = self.position(t)
        if type(direction) == type(None):
            direction = self.vel_label_dir
        vec = Vector(scale*f(t), color = color)
        vec = vec.shift(pos)
        if label_text != None:
            text=TextMobject(label_text, color = color)
            text.next_to(pos, direction = direction)
            vec= VGroup(vec,text)
        return vec

    def animate_graph(self):
        point = Dot(self.position(self.initial_time), color = DISTANCE_COLOR, radius=0.2)
        group = VGroup(point)
        if self.show_path:
            path = VMobject(color=DISTANCE_COLOR)
            path.set_points_as_corners([point.get_center(),point.get_center()+UP*0.001])
            group.add(path)
        if self.show_velocity:
            velocity_vector = self.cinematic_vector(self.initial_time, scale=self.vel_scale, label_text=self.vel_label)
            group.add(velocity_vector)
        if self.show_acceleration:
            acceleration_vector = self.cinematic_vector(self.initial_time,f=self.acceleration,color = ACCELERATION_COLOR, scale=self.acc_scale, direction = self.acc_label_dir)
            group.add(acceleration_vector)
        current_time=ValueTracker(self.initial_time)
        self.add(group)
        def update_points(group):
            t = current_time.get_value()
            pos = self.position(t)
            # Unpack the group
            # point, path, velocity_vector, acceleration_vector = group
            point, *r = group
            point.move_to(pos)
            if self.show_path:
                path, *r = r
                new_path=path.copy()
                new_path.append_vectorized_mobject(Line(new_path.points[-1],point.get_center()))
                new_path.make_smooth()
                path.become(new_path)
            if self.show_velocity:
                velocity_vector, *r = r 
                velocity_vector.become(self.cinematic_vector(t, scale=self.vel_scale, label_text=self.vel_label))
            if self.show_acceleration:
                acceleration_vector, *r = r
                acceleration_vector.become(self.cinematic_vector(t,f=self.acceleration,color = ACCELERATION_COLOR,
                                                                scale=self.acc_scale,  label_text=self.acc_label,
                                                                direction = self.acc_label_dir ))
        group.add_updater(update_points)
        self.play(current_time.set_value, self.initial_time + self.run_time, run_time=self.run_time , rate_func=linear)

    def construct(self):
        if self.show_title:
            self.mostrar_titulo()
        self.setup_axes()
        if not self.show_x_axis:
            self.remove(self.x_axis_label, self.x_axis)
        if not self.show_y_axis:
            self.remove(self.y_axis_label, self.y_axis)
        self.animate_graph()

        self.wait()
       

class movimiento1D(movimiento2D):
    CONFIG = {
        "x_min": -5,
        "x_max": 5,
        "x_tick_frequency": 1.0,
        "x_labeled_nums" : list(range(-5, 6, 1)),
        "x_axis_label" : "$x$ (m)",
        "y_min": -5,
        "y_max": 5,
        "y_tick_frequency": 1.0,
        "y_labeled_nums" : list(range(-5, 6, 1)),
        "y_axis_label" : "$y$ (m)",
        "exclude_zero_label": False,
        "graph_origin": (0,0,0),
        "title": "Movimiento en una dimensión",
        "show_title": True, 
        "show_x_axis": True,
        "show_y_axis": False,
        "show_path": True,
        "show_velocity": True,
        "show_acceleration": True,
        "vel_scale": 1.0,
        "acc_scale": 1.0,
        "vel_label": "$\\vec{v}$",
        "acc_label": "$\\vec{a}$",
        "vel_label_dir": UP,
        "acc_label_dir": DOWN,
    }
    def Y(self,t):
        return 0.0
    
class mov_1D_cub(movimiento1D):
    CONFIG = {
        "initial_time": -1.0,
        "run_time": 10.0,
    }
    def X(self,t):
        ts=t*0.55
        return 2*(0.3*ts**3-2.0*ts**2+3.0*ts)

class mov_1D_v_const(movimiento1D):
    CONFIG = {
        "title": "Movimiento con velocidad constante",
        "show_path": False,
        "show_acceleration": False,
        "initial_time": 0.0,
        "run_time": 10.0,
        "vel_scale": 2.0,
         "vel_label_dir": UP + RIGHT,
    }
    def X(self,t):
        return 0.8*t-4.5

class mov_1D_a_const(movimiento1D):
    CONFIG = {
        "title": "Movimiento con aceleración constante",
        "show_path": False,
        "acc_scale": 4.0,
        "initial_time": 0.0,
        "run_time": 10.0,
    }
    def X(self,t):
        return 0.14*t**2-0.8*t-1.0

class mov_caida_libre(movimiento2D):
    CONFIG = {
        "title": "Movimiento de caida libre",
        "exclude_zero_label": False,
        "acc_label": "$\\vec{a}=\\vec{g}$",
        "show_path": False,
        "show_x_axis": False,
        "vel_label_dir": 1.5 * RIGHT,
        "acc_label_dir": 2.0 * LEFT + DOWN,
        "initial_time": 0.0,
        "run_time":  2.3,
        "vel_scale": 0.2,
        "acc_scale": 0.2,
    }
    def X(self,t):
        return 0.0
    def Y(self,t):
        a=-9.8
        vy0=10.0
        y0=0.0
        y=(a/2.0)*t**2+vy0*t+y0
        return y

class mov_caida_libre_slow_mo(mov_caida_libre):
    CONFIG = {
        "run_time":  23.0,
        "vel_scale": 0.2*10.0,
        "acc_scale": 0.2*100.0,
    }
    def Y(self,t):
        a=-9.8
        vy0=10.0
        y0=0.0
        t=t/10.0
        y=(a/2.0)*t**2+vy0*t+y0
        return y