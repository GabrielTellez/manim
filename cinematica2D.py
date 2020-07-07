from manimlib.imports import *
from scipy.misc import derivative

VELOCITY_COLOR = GREEN
TIME_COLOR= YELLOW
DISTANCE_COLOR= BLUE
ACCELERATION_COLOR = RED
TITLE_COLOR = RED



class movimiento2D(GraphScene):
    """
    Anima un movimiento en 2D, mostrando vectores velocidad (show_velocity=True)
    y aceleración (show_acceleration=True)
    """
    CONFIG = {
        "x_min": -5,
        "x_max": 5,
        "x_tick_frequency": 1.0,
        "x_labeled_nums" : list(range(-5, 6, 1)),
        "x_axis_label" : "$x$ (m)",
        "x_axis_width": 6,
        "y_min": -5,
        "y_max": 5,
        "y_tick_frequency": 1.0,
        "y_labeled_nums" : list(range(-5, 6, 1)),
        "y_axis_label" : "$y$ (m)",
        "exclude_zero_label": True,
        "y_axis_height": 6,
        "graph_origin": (0,0,0),
        "title": "Movimiento en dos dimensiones",
        "title_position": ORIGIN + 3.725 * UP,
        "title_color": TITLE_COLOR,
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
    def mostrar_titulo(self, color = None, pos = None):
        if color == None:
            color = self.title_color
        if pos == None:
            pos = self.title_position
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

    def acc_component_vecs(
        self, t, 
        label_text_ac = "$\\vec{a}_c$", 
        label_dir_ac = 1.5 * DOWN,
        label_text_at= "$\\vec{a}_t$", 
        label_dir_at = 4.0 * UP + 2.0 * RIGHT,
        color = ACCELERATION_COLOR):
        """Creates the vector components of the acceleration (centripetal, tangential)

        Args:
            t (float): time
            label_text_ac (str, optional): label for centripetal acceleration. Defaults to "$\vec{a}_c$".
            label_dir_ac (optional): offset for the a_c label. Defaults to 1.5*DOWN.
            label_text_at (str, optional): label for the tangential acceleration. Defaults to "$\vec{a}_t$".
            label_dir_at (optional): offset for the a_t label. Defaults to 4.0*UP+2.0*RIGHT.
            color (optional): color for the vectors and label. Defaults to ACCELERATION_COLOR.

        Returns:
            [type]: [description]
        """
        (a_c, a_t) = self.acc_components(t)
        pos = self.position(t)
        a_c_vec = Vector(self.acc_scale*self.coords_to_point(a_c[0],a_c[1]), color = color)
        a_c_vec.shift(pos)
        a_t_vec = Vector(self.acc_scale*self.coords_to_point(a_t[0],a_t[1]), color = color)
        a_t_vec.shift(pos)
        components_list = []
        for vec, label_text, direction in [(a_c_vec, label_text_ac, label_dir_ac), (a_t_vec, label_text_at, label_dir_at)]:
            if label_text != None:
                text=TextMobject(label_text, color = color)
                text.next_to(pos, direction = direction)
                vec = VGroup(vec,text)
                components_list.append(vec)
        return components_list

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
        self.play(current_time.set_value, self.initial_time + self.run_time, run_time=self.run_time, rate_func=linear)
        return group

    def initialize_scene(self):
        if self.show_title:
            self.mostrar_titulo()
        self.setup_axes()
        if not self.show_x_axis:
            self.remove(self.x_axis_label, self.x_axis)
        if not self.show_y_axis:
            self.remove(self.y_axis_label, self.y_axis)

    def construct(self):
        self.initialize_scene()
        self.animate_graph()
        self.wait()
       

class movimiento1D(movimiento2D):
    CONFIG = {
        "x_min": -5,
        "x_max": 5,
        "x_tick_frequency": 1.0,
        "x_labeled_nums" : list(range(-5, 6, 1)),
        "x_axis_label" : "$x$ (m)",
        "x_axis_width": 9,
        "y_min": -5,
        "y_max": 5,
        "y_tick_frequency": 1.0,
        "y_labeled_nums" : list(range(-5, 6, 1)),
        "y_axis_label" : "$y$ (m)",
        "exclude_zero_label": False,
        "graph_origin": (0,0,0),
        "title": "Movimiento en una dimensión",
        "title_position": ORIGIN + 2.5 * UP,
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
        "vel_label_dir": 1.5 * UP,
        "acc_label_dir": 2.5 * DOWN,
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
class mov_1D_cub_notraces(mov_1D_cub):
    CONFIG = {
        "show_path": False,
        "show_velocity": False,
        "show_acceleration": False,
    }

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


class mov_circulos_alternos(movimiento2D):
    CONFIG = {
        "run_time" : 10.0,
        "omega": 1.0,
        "amp_x": 3.5,
        "amp_y": 3.5,
        "vel_scale": 0.5,
        "acc_scale": 0.5,
    }
    def X(self, t):
        x0 = - self.amp_x/2
        if t < PI/self.omega:
            x = x0 - self.amp_x * np.cos(self.omega*t)
        else:
            x =  x0 + 2 * self.amp_x - self.amp_x * np.cos(self.omega*t-PI)
        return x
    def Y(self,t):
        y= self.amp_y*np.sin(self.omega*t)
        return y

class mov_circular_uniforme(movimiento2D):
    """Anima un movimiento circular uniforme con velocidad angular omega."""
    CONFIG = {
        'amplitud': 5.0,
        'omega': 2.0,
        'vueltas': 2.0,
        'phi': 0.0,
        'run_time': None,
        'title': 'Movimiento circular uniforme',
    }

    def construct(self):
        if self.run_time == None:
            """Determina run_time con el numero de vueltas"""
            self.run_time = self.vueltas * TAU / self.omega
        return super().construct()

    def theta(self, t):
        return self.omega*t + self.phi

    def X(self,t):
        return self.amplitud * np.cos(self.theta(t))

    def Y(self,t):
        return self.amplitud * np.sin(self.theta(t))

class mov_circular_no_uniforme(mov_circular_uniforme):
    """Anima un movimiento circular no uniforme, con aceleración angular alpha constante"""
    CONFIG = {
        'amplitud': 5.0,
        'alpha': 0.5,
        'omega': 0.0,
        'phi': 0.0,
        'run_time': 6.0,
        'title': 'Movimiento circular no uniforme'
    }

    def theta(self, t):
        return (self.alpha/2.0) * t**2 + self.omega*t + self.phi

class mov_curvo_acel(mov_circular_no_uniforme):
    CONFIG = {
        'amplitud': 5.0,
        'alpha': -0.035,   #   -0.035
        'omega': -0.35,     #   -0.4
        'phi': PI,
        'run_time': 5.0,
        'time_rescale': 0.7,
        "vel_scale": 1.0,
        "acc_scale": 3.0,
        "vel_label_dir": 2 * UP +  LEFT,
        "acc_label_dir": 8.0 * RIGHT,
        'title': '',
        'show_title': False,
        "show_x_axis": False,
        "show_y_axis": False,
        "show_path": True,
        "show_velocity": True,
        "show_acceleration": False,
    }
    def X(self,t):
        xfactor = 2.4
        x0 = 4.0
        return x0 + xfactor * self.amplitud * np.cos(self.theta(self.time_rescale*t))
    def Y(self,t):
        y0 = - 1.5
        return y0 + self.amplitud * np.sin(self.theta(self.time_rescale*t))
        
class mov_curvo_acel_show_a(mov_curvo_acel):
    CONFIG = {
        "show_acceleration": True,
    }

class mov_curvo_acel_construction(mov_curvo_acel):
    CONFIG = {
        "dt": 1.0
    }
    def dv(self, t, dt = None):
        if dt == None:
            dt = self.dt
        return self.velocity(t+dt) - self.velocity(t)

    def animate_acceleration_construction(
        self, 
        t = 2.0,    # t =1.5, 2.0 
        dt = None, 
        v_t_label_txt = '$\\vec{v}(t)$',
        v_t_label_dir = None,
        v_t_dt_label_txt = '$\\vec{v}(t+\\Delta t)$',
        v_t_dt_label_dir = 0.5 * DOWN + 1.5 * RIGHT,
        dv_label_txt = '$\\Delta \\vec{v}$',
        dv_label_dir = UP + 0.5 * RIGHT,
        a_label_txt = '$$\\vec{a}_{\\text{med}}=\\frac{\\Delta \\vec{v}}{\\Delta t}$$',
        a_label_dir = 3.0* DOWN + 0.5 * RIGHT,
        a_scale = None,
        continue_path = True):
        """Animates the construction of the average acceleration."""

        if dt == None:
            dt = self.dt
        if v_t_label_dir == None:
            v_t_label_dir = self.vel_label
        if a_scale == None:
            a_scale = self.acc_scale
        original_run_time = self.run_time
        original_initial_time = self.initial_time
        self.run_time = t
        group = self.animate_graph()
        point, path, v = group
        t = self.run_time
        v_t, label_t = self.cinematic_vector(t, scale=self.vel_scale, label_text= v_t_label_txt)
        self.remove(v)
        self.play(
            Write(v_t),
            Write(label_t)
            )
        self.wait()
        self.initial_time = self.run_time
        self.run_time = dt
        group = self.animate_graph()
        point, path, v = group
        v_t_dt, label_t_dt = self.cinematic_vector(t+dt , scale=self.vel_scale, label_text=v_t_dt_label_txt, direction = v_t_dt_label_dir)
        self.remove(v)
        self.play(
            Write(v_t_dt),
            Write(label_t_dt)
            )
        self.wait()
        self.play(ApplyMethod(v_t_dt.shift, self.position(t)-self.position(t+dt)))
        self.remove(point, path)
        dv = self.cinematic_vector(
            t, f=self.dv, 
            scale = self.vel_scale, 
            label_text = dv_label_txt, color = ACCELERATION_COLOR,
            direction = dv_label_dir
        )
        dv.shift(self.vel_scale*self.velocity(t))
        self.play(ShowCreation(dv))
        self.wait()
        a = self.cinematic_vector(
            t, f=self.dv, 
            scale = a_scale * self.vel_scale, 
            label_text = a_label_txt,
            color = ACCELERATION_COLOR,
            direction = a_label_dir
        )
        self.play(Transform(dv, a))
        self.wait()
        if continue_path:
            self.remove(v_t_dt, label_t_dt)
            self.initial_time = t
            self.run_time = original_run_time - t
            self.animate_graph()

    def tangent_vec(self,t):
        vx=derivative(self.X,t,dx=0.001)
        vy=derivative(self.Y,t,dx=0.001)
        norm = np.sqrt(vx**2 + vy**2)
        ux = vx / norm
        uy = vy / norm
        return [ux, uy]
    def tangent_unit_vec(self,t, color = GREY):
        [ux, uy] = self.tangent_vec(t)
        return self.coords_to_point(ux, uy)

    def perp_vec(self,t):
        [ux, uy] = self.tangent_vec(t)
        return [uy, -ux]
    def perp_unit_vec(self,t):
        [ux, uy] = self.perp_vec(t)
        return self.coords_to_point(ux, uy)

    def acc_components(self, t):
        """Gives the centripetal and tangential components of the acceleration

        Args:
            t (float): time

        Returns: (np.array[ax_cen, ay_cen], np.array[ax_tan, ay_tan])
        """

        ax=derivative(self.X,t,dx=0.001,n=2)
        ay=derivative(self.Y,t,dx=0.001,n=2)
        a = np.array([ax, ay])
        t_vec = np.array(self.tangent_vec(t))
        c_vec = np.array(self.perp_vec(t))
        a_t = np.dot(a,t_vec) * t_vec
        a_c = np.dot(a,c_vec) * c_vec
        return (a_c, a_t)

    def perp_velocity(self,t):
        vx=derivative(self.X,t,dx=0.001)
        vy=derivative(self.Y,t,dx=0.001)
        return self.coords_to_point(vy,-vx)

    def animate_a_tangent_a_centripetal(
        self, 
        t = 2.0,    # t =1.5, 2.0 
        a_sum_text = "$\\vec{a} = \\vec{a}_c + \\vec{a}_t$",
        continue_path = True):
        """Shows the centripetal and tangent components of acceleration."""

        original_run_time = self.run_time
        original_initial_time = self.initial_time
        self.run_time = t
        self.show_velocity = True
        self.show_acceleration = True
        group = self.animate_graph()
        point, path, v_vec, a_vec = group
        tg = self.tangent_unit_vec(t)
        perp = self.perp_unit_vec(t)
        pos = self.position(t)
        tangent_line = Line(pos - 5.0 * tg, pos + 5.0 * tg , color = GREY)
        perp_line = Line( pos , pos + 5.0 * perp, color = GREY )
        self.play(
            ShowCreation(tangent_line),
            ShowCreation(perp_line)
            )
        [a_c_vec, a_t_vec] = self.acc_component_vecs(t)
        self.play(
            ShowCreation(a_c_vec),
            ShowCreation(a_t_vec)
            )
        a_vec, a_txt = a_vec
        a_decomp_txt = TextMobject(a_sum_text, color = ACCELERATION_COLOR)
        a_decomp_txt.next_to(pos, direction = self.acc_label_dir)
        self.remove(a_txt)
        self.play(Write(a_decomp_txt))
        

        
    def construct(self):
        self.initialize_scene()
        # self.animate_acceleration_construction()
        # self.wait()
        self.animate_a_tangent_a_centripetal()
       
        