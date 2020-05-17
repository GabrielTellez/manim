# from big_ol_pile_of_manim_imports import *
from manimlib.imports import *

class Formula(Scene):
    def construct(self):
        formula_tex=TexMobject(r"e^{2i\pi}=1, \sum_{k=0}^{10} k")
        inline_formula_tex=TextMobject(r"Inline $e^{2i\pi}=1$ and $\sum_{k=0}^{10} k$").move_to(2*DOWN)
        
        self.add(formula_tex)
        self.add(inline_formula_tex)
